"""
UI components and visualization utilities for the Streamlit dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DashboardComponents:
    """Main dashboard UI components"""
    
    @staticmethod
    def setup_page_config():
        """Configure Streamlit page settings"""
        from config import PAGE_TITLE, PAGE_ICON, LAYOUT
        st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout=LAYOUT,
        )
    
    @staticmethod
    def create_header():
        """Create the main header section"""
        st.title("🛡️ AI-Powered Anomaly Detection Dashboard")
        st.caption("Built with Streamlit + Isolation Forest to flag suspicious file access patterns.")
        st.markdown(
            "Detects unusual behaviors such as mass after-hours downloads of sensitive files to help prevent breaches like the CNSS cyberattack in Morocco."
        )
    
    @staticmethod
    def create_sidebar_controls() -> Dict:
        """Create sidebar controls and return their values"""
        with st.sidebar:
            st.header("🎛️ Controls")
            st.write("Use these to explore and simulate scenarios.")
            
            # Model controls
            contamination = st.slider(
                "Anomaly Sensitivity (contamination)", 
                min_value=0.005, 
                max_value=0.10, 
                value=0.02, 
                step=0.005,
                help="Lower values = more sensitive to anomalies"
            )
            
            refresh = st.button("🔄 Re-train Model", type="primary")
            
            st.markdown("---")
            
            # Attack simulation
            st.subheader("🎯 Simulate Attack")
            sim_user = st.text_input(
                "Impersonate User ID (optional)", 
                value="employee987",
                help="User ID to simulate suspicious activity for"
            )
            num_events = st.slider(
                "Events to generate", 
                100, 1000, 500, 50,
                help="Number of suspicious events to generate"
            )
            run_sim = st.button("🚨 Simulate Attack (2 AM mass downloads)", type="secondary")
            
            st.markdown("---")
            
            # Data controls
            st.subheader("📊 Data Controls")
            show_stats = st.checkbox("Show detailed statistics", value=False)
            export_data = st.button("📥 Export Data to CSV")
            
        return {
            'contamination': contamination,
            'refresh': refresh,
            'sim_user': sim_user,
            'num_events': num_events,
            'run_sim': run_sim,
            'show_stats': show_stats,
            'export_data': export_data
        }
    
    @staticmethod
    def create_filters(df: pd.DataFrame) -> Dict:
        """Create data filtering controls"""
        st.subheader("🔍 Filters")
        
        col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 1])
        
        with col_a:
            user_filter = st.multiselect(
                "👤 Users", 
                options=sorted(df["user_id"].unique()),
                help="Filter by specific users"
            )
        
        with col_b:
            type_filter = st.multiselect(
                "📁 File Types", 
                options=sorted(df["file_type"].unique()),
                help="Filter by file types"
            )
        
        with col_c:
            show_only_anoms = st.checkbox(
                "🚨 Show only anomalies", 
                value=False,
                help="Show only flagged suspicious events"
            )
        
        with col_d:
            risk_threshold = st.slider(
                "Risk Threshold", 
                0, 100, 50,
                help="Minimum risk score to show"
            )
        
        return {
            'user_filter': user_filter,
            'type_filter': type_filter,
            'show_only_anoms': show_only_anoms,
            'risk_threshold': risk_threshold
        }
    
    @staticmethod
    def create_summary_cards(df: pd.DataFrame):
        """Create summary metric cards"""
        st.markdown("### 📈 Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_anoms = int(df["anomaly_flag"].sum())
        total_events = len(df)
        anom_rate = (total_anoms / total_events * 100) if total_events > 0 else 0
        
        # Most suspicious users
        susp_users = (
            df[df["anomaly_flag"]]
            .groupby("user_id")
            .size()
            .sort_values(ascending=False)
            .head(3)
        )
        top_users_str = ", ".join([f"{u} ({c})" for u, c in susp_users.items()]) if len(susp_users) else "None"
        
        # Average risk score
        avg_risk = df["risk_score"].mean() if "risk_score" in df.columns else 0
        
        with col1:
            st.metric(
                "🚨 Total Anomalies", 
                value=total_anoms,
                delta=f"{anom_rate:.1f}% of events"
            )
        
        with col2:
            st.metric(
                "👥 Most Suspicious Users", 
                value=top_users_str,
                help="Users with most flagged events"
            )
        
        with col3:
            st.metric(
                "📊 Total Events", 
                value=total_events
            )
        
        with col4:
            st.metric(
                "⚖️ Avg Risk Score", 
                value=f"{avg_risk:.1f}",
                help="Average risk score across all events"
            )


class Visualizations:
    """Visualization components for the dashboard"""
    
    @staticmethod
    def downloads_per_hour_chart(df: pd.DataFrame):
        """Create downloads per hour chart with anomaly overlay"""
        tmp = df.copy()
        tmp["hour"] = tmp["access_time"].dt.hour
        
        # Count downloads by hour
        downloads = tmp[tmp["action"] == "download"].groupby("hour").size().reset_index(name="count")
        
        fig = px.bar(
            downloads, 
            x="hour", 
            y="count", 
            title="📥 Downloads per Hour",
            labels={"count": "Downloads", "hour": "Hour of Day"},
            color_discrete_sequence=['#1f77b4']
        )
        
        # Overlay anomalies as red markers
        anoms = tmp[(tmp["anomaly_flag"]) & (tmp["action"] == "download")]
        if not anoms.empty:
            anoms_grp = anoms.groupby("hour").size().reset_index(name="anomaly_count")
            if not anoms_grp.empty:
                scatter = px.scatter(
                    anoms_grp, 
                    x="hour", 
                    y="anomaly_count",
                    color_discrete_sequence=['red']
                )
                scatter.update_traces(
                    mode="markers", 
                    marker=dict(size=12, color="red", symbol="x"), 
                    name="Anomalies"
                )
                for trace in scatter.data:
                    fig.add_trace(trace)
        
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Hour of Day",
            yaxis_title="Number of Downloads"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def size_distribution_chart(df: pd.DataFrame):
        """Create file size distribution chart"""
        tmp = df.copy()
        tmp["label"] = np.where(tmp["anomaly_flag"], "Suspicious", "Normal")
        
        fig = px.histogram(
            tmp,
            x="file_size_MB",
            color="label",
            nbins=60,
            opacity=0.75,
            title="📊 File Size Distribution (Normal vs Suspicious)",
            labels={"file_size_MB": "File Size (MB)", "count": "Number of Files"},
            color_discrete_map={"Normal": "#1f77b4", "Suspicious": "#ff7f0e"}
        )
        
        fig.update_layout(
            barmode="overlay",
            xaxis_title="File Size (MB)",
            yaxis_title="Number of Files"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def risk_score_distribution(df: pd.DataFrame):
        """Create risk score distribution chart"""
        if "risk_score" not in df.columns:
            return
        
        fig = px.histogram(
            df,
            x="risk_score",
            color="anomaly_flag",
            nbins=50,
            opacity=0.7,
            title="🎯 Risk Score Distribution",
            labels={"risk_score": "Risk Score", "count": "Number of Events"},
            color_discrete_map={True: "#ff7f0e", False: "#1f77b4"}
        )
        
        fig.update_layout(
            xaxis_title="Risk Score",
            yaxis_title="Number of Events"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def user_activity_heatmap(df: pd.DataFrame):
        """Create user activity heatmap"""
        if "hour" not in df.columns:
            tmp = df.copy()
            tmp["hour"] = tmp["access_time"].dt.hour
        else:
            tmp = df.copy()
        
        # Get top 10 most active users
        top_users = tmp["user_id"].value_counts().head(10).index
        
        # Create pivot table for heatmap
        heatmap_data = tmp[tmp["user_id"].isin(top_users)].groupby(
            ["user_id", "hour"]
        ).size().unstack(fill_value=0)
        
        fig = px.imshow(
            heatmap_data,
            title="🔥 User Activity Heatmap (Top 10 Users)",
            labels={"x": "Hour of Day", "y": "User ID", "color": "Activity Count"},
            aspect="auto"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def anomaly_timeline(df: pd.DataFrame):
        """Create timeline of anomalies"""
        if "anomaly_flag" not in df.columns:
            return
        
        anoms = df[df["anomaly_flag"]].copy()
        if anoms.empty:
            st.info("No anomalies detected in the current dataset")
            return
        
        # Group by day and count anomalies
        anoms["date"] = anoms["access_time"].dt.date
        daily_anoms = anoms.groupby("date").size().reset_index(name="anomaly_count")
        
        fig = px.line(
            daily_anoms,
            x="date",
            y="anomaly_count",
            title="📈 Daily Anomaly Timeline",
            labels={"date": "Date", "anomaly_count": "Number of Anomalies"}
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Anomalies"
        )
        
        st.plotly_chart(fig, use_container_width=True)


class DataTable:
    """Data table components"""
    
    @staticmethod
    def format_main_table(df: pd.DataFrame):
        """Format and display the main data table"""
        st.markdown("### 📋 Access Logs (anomalies highlighted)")
        
        # Select columns to display
        show_cols = [
            "user_id", "file_type", "file_size_MB", 
            "access_time", "action", "risk_score", "anomaly_flag"
        ]
        
        # Filter to available columns
        available_cols = [col for col in show_cols if col in df.columns]
        df_view = df[available_cols].sort_values("access_time", ascending=False).reset_index(drop=True)
        
        # Apply styling
        def highlight_anomalies(row):
            if "anomaly_flag" in row and row["anomaly_flag"]:
                return ["background-color: #ffd6d6"] * len(row)
            return [""] * len(row)
        
        styled_df = df_view.style.apply(highlight_anomalies, axis=1)
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=400
        )
    
    @staticmethod
    def create_anomaly_details_table(df: pd.DataFrame):
        """Create detailed table for anomalies only"""
        anoms = df[df["anomaly_flag"]].copy()
        
        if anoms.empty:
            st.info("No anomalies found in the current dataset")
            return
        
        st.markdown("### 🚨 Detailed Anomaly Analysis")
        
        # Add additional analysis columns
        anoms["hour"] = anoms["access_time"].dt.hour
        anoms["day_of_week"] = anoms["access_time"].dt.day_name()
        
        # Group by user and show summary
        user_summary = anoms.groupby("user_id").agg({
            "risk_score": ["mean", "max", "count"],
            "file_type": lambda x: x.value_counts().index[0],
            "hour": lambda x: x.mode().iloc[0] if not x.empty else 0
        }).round(2)
        
        user_summary.columns = ["Avg Risk", "Max Risk", "Anomaly Count", "Most Common File Type", "Most Common Hour"]
        user_summary = user_summary.sort_values("Anomaly Count", ascending=False)
        
        st.dataframe(user_summary, use_container_width=True)


