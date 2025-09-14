"""
Demo script to showcase the improved anomaly detection dashboard
"""
import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    print("🚀 Starting AI-Powered Anomaly Detection Dashboard...")
    print("📊 This is the improved version with modular architecture!")
    print("🔧 Features include:")
    print("   - Modular code structure")
    print("   - Enhanced ML pipeline")
    print("   - Performance optimizations")
    print("   - Better UI/UX")
    print("   - Data validation and export")
    print("   - Real-time alerts")
    print("\n🌐 Opening dashboard in your browser...")
    
    try:
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        print("Make sure you have installed all dependencies: pip install -r requirements.txt")
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")

if __name__ == "__main__":
    main()


