#!/usr/bin/env python3
"""
EDA Autogen App - Launcher Script
Run this script to start the Streamlit application
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check if Ollama is running
    try:
        import requests
        response = requests.get("http://localhost:11434/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
        else:
            print("⚠️  Ollama responded but may not be ready")
    except:
        print("❌ Ollama is not running. Please start Ollama first:")
        print("   ollama serve")
        print("   ollama run mistral")
        return
    
    # Launch Streamlit
    print("🚀 Starting EDA Autogen App...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🔄 To stop the app, press Ctrl+C")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false"
    ])

if __name__ == "__main__":
    main()
