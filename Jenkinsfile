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
        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate && pip install --upgrade pip
                    . venv/bin/activate && pip install -r requirements.txt
                '''
                sh 'pwd'
                sh 'ls -l'
            }
        }
        stage('Install Allure') {
            steps {
                sh '''
                    echo "deb http://deb.debian.org/debian bullseye-backports main" >> /etc/apt/sources.list.d/bullseye-backports.list
                    apt-get update
                    apt-get install -y wget unzip openjdk-17-jdk
                    wget -qO- https://github.com/allure-framework/allure2/releases/download/2.20.0/allure-2.20.0.zip -O allure.zip
                    unzip -d /opt allure.zip
                    ln -s /opt/allure-2.20.0/bin/allure /usr/local/bin/allure
                    rm allure.zip
                '''
                sh 'which allure'
                sh 'allure --version'
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v -s --alluredir=reports
                '''
                sh 'pwd'
                sh 'ls -l reports'
            }
        }
        stage('Generate Allure Report') {
            steps {
                allure([
                    results: [[path: 'reports']],
                    reportBuildPolicy: 'ALWAYS'
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
