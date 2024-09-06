pipeline {
    agent {
        docker {
            image 'python:3.12'
            args '-u 0:0'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies and Allure') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate && pip install --upgrade pip
                    . venv/bin/activate && pip install -r requirements.txt

                    echo "deb http://deb.debian.org/debian bullseye-backports main" >> /etc/apt/sources.list.d/bullseye-backports.list
                    apt-get update
                    apt-get install -y wget unzip openjdk-17-jdk
                    wget -qO- https://github.com/allure-framework/allure2/releases/download/2.20.0/allure-2.20.0.zip -O allure.zip
                    unzip -d /opt allure.zip
                    ln -s /opt/allure-2.20.0/bin/allure /usr/local/bin/allure
                    rm allure.zip
                '''
            }
        }
        stage('Check PATH for Allure') {
            steps {
                sh '''
                    if ! echo $PATH | grep -q "/usr/local/bin"; then
                        echo "WARNING: /usr/local/bin is not in PATH. Adding it now."
                        export PATH=$PATH:/usr/local/bin
                    else
                        echo "/usr/local/bin is already in PATH."
                    fi

                    # Проверка доступности allure
                    if command -v allure &> /dev/null; then
                        echo "Allure is installed and available in PATH."
                    else
                        echo "ERROR: Allure is not found in PATH."
                        exit 1
                    fi
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v -s --alluredir=reports
                '''
            }
        }
        stage('Publish Allure Report') {
            steps {
                allure([
                    results: [[path: 'reports']]
                ])
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
