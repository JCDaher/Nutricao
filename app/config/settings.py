"""
Configurações centralizadas do sistema híbrido
"""
from enum import Enum
from pydantic import BaseModel
import os


class GenerationMode(str, Enum):
    """Modos de geração de dieta"""
    PYTHON_ONLY = "python_only"      # 100% Python, $0
    AUTO = "auto"                     # Inteligente (recomendado)
    API_MINIMAL = "api_minimal"       # Python + API só apresentação
    API_FULL = "api_full"            # API completa


class Settings(BaseModel):
    """Configurações globais"""

    # Modo padrão de operação
    default_generation_mode: GenerationMode = GenerationMode.AUTO

    # Thresholds de complexidade (scores)
    complexity_threshold_simple: int = 3    # Score <= 3: Python puro
    complexity_threshold_medium: int = 6    # Score <= 6: API minimal
    # Score > 6: API full

    # Custos em USD por dieta
    cost_python_only: float = 0.0
    cost_api_minimal: float = 0.015
    cost_api_full: float = 0.048

    # Configuração API Anthropic
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    anthropic_model: str = "claude-sonnet-4-5-20250929"

    # Configuração API FEEGOW
    feegow_api_token: str = os.getenv("FEEGOW_API_TOKEN", "")
    feegow_api_url: str = os.getenv("FEEGOW_API_URL", "https://api.feegow.com.br/v1/api")

    # Limites de tokens
    max_tokens_minimal: int = 800       # Para apresentação apenas
    max_tokens_full: int = 8000         # Para dieta completa

    # Features
    enable_cost_tracking: bool = True
    enable_statistics: bool = True

    class Config:
        use_enum_values = True


# Instância global
settings = Settings()
