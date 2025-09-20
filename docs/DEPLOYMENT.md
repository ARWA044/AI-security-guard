


# 🚀 Deployment Guide - AI-Powered Anomaly Detection Dashboard

This guide explains how to set up, configure, and deploy your Streamlit-based anomaly detection dashboard, with a focus on Streamlit Cloud as the sole deployment method.

## 📋 Prerequisites

- Python 3.11+
- Git
- (Optional) A virtual environment tool such as venv or conda
- A GitHub account
- A Streamlit Cloud account ([streamlit.io/cloud](https://streamlit.io/cloud))

## 🏠 Local Development

### Quick Start
```bash
# Clone the repository

cd AI-security-guard

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/main.py
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
streamlit run src/main.py
```

## ☁️ Deploying on Streamlit Cloud (Recommended)

Streamlit Cloud is the recommended and easiest way to deploy this app. It offers free hosting, GitHub integration, and automatic updates.

### Advantages
- Free tier available
- Easy GitHub integration
- Automatic deployments
- Built-in monitoring

### Steps
1. Push your code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to `src/main.py` (or adjust if your entry point is different)
6. Click "Deploy". Your app will build and launch automatically

### Configuration
- No additional configuration needed for most cases
- If you need to set environment variables, use the "Advanced settings" in the app dashboard
- Requirements are read from `requirements.txt` automatically

### Updating Your App
- Any push to your GitHub repository will automatically trigger a redeploy

## 🔧 Production Configuration

### Environment Variables
If you need to set environment variables (e.g., for secrets or custom config), use the Streamlit Cloud "Advanced settings" panel.

Example:
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
1. **HTTPS**: Streamlit Cloud uses HTTPS by default
2. **Authentication**: For sensitive data, consider adding authentication to your app
3. **Rate Limiting**: Not provided by default—implement in-app if needed
4. **Input Validation**: Always validate user inputs
5. **Secrets Management**: Use environment variables for sensitive data

### Monitoring and Logging
1. **Health Checks**: Streamlit Cloud provides basic health monitoring
2. **Logging**: Use Streamlit's built-in logging or write to files as needed
3. **Performance Monitoring**: Monitor app responsiveness and resource usage via Streamlit Cloud dashboard
4. **Error Tracking**: Use try/except and logging for error handling

## 📊 Performance Optimization

### For Production
1. **Caching**: Use Streamlit's `@st.cache_data` or `@st.cache_resource` for expensive operations
2. **Data Loading**: Implement lazy loading for large datasets
3. **Model Optimization**: Use smaller, optimized models for production
4. **Resource Limits**: Streamlit Cloud manages resources, but optimize your code for efficiency

### Scaling Considerations
1. **Horizontal Scaling**: Not supported on free Streamlit Cloud tier
2. **Database**: For large datasets, use external managed databases
3. **CDN**: Use CDN for static assets if needed
4. **Caching**: Use in-app caching for session management

## 🚨 Troubleshooting

### Common Issues
1. **App fails to deploy**: Check the logs in the Streamlit Cloud dashboard for errors
2. **Dependency issues**: Ensure all required packages are listed in `requirements.txt`
3. **File not found**: Make sure all necessary files are committed to your repository
4. **App not updating**: Confirm you pushed to the correct branch and redeploy if needed

## 📞 Support

For deployment issues:
1. Check the logs in the Streamlit Cloud dashboard
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Check your repository structure and entry point

## 🎯 Next Steps

After successful deployment:
1. Set up monitoring and alerting (if needed)
2. Configure backup strategies for your data
3. Implement additional security measures
4. Plan for scaling as your usage grows

---

**Happy Deploying on Streamlit Cloud! 🚀**
