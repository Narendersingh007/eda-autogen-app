from backend.llm.ollama_wrapper import OllamaWrapper

ollama_client = OllamaWrapper(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # dummy key
    model="mistral",
    temperature=0.2,
    timeout=360,
    price=[0.0, 0.0],
)

llm_config = {
    "config_list": [{"model": "mistral"}],
    "client": ollama_client,
}