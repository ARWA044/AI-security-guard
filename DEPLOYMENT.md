# 🚀 Deployment Guide - AI-Powered Anomaly Detection Dashboard

This guide provides multiple deployment options for your Streamlit-based anomaly detection dashboard.

## 📋 Prerequisites

- Python 3.11+
- Git
- Docker (for containerized deployment)
- Cloud platform account (for cloud deployment)

## 🏠 Local Development

### Quick Start
```bash
# Clone the repository
git clone <your-repo-url>
cd cnss_project

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

### Using Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

## 🐳 Docker Deployment

### Option 1: Docker Run
```bash
# Build the image
docker build -t anomaly-detection-dashboard .

# Run the container
docker run -d \
  --name anomaly-detection-app \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/models:/app/models \
  --restart unless-stopped \
  anomaly-detection-dashboard
```

### Option 2: Docker Compose
```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## ☁️ Cloud Deployment Options

### 1. Streamlit Cloud (Recommended for Quick Deployment)

**Advantages:**
- Free tier available
- Easy GitHub integration
- Automatic deployments
- Built-in monitoring

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Click "New app"
4. Connect your GitHub repository
5. Set main file path to `main.py`
6. Deploy!

**Configuration:**
- No additional configuration needed
- Streamlit Cloud handles everything automatically

### 2. Heroku

**Advantages:**
- Easy deployment
- Good free tier
- Add-ons available
- Automatic scaling

**Steps:**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`
5. Open: `heroku open`

**Configuration:**
- Uses `Procfile` and `runtime.txt`
- Environment variables set in `app.json`

### 3. AWS Elastic Beanstalk

**Advantages:**
- Enterprise-grade
- Auto-scaling
- Load balancing
- Monitoring and logging

**Steps:**
1. Install AWS CLI
2. Configure credentials: `aws configure`
3. Deploy using EB CLI:
   ```bash
   # Install EB CLI
   pip install awsebcli
   
   # Initialize EB application
   eb init
   
   # Create environment
   eb create production
   
   # Deploy
   eb deploy
   ```

### 4. Google Cloud Platform

**Steps:**
1. Install Google Cloud SDK
2. Create a new project
3. Enable App Engine
4. Deploy:
   ```bash
   gcloud app deploy
   ```

### 5. Azure App Service

**Steps:**
1. Install Azure CLI
2. Login: `az login`
3. Create resource group: `az group create --name myResourceGroup --location eastus`
4. Create app service plan: `az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux`
5. Create web app: `az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myAppName --runtime "PYTHON|3.11"`
6. Deploy: `az webapp deployment source config --name myAppName --resource-group myResourceGroup --repo-url <your-repo-url> --branch main --manual-integration`

## 🔧 Production Configuration

### Environment Variables
```bash
# Streamlit Configuration
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true

# Application Configuration
PYTHONPATH=/app
LOG_LEVEL=INFO
```

### Security Considerations
1. **HTTPS**: Always use HTTPS in production
2. **Authentication**: Consider adding authentication for sensitive data
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Input Validation**: Validate all user inputs
5. **Secrets Management**: Use environment variables for sensitive data

### Monitoring and Logging
1. **Health Checks**: Application includes health check endpoints
2. **Logging**: Comprehensive logging to `logs/` directory
3. **Performance Monitoring**: Built-in performance metrics
4. **Error Tracking**: Structured error handling and reporting

## 📊 Performance Optimization

### For Production:
1. **Caching**: Enable Streamlit caching for expensive operations
2. **Data Loading**: Implement lazy loading for large datasets
3. **Model Optimization**: Use smaller, optimized models for production
4. **Resource Limits**: Set appropriate memory and CPU limits

### Scaling Considerations:
1. **Horizontal Scaling**: Use load balancers for multiple instances
2. **Database**: Consider external database for large datasets
3. **CDN**: Use CDN for static assets
4. **Caching**: Implement Redis for session management

## 🚨 Troubleshooting

### Common Issues:

1. **Port Already in Use**:
   ```bash
   # Find process using port 8501
   lsof -i :8501
   # Kill the process
   kill -9 <PID>
   ```

2. **Memory Issues**:
   - Increase container memory limits
   - Optimize data loading
   - Use data sampling for large datasets

3. **Model Loading Errors**:
   - Check model file permissions
   - Ensure model files are in the correct directory
   - Verify model compatibility

4. **Docker Build Failures**:
   - Check Dockerfile syntax
   - Ensure all dependencies are in requirements.txt
   - Clear Docker cache: `docker system prune`

## 📈 Monitoring

### Health Check Endpoint
- URL: `http://your-app-url/_stcore/health`
- Returns: 200 OK if healthy

### Log Files
- Location: `logs/` directory
- Format: Structured JSON logs
- Rotation: Automatic log rotation

### Performance Metrics
- Data loading time
- Model training duration
- Prediction latency
- Memory usage

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

## 📞 Support

For deployment issues:
1. Check the logs in `logs/` directory
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Check network connectivity and firewall settings

## 🎯 Next Steps

After successful deployment:
1. Set up monitoring and alerting
2. Configure backup strategies
3. Implement security measures
4. Plan for scaling
5. Set up CI/CD pipeline

---

**Happy Deploying! 🚀**
