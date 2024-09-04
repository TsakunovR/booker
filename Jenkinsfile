pipeline {
    agent {
        docker {
            image 'python:3.12-buster'
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
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Install Allure') {
            steps {
                sh 'apt-get update && apt-get install -y wget unzip'
                sh '''
            wget -qO- https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.30.0/allure-commandline-2.30.0.zip -O allure.zip
            if unzip -d /opt allure.zip; then
                echo "Allure установлен успешно."
            else
                echo "Ошибка при установке Allure."
                exit 1
            fi
            '''
                sh 'ln -s /opt/allure-commandline-2.30.0/bin/allure /usr/local/bin/allure'
            }
        }
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest -v -s --alluredir=reports'
            }
        }
        stage('Generate Allure Report') {
            steps {
                script {
                    sh '''
                    cd /opt/allure/bin
                    ./allure --version
                    ./allure generate reports -o allure-report
                    '''
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
        }
    }
}
