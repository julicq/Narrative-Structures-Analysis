# shared/constants.py

from enum import Enum

class ModelType(Enum):
    OLLAMA = "llama3.2",
    OPENAI = "gpt-4",
    GIGACHAT = "GigaChat:latest",
    ANTHROPIC = "claude-3-opus-20240229"

DASHBOARD_CONFIG_DIR = 'config'
