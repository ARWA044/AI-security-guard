from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd
from data_generator import DataGenerator
from ml_pipeline import AnomalyDetector
from utils import DataValidator, PerformanceMonitor


def test_data_generation():
    generator = DataGenerator()
    normal = generator.generate_normal_events(n=100)
    suspicious = generator.generate_suspicious_events(n=20)
    assert len(normal) == 100
    assert len(suspicious) == 20
    assert set(normal.columns) == set(suspicious.columns)


def test_ml_pipeline():
    generator = DataGenerator()
    data = pd.concat([generator.generate_normal_events(n=200),
                      generator.generate_suspicious_events(n=50)], ignore_index=True)
    _, scored = AnomalyDetector(contamination=0.1, n_estimators=50).fit_and_score(data)
    assert len(scored) == len(data)
    assert scored["risk_score"].notna().all()
    assert scored["risk_score"].between(0, 100).all()
    assert scored["anomaly_flag"].isin([True, False]).all()


def test_data_validation():
    data = DataGenerator().generate_normal_events(n=100)
    assert DataValidator.validate_dataframe(data)["is_valid"]
    assert not DataValidator.validate_dataframe(pd.DataFrame())["is_valid"]


def test_performance_monitor():
    monitor = PerformanceMonitor()
    monitor.start_timer("test")
    assert monitor.end_timer("test") >= 0


def test_risk_consistent_for_single_record_and_batch(tmp_path):
    generator = DataGenerator()
    train = generator.generate_normal_events(n=200)
    model = AnomalyDetector(n_estimators=30)
    model.fit_and_score(train)
    sample = generator.generate_suspicious_events(n=20).reset_index(drop=True)
    alone = model.predict_new_data(sample.iloc[[0]])
    batch = model.predict_new_data(sample)
    assert alone.iloc[0]['risk_score'] == batch.iloc[0]['risk_score']
    assert alone.iloc[0]['anomaly_flag'] == batch.iloc[0]['anomaly_flag']
    model.model_path = tmp_path / 'model.pkl'
    model.save_model()
    restored = AnomalyDetector()
    restored.model_path = model.model_path
    assert restored.load_model()
    assert restored.predict_new_data(sample)['risk_score'].equals(batch['risk_score'])
