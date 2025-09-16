"""
Data generation and simulation utilities for the anomaly detection dashboard
"""
import os
import uuid
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

from config import (
    FILE_TYPES, ACTIONS, RANDOM_SEED, DEFAULT_NORMAL_EVENTS, 
    DEFAULT_SUSPICIOUS_EVENTS, DEFAULT_DAYS, WORK_START_HOUR, 
    WORK_END_HOUR, TYPICAL_HOUR_MEAN, TYPICAL_HOUR_STD
)

# Set random seeds
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

logger = logging.getLogger(__name__)


class DataGenerator:
    """Handles generation of normal and suspicious file access events"""
    
    def __init__(self):
        self.file_type_weights = [35, 20, 5, 15, 10, 8, 7]  # PDF, Excel, DB, CSV, Doc, PPT, Image
        self.action_weights = [75, 25]  # view, download
    
    def random_user(self) -> str:
        """Generate a random employee ID"""
        return f"employee{np.random.randint(100, 999)}"
    
    def generate_normal_events(
        self, 
        n: int = DEFAULT_NORMAL_EVENTS, 
        start_date: Optional[datetime] = None, 
        days: int = DEFAULT_DAYS
    ) -> pd.DataFrame:
        """
        Generate normal file access events
        
        Args:
            n: Number of events to generate
            start_date: Start date for events (defaults to now - days)
            days: Number of days to span
            
        Returns:
            DataFrame with normal events
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=days)
        
        logger.info(f"Generating {n} normal events over {days} days")
        
        rows = []
        for _ in range(n):
            user = self.random_user()
            file_type = random.choices(FILE_TYPES, weights=self.file_type_weights)[0]
            action = random.choices(ACTIONS, weights=self.action_weights)[0]
            
            # Generate access time during working hours
            day_offset = np.random.randint(0, days)
            hour = int(np.clip(np.random.normal(TYPICAL_HOUR_MEAN, TYPICAL_HOUR_STD), 
                              WORK_START_HOUR, WORK_END_HOUR))
            minute = np.random.randint(0, 60)
            access_time = start_date + timedelta(days=day_offset, hours=hour, minutes=minute)
            
            # Generate realistic file sizes
            file_size = self._generate_file_size(file_type, action)
            
            rows.append({
                "event_id": str(uuid.uuid4()),
                "user_id": user,
                "file_type": file_type,
                "file_size_MB": round(file_size, 3),
                "access_time": access_time,
                "action": action,
            })
        
        return pd.DataFrame(rows)
    
    def generate_suspicious_events(
        self,
        n: int = DEFAULT_SUSPICIOUS_EVENTS,
        start_date: Optional[datetime] = None,
        label_user: Optional[str] = None,
        pattern: str = "mass_downloads"
    ) -> pd.DataFrame:
        """
        Generate suspicious file access events
        
        Args:
            n: Number of events to generate
            start_date: Start date for events
            label_user: Specific user to target
            pattern: Type of suspicious pattern
            
        Returns:
            DataFrame with suspicious events
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=1)
        
        logger.info(f"Generating {n} suspicious events with pattern: {pattern}")
        
        if pattern == "mass_downloads":
            return self._generate_mass_downloads(n, start_date, label_user)
        else:
            return self._generate_generic_suspicious(n, start_date, label_user)
    
    def _generate_file_size(self, file_type: str, action: str) -> float:
        """Generate realistic file size based on type and action"""
        # Base size multipliers
        if file_type == "Database export":
            base = np.random.exponential(scale=15) + 10
        elif file_type in ["Excel", "PPT", "Doc"]:
            base = np.random.exponential(scale=3) + 1
        elif file_type in ["PDF", "CSV"]:
            base = np.random.exponential(scale=2) + 0.5
        else:  # Image
            base = np.random.exponential(scale=1.5) + 0.2
        
        # Downloads are typically larger
        multiplier = 1.3 if action == "download" else 1.0
        return float(np.clip(base * multiplier, 0.1, 120.0))
    
    def _generate_mass_downloads(
        self, 
        n: int, 
        start_date: datetime, 
        label_user: Optional[str]
    ) -> pd.DataFrame:
        """Generate mass download pattern (after-hours bulk downloads)"""
        rows = []
        susp_user = label_user or f"employee{np.random.randint(900, 999)}"
        base_time = start_date.replace(hour=2, minute=0, second=0, microsecond=0)
        
        for i in range(n):
            offset_min = np.random.randint(0, 180)  # 3-hour window
            access_time = base_time + timedelta(minutes=offset_min)
            file_type = random.choices(["PDF", "Database export", "Excel"], weights=[70, 20, 10])[0]
            action = "download"
            
            # Suspicious files are typically larger
            if file_type == "Database export":
                file_size = np.random.uniform(50, 300)
            elif file_type == "PDF":
                file_size = np.random.uniform(5, 50)
            else:
                file_size = np.random.uniform(10, 80)
            
            rows.append({
                "event_id": str(uuid.uuid4()),
                "user_id": susp_user,
                "file_type": file_type,
                "file_size_MB": round(float(file_size), 3),
                "access_time": access_time,
                "action": action,
            })
        
        return pd.DataFrame(rows)
    
    def _generate_generic_suspicious(
        self, 
        n: int, 
        start_date: datetime, 
        label_user: Optional[str]
    ) -> pd.DataFrame:
        """Generate generic suspicious pattern (odd hours, mixed types)"""
        rows = []
        
        for i in range(n):
            user = label_user or self.random_user()
            day_offset = np.random.randint(0, 3)
            access_time = (start_date - timedelta(days=day_offset)).replace(
                hour=3, minute=np.random.randint(0, 60)
            )
            file_type = random.choice(FILE_TYPES)
            action = "download"
            file_size = np.random.uniform(10, 150)
            
            rows.append({
                "event_id": str(uuid.uuid4()),
                "user_id": user,
                "file_type": file_type,
                "file_size_MB": round(float(file_size), 3),
                "access_time": access_time,
                "action": action,
            })
        
        return pd.DataFrame(rows)


class DataManager:
    """Handles data loading, saving, and management"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.generator = DataGenerator()
    
    def load_or_generate(self) -> pd.DataFrame:
        """Load existing data or generate new dataset"""
        if os.path.exists(self.csv_path):
            logger.info(f"Loading existing data from {self.csv_path}")
            df = pd.read_csv(self.csv_path, parse_dates=["access_time"])
            return df
        
        logger.info("Generating new dataset")
        # Create initial dataset with normal + suspicious events
        df_normal = self.generator.generate_normal_events(n=2500, days=10)
        df_susp = pd.concat([
            self.generator.generate_suspicious_events(n=120, pattern="mass_downloads"),
            self.generator.generate_suspicious_events(n=60, pattern="generic"),
        ], ignore_index=True)
        
        df = pd.concat([df_normal, df_susp], ignore_index=True)
        df = df.sample(frac=1.0, random_state=RANDOM_SEED).reset_index(drop=True)
        
        # Save to CSV
        df.to_csv(self.csv_path, index=False)
        logger.info(f"Dataset saved to {self.csv_path}")
        return df
    
    def save_data(self, df: pd.DataFrame) -> None:
        """Save DataFrame to CSV"""
        try:
            df.to_csv(self.csv_path, index=False)
            logger.info(f"Data saved to {self.csv_path}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            raise
