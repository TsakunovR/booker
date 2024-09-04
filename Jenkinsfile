pipeline {
    agent {
        docker {
            image 'python:3.12'
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
                sh '''
                    echo "deb http://deb.debian.org/debian bullseye-backports main" >> /etc/apt/sources.list.d/bullseye-backports.list
                    apt-get update
                    apt-get install -y wget unzip openjdk-17-jdk
                    wget -qO- https://github.com/allure-framework/allure2/releases/download/2.30.0/allure-2.30.0.zip -O allure.zip
                    unzip -d /opt allure.zip
                    ln -s /opt/allure-2.30.0/bin/allure /usr/local/bin/allure
                    rm allure.zip
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest -v -s --alluredir=reports'
            }
        }
        stage('Generate Allure Report') {
            steps {
                sh '''
                    mkdir -p allure-report
                    chmod -R 777 allure-report
                    allure generate reports --clean -o allure-report
                '''
            }
        }
        stage('Publish Allure Report') {
            steps {
                script {
                    def allureReportPath = 'allure-report'
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
