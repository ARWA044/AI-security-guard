"""
Utility functions and helpers for the anomaly detection dashboard
"""
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

# Configure logging
def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration"""
    from config import LOGS_DIR
    
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOGS_DIR / "anomaly_detection.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


class SessionStateManager:
    """Manages Streamlit session state"""
    
    @staticmethod
    def ensure_session_state():
        """Ensure required session state variables exist"""
        required_keys = ["df", "model", "df_scored"]
        
        for key in required_keys:
            if key not in st.session_state:
                st.session_state[key] = None


class DataValidator:
    """Validates data integrity and structure"""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate DataFrame structure and content
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }
        
        # Required columns
        required_columns = ["event_id", "user_id", "file_type", "file_size_MB", "access_time", "action"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            validation_results["is_valid"] = False
            validation_results["errors"].append(f"Missing required columns: {missing_columns}")
        
        # Check for empty DataFrame
        if df.empty:
            validation_results["is_valid"] = False
            validation_results["errors"].append("DataFrame is empty")
            return validation_results
        
        # Check data types
        if "access_time" in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df["access_time"]):
                validation_results["warnings"].append("access_time column is not datetime type")
        
        if "file_size_MB" in df.columns:
            if not pd.api.types.is_numeric_dtype(df["file_size_MB"]):
                validation_results["warnings"].append("file_size_MB column is not numeric type")
        
        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.any():
            validation_results["warnings"].append(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
        
        # Basic statistics
        validation_results["stats"] = {
            "total_rows": len(df),
            "unique_users": df["user_id"].nunique() if "user_id" in df.columns else 0,
            "unique_file_types": df["file_type"].nunique() if "file_type" in df.columns else 0,
            "date_range": {
                "start": df["access_time"].min().isoformat() if "access_time" in df.columns else None,
                "end": df["access_time"].max().isoformat() if "access_time" in df.columns else None
            }
        }
        
        return validation_results
    
    @staticmethod
    def validate_ml_predictions(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate ML model predictions
        
        Args:
            df: DataFrame with predictions
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }
        
        # Check for required prediction columns
        if "risk_score" not in df.columns:
            validation_results["is_valid"] = False
            validation_results["errors"].append("Missing risk_score column")
        
        if "anomaly_flag" not in df.columns:
            validation_results["is_valid"] = False
            validation_results["errors"].append("Missing anomaly_flag column")
        
        if not validation_results["is_valid"]:
            return validation_results
        
        # Validate risk scores
        risk_scores = df["risk_score"]
        if not pd.api.types.is_numeric_dtype(risk_scores):
            validation_results["errors"].append("risk_score column is not numeric")
        else:
            if risk_scores.min() < 0 or risk_scores.max() > 100:
                validation_results["warnings"].append("risk_score values outside expected range [0, 100]")
        
        # Validate anomaly flags
        anomaly_flags = df["anomaly_flag"]
        if not pd.api.types.is_bool_dtype(anomaly_flags):
            validation_results["warnings"].append("anomaly_flag column is not boolean type")
        
        # Statistics
        validation_results["stats"] = {
            "total_predictions": len(df),
            "anomalies_detected": int(anomaly_flags.sum()) if pd.api.types.is_bool_dtype(anomaly_flags) else 0,
            "anomaly_rate": float(anomaly_flags.mean()) if pd.api.types.is_bool_dtype(anomaly_flags) else 0,
            "avg_risk_score": float(risk_scores.mean()) if pd.api.types.is_numeric_dtype(risk_scores) else 0,
            "max_risk_score": float(risk_scores.max()) if pd.api.types.is_numeric_dtype(risk_scores) else 0
        }
        
        return validation_results


class PerformanceMonitor:
    """Monitors application performance"""
    
    def __init__(self):
        self.start_times = {}
        self.metrics = {}
    
    def start_timer(self, operation: str) -> None:
        """Start timing an operation"""
        self.start_times[operation] = datetime.now()
    
    def end_timer(self, operation: str) -> float:
        """End timing an operation and return duration"""
        if operation not in self.start_times:
            return 0.0
        
        duration = (datetime.now() - self.start_times[operation]).total_seconds()
        self.metrics[operation] = duration
        del self.start_times[operation]
        return duration
    
    def get_metrics(self) -> Dict[str, float]:
        """Get performance metrics"""
        return self.metrics.copy()
    
    def log_performance(self, operation: str, duration: float) -> None:
        """Log performance metrics"""
        logger = logging.getLogger(__name__)
        logger.info(f"Performance - {operation}: {duration:.2f}s")


class DataExporter:
    """Handles data export functionality"""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str = None) -> str:
        """
        Export DataFrame to CSV
        
        Args:
            df: DataFrame to export
            filename: Optional custom filename
            
        Returns:
            Path to exported file
        """
        from config import DATA_DIR
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"anomaly_data_export_{timestamp}.csv"
        
        filepath = DATA_DIR / filename
        df.to_csv(filepath, index=False)
        
        logger = logging.getLogger(__name__)
        logger.info(f"Data exported to {filepath}")
        
        return str(filepath)
    
    @staticmethod
    def export_anomalies_only(df: pd.DataFrame, filename: str = None) -> str:
        """
        Export only anomalies to CSV
        
        Args:
            df: DataFrame with anomaly flags
            filename: Optional custom filename
            
        Returns:
            Path to exported file
        """
        if "anomaly_flag" not in df.columns:
            raise ValueError("DataFrame must contain anomaly_flag column")
        
        anomalies = df[df["anomaly_flag"]].copy()
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"anomalies_only_{timestamp}.csv"
        
        return DataExporter.export_to_csv(anomalies, filename)


class AlertManager:
    """Manages alerts and notifications"""
    
    @staticmethod
    def check_high_risk_events(df: pd.DataFrame, threshold: float = 80.0) -> List[Dict]:
        """
        Check for high-risk events that need immediate attention
        
        Args:
            df: DataFrame with risk scores
            threshold: Risk score threshold for alerts
            
        Returns:
            List of high-risk events
        """
        if "risk_score" not in df.columns:
            return []
        
        high_risk = df[df["risk_score"] >= threshold].copy()
        
        alerts = []
        for _, row in high_risk.iterrows():
            alerts.append({
                "event_id": row.get("event_id", "unknown"),
                "user_id": row.get("user_id", "unknown"),
                "risk_score": row.get("risk_score", 0),
                "file_type": row.get("file_type", "unknown"),
                "access_time": row.get("access_time", "unknown"),
                "action": row.get("action", "unknown")
            })
        
        return alerts
    
    @staticmethod
    def display_alerts(alerts: List[Dict]) -> None:
        """Display alerts in the UI"""
        if not alerts:
            return
        
        st.warning(f"🚨 {len(alerts)} high-risk events detected!")
        
        for alert in alerts[:5]:  # Show top 5
            st.error(
                f"**User {alert['user_id']}** - Risk Score: {alert['risk_score']:.1f} - "
                f"{alert['action']} {alert['file_type']} at {alert['access_time']}"
            )
        
        if len(alerts) > 5:
            st.info(f"... and {len(alerts) - 5} more high-risk events")


class CacheManager:
    """Manages caching for performance optimization"""
    
    @staticmethod
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def load_data_cached(csv_path: str) -> pd.DataFrame:
        """Cached data loading function"""
        return pd.read_csv(csv_path, parse_dates=["access_time"])
    
    @staticmethod
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def process_data_cached(df: pd.DataFrame, contamination: float) -> tuple:
        """Cached data processing function"""
        from ml_pipeline import AnomalyDetector
        
        detector = AnomalyDetector(contamination=contamination)
        pipeline, df_scored = detector.fit_and_score(df)
        
        return pipeline, df_scored


