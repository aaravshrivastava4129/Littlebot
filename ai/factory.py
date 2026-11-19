from config.settings import AI_PROVIDER
from ai.cloud_provider import CloudLlamaProvider

def get_ai_provider():
    if AI_PROVIDER == "cloudflare":
        return CloudLlamaProvider()
    
    elif AI_PROVIDER == "ollama":
        from ai.ollama_provider import OllamaProvider
        return OllamaProvider()

    else:
        raise ValueError(f"Unsupported AI provider: {AI_PROVIDER}")