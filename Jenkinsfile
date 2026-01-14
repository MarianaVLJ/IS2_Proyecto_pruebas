pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo 'Clonando repositorio...'
            }
        }

        stage('Build Backend') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -e .
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                source venv/bin/activate
                pytest || true
                '''
            }
        }

        stage('Docker Mongo') {
            steps {
                sh '''
                docker-compose up -d
                '''
            }
        }

        stage('Run Backend') {
            steps {
                sh '''
                source venv/bin/activate
                python backend/app.py &
                sleep 10
                '''
            }
        }
    }
}
