pipeline {
    agent any
    
    environment {
        FLASK_HOST = '127.0.0.1'
        FLASK_PORT = '5000'
        FLASK_BASE_URL = "http://${FLASK_HOST}:${FLASK_PORT}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                bat '''
                    if not exist "venv" (
                        python -m venv venv
                    )
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Initialize Database') {
            steps {
                bat '''
                    venv\\Scripts\\python.exe db_init.py
                '''
            }
        }
        
        stage('Start Flask (background)') {
            steps {
                script {
                    // Start Flask app in background
                    bat '''
                        start /b venv\\Scripts\\python.exe app.py
                        timeout /t 5
                    '''
                }
            }
        }
        
        stage('Run Worker') {
            steps {
                bat '''
                    venv\\Scripts\\python.exe worker.py
                '''
            }
        }
        
        stage('Archive DB') {
            steps {
                // Archive the database file as build artifact
                archiveArtifacts artifacts: 'moviebooker.db', allowEmptyArchive: true
                
                // Also archive any logs if they exist
                archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            // Clean up: kill any python processes started by Jenkins
            bat '''
                taskkill /F /IM python.exe /T || exit 0
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs above for details.'
        }
    }
}
