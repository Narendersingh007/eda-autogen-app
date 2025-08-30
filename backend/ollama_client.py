"""
Ollama Client for EDA Autogen App
Handles communication with local Ollama instance
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'EDA-Autogen-App/1.0'
        })
    
    def is_running(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List available models"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return data.get('models', [])
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def generate(self, 
                model: str, 
                prompt: str, 
                temperature: float = 0.2,
                max_tokens: int = 2048,
                **kwargs) -> Optional[str]:
        """Generate text using Ollama"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "top_k": kwargs.get('top_k', 40),
                    "top_p": kwargs.get('top_p', 0.9),
                    "repeat_penalty": kwargs.get('repeat_penalty', 1.1),
                    "seed": kwargs.get('seed', 42)
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', '')
            else:
                print(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error generating text: {e}")
            return None
    
    def chat(self, 
             model: str, 
             messages: List[Dict[str, str]], 
             temperature: float = 0.2,
             max_tokens: int = 2048,
             **kwargs) -> Optional[str]:
        """Chat completion using Ollama"""
        try:
            # Convert messages to Ollama format
            prompt = ""
            for msg in messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                if role == 'user':
                    prompt += f"User: {content}\n"
                elif role == 'assistant':
                    prompt += f"Assistant: {content}\n"
                elif role == 'system':
                    prompt += f"System: {content}\n"
            
            prompt += "Assistant: "
            
            return self.generate(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return None

# Global Ollama client instance
ollama_client = OllamaClient()

def get_ollama_config(model: str = "mistral", temperature: float = 0.2) -> Dict[str, Any]:
    """Get Ollama configuration for AutoGen"""
    return {
        "config_list": [{
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",  # Dummy key for local Ollama
            "model": model,
            "temperature": temperature,
            "max_tokens": 2048,
            "context_length": 4096,
            "repeat_penalty": 1.1,
            "seed": 42,
            "top_k": 40,
            "top_p": 0.9
        }],
        "client": ollama_client
    }

def test_ollama_connection() -> bool:
    """Test if Ollama is accessible"""
    return ollama_client.is_running()

def get_available_models() -> List[str]:
    """Get list of available Ollama models"""
    models = ollama_client.list_models()
    return [model['name'] for model in models]

