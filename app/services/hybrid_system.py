"""
Sistema híbrido: orquestra Python + API
ESTE É O COMPONENTE PRINCIPAL
"""
import time
from typing import Tuple, Optional

from app.models import PatientData, DietPlan, NutritionData
from app.services.complexity_analyzer import ComplexityAnalyzer
from app.services.nutrition_calc import NutritionCalculator
from app.services.meal_builder import MealBuilder
from app.services.markdown_formatter import MarkdownFormatter
from app.services.api_diet_generator import APIDietGenerator
from app.utils.cost_tracker import CostTracker
from app.config.settings import settings, GenerationMode


class HybridDietSystem:
    """
    Orquestrador: decide Python vs API
    """

    def __init__(self):
        # Python components
        self.complexity_analyzer = ComplexityAnalyzer()
        self.nutrition_calc = NutritionCalculator()
        self.markdown_formatter = MarkdownFormatter()

        # API component
        try:
            self.api_generator = APIDietGenerator()
            self.api_available = True
        except ValueError as e:
            self.api_available = False
            print(f"API não disponível: {e}")

        # Tracking
        self.cost_tracker = CostTracker()

    def generate_diet(
        self,
        patient_data: PatientData,
        mode: Optional[GenerationMode] = None
    ) -> Tuple[str, dict]:
        """
        Gera dieta usando estratégia híbrida

        Args:
            patient_data: Dados do paciente
            mode: Modo de geração (None = usar padrão AUTO)

        Returns:
            (markdown, metadata)
        """

        start_time = time.time()

        # Modo padrão
        if mode is None:
            mode = GenerationMode(settings.default_generation_mode)

        # Análise de complexidade
        complexity = self.complexity_analyzer.analyze(patient_data)

        # Calcular nutrição (sempre Python)
        nutrition_data = self._calculate_nutrition(patient_data)

        # Criar MealBuilder com tipo de dieta específico
        meal_builder = MealBuilder(tipo_dieta=patient_data.tipo_dieta)
        meals = meal_builder.build_complete_plan(
            nutrition_data.distribuicao_refeicoes,
            nutrition_data.macros
        )

        # Decidir estratégia
        if mode == GenerationMode.PYTHON_ONLY:
            markdown, cost, tokens = self._generate_python_only(
                patient_data, nutrition_data, meals
            )
            mode_used = "python_only"

        elif mode == GenerationMode.AUTO:
            # Inteligente - baseado no score de complexidade
            if complexity['score'] <= settings.complexity_threshold_simple:
                markdown, cost, tokens = self._generate_python_only(
                    patient_data, nutrition_data, meals
                )
                mode_used = "python_only"
            elif complexity['score'] <= settings.complexity_threshold_medium:
                markdown, cost, tokens = self._generate_api_minimal(
                    patient_data, nutrition_data, meals
                )
                mode_used = "api_minimal"
            else:
                markdown, cost, tokens = self._generate_api_full(
                    patient_data, nutrition_data, meals
                )
                mode_used = "api_full"

        elif mode == GenerationMode.API_MINIMAL:
            markdown, cost, tokens = self._generate_api_minimal(
                patient_data, nutrition_data, meals
            )
            mode_used = "api_minimal"

        elif mode == GenerationMode.API_FULL:
            markdown, cost, tokens = self._generate_api_full(
                patient_data, nutrition_data, meals
            )
            mode_used = "api_full"

        else:
            # Fallback
            markdown, cost, tokens = self._generate_python_only(
                patient_data, nutrition_data, meals
            )
            mode_used = "python_only"

        # Tempo
        generation_time = time.time() - start_time

        # Tracking
        if settings.enable_cost_tracking:
            self.cost_tracker.record_generation(
                patient_name=patient_data.nome,
                mode=mode_used,
                tokens_used=tokens,
                complexity_score=complexity['score']
            )

        # Calcular resumo nutricional
        resumo = meal_builder.get_resumo_nutricional(meals)

        # Metadata
        metadata = {
            'mode_used': mode_used,
            'cost_usd': cost,
            'tokens_used': tokens,
            'complexity_score': complexity['score'],
            'complexity_factors': [f.description for f in complexity['factors']],
            'complexity_recommendation': complexity['recommendation'],
            'generation_time_seconds': round(generation_time, 2),
            'tmb': round(nutrition_data.tmb, 0),
            'necessidade_calorica': round(nutrition_data.necessidade_calorica, 0),
            'meta_calorica': round(nutrition_data.meta_calorica, 0),
            'imc': round(nutrition_data.imc, 1),
            'classificacao_imc': self.nutrition_calc.classificar_imc(nutrition_data.imc),
            'tipo_dieta': patient_data.tipo_dieta,
            'nivel_deficit': patient_data.nivel_deficit,
            'risco_cardiovascular': nutrition_data.risco_cardiovascular,
            'relacao_cintura_altura': nutrition_data.relacao_cintura_altura,
            'calorias_reais': round(resumo['calorias'], 0),
            'macros': {
                'carboidratos_g': round(resumo['carboidratos_g'], 0),
                'proteinas_g': round(resumo['proteinas_g'], 0),
                'gorduras_g': round(resumo['gorduras_g'], 0)
            }
        }

        return (markdown, metadata)

    def _calculate_nutrition(self, patient: PatientData) -> NutritionData:
        """Cálculos nutricionais (Python)"""

        tmb = self.nutrition_calc.calcular_tmb(
            patient.peso, patient.altura, patient.idade, patient.sexo
        )
        necessidade = self.nutrition_calc.necessidade_calorica(tmb, 'leve')
        imc = self.nutrition_calc.calcular_imc(patient.peso, patient.altura)

        # Usar nível de déficit escolhido pelo usuário
        meta = self.nutrition_calc.calcular_meta_por_nivel(
            necessidade, patient.nivel_deficit, patient.sexo
        )

        # Distribuir macros usando tipo de dieta escolhido
        macros = self.nutrition_calc.distribuir_macros(meta, tipo_dieta=patient.tipo_dieta)
        distribuicao = self.nutrition_calc.distribuir_por_refeicoes(meta)

        # Calcular risco cardiovascular se cintura informada
        risco_cardiovascular = None
        relacao_cintura_altura = None
        if patient.cintura:
            risco_cv = self.nutrition_calc.classificar_risco_cardiovascular(
                patient.cintura, patient.altura, patient.sexo
            )
            risco_cardiovascular = risco_cv['risco_cardiovascular']
            relacao_cintura_altura = risco_cv['relacao_cintura_altura']

        return NutritionData(
            tmb=tmb,
            necessidade_calorica=necessidade,
            meta_calorica=meta,
            imc=imc,
            macros=macros,
            distribuicao_refeicoes=distribuicao,
            risco_cardiovascular=risco_cardiovascular,
            relacao_cintura_altura=relacao_cintura_altura
        )

    def _generate_python_only(
        self, patient: PatientData, nutrition: NutritionData, meals: list
    ) -> Tuple[str, float, int]:
        """100% Python - $0"""

        markdown = self.markdown_formatter.format_complete_diet(
            patient=patient, nutrition=nutrition, meals=meals
        )
        return (markdown, 0.0, 0)

    def _generate_api_minimal(
        self, patient: PatientData, nutrition: NutritionData, meals: list
    ) -> Tuple[str, float, int]:
        """Python + API apenas para apresentação"""

        if not self.api_available:
            return self._generate_python_only(patient, nutrition, meals)

        try:
            # API só para apresentação personalizada
            apresentacao, tokens = self.api_generator.generate_minimal(patient, nutrition)

            # Python faz o resto
            markdown = self.markdown_formatter.format_complete_diet(
                patient=patient,
                nutrition=nutrition,
                meals=meals,
                custom_presentation=apresentacao
            )

            return (markdown, settings.cost_api_minimal, tokens)
        except Exception as e:
            print(f"Erro na API minimal: {e}. Usando Python puro.")
            return self._generate_python_only(patient, nutrition, meals)

    def _generate_api_full(
        self, patient: PatientData, nutrition: NutritionData, meals: list
    ) -> Tuple[str, float, int]:
        """API completa para casos complexos"""

        if not self.api_available:
            return self._generate_python_only(patient, nutrition, meals)

        try:
            diet_plan = DietPlan(
                paciente=patient, calculos=nutrition, refeicoes=meals
            )

            markdown, tokens = self.api_generator.generate_full(diet_plan)
            return (markdown, settings.cost_api_full, tokens)
        except Exception as e:
            print(f"Erro na API full: {e}. Usando Python puro.")
            return self._generate_python_only(patient, nutrition, meals)

    def get_stats(self, month: int = None, year: int = None) -> dict:
        """Retorna estatísticas de uso"""
        if month and year:
            return self.cost_tracker.get_monthly_stats(year, month)
        else:
            return self.cost_tracker.get_all_time_stats()

    def analyze_complexity(self, patient: PatientData) -> dict:
        """Analisa complexidade do caso sem gerar dieta"""
        return self.complexity_analyzer.analyze(patient)
