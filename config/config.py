# ==============================
# AI AGENT CONFIGURATION
# ==============================

MEM0_CONFIG = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.2:3b",
            "ollama_base_url": "http://localhost:11434",
            "temperature": 0.2
        }
    },

    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": "http://localhost:11434"
        }
    },

    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "self_learning_agent",
            "embedding_model_dims": 768,
            "path": r"D:\self_learning_ai_agent\data\qdrant"
        }
    }
}


# User ID
USER_ID = "nick"


# Ollama model
OLLAMA_MODEL = "llama3.2:3b"


# Ollama URL
OLLAMA_BASE_URL = "http://localhost:11434"
