"""
AI Explanation Engine Configuration Module for C/C++ Security Analyzer.

Supports switching between cloud providers (OpenAI) and offline local LLMs (Ollama)
via a single provider configuration switch and .env file loading.
"""

import os
from typing import Dict, Any

# Load environment variables from .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Provider Switch: "openai", "ollama", or "mock"
AI_PROVIDER: str = os.getenv("AI_PROVIDER", "ollama")

# OpenAI API Settings
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TIMEOUT: int = 15

# Ollama Local LLM Settings
OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_TIMEOUT: int = 20

# Mock Mode Fallback for Testing / Offline environments
ENABLE_MOCK_FALLBACK: bool = os.getenv("ENABLE_MOCK_FALLBACK", "true").lower() in ("true", "1", "yes")
