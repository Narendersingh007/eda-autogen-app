#!/usr/bin/env python3
"""
Demo script for EDA Autogen App
Test the basic functionality without the Streamlit interface
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import autogen
        print("✅ autogen imported successfully")
    except ImportError as e:
        print(f"❌ autogen import failed: {e}")
        return False
    
    try:
        import ollama
        print("✅ ollama imported successfully")
    except ImportError as e:
        print(f"❌ ollama import failed: {e}")
        return False
    
    try:
        from backend.agents.eda_agents import setup_groupchat_with_agents
        print("✅ EDA agents imported successfully")
    except ImportError as e:
        print(f"❌ EDA agents import failed: {e}")
        return False
    
    return True

def test_ollama_connection():
    """Test connection to Ollama"""
    print("\n🔌 Testing Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama is running and accessible")
            print(f"📋 Available models: {[model['name'] for model in models.get('models', [])]}")
            return True
        else:
            print(f"⚠️  Ollama responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False

def test_agent_setup():
    """Test if agents can be set up"""
    print("\n🤖 Testing agent setup...")
    
    try:
        from backend.agents.eda_agents import setup_groupchat_with_agents
        
        # Test with sample data
        sample_data = "col1,col2,col3\n1,2,3\n4,5,6\n7,8,9"
        
        user_proxy, manager, message = setup_groupchat_with_agents(
            sample_data,
            model="mistral",
            temperature=0.2,
            max_rounds=5
        )
        
        print("✅ Agents setup successful")
        print(f"📝 Message length: {len(message)} characters")
        print(f"🔄 Max rounds: {manager.groupchat.max_round}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent setup failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 EDA Autogen App - System Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    # Test Ollama connection
    if not test_ollama_connection():
        print("\n❌ Ollama connection failed. Please start Ollama first:")
        print("   ollama serve")
        print("   ollama run mistral")
        return False
    
    # Test agent setup
    if not test_agent_setup():
        print("\n❌ Agent setup failed. Check the backend configuration.")
        return False
    
    print("\n🎉 All tests passed! The app is ready to run.")
    print("\n🚀 To start the app, run:")
    print("   python run.py")
    print("   # or")
    print("   streamlit run app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
