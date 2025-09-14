"""
Production configuration for the AI-Powered Anomaly Detection Dashboard
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
MODELS_DIR = PROJECT_ROOT / "models"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Data settings
CSV_PATH = DATA_DIR / "file_access_logs.csv"
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))

# ML settings - Production optimized
DEFAULT_CONTAMINATION = float(os.getenv("DEFAULT_CONTAMINATION", "0.02"))
N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", "100"))  # Reduced for production
MAX_SAMPLES = os.getenv("MAX_SAMPLES", "auto")

# UI settings
PAGE_TITLE = os.getenv("PAGE_TITLE", "AI-Powered Anomaly Detection Dashboard")
PAGE_ICON = os.getenv("PAGE_ICON", "🛡️")
LAYOUT = os.getenv("LAYOUT", "wide")

# File types and actions
FILE_TYPES = ["PDF", "Excel", "Database export", "CSV", "Doc", "PPT", "Image"]
ACTIONS = ["view", "download"]

# Simulation settings - Production optimized
DEFAULT_NORMAL_EVENTS = int(os.getenv("DEFAULT_NORMAL_EVENTS", "1000"))  # Reduced for production
DEFAULT_SUSPICIOUS_EVENTS = int(os.getenv("DEFAULT_SUSPICIOUS_EVENTS", "50"))  # Reduced for production
DEFAULT_DAYS = int(os.getenv("DEFAULT_DAYS", "7"))  # Reduced for production

# Working hours (for normal event generation)
WORK_START_HOUR = int(os.getenv("WORK_START_HOUR", "8"))
WORK_END_HOUR = int(os.getenv("WORK_END_HOUR", "19"))
TYPICAL_HOUR_MEAN = int(os.getenv("TYPICAL_HOUR_MEAN", "13"))
TYPICAL_HOUR_STD = float(os.getenv("TYPICAL_HOUR_STD", "2.5"))

# Production settings
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "200"))  # MB
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # seconds

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Database settings (for future use)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Monitoring settings
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
METRICS_PORT = int(os.getenv("METRICS_PORT", "9090"))

# Alert settings
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")
ALERT_WEBHOOK = os.getenv("ALERT_WEBHOOK", "")
HIGH_RISK_THRESHOLD = float(os.getenv("HIGH_RISK_THRESHOLD", "80.0"))
