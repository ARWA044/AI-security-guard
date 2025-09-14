"""
Main application file for the AI-Powered Anomaly Detection Dashboard
"""
import streamlit as st
import pandas as pd
import logging
from typing import Dict, Any
# Import our modules
from config import CSV_PATH
from data_generator import DataManager
from ml_pipeline import AnomalyDetector
from ui_components import DashboardComponents, Visualizations, DataTable
from utils import (
    setup_logging, SessionStateManager, DataValidator, 
    PerformanceMonitor, DataExporter, AlertManager, CacheManager
)

# Setup logging
setup_logging()

logger = logging.getLogger(__name__)


class AnomalyDetectionApp:
    """Main application class"""
    
    def __init__(self):
        self.data_manager = DataManager(str(CSV_PATH))
        self.performance_monitor = PerformanceMonitor()
        self.data_validator = DataValidator()
    
    def run(self):
        """Run the main application"""
        try:
            # Setup page configuration
            DashboardComponents.setup_page_config()
            DashboardComponents.create_header()
            
            # Create sidebar controls
            controls = DashboardComponents.create_sidebar_controls()
            
            # Initialize session state
            SessionStateManager.ensure_session_state()
            
            # Load or generate data
            self._load_data()
            
            # Handle model retraining
            if controls['refresh']:
                self._retrain_model(controls['contamination'])
            
            # Handle attack simulation
            if controls['run_sim']:
                self._simulate_attack(controls['sim_user'], controls['num_events'])
            
            # Handle data export
            if controls['export_data']:
                self._export_data()
            
            # Create filters
            filters = DashboardComponents.create_filters(st.session_state.df_scored)
            
            # Apply filters
            filtered_df = self._apply_filters(st.session_state.df_scored, filters)
            
            # Display summary
            DashboardComponents.create_summary_cards(filtered_df)
            
            # Check for high-risk alerts
            alerts = AlertManager.check_high_risk_events(filtered_df, threshold=80.0)
            AlertManager.display_alerts(alerts)
            
            # Create visualizations
            self._create_visualizations(filtered_df)
            
            # Display data tables
            self._display_data_tables(filtered_df, controls['show_stats'])
            
            # Display footer
            self._create_footer()
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            st.error(f"An error occurred: {e}")
            st.error("Please check the logs for more details.")
    
    def _load_data(self):
        """Load or generate data"""
        self.performance_monitor.start_timer("data_loading")
        
        try:
            if st.session_state.df is None:
                st.session_state.df = self.data_manager.load_or_generate()
            
            if st.session_state.model is None or st.session_state.df_scored is None:
                # Try to load existing model first
                detector = AnomalyDetector()
                if not detector.load_model():
                    # Train new model if no existing model found
                    detector, st.session_state.df_scored = detector.fit_and_score(st.session_state.df)
                else:
                    # Use loaded model to score data
                    st.session_state.df_scored = detector.predict_new_data(st.session_state.df)
                
                st.session_state.model = detector
            
            duration = self.performance_monitor.end_timer("data_loading")
            logger.info(f"Data loaded in {duration:.2f}s")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            st.error("Failed to load data. Please check the logs.")
            raise
    
    def _retrain_model(self, contamination: float):
        """Retrain the model with new contamination parameter"""
        self.performance_monitor.start_timer("model_training")
        
        try:
            detector = AnomalyDetector(contamination=contamination)
            detector, df_scored = detector.fit_and_score(st.session_state.df)
            
            st.session_state.model = detector
            st.session_state.df_scored = df_scored
            
            # Save the model
            detector.save_model()
            
            duration = self.performance_monitor.end_timer("model_training")
            logger.info(f"Model retrained in {duration:.2f}s")
            
            st.success("✅ Model re-trained successfully!")
            
        except Exception as e:
            logger.error(f"Error retraining model: {e}")
            st.error("Failed to retrain model. Please check the logs.")
    
    def _simulate_attack(self, user_id: str, num_events: int):
        """Simulate a cyber attack"""
        self.performance_monitor.start_timer("attack_simulation")
        
        try:
            from data_generator import DataGenerator
            
            generator = DataGenerator()
            new_events = generator.generate_suspicious_events(
                n=num_events, 
                label_user=user_id, 
                pattern="mass_downloads"
            )
            
            # Combine with existing data
            combined_df = pd.concat([st.session_state.df, new_events], ignore_index=True)
            st.session_state.df = combined_df
            
            # Retrain model with new data
            detector = AnomalyDetector()
            detector, df_scored = detector.fit_and_score(combined_df)
            
            st.session_state.model = detector
            st.session_state.df_scored = df_scored
            
            # Save updated data
            self.data_manager.save_data(combined_df)
            
            duration = self.performance_monitor.end_timer("attack_simulation")
            logger.info(f"Attack simulated in {duration:.2f}s")
            
            st.warning(f"🚨 Attack simulated: {num_events} suspicious events added for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error simulating attack: {e}")
            st.error("Failed to simulate attack. Please check the logs.")
    
    def _export_data(self):
        """Export data to CSV"""
        try:
            exporter = DataExporter()
            filepath = exporter.export_to_csv(st.session_state.df_scored)
            
            st.success(f"✅ Data exported to {filepath}")
            
            # Provide download link
            with open(filepath, "rb") as f:
                st.download_button(
                    label="📥 Download CSV",
                    data=f.read(),
                    file_name=filepath.split("/")[-1],
                    mime="text/csv"
                )
                
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            st.error("Failed to export data. Please check the logs.")
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to the dataframe"""
        filtered_df = df.copy()
        
        # User filter
        if filters['user_filter']:
            filtered_df = filtered_df[filtered_df["user_id"].isin(filters['user_filter'])]
        
        # File type filter
        if filters['type_filter']:
            filtered_df = filtered_df[filtered_df["file_type"].isin(filters['type_filter'])]
        
        # Anomaly filter
        if filters['show_only_anoms']:
            filtered_df = filtered_df[filtered_df["anomaly_flag"]]
        
        # Risk threshold filter
        if "risk_score" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["risk_score"] >= filters['risk_threshold']]
        
        return filtered_df
    
    def _create_visualizations(self, df: pd.DataFrame):
        """Create all visualizations"""
        st.markdown("### 📊 Trends and Distributions")
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs([
            "📥 Downloads by Hour", 
            "📊 File Size Distribution", 
            "🎯 Risk Score Distribution",
            "🔥 User Activity Heatmap"
        ])
        
        with tab1:
            Visualizations.downloads_per_hour_chart(df)
        
        with tab2:
            Visualizations.size_distribution_chart(df)
        
        with tab3:
            Visualizations.risk_score_distribution(df)
        
        with tab4:
            Visualizations.user_activity_heatmap(df)
        
        # Timeline chart
        st.markdown("### 📈 Timeline Analysis")
        Visualizations.anomaly_timeline(df)
    
    def _display_data_tables(self, df: pd.DataFrame, show_stats: bool):
        """Display data tables"""
        # Main data table
        DataTable.format_main_table(df)
        
        # Detailed anomaly analysis if requested
        if show_stats:
            DataTable.create_anomaly_details_table(df)
    
    def _create_footer(self):
        """Create application footer"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.caption("🛡️ **AI-Powered Anomaly Detection**")
            st.caption("Built with Streamlit + Isolation Forest")
        
        with col2:
            # Performance metrics
            metrics = self.performance_monitor.get_metrics()
            if metrics:
                st.caption("⚡ **Performance Metrics**")
                for operation, duration in metrics.items():
                    st.caption(f"{operation}: {duration:.2f}s")
        
        with col3:
            st.caption("🔧 **Data Validation**")
            validation = self.data_validator.validate_dataframe(st.session_state.df)
            if validation["is_valid"]:
                st.caption("✅ Data integrity verified")
            else:
                st.caption("⚠️ Data validation issues detected")


def main():
    """Main entry point"""
    app = AnomalyDetectionApp()
    app.run()


if __name__ == "__main__":
    main()


