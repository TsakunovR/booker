pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root'
        }
    }

    environment {
        ALLURE_COMMANDLINE = '/usr/local/bin/allure'
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
                    sh '${ALLURE_COMMANDLINE} generate reports --clean -o allure-report'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-report/**', fingerprint: true

            allure([
                results: [[path: 'allure-report']]
            ])
        }
    }
}
