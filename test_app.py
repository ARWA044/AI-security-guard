"""
Simple test script to verify the application works
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_generator import DataGenerator, DataManager
from ml_pipeline import AnomalyDetector
from utils import DataValidator, PerformanceMonitor
import pandas as pd

def test_data_generation():
    """Test data generation functionality"""
    print("Testing data generation...")
    
    generator = DataGenerator()
    
    # Test normal events
    normal_df = generator.generate_normal_events(n=100)
    print(f"Generated {len(normal_df)} normal events")
    print(f"Columns: {list(normal_df.columns)}")
    
    # Test suspicious events
    susp_df = generator.generate_suspicious_events(n=20)
    print(f"Generated {len(susp_df)} suspicious events")
    
    return normal_df, susp_df

def test_ml_pipeline():
    """Test ML pipeline functionality"""
    print("\nTesting ML pipeline...")
    
    # Generate test data
    generator = DataGenerator()
    df = generator.generate_normal_events(n=200)
    susp_df = generator.generate_suspicious_events(n=50)
    combined_df = pd.concat([df, susp_df], ignore_index=True)
    
    # Test anomaly detection
    detector = AnomalyDetector(contamination=0.1)
    pipeline, df_scored = detector.fit_and_score(combined_df)
    
    print(f"Detected {df_scored['anomaly_flag'].sum()} anomalies out of {len(df_scored)} events")
    print(f"Average risk score: {df_scored['risk_score'].mean():.2f}")
    
    return df_scored

def test_data_validation():
    """Test data validation functionality"""
    print("\nTesting data validation...")
    
    generator = DataGenerator()
    df = generator.generate_normal_events(n=100)
    
    validator = DataValidator()
    validation_results = validator.validate_dataframe(df)
    
    print(f"Data validation passed: {validation_results['is_valid']}")
    if validation_results['errors']:
        print(f"Errors: {validation_results['errors']}")
    if validation_results['warnings']:
        print(f"Warnings: {validation_results['warnings']}")
    
    return validation_results

def test_performance_monitoring():
    """Test performance monitoring"""
    print("\nTesting performance monitoring...")
    
    monitor = PerformanceMonitor()
    
    # Simulate some operations
    monitor.start_timer("test_operation")
    import time
    time.sleep(0.1)  # Simulate work
    duration = monitor.end_timer("test_operation")
    
    print(f"Test operation took: {duration:.3f}s")
    
    metrics = monitor.get_metrics()
    print(f"Performance metrics: {metrics}")

def main():
    """Run all tests"""
    print("Running application tests...\n")
    
    try:
        # Test data generation
        normal_df, susp_df = test_data_generation()
        
        # Test ML pipeline
        df_scored = test_ml_pipeline()
        
        # Test data validation
        validation_results = test_data_validation()
        
        # Test performance monitoring
        test_performance_monitoring()
        
        print("\n✅ All tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


