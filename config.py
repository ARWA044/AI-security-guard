"""
Configuration settings for the AI-Powered Anomaly Detection Dashboard
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
RANDOM_SEED = 42

# ML settings
DEFAULT_CONTAMINATION = 0.02
N_ESTIMATORS = 300
MAX_SAMPLES = "auto"

# UI settings
PAGE_TITLE = "AI-Powered Anomaly Detection Dashboard"
PAGE_ICON = "🛡️"
LAYOUT = "wide"

# File types and actions
FILE_TYPES = ["PDF", "Excel", "Database export", "CSV", "Doc", "PPT", "Image"]
ACTIONS = ["view", "download"]

# Simulation settings
DEFAULT_NORMAL_EVENTS = 2500
DEFAULT_SUSPICIOUS_EVENTS = 180
DEFAULT_DAYS = 10

# Working hours (for normal event generation)
WORK_START_HOUR = 8
WORK_END_HOUR = 19
TYPICAL_HOUR_MEAN = 13
TYPICAL_HOUR_STD = 2.5


