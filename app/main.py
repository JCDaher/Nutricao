"""
FastAPI Application - Gerador de Dietas para Diabetes
Sistema otimizado para mínimo uso de tokens da API Anthropic
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
from pathlib import Path

from app.models import PatientData, NutritionData, DietPlan
from app.services.nutrition_calc import NutritionCalculator
from app.services.meal_builder import MealBuilder
from app.services.diet_generator import DietGenerator, generate_diet_offline

# Configurar caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Criar aplicação FastAPI
app = FastAPI(
    title="Gerador de Dietas para Diabetes",
    description="Sistema de geração de planos alimentares personalizados para diabetes",
    version="1.0.0"
)

# Montar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Inicializar serviços
calc = NutritionCalculator()
builder = MealBuilder()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal com formulário"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/gerar-dieta")
async def gerar_dieta(patient: PatientData):
    """
    Endpoint principal: recebe dados do paciente,
    calcula tudo localmente e retorna Markdown

    Fluxo:
    1. Calcular TMB, necessidade calórica, macros (Python - 0 tokens)
    2. Montar refeições com alimentos da base de dados (Python - 0 tokens)
    3. Formatar com Claude (mínimo de tokens ~4.000)

    Args:
        patient: Dados do paciente do formulário

    Returns:
        JSON com markdown formatado e metadados
    """

    try:
        # ==================== 1. CÁLCULOS NUTRICIONAIS (Python - 0 tokens) ====================

        # Calcular Taxa Metabólica Basal
        tmb = calc.calcular_tmb(
            peso=patient.peso,
            altura=patient.altura,
            idade=patient.idade,
            sexo=patient.sexo
        )

        # Calcular necessidade calórica (atividade leve para diabéticos)
        necessidade = calc.necessidade_calorica(tmb, nivel_atividade='leve')

        # Calcular IMC
        imc = calc.calcular_imc(patient.peso, patient.altura)

        # Determinar objetivo baseado em IMC
        objetivo = calc.determinar_objetivo(imc, patient.hba1c, patient.glicemia)

        # Calcular meta calórica
        meta = calc.calcular_meta(necessidade, objetivo)

        # Distribuir macros (padrão personalizado para diabetes: 50/20/30)
        macros = calc.distribuir_macros(meta, tipo_dieta='personalizado')

        # Distribuir por refeições (5 refeições com ceia)
        distribuicao = calc.distribuir_por_refeicoes(meta, num_refeicoes=5)

        # Criar objeto NutritionData
        nutrition_data = NutritionData(
            tmb=tmb,
            necessidade_calorica=necessidade,
            meta_calorica=meta,
            imc=imc,
            macros=macros,
            distribuicao_refeicoes=distribuicao
        )

        # ==================== 2. MONTAGEM DE REFEIÇÕES (Python - 0 tokens) ====================

        refeicoes = builder.build_complete_plan(distribuicao, macros)

        # ==================== 3. CRIAR PLANO COMPLETO ====================

        diet_plan = DietPlan(
            paciente=patient,
            calculos=nutrition_data,
            refeicoes=refeicoes
        )

        # ==================== 4. FORMATAR COM CLAUDE (mínimo de tokens) ====================

        # Verificar se a API key está configurada
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if api_key:
            try:
                generator = DietGenerator()
                markdown_output = generator.generate(diet_plan)
            except Exception as api_error:
                # Fallback para modo offline se API falhar
                print(f"Erro na API Claude: {api_error}. Usando modo offline.")
                markdown_output = generate_diet_offline(diet_plan)
        else:
            # Modo offline quando não há API key
            markdown_output = generate_diet_offline(diet_plan)

        # ==================== 5. RETORNAR RESULTADO ====================

        # Gerar nome do arquivo
        nome_limpo = patient.nome.replace(" ", "_").replace(".", "")
        data_atual = datetime.now().strftime('%Y-%m-%d')
        filename = f"Dieta_{nome_limpo}_{data_atual}.md"

        # Calcular resumo nutricional real
        resumo = builder.get_resumo_nutricional(refeicoes)

        return JSONResponse({
            "success": True,
            "markdown": markdown_output,
            "filename": filename,
            "metadata": {
                "tmb": round(tmb, 0),
                "necessidade_calorica": round(necessidade, 0),
                "meta_calorica": round(meta, 0),
                "imc": round(imc, 1),
                "classificacao_imc": calc.classificar_imc(imc),
                "objetivo": objetivo,
                "calorias_reais": round(resumo['calorias'], 0),
                "macros": {
                    "carboidratos_g": round(resumo['carboidratos_g'], 0),
                    "proteinas_g": round(resumo['proteinas_g'], 0),
                    "gorduras_g": round(resumo['gorduras_g'], 0)
                }
            }
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """
    Health check endpoint

    Verifica:
    - Status da aplicação
    - Presença da chave da API Anthropic
    """
    api_configured = bool(os.getenv("ANTHROPIC_API_KEY"))

    return {
        "status": "ok",
        "anthropic_api_configured": api_configured,
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/calcular-preview")
async def calcular_preview(
    peso: float,
    altura: float,
    idade: int,
    sexo: str
):
    """
    Endpoint para preview dos cálculos (sem gerar dieta completa)

    Útil para mostrar ao usuário uma prévia antes de gerar a dieta

    Args:
        peso: Peso em kg
        altura: Altura em cm
        idade: Idade em anos
        sexo: M ou F

    Returns:
        JSON com cálculos básicos
    """
    try:
        tmb = calc.calcular_tmb(peso, altura, idade, sexo)
        imc = calc.calcular_imc(peso, altura)
        necessidade = calc.necessidade_calorica(tmb, 'leve')
        objetivo = calc.determinar_objetivo(imc)
        meta = calc.calcular_meta(necessidade, objetivo)
        peso_ideal = calc.calcular_peso_ideal(altura, sexo)
        agua = calc.calcular_agua(peso)

        return {
            "tmb": round(tmb, 0),
            "imc": round(imc, 1),
            "classificacao_imc": calc.classificar_imc(imc),
            "necessidade_calorica": round(necessidade, 0),
            "meta_calorica": round(meta, 0),
            "objetivo": objetivo,
            "peso_ideal": peso_ideal,
            "agua_litros": round(agua, 1)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Handler para Vercel
handler = app
