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
                . venv/bin/activate
                pip install -r backend/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest backend
                '''
            }
        }

        stage('Run Backend') {
            steps {
                sh '''
                . venv/bin/activate
                python backend/app.py &
                sleep 10
                '''
            }
        }

        stage('OpenAPI Check') {
            steps {
                sh '''
                curl http://localhost:5000/swagger || true
                '''
            }
        }
    }
}

