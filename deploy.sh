#!/bin/bash

# AI-Powered Anomaly Detection Dashboard Deployment Script
# This script provides multiple deployment options

set -e

echo "🛡️ AI-Powered Anomaly Detection Dashboard - Deployment Script"
echo "=============================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to deploy with Docker
deploy_docker() {
    echo "🐳 Deploying with Docker..."
    
    if ! command_exists docker; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Build the Docker image
    echo "Building Docker image..."
    docker build -t anomaly-detection-dashboard .
    
    # Run the container
    echo "Starting container..."
    docker run -d \
        --name anomaly-detection-app \
        -p 8501:8501 \
        -v $(pwd)/data:/app/data \
        -v $(pwd)/logs:/app/logs \
        -v $(pwd)/models:/app/models \
        --restart unless-stopped \
        anomaly-detection-dashboard
    
    echo "✅ Application deployed! Access it at http://localhost:8501"
}

# Function to deploy with Docker Compose
deploy_docker_compose() {
    echo "🐳 Deploying with Docker Compose..."
    
    if ! command_exists docker-compose; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Start the services
    docker-compose up -d
    
    echo "✅ Application deployed! Access it at http://localhost:8501"
}

# Function to deploy to Streamlit Cloud
deploy_streamlit_cloud() {
    echo "☁️ Preparing for Streamlit Cloud deployment..."
    
    # Check if git is initialized
    if [ ! -d ".git" ]; then
        echo "Initializing git repository..."
        git init
    fi
    
    # Create .gitignore if it doesn't exist
    if [ ! -f ".gitignore" ]; then
        cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Data and models
data/
logs/
models/
*.pkl
*.csv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml
EOF
    fi
    
    echo "📝 Instructions for Streamlit Cloud deployment:"
    echo "1. Push your code to GitHub:"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git branch -M main"
    echo "   git remote add origin <your-github-repo-url>"
    echo "   git push -u origin main"
    echo ""
    echo "2. Go to https://share.streamlit.io/"
    echo "3. Click 'New app' and connect your GitHub repository"
    echo "4. Set the main file path to: main.py"
    echo "5. Deploy!"
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "🚀 Preparing for Heroku deployment..."
    
    # Create Procfile
    cat > Procfile << EOF
web: streamlit run main.py --server.port=\$PORT --server.address=0.0.0.0
EOF
    
    # Create runtime.txt
    echo "python-3.11.0" > runtime.txt
    
    # Create app.json for Heroku
    cat > app.json << EOF
{
  "name": "AI-Powered Anomaly Detection Dashboard",
  "description": "A comprehensive cybersecurity dashboard built with Streamlit and scikit-learn",
  "repository": "https://github.com/yourusername/cnss_project",
  "keywords": ["streamlit", "machine-learning", "anomaly-detection", "cybersecurity"],
  "stack": "heroku-22"
}
EOF
    
    echo "📝 Instructions for Heroku deployment:"
    echo "1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
    echo "2. Login to Heroku: heroku login"
    echo "3. Create app: heroku create your-app-name"
    echo "4. Deploy: git push heroku main"
    echo "5. Open app: heroku open"
}

# Function to run locally
run_local() {
    echo "🏠 Running locally..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    # Run the application
    echo "Starting application..."
    streamlit run main.py
}

# Main menu
echo ""
echo "Select deployment option:"
echo "1) Run locally"
echo "2) Deploy with Docker"
echo "3) Deploy with Docker Compose"
echo "4) Deploy to Streamlit Cloud"
echo "5) Deploy to Heroku"
echo "6) Exit"
echo ""

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        run_local
        ;;
    2)
        deploy_docker
        ;;
    3)
        deploy_docker_compose
        ;;
    4)
        deploy_streamlit_cloud
        ;;
    5)
        deploy_heroku
        ;;
    6)
        echo "Goodbye! 👋"
        exit 0
        ;;
    *)
        echo "Invalid option. Please run the script again."
        exit 1
        ;;
esac
