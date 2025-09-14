# AI-Powered Anomaly Detection Dashboard

A comprehensive cybersecurity dashboard built with Streamlit and scikit-learn that detects suspicious file access patterns to help prevent data breaches.

## 🚀 Key Improvements Made

### 1. **Modular Architecture**
- **Separated concerns** into focused modules:
  - `config.py` - Configuration management
  - `data_generator.py` - Data simulation and generation
  - `ml_pipeline.py` - Machine learning pipeline
  - `ui_components.py` - UI components and visualizations
  - `utils.py` - Utility functions and helpers
  - `main.py` - Main application orchestrator

### 2. **Enhanced Machine Learning**
- **Advanced feature engineering** with time-based and behavioral features
- **Model persistence** with joblib for saving/loading trained models
- **Improved anomaly detection** with better risk scoring
- **Model validation** and performance metrics
- **Feature importance** analysis

### 3. **Performance Optimizations**
- **Caching** for expensive operations using Streamlit's cache decorators
- **Performance monitoring** with timing metrics
- **Efficient data processing** with vectorized operations
- **Lazy loading** for large datasets

### 4. **Enhanced UI/UX**
- **Responsive design** with better column layouts
- **Interactive visualizations** with Plotly
- **Tabbed interface** for different chart types
- **Real-time alerts** for high-risk events
- **Data export** functionality
- **Advanced filtering** options

### 5. **Data Management**
- **Structured data validation** with comprehensive checks
- **Data export** capabilities (CSV format)
- **Session state management** for better user experience
- **Error handling** and logging throughout

### 6. **Security Features**
- **High-risk event alerts** with configurable thresholds
- **Audit logging** for all operations
- **Data integrity validation**
- **Input sanitization** and validation

## 📁 Project Structure

```
cnss_project/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── data_generator.py      # Data simulation and generation
├── ml_pipeline.py         # Machine learning pipeline
├── ui_components.py       # UI components and visualizations
├── utils.py              # Utility functions and helpers
├── test_app.py           # Test script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── data/               # Data directory
│   └── file_access_logs.csv
├── logs/               # Log files
└── models/            # Saved ML models
    └── isolation_forest_model.pkl
```

## 🛠️ Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run main.py
   ```

3. **Run tests:**
   ```bash
   python test_app.py
   ```

## 🎯 Features

### **Dashboard Components**
- **Real-time anomaly detection** using Isolation Forest
- **Interactive visualizations** with multiple chart types
- **Advanced filtering** by user, file type, risk level
- **Attack simulation** for testing and demonstration
- **Data export** functionality

### **Machine Learning**
- **Isolation Forest** algorithm for unsupervised anomaly detection
- **Feature engineering** with time-based and behavioral features
- **Risk scoring** from 0-100 for each event
- **Model persistence** and loading capabilities
- **Performance monitoring** and validation

### **Data Management**
- **Simulated data generation** with realistic patterns
- **Data validation** and integrity checks
- **CSV export** with download functionality
- **Session state management** for better UX

## 🔧 Configuration

Key settings can be modified in `config.py`:

- **File types** and actions to simulate
- **ML model parameters** (contamination, estimators)
- **Working hours** for normal event generation
- **Data paths** and logging configuration

## 📊 Visualizations

1. **Downloads per Hour** - Bar chart with anomaly overlay
2. **File Size Distribution** - Histogram comparing normal vs suspicious
3. **Risk Score Distribution** - Risk score histogram
4. **User Activity Heatmap** - Activity patterns by user and hour
5. **Anomaly Timeline** - Daily anomaly trends

## 🚨 Alert System

The dashboard includes an alert system that:
- **Identifies high-risk events** (configurable threshold)
- **Displays real-time warnings** in the UI
- **Provides detailed event information**
- **Tracks suspicious user patterns**

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_app.py
```

Tests cover:
- Data generation
- ML pipeline
- Data validation
- Performance monitoring

## 📈 Performance

The application includes performance monitoring for:
- Data loading times
- Model training duration
- Prediction latency
- Overall application performance

## 🔒 Security Considerations

- **Input validation** for all user inputs
- **Data sanitization** before processing
- **Audit logging** for security events
- **Error handling** to prevent information leakage

## 🚀 Future Enhancements

Potential improvements for future versions:
- **Database integration** (PostgreSQL, MongoDB)
- **Real-time data ingestion** from APIs
- **User authentication** and authorization
- **Advanced ML models** (ensemble methods)
- **Mobile-responsive design**
- **API endpoints** for external integration

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Built with ❤️ using Streamlit, scikit-learn, and Plotly**


