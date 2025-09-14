"""
Machine Learning pipeline for anomaly detection
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import logging
from typing import Tuple, Dict, Any
import joblib
from pathlib import Path

from config import RANDOM_SEED, MODELS_DIR

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Handles feature engineering for the ML pipeline"""
    
    @staticmethod
    def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer features from raw data
        
        Args:
            df: Raw DataFrame with access logs
            
        Returns:
            DataFrame with engineered features
        """
        df_feat = df.copy()
        
        # Time-based features
        df_feat["hour"] = df_feat["access_time"].dt.hour
        df_feat["dayofweek"] = df_feat["access_time"].dt.dayofweek
        df_feat["is_weekend"] = df_feat["dayofweek"].isin([5, 6]).astype(int)
        df_feat["is_after_hours"] = ((df_feat["hour"] < 8) | (df_feat["hour"] > 19)).astype(int)
        
        # User behavior features (if we have historical data)
        user_stats = df_feat.groupby("user_id").agg({
            "file_size_MB": ["mean", "std", "count"],
            "action": lambda x: (x == "download").sum()
        }).round(3)
        
        user_stats.columns = ["avg_file_size", "std_file_size", "total_access", "download_count"]
        user_stats["download_ratio"] = user_stats["download_count"] / user_stats["total_access"]
        
        df_feat = df_feat.merge(user_stats, left_on="user_id", right_index=True, how="left")
        
        # File type risk scoring (based on typical sensitivity)
        file_risk_scores = {
            "Database export": 10,
            "PDF": 7,
            "Excel": 6,
            "CSV": 5,
            "Doc": 4,
            "PPT": 3,
            "Image": 2
        }
        df_feat["file_type_risk"] = df_feat["file_type"].map(file_risk_scores)
        
        # Size-based features
        df_feat["is_large_file"] = (df_feat["file_size_MB"] > 50).astype(int)
        df_feat["size_risk_score"] = np.where(
            df_feat["file_size_MB"] > 100, 10,
            np.where(df_feat["file_size_MB"] > 50, 7,
            np.where(df_feat["file_size_MB"] > 10, 4, 1))
        )
        
        return df_feat


class AnomalyDetector:
    """Main anomaly detection class using Isolation Forest"""
    
    def __init__(self, contamination: float = 0.02, n_estimators: int = 300):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.pipeline = None
        self.feature_columns = None
        self.model_path = MODELS_DIR / "isolation_forest_model.pkl"
    
    def build_pipeline(self) -> Pipeline:
        """Build the ML pipeline with preprocessing and model"""
        cat_features = ["file_type", "action", "user_id"]
        num_features = [
            "file_size_MB", "hour", "dayofweek", "is_weekend", 
            "is_after_hours", "file_type_risk", "is_large_file", 
            "size_risk_score", "avg_file_size", "std_file_size", 
            "download_ratio"
        ]
        
        preprocess = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features),
                ("num", "passthrough", num_features),
            ]
        )
        
        iforest = IsolationForest(
            n_estimators=self.n_estimators,
            max_samples="auto",
            contamination=self.contamination,
            random_state=RANDOM_SEED,
            n_jobs=-1,
        )
        
        pipeline = Pipeline(steps=[("prep", preprocess), ("model", iforest)])
        return pipeline
    
    def fit_and_score(self, df: pd.DataFrame) -> Tuple[Pipeline, pd.DataFrame]:
        """
        Fit the model and score the data
        
        Args:
            df: DataFrame with access logs
            
        Returns:
            Tuple of (fitted_pipeline, scored_dataframe)
        """
        logger.info("Starting model training and scoring")
        
        # Engineer features
        df_feat = FeatureEngineer.engineer_features(df)
        
        # Build and fit pipeline
        self.pipeline = self.build_pipeline()
        self.pipeline.fit(df_feat)
        
        # Store feature columns for later use
        self.feature_columns = df_feat.columns.tolist()
        
        # Score samples
        scores = self.pipeline.named_steps["model"].score_samples(
            self.pipeline.named_steps["prep"].transform(df_feat)
        )
        
        # Convert to risk scores (0-100)
        raw = -scores
        risk = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9) * 100.0
        
        # Get predictions
        preds = self.pipeline.named_steps["model"].predict(
            self.pipeline.named_steps["prep"].transform(df_feat)
        )
        
        # Create scored dataframe
        df_scored = df.copy()
        df_scored["risk_score"] = risk.round(2)
        df_scored["anomaly_flag"] = preds == -1
        
        # Add additional features for analysis
        df_scored["hour"] = df_feat["hour"]
        df_scored["dayofweek"] = df_feat["dayofweek"]
        df_scored["is_weekend"] = df_feat["is_weekend"]
        df_scored["is_after_hours"] = df_feat["is_after_hours"]
        
        logger.info(f"Model training completed. Detected {df_scored['anomaly_flag'].sum()} anomalies")
        
        return self.pipeline, df_scored
    
    def predict_new_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict anomalies for new data using fitted model
        
        Args:
            df: New DataFrame to score
            
        Returns:
            DataFrame with risk scores and anomaly flags
        """
        if self.pipeline is None:
            raise ValueError("Model must be fitted before making predictions")
        
        df_feat = FeatureEngineer.engineer_features(df)
        
        # Ensure same features as training
        missing_features = set(self.feature_columns) - set(df_feat.columns)
        if missing_features:
            logger.warning(f"Missing features: {missing_features}")
            for feature in missing_features:
                df_feat[feature] = 0
        
        # Reorder columns to match training
        df_feat = df_feat[self.feature_columns]
        
        # Score samples
        scores = self.pipeline.named_steps["model"].score_samples(
            self.pipeline.named_steps["prep"].transform(df_feat)
        )
        
        # Convert to risk scores
        raw = -scores
        risk = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9) * 100.0
        
        # Get predictions
        preds = self.pipeline.named_steps["model"].predict(
            self.pipeline.named_steps["prep"].transform(df_feat)
        )
        
        # Create scored dataframe
        df_scored = df.copy()
        df_scored["risk_score"] = risk.round(2)
        df_scored["anomaly_flag"] = preds == -1
        
        return df_scored
    
    def save_model(self) -> None:
        """Save the trained model to disk"""
        if self.pipeline is None:
            raise ValueError("No model to save")
        
        joblib.dump({
            'pipeline': self.pipeline,
            'feature_columns': self.feature_columns,
            'contamination': self.contamination,
            'n_estimators': self.n_estimators
        }, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self) -> bool:
        """Load a pre-trained model from disk"""
        try:
            if self.model_path.exists():
                model_data = joblib.load(self.model_path)
                self.pipeline = model_data['pipeline']
                self.feature_columns = model_data['feature_columns']
                self.contamination = model_data['contamination']
                self.n_estimators = model_data['n_estimators']
                logger.info(f"Model loaded from {self.model_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
        return False
    
    def evaluate_model(self, df: pd.DataFrame, true_labels: pd.Series = None) -> Dict[str, Any]:
        """
        Evaluate model performance (if true labels are available)
        
        Args:
            df: DataFrame with features
            true_labels: True anomaly labels (if available)
            
        Returns:
            Dictionary with evaluation metrics
        """
        if true_labels is None:
            logger.warning("No true labels provided for evaluation")
            return {}
        
        df_feat = FeatureEngineer.engineer_features(df)
        preds = self.pipeline.named_steps["model"].predict(
            self.pipeline.named_steps["prep"].transform(df_feat)
        )
        
        # Convert to binary (1 = normal, 0 = anomaly)
        preds_binary = (preds == 1).astype(int)
        
        # Calculate metrics
        report = classification_report(true_labels, preds_binary, output_dict=True)
        cm = confusion_matrix(true_labels, preds_binary)
        
        return {
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'accuracy': report['accuracy'],
            'precision': report['1']['precision'],
            'recall': report['1']['recall'],
            'f1_score': report['1']['f1-score']
        }


