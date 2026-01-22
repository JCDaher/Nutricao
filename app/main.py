"""
FastAPI Application - Gerador de Dietas para Diabetes
Sistema híbrido otimizado: Python + API Anthropic inteligente
"""
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import Optional
import os
from pathlib import Path

from app.models import PatientData
from app.services.nutrition_calc import NutritionCalculator
from app.services.hybrid_system import HybridDietSystem
from app.config.settings import settings, GenerationMode

# Detectar ambiente Vercel
IS_VERCEL = os.environ.get('VERCEL', False)

# Configurar caminhos - funciona tanto local quanto no Vercel
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Criar aplicação FastAPI
app = FastAPI(
    title="Gerador de Dietas para Diabetes",
    description="Sistema híbrido de geração de planos alimentares personalizados para diabetes",
    version="2.0.0"
)

# Montar arquivos estáticos apenas em ambiente local
if not IS_VERCEL and STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Inicializar templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Inicializar serviços
calc = NutritionCalculator()
hybrid_system = HybridDietSystem()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal com formulário"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/gerar-dieta")
async def gerar_dieta(
    patient: PatientData,
    mode: Optional[str] = Query(None, description="Modo: python_only, auto, api_minimal, api_full")
):
    """
    Endpoint principal: gera dieta usando sistema híbrido inteligente

    Modos disponíveis:
    - python_only: 100% Python, custo $0
    - auto: Decisão inteligente baseada na complexidade (recomendado)
    - api_minimal: Python + API apenas para apresentação
    - api_full: API completa para casos complexos

    Args:
        patient: Dados do paciente do formulário
        mode: Modo de geração (opcional, padrão: auto)

    Returns:
        JSON com markdown formatado e metadados completos
    """

    try:
        # Converter string de mode para enum se fornecido
        generation_mode = None
        if mode:
            try:
                generation_mode = GenerationMode(mode)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Modo inválido: {mode}. Use: python_only, auto, api_minimal, api_full"
                )

        # Gerar dieta usando sistema híbrido
        markdown, metadata = hybrid_system.generate_diet(
            patient_data=patient,
            mode=generation_mode
        )

        # Gerar nome do arquivo
        nome_limpo = patient.nome.replace(" ", "_").replace(".", "")
        data_atual = datetime.now().strftime('%Y-%m-%d')
        filename = f"Dieta_{nome_limpo}_{data_atual}.md"

        return JSONResponse({
            "success": True,
            "markdown": markdown,
            "filename": filename,
            "metadata": metadata
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """
    Health check endpoint

    Verifica:
    - Status da aplicação
    - Disponibilidade da API Anthropic
    - Versão do sistema
    """
    return {
        "status": "ok",
        "api_available": hybrid_system.api_available,
        "default_mode": settings.default_generation_mode,
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/calcular-preview")
async def calcular_preview(
    peso: float,
    altura: float,
    idade: int,
    sexo: str,
    nivel_deficit: str = "moderado",
    cintura: float = None
):
    """
    Endpoint para preview dos cálculos (sem gerar dieta completa)

    Útil para mostrar ao usuário uma prévia antes de gerar a dieta

    Args:
        peso: Peso em kg
        altura: Altura em cm
        idade: Idade em anos
        sexo: M ou F
        nivel_deficit: Nível de déficit calórico (leve, moderado, intenso, muito_intenso)
        cintura: Circunferência abdominal em cm (opcional)

    Returns:
        JSON com cálculos básicos
    """
    try:
        tmb = calc.calcular_tmb(peso, altura, idade, sexo)
        imc = calc.calcular_imc(peso, altura)
        necessidade = calc.necessidade_calorica(tmb, 'leve')
        meta = calc.calcular_meta_por_nivel(necessidade, nivel_deficit, sexo)
        peso_ideal = calc.calcular_peso_ideal(altura, sexo)
        agua = calc.calcular_agua(peso)

        result = {
            "tmb": round(tmb, 0),
            "imc": round(imc, 1),
            "classificacao_imc": calc.classificar_imc(imc),
            "necessidade_calorica": round(necessidade, 0),
            "meta_calorica": round(meta, 0),
            "nivel_deficit": nivel_deficit,
            "deficit_descricao": calc.DESCRICAO_DEFICIT.get(nivel_deficit, ""),
            "peso_ideal": peso_ideal,
            "agua_litros": round(agua, 1)
        }

        # Adicionar risco cardiovascular se cintura foi informada
        if cintura:
            risco_cv = calc.classificar_risco_cardiovascular(cintura, altura, sexo)
            result["risco_cardiovascular"] = risco_cv

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/stats")
async def get_stats(
    month: Optional[int] = Query(None, ge=1, le=12, description="Mês (1-12)"),
    year: Optional[int] = Query(None, ge=2024, le=2030, description="Ano")
):
    """
    Estatísticas de uso do sistema

    Args:
        month: Mês para filtrar (opcional)
        year: Ano para filtrar (opcional)

    Returns:
        JSON com estatísticas de geração de dietas
    """
    if month and year:
        stats = hybrid_system.get_stats(month=month, year=year)
        period = f"{year}-{month:02d}"
    else:
        stats = hybrid_system.get_stats()
        period = "all_time"

    return {
        "period": period,
        "stats": stats
    }


@app.get("/config")
async def get_config():
    """
    Configuração atual do sistema

    Returns:
        JSON com configurações do sistema híbrido
    """
    return {
        "default_mode": settings.default_generation_mode,
        "complexity_thresholds": {
            "simple": settings.complexity_threshold_simple,
            "medium": settings.complexity_threshold_medium
        },
        "costs": {
            "python_only": settings.cost_python_only,
            "api_minimal": settings.cost_api_minimal,
            "api_full": settings.cost_api_full
        },
        "api_available": hybrid_system.api_available,
        "api_model": settings.anthropic_model
    }


@app.post("/api/analyze-complexity")
async def analyze_complexity(patient: PatientData):
    """
    Analisa a complexidade do caso sem gerar dieta

    Útil para entender qual modo será usado em modo AUTO

    Args:
        patient: Dados do paciente

    Returns:
        JSON com análise de complexidade
    """
    try:
        analysis = hybrid_system.analyze_complexity(patient)

        return {
            "score": analysis['score'],
            "factors": [f.description for f in analysis['factors']],
            "recommendation": analysis['recommendation'],
            "rationale": analysis['rationale'],
            "patient_summary": analysis['patient_summary'],
            "estimated_cost": {
                "python_only": settings.cost_python_only,
                "api_minimal": settings.cost_api_minimal,
                "api_full": settings.cost_api_full
            }[analysis['recommendation']]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Handler para Vercel
handler = app
