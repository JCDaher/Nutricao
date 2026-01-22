"""
Calculadora de necessidades nutricionais
Todos os cálculos são feitos localmente para minimizar uso de tokens da API
"""
from typing import Dict


class NutritionCalculator:
    """
    Classe para cálculos nutricionais baseados em fórmulas científicas
    """

    # Fatores de atividade física
    FATORES_ATIVIDADE = {
        'sedentario': 1.2,
        'leve': 1.375,
        'moderado': 1.55,
        'intenso': 1.725,
        'muito_intenso': 1.9
    }

    # Fatores de ajuste calórico por objetivo
    FATORES_OBJETIVO = {
        'manutencao': 1.0,
        'perda_leve': 0.85,        # ~15% déficit
        'perda_moderada': 0.80,    # ~20% déficit (~500 kcal)
        'perda_intensa': 0.70,     # ~30% déficit (~750 kcal)
        'ganho_leve': 1.10,        # +10% superávit
        'ganho_moderado': 1.15     # +15% superávit
    }

    # Distribuição de macros por tipo de dieta (percentuais)
    DISTRIBUICAO_MACROS = {
        'personalizado': {'carb': 50, 'prot': 20, 'gord': 30},
        'low_carb': {'carb': 25, 'prot': 30, 'gord': 45},
        'low_carb_moderado': {'carb': 35, 'prot': 25, 'gord': 40},
        'mediterraneo': {'carb': 45, 'prot': 25, 'gord': 30},
        'high_protein': {'carb': 40, 'prot': 35, 'gord': 25}
    }

    # Distribuição de calorias por refeição (5 refeições com ceia)
    DISTRIBUICAO_REFEICOES = {
        'cafe': {'nome': 'Café da Manhã', 'horario': '07:00', 'percent': 20},
        'almoco': {'nome': 'Almoço', 'horario': '12:00', 'percent': 30},
        'lanche': {'nome': 'Lanche da Tarde', 'horario': '15:00', 'percent': 15},
        'jantar': {'nome': 'Jantar', 'horario': '19:00', 'percent': 25},
        'ceia': {'nome': 'Ceia', 'horario': '21:30', 'percent': 10}
    }

    @staticmethod
    def calcular_tmb(peso: float, altura: float, idade: int, sexo: str) -> float:
        """
        Calcula a Taxa Metabólica Basal usando a equação de Mifflin-St Jeor

        Fórmulas:
        - Homens: (10 × peso) + (6.25 × altura) - (5 × idade) + 5
        - Mulheres: (10 × peso) + (6.25 × altura) - (5 × idade) - 161

        Args:
            peso: Peso em kg
            altura: Altura em cm
            idade: Idade em anos
            sexo: 'M' para masculino, 'F' para feminino

        Returns:
            TMB em kcal/dia
        """
        base = (10 * peso) + (6.25 * altura) - (5 * idade)

        if sexo.upper() == 'M':
            return base + 5
        else:
            return base - 161

    @staticmethod
    def calcular_imc(peso: float, altura: float) -> float:
        """
        Calcula o Índice de Massa Corporal

        IMC = peso / (altura_m²)

        Args:
            peso: Peso em kg
            altura: Altura em cm

        Returns:
            IMC em kg/m²
        """
        altura_m = altura / 100
        return peso / (altura_m ** 2)

    @staticmethod
    def classificar_imc(imc: float) -> str:
        """
        Classifica o IMC segundo a OMS

        Args:
            imc: Valor do IMC

        Returns:
            Classificação do IMC
        """
        if imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        elif imc < 35:
            return "Obesidade grau I"
        elif imc < 40:
            return "Obesidade grau II"
        else:
            return "Obesidade grau III"

    @classmethod
    def necessidade_calorica(cls, tmb: float, nivel_atividade: str = 'leve') -> float:
        """
        Calcula a necessidade calórica diária total

        GET (Gasto Energético Total) = TMB × Fator de Atividade

        Args:
            tmb: Taxa Metabólica Basal em kcal/dia
            nivel_atividade: Nível de atividade física

        Returns:
            Necessidade calórica em kcal/dia
        """
        fator = cls.FATORES_ATIVIDADE.get(nivel_atividade, 1.375)
        return tmb * fator

    @classmethod
    def calcular_meta(cls, necessidade: float, objetivo: str = 'perda_moderada') -> float:
        """
        Calcula a meta calórica baseada no objetivo

        Args:
            necessidade: Necessidade calórica total
            objetivo: Objetivo nutricional

        Returns:
            Meta calórica ajustada em kcal/dia
        """
        fator = cls.FATORES_OBJETIVO.get(objetivo, 0.80)
        meta = necessidade * fator

        # Garantir mínimo de 1200 kcal para mulheres e 1500 para homens
        # Como não temos o sexo aqui, usamos 1200 como mínimo absoluto
        return max(meta, 1200)

    @classmethod
    def distribuir_macros(cls, calorias: float, tipo_dieta: str = 'personalizado') -> Dict:
        """
        Distribui macronutrientes baseado nas calorias e tipo de dieta

        Conversões:
        - 1g carboidrato = 4 kcal
        - 1g proteína = 4 kcal
        - 1g gordura = 9 kcal

        Args:
            calorias: Meta calórica diária
            tipo_dieta: Tipo de distribuição de macros

        Returns:
            Dict com distribuição de macros em gramas e kcal
        """
        distribuicao = cls.DISTRIBUICAO_MACROS.get(tipo_dieta, cls.DISTRIBUICAO_MACROS['personalizado'])

        carb_percent = distribuicao['carb']
        prot_percent = distribuicao['prot']
        gord_percent = distribuicao['gord']

        carb_kcal = calorias * (carb_percent / 100)
        prot_kcal = calorias * (prot_percent / 100)
        gord_kcal = calorias * (gord_percent / 100)

        return {
            'carb_g': carb_kcal / 4,
            'prot_g': prot_kcal / 4,
            'gord_g': gord_kcal / 9,
            'carb_kcal': carb_kcal,
            'prot_kcal': prot_kcal,
            'gord_kcal': gord_kcal,
            'carb_percent': carb_percent,
            'prot_percent': prot_percent,
            'gord_percent': gord_percent
        }

    @classmethod
    def distribuir_por_refeicoes(cls, calorias_total: float, num_refeicoes: int = 5) -> Dict:
        """
        Distribui calorias por refeição

        Para 5 refeições (padrão com CEIA):
        - Café: 20%
        - Almoço: 30%
        - Lanche: 15%
        - Jantar: 25%
        - Ceia: 10%

        Args:
            calorias_total: Total de calorias do dia
            num_refeicoes: Número de refeições (default 5)

        Returns:
            Dict com distribuição de calorias por refeição
        """
        resultado = {}

        for key, info in cls.DISTRIBUICAO_REFEICOES.items():
            resultado[key] = {
                'nome': info['nome'],
                'horario': info['horario'],
                'kcal': calorias_total * (info['percent'] / 100)
            }

        return resultado

    @staticmethod
    def determinar_objetivo(imc: float, hba1c: float = None, glicemia: float = None) -> str:
        """
        Determina o objetivo nutricional baseado nos dados do paciente

        Args:
            imc: Índice de Massa Corporal
            hba1c: Hemoglobina glicada (opcional)
            glicemia: Glicemia de jejum (opcional)

        Returns:
            Objetivo nutricional recomendado
        """
        # Se IMC indica sobrepeso ou obesidade, priorizar perda de peso
        if imc >= 30:
            return 'perda_moderada'  # Obesidade: déficit moderado
        elif imc >= 25:
            return 'perda_leve'  # Sobrepeso: déficit leve
        elif imc < 18.5:
            return 'ganho_leve'  # Baixo peso: superávit
        else:
            return 'manutencao'  # Peso normal: manutenção

    @staticmethod
    def calcular_peso_ideal(altura: float, sexo: str) -> Dict[str, float]:
        """
        Calcula a faixa de peso ideal baseado na altura e sexo

        Args:
            altura: Altura em cm
            sexo: 'M' ou 'F'

        Returns:
            Dict com peso mínimo, ideal e máximo
        """
        altura_m = altura / 100

        # IMC ideal: 18.5 a 24.9
        peso_min = 18.5 * (altura_m ** 2)
        peso_max = 24.9 * (altura_m ** 2)

        # Peso ideal usando fórmula de Lorentz
        if sexo.upper() == 'M':
            peso_ideal = altura - 100 - ((altura - 150) / 4)
        else:
            peso_ideal = altura - 100 - ((altura - 150) / 2.5)

        return {
            'peso_min': round(peso_min, 1),
            'peso_ideal': round(peso_ideal, 1),
            'peso_max': round(peso_max, 1)
        }

    @staticmethod
    def calcular_agua(peso: float) -> float:
        """
        Calcula a recomendação de ingestão de água

        Fórmula: 35ml por kg de peso corporal

        Args:
            peso: Peso em kg

        Returns:
            Quantidade de água em litros
        """
        return (peso * 35) / 1000
