"""
Configuration management for Safe DeFi Assistant
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8080))
    
    # API Keys
    SERPER_API_KEY: Optional[str] = os.getenv("SERPER_API_KEY")
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    JINA_API_KEY: Optional[str] = os.getenv("JINA_API_KEY")
    LITELLM_API_KEY: Optional[str] = os.getenv("LITELLM_API_KEY")
    LITELLM_MODEL_ID: str = os.getenv("LITELLM_MODEL_ID", "openrouter/google/gemini-2.0-flash-001")
    
    # Blockchain APIs
    ETHERSCAN_API_KEY: Optional[str] = os.getenv("ETHERSCAN_API_KEY")
    MORALIS_API_KEY: Optional[str] = os.getenv("MORALIS_API_KEY")
    ALCHEMY_API_KEY: Optional[str] = os.getenv("ALCHEMY_API_KEY")
    DEBANK_API_KEY: Optional[str] = os.getenv("DEBANK_API_KEY")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "defi_assistant.log")
    
    @classmethod
    def validate_required_keys(cls) -> bool:
        """Validate that required API keys are present"""
        required_keys = [
            cls.SERPER_API_KEY,
            cls.OPENROUTER_API_KEY,
            cls.JINA_API_KEY,
            cls.LITELLM_API_KEY,
            cls.ETHERSCAN_API_KEY
        ]
        return all(key is not None for key in required_keys)
    
    @classmethod
    def get_missing_keys(cls) -> list[str]:
        """Get list of missing required API keys"""
        required_keys = {
            "SERPER_API_KEY": cls.SERPER_API_KEY,
            "OPENROUTER_API_KEY": cls.OPENROUTER_API_KEY,
            "JINA_API_KEY": cls.JINA_API_KEY,
            "LITELLM_API_KEY": cls.LITELLM_API_KEY,
            "ETHERSCAN_API_KEY": cls.ETHERSCAN_API_KEY
        }
        return [key for key, value in required_keys.items() if value is None]

# Global config instance
config = Config()
