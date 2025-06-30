import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm_config = {
    "config_list": [{"model": "gpt-3.5-turbo", "api_key": api_key}],
    "cache_seed": 42
}