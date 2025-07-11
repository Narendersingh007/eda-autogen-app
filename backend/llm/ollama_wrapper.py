from autogen.oai.client import OpenAIWrapper

class OllamaWrapper(OpenAIWrapper):
    def __init__(self, **kwargs):
        kwargs.setdefault("base_url", "http://localhost:11434/v1")
        kwargs.setdefault("api_key", "ollama")  # dummy key for local
        super().__init__(**kwargs)