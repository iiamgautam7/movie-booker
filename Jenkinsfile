pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python310\\python.exe'
        VENV = "${WORKSPACE}\\venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat """
                if not exist "${VENV}" (${PYTHON} -m venv "${VENV}")
                "${VENV}\\Scripts\\python.exe" -m pip install --upgrade pip
                "${VENV}\\Scripts\\python.exe" -m pip install -r requirements.txt
                """
            }
        }

        stage('Start Flask (background)') {
            steps {
                bat """
                REM Start Flask in background using START (non-blocking)
                start "" /B "${VENV}\\Scripts\\python.exe" app.py > flask.log 2>&1
                powershell -Command "Start-Sleep -Seconds 3"
                REM Wait until the site responds (timeout 30s)
                powershell -Command ^
                \"$url='http://127.0.0.1:5000'; $t=0; while ($t -lt 30) { try { $r=Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 3; if ($r.StatusCode -eq 200) { Write-Host 'Flask ready'; exit 0 } } catch {}; Start-Sleep -Seconds 1; $t++ }; Write-Error 'Flask did not respond'; exit 1\"
                """
            }
        }

        stage('Run Worker') {
            steps {
                bat """
                "${VENV}\\Scripts\\python.exe" worker.py
                """
            }
        }

        stage('Archive DB') {
            steps {
                archiveArtifacts artifacts: 'moviebooker.db', fingerprint: true
            }
        }
    }

    post {
        always {
            bat """
            REM Clean up: kill any python processes started by Jenkins (optional)
            taskkill /F /IM python.exe /T || exit 0
            """
        }
    }
}