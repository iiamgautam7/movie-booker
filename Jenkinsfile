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
                        ping 127.0.0.1 -n 6 > nul
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
            
            // Send success email notification
            emailext (
                subject: "✅ Movie Booker Build SUCCESS - Build #${BUILD_NUMBER}",
                body: """
                <h2>🎉 Build Completed Successfully!</h2>
                
                <h3>Build Details:</h3>
                <ul>
                    <li><strong>Project:</strong> ${JOB_NAME}</li>
                    <li><strong>Build Number:</strong> ${BUILD_NUMBER}</li>
                    <li><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></li>
                    <li><strong>Duration:</strong> ${BUILD_DURATION}</li>
                    <li><strong>Timestamp:</strong> ${BUILD_TIMESTAMP}</li>
                </ul>
                
                <h3>Changes:</h3>
                <p>${CHANGES}</p>
                
                <h3>Artifacts:</h3>
                <p>Database file (moviebooker.db) has been archived and is available for download.</p>
                
                <p>All stages completed successfully:
                ✅ Python Setup<br>
                ✅ Database Initialization<br>
                ✅ Flask Server Started<br>
                ✅ Worker Execution<br>
                ✅ Artifact Archiving</p>
                
                <p><em>Automated message from Jenkins CI/CD Pipeline</em></p>
                """,
                mimeType: 'text/html',
                to: 'your-email@example.com'  // Replace with your actual email
            )
        }
        failure {
            echo 'Pipeline failed. Check the logs above for details.'
            
            // Send failure email notification
            emailext (
                subject: "❌ Movie Booker Build FAILED - Build #${BUILD_NUMBER}",
                body: """
                <h2>🚨 Build Failed!</h2>
                
                <h3>Build Details:</h3>
                <ul>
                    <li><strong>Project:</strong> ${JOB_NAME}</li>
                    <li><strong>Build Number:</strong> ${BUILD_NUMBER}</li>
                    <li><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></li>
                    <li><strong>Duration:</strong> ${BUILD_DURATION}</li>
                    <li><strong>Timestamp:</strong> ${BUILD_TIMESTAMP}</li>
                </ul>
                
                <h3>Changes:</h3>
                <p>${CHANGES}</p>
                
                <h3>Failure Details:</h3>
                <p>Please check the build logs at: <a href="${BUILD_URL}console">${BUILD_URL}console</a></p>
                
                <p><em>Automated message from Jenkins CI/CD Pipeline</em></p>
                """,
                mimeType: 'text/html',
                to: 'your-email@example.com'  // Replace with your actual email
            )
        }
    }
}
