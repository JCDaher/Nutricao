"""
Analisa complexidade de casos para decidir estratégia de geração
"""
from typing import Dict, List

from app.models import PatientData
from app.services.nutrition_calc import NutritionCalculator


class ComplexityFactor:
    """Representa um fator de complexidade"""

    def __init__(self, name: str, score: int, description: str):
        self.name = name
        self.score = score
        self.description = description


class ComplexityAnalyzer:
    """
    Analisa complexidade do caso clínico
    Score: 0-10 (quanto maior, mais complexo)
    """

    def __init__(self):
        self.calc = NutritionCalculator()

    def analyze(self, patient: PatientData) -> Dict:
        """
        Analisa complexidade retornando score e fatores

        Returns:
            {
                'score': int (0-10),
                'factors': List[ComplexityFactor],
                'recommendation': str,
                'rationale': str,
                'patient_summary': str
            }
        """

        factors = []
        total_score = 0

        # Calcular IMC
        imc = self.calc.calcular_imc(patient.peso, patient.altura)

        # FATOR 1: IMC extremo
        if imc > 40:
            factor = ComplexityFactor(
                name="obesidade_grave",
                score=2,
                description=f"Obesidade grau III (IMC {imc:.1f})"
            )
            factors.append(factor)
            total_score += 2
        elif imc > 35:
            factor = ComplexityFactor(
                name="obesidade_moderada",
                score=1,
                description=f"Obesidade grau II (IMC {imc:.1f})"
            )
            factors.append(factor)
            total_score += 1
        elif imc < 18.5:
            factor = ComplexityFactor(
                name="baixo_peso",
                score=2,
                description=f"Baixo peso (IMC {imc:.1f})"
            )
            factors.append(factor)
            total_score += 2

        # FATOR 2: HbA1c muito elevada
        if patient.hba1c:
            if patient.hba1c > 10:
                factor = ComplexityFactor(
                    name="hba1c_muito_alta",
                    score=2,
                    description=f"HbA1c muito elevada ({patient.hba1c}%)"
                )
                factors.append(factor)
                total_score += 2
            elif patient.hba1c > 8:
                factor = ComplexityFactor(
                    name="hba1c_alta",
                    score=1,
                    description=f"HbA1c elevada ({patient.hba1c}%)"
                )
                factors.append(factor)
                total_score += 1

        # FATOR 3: Glicemia muito alta (alternativa a HbA1c)
        elif patient.glicemia:
            if patient.glicemia > 300:
                factor = ComplexityFactor(
                    name="glicemia_muito_alta",
                    score=2,
                    description=f"Glicemia muito elevada ({patient.glicemia} mg/dL)"
                )
                factors.append(factor)
                total_score += 2
            elif patient.glicemia > 200:
                factor = ComplexityFactor(
                    name="glicemia_alta",
                    score=1,
                    description=f"Glicemia elevada ({patient.glicemia} mg/dL)"
                )
                factors.append(factor)
                total_score += 1

        # FATOR 4: Idade avançada
        if patient.idade > 75:
            factor = ComplexityFactor(
                name="idade_avancada",
                score=1,
                description=f"Idade avançada ({patient.idade} anos)"
            )
            factors.append(factor)
            total_score += 1

        # FATOR 5: Diabetes em idade muito jovem (atípico para DM2)
        if patient.idade < 30:
            factor = ComplexityFactor(
                name="idade_jovem_dm",
                score=1,
                description=f"Diabetes em idade jovem ({patient.idade} anos)"
            )
            factors.append(factor)
            total_score += 1

        # FATOR 6: Risco cardiovascular elevado (se cintura informada)
        if patient.cintura:
            risco_cv = self.calc.classificar_risco_cardiovascular(
                patient.cintura, patient.altura, patient.sexo
            )
            if risco_cv['risco_cardiovascular'] in ['Elevado', 'Risco muito aumentado']:
                factor = ComplexityFactor(
                    name="risco_cardiovascular",
                    score=1,
                    description=f"Risco cardiovascular {risco_cv['risco_cardiovascular']}"
                )
                factors.append(factor)
                total_score += 1

        # Determinar recomendação baseada no score
        if total_score <= 3:
            recommendation = "python_only"
            rationale = "Caso padrão - templates Python profissionais são suficientes"
        elif total_score <= 6:
            recommendation = "api_minimal"
            rationale = "Caso moderado - API para humanizar apresentação"
        else:
            recommendation = "api_full"
            rationale = "Caso complexo - API completa para máxima qualidade"

        # Gerar resumo do paciente
        tratamento = "Sr." if patient.sexo == "M" else "Sra."
        patient_summary = f"{tratamento} {patient.nome}, {patient.idade} anos, IMC {imc:.1f}"
        if patient.hba1c:
            patient_summary += f", HbA1c {patient.hba1c}%"
        elif patient.glicemia:
            patient_summary += f", glicemia {patient.glicemia} mg/dL"

        return {
            'score': total_score,
            'factors': factors,
            'recommendation': recommendation,
            'rationale': rationale,
            'patient_summary': patient_summary
        }
