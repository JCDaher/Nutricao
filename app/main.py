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
from app.services.feegow_service import feegow_service
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


# =============================================================================
# ENDPOINTS FEEGOW - Integração com prontuário eletrônico
# =============================================================================

@app.get("/api/feegow/status")
async def feegow_status():
    """
    Verifica status da integração FEEGOW

    Returns:
        JSON com status da configuração
    """
    return {
        "configured": feegow_service.is_configured,
        "message": "FEEGOW configurado" if feegow_service.is_configured else "Token FEEGOW não configurado"
    }


@app.get("/api/feegow/debug")
async def feegow_debug(test_name: str = "maria"):
    """
    Endpoint de debug para testar a API FEEGOW
    Mostra resposta bruta e testa filtro local
    """
    import httpx

    if not feegow_service.is_configured:
        return {"error": "FEEGOW não configurado"}

    headers = {
        "x-access-token": settings.feegow_api_token,
        "Content-Type": "application/json"
    }

    base_url = settings.feegow_api_url

    results = {
        "base_url": base_url,
        "test_name": test_name,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # Buscar SEM parâmetros
            response = await client.get(
                f"{base_url}/patient/list",
                headers=headers
            )

            results["status_code"] = response.status_code

            if response.status_code == 200:
                data = response.json()
                patients = data.get("content", data.get("data", []))

                results["total_patients"] = len(patients)
                results["response_keys"] = list(data.keys())

                # Mostrar primeiros 3 pacientes como exemplo
                results["sample_patients"] = patients[:3] if patients else []

                # Filtrar pelo nome
                if test_name and patients:
                    test_lower = test_name.lower()
                    filtered = [p for p in patients if p.get("nome") and test_lower in p.get("nome", "").lower()]
                    results["filtered_count"] = len(filtered)
                    results["filtered_sample"] = filtered[:3] if filtered else []
            else:
                results["error"] = response.text[:500]

        except Exception as e:
            results["exception"] = str(e)

    return results


@app.get("/api/feegow/patients/search")
async def feegow_search_patients(
    nome: Optional[str] = Query(None, description="Nome do paciente (busca parcial)"),
    cpf: Optional[str] = Query(None, description="CPF do paciente"),
    prontuario: Optional[str] = Query(None, description="Número do prontuário"),
    limit: int = Query(20, ge=1, le=100, description="Limite de resultados")
):
    """
    Busca pacientes no FEEGOW

    Args:
        nome: Nome do paciente (busca parcial)
        cpf: CPF do paciente
        prontuario: Número do prontuário
        limit: Limite de resultados

    Returns:
        JSON com lista de pacientes encontrados
    """
    if not feegow_service.is_configured:
        raise HTTPException(status_code=503, detail="FEEGOW não configurado")

    if not nome and not cpf and not prontuario:
        raise HTTPException(status_code=400, detail="Informe nome, CPF ou prontuário para busca")

    result = await feegow_service.search_patients(
        nome=nome, cpf=cpf, prontuario=prontuario, limit=limit
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Erro na busca"))

    return result


@app.get("/api/feegow/patients/{patient_id}")
async def feegow_get_patient(patient_id: int):
    """
    Busca dados completos de um paciente pelo ID

    Args:
        patient_id: ID do paciente no FEEGOW

    Returns:
        JSON com dados completos do paciente
    """
    if not feegow_service.is_configured:
        raise HTTPException(status_code=503, detail="FEEGOW não configurado")

    result = await feegow_service.get_patient(patient_id)

    if not result["success"]:
        raise HTTPException(status_code=404, detail=result.get("error", "Paciente não encontrado"))

    return result


@app.post("/api/feegow/upload-diet")
async def feegow_upload_diet(
    patient_id: int = Query(..., description="ID do paciente no FEEGOW"),
    diet_content: str = Query(..., description="Conteúdo da dieta em Markdown"),
    patient_name: str = Query(..., description="Nome do paciente para o arquivo")
):
    """
    Faz upload da dieta gerada para o prontuário do paciente no FEEGOW

    Args:
        patient_id: ID do paciente no FEEGOW
        diet_content: Conteúdo da dieta em Markdown
        patient_name: Nome do paciente para compor o nome do arquivo

    Returns:
        JSON com resultado do upload
    """
    if not feegow_service.is_configured:
        raise HTTPException(status_code=503, detail="FEEGOW não configurado")

    # Gerar nome do arquivo
    nome_limpo = patient_name.replace(" ", "_").replace(".", "")
    data_atual = datetime.now().strftime('%Y-%m-%d')
    filename = f"Dieta_{nome_limpo}_{data_atual}.md"

    result = await feegow_service.upload_diet_to_record(
        patient_id=patient_id,
        diet_content=diet_content,
        filename=filename,
        description=f"Plano Alimentar Personalizado - {patient_name}"
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Erro no upload"))

    return result


@app.post("/api/feegow/patients/create")
async def feegow_create_patient(
    nome: str = Query(..., min_length=3, description="Nome completo do paciente"),
    sexo: str = Query(..., regex="^[MF]$", description="Sexo: M ou F"),
    data_nascimento: Optional[str] = Query(None, description="Data nascimento (YYYY-MM-DD)"),
    cpf: Optional[str] = Query(None, description="CPF do paciente"),
    telefone: Optional[str] = Query(None, description="Telefone do paciente"),
    email: Optional[str] = Query(None, description="Email do paciente"),
    peso: Optional[float] = Query(None, ge=30, le=300, description="Peso em kg"),
    altura: Optional[float] = Query(None, ge=100, le=250, description="Altura em cm")
):
    """
    Cria um novo paciente no FEEGOW

    Args:
        nome: Nome completo do paciente (obrigatório)
        sexo: Sexo do paciente - M ou F (obrigatório)
        data_nascimento: Data de nascimento (YYYY-MM-DD)
        cpf: CPF do paciente
        telefone: Telefone do paciente
        email: Email do paciente
        peso: Peso em kg
        altura: Altura em cm

    Returns:
        JSON com dados do paciente criado
    """
    if not feegow_service.is_configured:
        raise HTTPException(status_code=503, detail="FEEGOW não configurado")

    result = await feegow_service.create_patient(
        nome=nome,
        sexo=sexo,
        data_nascimento=data_nascimento,
        cpf=cpf,
        telefone=telefone,
        email=email,
        peso=peso,
        altura=altura
    )

    if not result["success"]:
        status_code = 409 if "já existe" in result.get("error", "") else 500
        raise HTTPException(status_code=status_code, detail=result.get("error", "Erro ao criar paciente"))

    return result


# Handler para Vercel
handler = app
