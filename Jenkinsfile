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

        stage('Check Homebrew Installation') {
            steps {
                script {
                    sh '''
                        if command -v brew &> /dev/null
                        then
                            echo "Homebrew is installed."
                            brew --version
                        else
                            echo "Homebrew is not installed."
                            exit 1
                        fi
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install --upgrade pip'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                    sh 'brew install allure'
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
