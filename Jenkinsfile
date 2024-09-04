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
                    wget -qO- https://github.com/allure-framework/allure2/releases/download/2.30.0/allure-2.30.0.zip -O allure.zip
                    unzip -d /opt allure.zip
                    ln -s /opt/allure-2.30.0/bin/allure /usr/local/bin/allure
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
                sh '''
                    mkdir -p allure-report
                    chmod -R 777 allure-report
                    mkdir -p reports
                    chmod -R 777 reports
                    allure generate reports --clean -o allure-report
                '''
                sh 'pwd'
                sh 'ls -l allure-report'
            }
        }
        stage('Publish Allure Report') {
            steps {
                script {
                    def allureReportPath = 'allure-report'
                    sh "chmod -R 777 ${allureReportPath}"
                    sh "ls -l ${allureReportPath}"
                    allure([
                        results: [[path: allureReportPath]]
                    ])
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
