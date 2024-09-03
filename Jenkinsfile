pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install --upgrade pip'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '. venv/bin/activate && pytest -v -s --alluredir reports'
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    sh '. venv/bin/activate && allure generate reports --clean'
                    sh '. venv/bin/activate && allure serve reports'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', fingerprint: true
            junit 'reports/**/*.xml'
        }
    }
}
