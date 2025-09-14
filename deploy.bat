@echo off
REM AI-Powered Anomaly Detection Dashboard Deployment Script for Windows
REM This script provides multiple deployment options

echo 🛡️ AI-Powered Anomaly Detection Dashboard - Deployment Script
echo ==============================================================

:menu
echo.
echo Select deployment option:
echo 1) Run locally
echo 2) Deploy with Docker
echo 3) Deploy with Docker Compose
echo 4) Deploy to Streamlit Cloud
echo 5) Deploy to Heroku
echo 6) Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto local
if "%choice%"=="2" goto docker
if "%choice%"=="3" goto docker_compose
if "%choice%"=="4" goto streamlit_cloud
if "%choice%"=="5" goto heroku
if "%choice%"=="6" goto exit
goto menu

:local
echo 🏠 Running locally...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Starting application...
streamlit run main.py
goto end

:docker
echo 🐳 Deploying with Docker...
docker build -t anomaly-detection-dashboard .
docker run -d --name anomaly-detection-app -p 8501:8501 -v %cd%\data:/app/data -v %cd%\logs:/app/logs -v %cd%\models:/app/models --restart unless-stopped anomaly-detection-dashboard
echo ✅ Application deployed! Access it at http://localhost:8501
goto end

:docker_compose
echo 🐳 Deploying with Docker Compose...
docker-compose up -d
echo ✅ Application deployed! Access it at http://localhost:8501
goto end

:streamlit_cloud
echo ☁️ Preparing for Streamlit Cloud deployment...
if not exist .git (
    echo Initializing git repository...
    git init
)
echo 📝 Instructions for Streamlit Cloud deployment:
echo 1. Push your code to GitHub:
echo    git add .
echo    git commit -m "Initial commit"
echo    git branch -M main
echo    git remote add origin ^<your-github-repo-url^>
echo    git push -u origin main
echo.
echo 2. Go to https://share.streamlit.io/
echo 3. Click 'New app' and connect your GitHub repository
echo 4. Set the main file path to: main.py
echo 5. Deploy!
goto end

:heroku
echo 🚀 Preparing for Heroku deployment...
echo 📝 Instructions for Heroku deployment:
echo 1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
echo 2. Login to Heroku: heroku login
echo 3. Create app: heroku create your-app-name
echo 4. Deploy: git push heroku main
echo 5. Open app: heroku open
goto end

:exit
echo Goodbye! 👋
goto end

:end
pause
