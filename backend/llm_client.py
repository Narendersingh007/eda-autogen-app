"""
Unified LLM Client for EDA Autogen App
Supports Ollama (local), OpenAI, and Gemini
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from config import (
    LLM_PROVIDER, 
    OPENAI_API_KEY, 
    OPENAI_BASE_URL,
    GEMINI_API_KEY,
    get_available_models_for_provider
)

class BaseLLMClient:
    """Base class for LLM clients"""
    
    def __init__(self):
        self.provider = LLM_PROVIDER
    
    def generate(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate text - to be implemented by subclasses"""
        raise NotImplementedError
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Optional[str]:
        """Chat completion - to be implemented by subclasses"""
        raise NotImplementedError

class OllamaClient(BaseLLMClient):
    """Ollama client for local LLM"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        super().__init__()
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

class OpenAIClient(BaseLLMClient):
    """OpenAI client for cloud LLM"""
    
    def __init__(self):
        super().__init__()
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        self.api_key = OPENAI_API_KEY
        self.base_url = OPENAI_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def generate(self, 
                model: str, 
                prompt: str, 
                temperature: float = 0.2,
                max_tokens: int = 2048,
                **kwargs) -> Optional[str]:
        """Generate text using OpenAI"""
        try:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                print(f"OpenAI API error: {response.status_code} - {response.text}")
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
        """Chat completion using OpenAI"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                print(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return None

class GeminiClient(BaseLLMClient):
    """Gemini client for cloud LLM"""
    
    def __init__(self):
        super().__init__()
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured")
        
        self.api_key = GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.session = requests.Session()
    
    def generate(self, 
                model: str, 
                prompt: str, 
                temperature: float = 0.2,
                max_tokens: int = 2048,
                **kwargs) -> Optional[str]:
        """Generate text using Gemini"""
        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                    "topK": kwargs.get('top_k', 40),
                    "topP": kwargs.get('top_p', 0.9)
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/models/{model}:generateContent?key={self.api_key}",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
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
        """Chat completion using Gemini"""
        try:
            # Convert messages to Gemini format
            contents = []
            for msg in messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                if role == 'system':
                    # Gemini doesn't support system messages, prepend to user message
                    if contents and contents[-1]['role'] == 'user':
                        contents[-1]['parts'][0]['text'] = f"System: {content}\n\nUser: {contents[-1]['parts'][0]['text']}"
                    else:
                        contents.append({
                            "role": "user",
                            "parts": [{"text": f"System: {content}"}]
                        })
                else:
                    contents.append({
                        "role": role,
                        "parts": [{"text": content}]
                    })
            
            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                    "topK": kwargs.get('top_k', 40),
                    "topP": kwargs.get('top_p', 0.9)
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/models/{model}:generateContent?key={self.api_key}",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return None

def get_llm_client() -> BaseLLMClient:
    """Get the appropriate LLM client based on configuration"""
    try:
        if LLM_PROVIDER == "openai":
            return OpenAIClient()
        elif LLM_PROVIDER == "gemini":
            return GeminiClient()
        else:  # ollama
            return OllamaClient()
    except Exception as e:
        print(f"Failed to initialize {LLM_PROVIDER} client: {e}")
        print("Falling back to Ollama...")
        return OllamaClient()

def get_llm_config(model: str = None, temperature: float = 0.2) -> Dict[str, Any]:
    """Get LLM configuration for AutoGen"""
    provider = LLM_PROVIDER
    
    if provider == "openai":
        return {
            "config_list": [{
                "model": model or "gpt-3.5-turbo",
                "api_key": OPENAI_API_KEY,
                "base_url": OPENAI_BASE_URL
            }],
            "temperature": temperature
        }
    elif provider == "gemini":
        return {
            "config_list": [{
                "model": model or "gemini-1.5-flash",
                "api_key": GEMINI_API_KEY,
                "base_url": "https://generativelanguage.googleapis.com/v1beta"
            }],
            "temperature": temperature
        }
    else:  # ollama
        return {
            "config_list": [{
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
                "model": model or "mistral",
                "temperature": temperature,
                "max_tokens": 2048
            }]
        }

# Global LLM client instance
llm_client = get_llm_client()

def main():
    """Main application entry point handling UI and workflow."""
    pass  # Placeholder for the main function implementation
