"""
Configuration file for EDA Autogen App
Centralized settings for easy customization and deployment
"""

import os
from typing import Dict, List, Optional

# LLM Provider Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()  # ollama, openai, gemini

# Ollama Configuration (Local)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")  # Dummy key for local Ollama

# OpenAI Configuration (Cloud)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Gemini Configuration (Cloud)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Default Model Settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mistral")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.2"))
DEFAULT_MAX_ROUNDS = int(os.getenv("DEFAULT_MAX_ROUNDS", "10"))

# Available Models by Provider
AVAILABLE_MODELS = {
    "ollama": [
        "mistral",      # Fast, balanced performance
        "llama3",       # High quality, slower
        "codellama",    # Code-specialized
        "qwen",         # Good balance
        "neural-chat",  # Intel's optimized model
        "phi3",         # Microsoft's lightweight model
    ],
    "openai": [
        "gpt-3.5-turbo",    # Fast, cost-effective
        "gpt-4",            # High quality, more expensive
        "gpt-4-turbo",      # Balanced performance
    ],
    "gemini": [
        "gemini-1.5-flash", # Fast, cost-effective
        "gemini-1.5-pro",   # High quality
        "gemini-2.0-flash", # Latest model
    ]
}

# Streamlit Configuration
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
STREAMLIT_HOST = os.getenv("STREAMLIT_HOST", "localhost")

# Analysis Configuration
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))  # Maximum CSV file size
SUPPORTED_FILE_TYPES = [".csv", ".xlsx", ".xls"]  # Supported file formats

# UI Configuration
THEME_COLORS = {
    "primary": "#00e676",
    "secondary": "#00c853",
    "accent": "#2196f3",
    "warning": "#ff9800",
    "error": "#f44336",
    "success": "#4caf50",
    "info": "#2196f3"
}

# Agent Configuration
AGENT_SYSTEM_MESSAGES = {
    "user": "You are a human who wants an EDA analysis from AI agents.",
    "coder": "You are an expert Python data scientist specializing in Exploratory Data Analysis (EDA).",
    "critic": "You are a highly skilled data science reviewer and quality assurance expert.",
    "analyst": "You are a senior data analyst and business intelligence expert."
}

# Development Settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Deployment Settings
IS_DEPLOYED = os.getenv("IS_DEPLOYED", "False").lower() == "true"
DEPLOYMENT_URL = os.getenv("DEPLOYMENT_URL", "")

def get_available_models_for_provider(provider: str = None) -> List[str]:
    """Get available models for a specific provider"""
    provider = provider or LLM_PROVIDER
    return AVAILABLE_MODELS.get(provider, [])

def get_default_model_for_provider(provider: str = None) -> str:
    """Get default model for a specific provider"""
    provider = provider or LLM_PROVIDER
    models = get_available_models_for_provider(provider)
    
    if provider == "openai":
        return "gpt-3.5-turbo"
    elif provider == "gemini":
        return "gemini-1.5-flash"
    else:  # ollama
        return "mistral"

def is_provider_configured(provider: str = None) -> bool:
    """Check if a provider is properly configured"""
    provider = provider or LLM_PROVIDER
    
    if provider == "openai":
        return bool(OPENAI_API_KEY)
    elif provider == "gemini":
        return bool(GEMINI_API_KEY)
    else:  # ollama
        return True  # Always available locally
