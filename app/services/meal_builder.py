"""
Montador de refeições balanceadas
Utiliza a base de alimentos para construir refeições que atendam às metas calóricas
"""
from typing import List, Dict
import random

from app.data.alimentos_base import (
    ALIMENTOS, ALIMENTOS_POR_REFEICAO, calcular_nutricao_porcao
)
from app.models import Meal, FoodItem


class MealBuilder:
    """
    Monta refeições balanceadas usando alimentos da base de dados
    """

    # Multiplicadores por tipo de dieta para cada grupo alimentar
    # Ajustam as proporções de carboidratos, proteínas e gorduras em cada refeição
    AJUSTES_DIETA = {
        'personalizado': {
            'cereais': 1.0,      # Proporção normal de carboidratos
            'proteinas': 1.0,   # Proporção normal de proteínas
            'gorduras': 1.0,    # Proporção normal de gorduras
            'frutas': 1.0,
            'leguminosas': 1.0
        },
        'low_carb': {
            'cereais': 0.4,      # Reduz carboidratos significativamente
            'proteinas': 1.5,    # Aumenta proteínas
            'gorduras': 1.8,     # Aumenta gorduras
            'frutas': 0.6,       # Reduz frutas
            'leguminosas': 0.7
        },
        'low_carb_moderado': {
            'cereais': 0.6,
            'proteinas': 1.3,
            'gorduras': 1.4,
            'frutas': 0.8,
            'leguminosas': 0.8
        },
        'mediterraneo': {
            'cereais': 0.9,
            'proteinas': 1.1,
            'gorduras': 1.2,     # Mais azeite e gorduras boas
            'frutas': 1.0,
            'leguminosas': 1.2
        },
        'high_protein': {
            'cereais': 0.7,
            'proteinas': 1.8,    # Muito mais proteína
            'gorduras': 0.8,
            'frutas': 0.8,
            'leguminosas': 1.3
        }
    }

    def __init__(self, tipo_dieta: str = 'personalizado'):
        self.alimentos = ALIMENTOS
        self.alimentos_por_refeicao = ALIMENTOS_POR_REFEICAO
        self.tipo_dieta = tipo_dieta
        self.ajustes = self.AJUSTES_DIETA.get(tipo_dieta, self.AJUSTES_DIETA['personalizado'])

    def _criar_food_item(self, key: str, gramas: float = None) -> FoodItem:
        """
        Cria um FoodItem a partir da chave do alimento

        Args:
            key: Chave do alimento na base de dados
            gramas: Quantidade em gramas (opcional)

        Returns:
            FoodItem com dados nutricionais calculados
        """
        dados = calcular_nutricao_porcao(key, gramas)
        if not dados:
            return None

        return FoodItem(
            nome=dados['nome'],
            porcao=dados['porcao'],
            gramas=dados['gramas'],
            kcal=dados['kcal'],
            carb=dados['carb'],
            prot=dados['prot'],
            gord=dados['gord'],
            fibra=dados['fibra']
        )

    def _ajustar_porcao(self, key: str, calorias_alvo: float, min_mult: float = 0.3, max_mult: float = 3.0) -> FoodItem:
        """
        Ajusta a porção de um alimento para atingir as calorias alvo

        Args:
            key: Chave do alimento
            calorias_alvo: Calorias desejadas
            min_mult: Multiplicador mínimo da porção padrão (default 0.3)
            max_mult: Multiplicador máximo da porção padrão (default 3.0)

        Returns:
            FoodItem com porção ajustada
        """
        alimento = self.alimentos.get(key)
        if not alimento:
            return None

        # Calcular gramas necessárias para atingir calorias alvo
        kcal_por_100g = alimento['kcal']
        if kcal_por_100g <= 0:
            return self._criar_food_item(key)

        gramas_necessarias = (calorias_alvo / kcal_por_100g) * 100

        # Limitar a uma porção razoável (mínimo e máximo configuráveis)
        porcao_padrao = alimento['gramas_porcao']
        min_gramas = porcao_padrao * min_mult
        max_gramas = porcao_padrao * max_mult
        gramas_ajustadas = max(min_gramas, min(gramas_necessarias, max_gramas))

        return self._criar_food_item(key, gramas_ajustadas)

    def build_cafe_manha(self, calorias_alvo: float, macros_dia: dict) -> Meal:
        """
        Monta café da manhã balanceado (~20% das calorias diárias)

        Estrutura ajustada conforme tipo de dieta:
        - Cereal/pão (ajustado por tipo_dieta)
        - Proteína/laticínio (ajustado por tipo_dieta)
        - Fruta (ajustado por tipo_dieta)
        - Gordura saudável (ajustado por tipo_dieta)

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia (para referência)

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []
        aj = self.ajustes

        # Calcular proporções base e aplicar ajustes
        # Base: cereal 40%, proteina 25%, lacteo 15%, fruta 15%, gordura 5%
        prop_cereal = 0.40 * aj['cereais']
        prop_proteina = 0.25 * aj['proteinas']
        prop_lacteo = 0.15 * aj['proteinas']
        prop_fruta = 0.15 * aj['frutas']
        prop_gordura = 0.05 * aj['gorduras']

        # Normalizar para somar 100%
        total = prop_cereal + prop_proteina + prop_lacteo + prop_fruta + prop_gordura
        prop_cereal /= total
        prop_proteina /= total
        prop_lacteo /= total
        prop_fruta /= total
        prop_gordura /= total

        # 1. Cereal/Pão
        cal_cereal = calorias_alvo * prop_cereal
        cereais_opcoes = self.alimentos_por_refeicao['cafe_manha']['cereais']
        cereal_key = random.choice(cereais_opcoes)
        cereal = self._ajustar_porcao(cereal_key, cal_cereal)
        if cereal:
            alimentos.append(cereal)

        # 2. Proteína/Ovo
        cal_proteina = calorias_alvo * prop_proteina
        proteinas_opcoes = self.alimentos_por_refeicao['cafe_manha']['proteinas']
        proteina_key = random.choice(proteinas_opcoes)
        proteina = self._ajustar_porcao(proteina_key, cal_proteina)
        if proteina:
            alimentos.append(proteina)

        # 3. Laticínio
        cal_lacteo = calorias_alvo * prop_lacteo
        lacteos_opcoes = self.alimentos_por_refeicao['cafe_manha']['lacteos']
        lacteo_key = random.choice(lacteos_opcoes)
        lacteo = self._ajustar_porcao(lacteo_key, cal_lacteo)
        if lacteo:
            alimentos.append(lacteo)

        # 4. Fruta
        cal_fruta = calorias_alvo * prop_fruta
        frutas_opcoes = self.alimentos_por_refeicao['cafe_manha']['frutas']
        fruta_key = random.choice(frutas_opcoes)
        fruta = self._ajustar_porcao(fruta_key, cal_fruta)
        if fruta:
            alimentos.append(fruta)

        # 5. Gordura saudável (sementes)
        cal_gordura = calorias_alvo * prop_gordura
        gorduras_opcoes = ['chia', 'linhaça']
        gordura_key = random.choice(gorduras_opcoes)
        gordura = self._ajustar_porcao(gordura_key, cal_gordura)
        if gordura:
            alimentos.append(gordura)

        # Adicionar café sem açúcar
        cafe = self._criar_food_item('cafe_sem_acucar')
        if cafe:
            alimentos.append(cafe)

        return Meal(
            nome="Café da Manhã",
            horario="07:00",
            calorias_alvo=calorias_alvo,
            alimentos=alimentos
        )

    def build_almoco(self, calorias_alvo: float, macros_dia: dict) -> Meal:
        """
        Monta almoço balanceado (~30% das calorias diárias)

        Estrutura ajustada conforme tipo de dieta

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []
        aj = self.ajustes

        # Calcular proporções base e aplicar ajustes
        # Base: cereal 25%, leguminosa 15%, proteina 30%, legume 10%, azeite 10%
        prop_cereal = 0.25 * aj['cereais']
        prop_leguminosa = 0.15 * aj['leguminosas']
        prop_proteina = 0.30 * aj['proteinas']
        prop_legume = 0.10  # Legumes mantêm proporção (são baixos em carb)
        prop_azeite = 0.10 * aj['gorduras']

        # Normalizar (verduras não contam muito)
        total = prop_cereal + prop_leguminosa + prop_proteina + prop_legume + prop_azeite
        prop_cereal /= total
        prop_leguminosa /= total
        prop_proteina /= total
        prop_legume /= total
        prop_azeite /= total

        # 1. Arroz/Cereal
        cal_cereal = calorias_alvo * prop_cereal
        cereais_opcoes = self.alimentos_por_refeicao['almoco']['cereais']
        cereal_key = random.choice(cereais_opcoes)
        cereal = self._ajustar_porcao(cereal_key, cal_cereal)
        if cereal:
            alimentos.append(cereal)

        # 2. Feijão/Leguminosa
        cal_leguminosa = calorias_alvo * prop_leguminosa
        leguminosas_opcoes = self.alimentos_por_refeicao['almoco']['leguminosas']
        leguminosa_key = random.choice(leguminosas_opcoes)
        leguminosa = self._ajustar_porcao(leguminosa_key, cal_leguminosa)
        if leguminosa:
            alimentos.append(leguminosa)

        # 3. Proteína
        cal_proteina = calorias_alvo * prop_proteina
        proteinas_opcoes = self.alimentos_por_refeicao['almoco']['proteinas']
        proteina_key = random.choice(proteinas_opcoes)
        proteina = self._ajustar_porcao(proteina_key, cal_proteina)
        if proteina:
            alimentos.append(proteina)

        # 4. Salada (verduras à vontade - ajustar conforme calorias totais)
        verduras_opcoes = self.alimentos_por_refeicao['almoco']['verduras']
        verdura_key = random.choice(verduras_opcoes)
        # Porção de salada varia com calorias totais (mais salada em dietas restritivas)
        porcao_verdura = 50 + (max(0, 1800 - calorias_alvo) / 20)  # Mais salada se menos calorias
        verdura = self._criar_food_item(verdura_key, porcao_verdura)
        if verdura:
            alimentos.append(verdura)

        # 5. Legume cozido
        cal_legume = calorias_alvo * prop_legume
        legumes_opcoes = self.alimentos_por_refeicao['almoco']['legumes']
        legume_key = random.choice(legumes_opcoes)
        legume = self._ajustar_porcao(legume_key, cal_legume)
        if legume:
            alimentos.append(legume)

        # 6. Tomate na salada
        tomate = self._criar_food_item('tomate', 60)
        if tomate:
            alimentos.append(tomate)

        # 7. Azeite
        cal_azeite = calorias_alvo * prop_azeite
        azeite = self._ajustar_porcao('azeite_oliva', cal_azeite)
        if azeite:
            alimentos.append(azeite)

        return Meal(
            nome="Almoço",
            horario="12:00",
            calorias_alvo=calorias_alvo,
            alimentos=alimentos
        )

    def build_lanche(self, calorias_alvo: float, macros_dia: dict) -> Meal:
        """
        Monta lanche da tarde (~15% das calorias diárias)

        Estrutura ajustada conforme tipo de dieta

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []
        aj = self.ajustes

        # Calcular proporções base e aplicar ajustes
        # Base: fruta 40%, lacteo 35%, gordura 25%
        prop_fruta = 0.40 * aj['frutas']
        prop_lacteo = 0.35 * aj['proteinas']
        prop_gordura = 0.25 * aj['gorduras']

        # Normalizar
        total = prop_fruta + prop_lacteo + prop_gordura
        prop_fruta /= total
        prop_lacteo /= total
        prop_gordura /= total

        # 1. Fruta
        cal_fruta = calorias_alvo * prop_fruta
        frutas_opcoes = self.alimentos_por_refeicao['lanche']['frutas']
        fruta_key = random.choice(frutas_opcoes)
        fruta = self._ajustar_porcao(fruta_key, cal_fruta)
        if fruta:
            alimentos.append(fruta)

        # 2. Iogurte
        cal_lacteo = calorias_alvo * prop_lacteo
        lacteos_opcoes = self.alimentos_por_refeicao['lanche']['lacteos']
        lacteo_key = random.choice(lacteos_opcoes)
        lacteo = self._ajustar_porcao(lacteo_key, cal_lacteo)
        if lacteo:
            alimentos.append(lacteo)

        # 3. Castanhas
        cal_gordura = calorias_alvo * prop_gordura
        gorduras_opcoes = self.alimentos_por_refeicao['lanche']['gorduras']
        gordura_key = random.choice(gorduras_opcoes)
        gordura = self._ajustar_porcao(gordura_key, cal_gordura)
        if gordura:
            alimentos.append(gordura)

        return Meal(
            nome="Lanche da Tarde",
            horario="15:00",
            calorias_alvo=calorias_alvo,
            alimentos=alimentos
        )

    def build_jantar(self, calorias_alvo: float, macros_dia: dict) -> Meal:
        """
        Monta jantar balanceado (~25% das calorias diárias)

        Estrutura ajustada conforme tipo de dieta

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []
        aj = self.ajustes

        # Calcular proporções base e aplicar ajustes
        # Base: cereal 25%, proteina 35%, legume 20%, azeite 10%
        prop_cereal = 0.25 * aj['cereais']
        prop_proteina = 0.35 * aj['proteinas']
        prop_legume = 0.20  # Legumes mantêm proporção
        prop_azeite = 0.10 * aj['gorduras']

        # Normalizar
        total = prop_cereal + prop_proteina + prop_legume + prop_azeite
        prop_cereal /= total
        prop_proteina /= total
        prop_legume /= total
        prop_azeite /= total

        # 1. Arroz/Cereal
        cal_cereal = calorias_alvo * prop_cereal
        cereais_opcoes = self.alimentos_por_refeicao['jantar']['cereais']
        cereal_key = random.choice(cereais_opcoes)
        cereal = self._ajustar_porcao(cereal_key, cal_cereal)
        if cereal:
            alimentos.append(cereal)

        # 2. Proteína
        cal_proteina = calorias_alvo * prop_proteina
        proteinas_opcoes = self.alimentos_por_refeicao['jantar']['proteinas']
        proteina_key = random.choice(proteinas_opcoes)
        proteina = self._ajustar_porcao(proteina_key, cal_proteina)
        if proteina:
            alimentos.append(proteina)

        # 3. Salada (verduras à vontade - mais em dietas restritivas)
        verduras_opcoes = self.alimentos_por_refeicao['jantar']['verduras']
        verdura_key = random.choice(verduras_opcoes)
        porcao_verdura = 50 + (max(0, 1800 - calorias_alvo) / 20)
        verdura = self._criar_food_item(verdura_key, porcao_verdura)
        if verdura:
            alimentos.append(verdura)

        # 4. Legume cozido
        cal_legume = calorias_alvo * prop_legume
        legumes_opcoes = self.alimentos_por_refeicao['jantar']['legumes']
        legume_key = random.choice(legumes_opcoes)
        legume = self._ajustar_porcao(legume_key, cal_legume)
        if legume:
            alimentos.append(legume)

        # 5. Pepino na salada
        pepino = self._criar_food_item('pepino', 60)
        if pepino:
            alimentos.append(pepino)

        # 6. Azeite
        cal_azeite = calorias_alvo * prop_azeite
        azeite = self._ajustar_porcao('azeite_oliva', cal_azeite)
        if azeite:
            alimentos.append(azeite)

        return Meal(
            nome="Jantar",
            horario="19:00",
            calorias_alvo=calorias_alvo,
            alimentos=alimentos
        )

    def build_ceia(self, calorias_alvo: float, macros_dia: dict) -> Meal:
        """
        Monta ceia leve (~10% das calorias diárias)

        Estrutura ajustada conforme tipo de dieta

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []
        aj = self.ajustes

        # Calcular proporções base e aplicar ajustes
        # Base: lacteo 60%, fruta 40%
        prop_lacteo = 0.60 * aj['proteinas']
        prop_fruta = 0.40 * aj['frutas']

        # Normalizar
        total = prop_lacteo + prop_fruta
        prop_lacteo /= total
        prop_fruta /= total

        # 1. Iogurte ou leite
        cal_lacteo = calorias_alvo * prop_lacteo
        lacteos_opcoes = self.alimentos_por_refeicao['ceia']['lacteos']
        lacteo_key = random.choice(lacteos_opcoes)
        lacteo = self._ajustar_porcao(lacteo_key, cal_lacteo)
        if lacteo:
            alimentos.append(lacteo)

        # 2. Fruta leve
        cal_fruta = calorias_alvo * prop_fruta
        frutas_opcoes = self.alimentos_por_refeicao['ceia']['frutas']
        fruta_key = random.choice(frutas_opcoes)
        fruta = self._ajustar_porcao(fruta_key, cal_fruta)
        if fruta:
            alimentos.append(fruta)

        # Opcional: Chá
        cha = self._criar_food_item('cha_verde')
        if cha:
            alimentos.append(cha)

        return Meal(
            nome="Ceia",
            horario="21:30",
            calorias_alvo=calorias_alvo,
            alimentos=alimentos
        )

    def build_complete_plan(self, distribuicao: dict, macros_dia: dict) -> List[Meal]:
        """
        Monta todas as 5 refeições do dia

        Args:
            distribuicao: Dict com calorias por refeição
            macros_dia: Dict com macros totais do dia

        Returns:
            Lista de 5 objetos Meal
        """
        # Usar seed baseada no dia para consistência (opcional)
        # random.seed(42)  # Descomente para reprodutibilidade

        return [
            self.build_cafe_manha(distribuicao['cafe']['kcal'], macros_dia),
            self.build_almoco(distribuicao['almoco']['kcal'], macros_dia),
            self.build_lanche(distribuicao['lanche']['kcal'], macros_dia),
            self.build_jantar(distribuicao['jantar']['kcal'], macros_dia),
            self.build_ceia(distribuicao['ceia']['kcal'], macros_dia)
        ]

    def get_resumo_nutricional(self, refeicoes: List[Meal]) -> dict:
        """
        Calcula o resumo nutricional de todas as refeições

        Args:
            refeicoes: Lista de refeições

        Returns:
            Dict com totais de calorias, carbs, proteínas e gorduras
        """
        total_kcal = sum(r.calorias_total for r in refeicoes)
        total_carb = sum(r.carb_total for r in refeicoes)
        total_prot = sum(r.prot_total for r in refeicoes)
        total_gord = sum(r.gord_total for r in refeicoes)

        return {
            'calorias': total_kcal,
            'carboidratos_g': total_carb,
            'proteinas_g': total_prot,
            'gorduras_g': total_gord,
            'carboidratos_percent': (total_carb * 4 / total_kcal * 100) if total_kcal > 0 else 0,
            'proteinas_percent': (total_prot * 4 / total_kcal * 100) if total_kcal > 0 else 0,
            'gorduras_percent': (total_gord * 9 / total_kcal * 100) if total_kcal > 0 else 0
        }
