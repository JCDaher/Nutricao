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

    def __init__(self):
        self.alimentos = ALIMENTOS
        self.alimentos_por_refeicao = ALIMENTOS_POR_REFEICAO

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

    def _ajustar_porcao(self, key: str, calorias_alvo: float) -> FoodItem:
        """
        Ajusta a porção de um alimento para atingir as calorias alvo

        Args:
            key: Chave do alimento
            calorias_alvo: Calorias desejadas

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

        # Limitar a uma porção razoável (máximo 2x a porção usual)
        max_gramas = alimento['gramas_porcao'] * 2
        gramas_ajustadas = min(gramas_necessarias, max_gramas)

        return self._criar_food_item(key, gramas_ajustadas)

    def build_cafe_manha(self, calorias_alvo: float, macros_dia: dict) -> Meal:
        """
        Monta café da manhã balanceado (~20% das calorias diárias)

        Estrutura padrão:
        - Cereal/pão (40% das calorias)
        - Proteína/laticínio (25% das calorias)
        - Fruta (20% das calorias)
        - Gordura saudável (15% das calorias)

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia (para referência)

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []

        # 1. Cereal/Pão (~40% das calorias)
        cal_cereal = calorias_alvo * 0.40
        cereais_opcoes = self.alimentos_por_refeicao['cafe_manha']['cereais']
        cereal_key = random.choice(cereais_opcoes)
        cereal = self._ajustar_porcao(cereal_key, cal_cereal)
        if cereal:
            alimentos.append(cereal)

        # 2. Proteína/Ovo (~25% das calorias)
        cal_proteina = calorias_alvo * 0.25
        proteinas_opcoes = self.alimentos_por_refeicao['cafe_manha']['proteinas']
        proteina_key = random.choice(proteinas_opcoes)
        proteina = self._ajustar_porcao(proteina_key, cal_proteina)
        if proteina:
            alimentos.append(proteina)

        # 3. Laticínio (~15% das calorias)
        cal_lacteo = calorias_alvo * 0.15
        lacteos_opcoes = self.alimentos_por_refeicao['cafe_manha']['lacteos']
        lacteo_key = random.choice(lacteos_opcoes)
        lacteo = self._ajustar_porcao(lacteo_key, cal_lacteo)
        if lacteo:
            alimentos.append(lacteo)

        # 4. Fruta (~15% das calorias)
        cal_fruta = calorias_alvo * 0.15
        frutas_opcoes = self.alimentos_por_refeicao['cafe_manha']['frutas']
        fruta_key = random.choice(frutas_opcoes)
        fruta = self._ajustar_porcao(fruta_key, cal_fruta)
        if fruta:
            alimentos.append(fruta)

        # 5. Gordura saudável (~5% das calorias - sementes)
        cal_gordura = calorias_alvo * 0.05
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

        Estrutura padrão brasileiro:
        - Arroz/cereal (25% das calorias)
        - Feijão/leguminosa (15% das calorias)
        - Proteína (30% das calorias)
        - Salada/verduras (5% das calorias - livre)
        - Legume cozido (10% das calorias)
        - Azeite (15% das calorias)

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []

        # 1. Arroz/Cereal (~25%)
        cal_cereal = calorias_alvo * 0.25
        cereais_opcoes = self.alimentos_por_refeicao['almoco']['cereais']
        cereal_key = random.choice(cereais_opcoes)
        cereal = self._ajustar_porcao(cereal_key, cal_cereal)
        if cereal:
            alimentos.append(cereal)

        # 2. Feijão/Leguminosa (~15%)
        cal_leguminosa = calorias_alvo * 0.15
        leguminosas_opcoes = self.alimentos_por_refeicao['almoco']['leguminosas']
        leguminosa_key = random.choice(leguminosas_opcoes)
        leguminosa = self._ajustar_porcao(leguminosa_key, cal_leguminosa)
        if leguminosa:
            alimentos.append(leguminosa)

        # 3. Proteína (~30%)
        cal_proteina = calorias_alvo * 0.30
        proteinas_opcoes = self.alimentos_por_refeicao['almoco']['proteinas']
        proteina_key = random.choice(proteinas_opcoes)
        proteina = self._ajustar_porcao(proteina_key, cal_proteina)
        if proteina:
            alimentos.append(proteina)

        # 4. Salada (verduras à vontade)
        verduras_opcoes = self.alimentos_por_refeicao['almoco']['verduras']
        verdura_key = random.choice(verduras_opcoes)
        verdura = self._criar_food_item(verdura_key, 50)  # Porção fixa
        if verdura:
            alimentos.append(verdura)

        # 5. Legume cozido (~10%)
        cal_legume = calorias_alvo * 0.10
        legumes_opcoes = self.alimentos_por_refeicao['almoco']['legumes']
        legume_key = random.choice(legumes_opcoes)
        legume = self._ajustar_porcao(legume_key, cal_legume)
        if legume:
            alimentos.append(legume)

        # 6. Tomate na salada
        tomate = self._criar_food_item('tomate', 60)
        if tomate:
            alimentos.append(tomate)

        # 7. Azeite (~15% para tempero)
        cal_azeite = calorias_alvo * 0.10
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

        Estrutura leve:
        - Fruta (40% das calorias)
        - Iogurte/laticínio (35% das calorias)
        - Castanhas/gordura saudável (25% das calorias)

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []

        # 1. Fruta (~40%)
        cal_fruta = calorias_alvo * 0.40
        frutas_opcoes = self.alimentos_por_refeicao['lanche']['frutas']
        fruta_key = random.choice(frutas_opcoes)
        fruta = self._ajustar_porcao(fruta_key, cal_fruta)
        if fruta:
            alimentos.append(fruta)

        # 2. Iogurte (~35%)
        cal_lacteo = calorias_alvo * 0.35
        lacteos_opcoes = self.alimentos_por_refeicao['lanche']['lacteos']
        lacteo_key = random.choice(lacteos_opcoes)
        lacteo = self._ajustar_porcao(lacteo_key, cal_lacteo)
        if lacteo:
            alimentos.append(lacteo)

        # 3. Castanhas (~25%)
        cal_gordura = calorias_alvo * 0.25
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

        Estrutura similar ao almoço, mas mais leve:
        - Arroz/cereal (25% das calorias)
        - Proteína (35% das calorias)
        - Salada/verduras (5% das calorias)
        - Legume cozido (20% das calorias)
        - Azeite (15% das calorias)

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []

        # 1. Arroz/Cereal (~25%)
        cal_cereal = calorias_alvo * 0.25
        cereais_opcoes = self.alimentos_por_refeicao['jantar']['cereais']
        cereal_key = random.choice(cereais_opcoes)
        cereal = self._ajustar_porcao(cereal_key, cal_cereal)
        if cereal:
            alimentos.append(cereal)

        # 2. Proteína (~35%)
        cal_proteina = calorias_alvo * 0.35
        proteinas_opcoes = self.alimentos_por_refeicao['jantar']['proteinas']
        proteina_key = random.choice(proteinas_opcoes)
        proteina = self._ajustar_porcao(proteina_key, cal_proteina)
        if proteina:
            alimentos.append(proteina)

        # 3. Salada (verduras à vontade)
        verduras_opcoes = self.alimentos_por_refeicao['jantar']['verduras']
        verdura_key = random.choice(verduras_opcoes)
        verdura = self._criar_food_item(verdura_key, 50)
        if verdura:
            alimentos.append(verdura)

        # 4. Legume cozido (~20%)
        cal_legume = calorias_alvo * 0.20
        legumes_opcoes = self.alimentos_por_refeicao['jantar']['legumes']
        legume_key = random.choice(legumes_opcoes)
        legume = self._ajustar_porcao(legume_key, cal_legume)
        if legume:
            alimentos.append(legume)

        # 5. Pepino na salada
        pepino = self._criar_food_item('pepino', 60)
        if pepino:
            alimentos.append(pepino)

        # 6. Azeite (~10%)
        cal_azeite = calorias_alvo * 0.10
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

        Estrutura muito leve para evitar pico glicêmico noturno:
        - Iogurte ou leite (60% das calorias)
        - Fruta leve (40% das calorias)

        Args:
            calorias_alvo: Calorias totais para a refeição
            macros_dia: Macros totais do dia

        Returns:
            Meal com alimentos balanceados
        """
        alimentos = []

        # 1. Iogurte ou leite (~60%)
        cal_lacteo = calorias_alvo * 0.60
        lacteos_opcoes = self.alimentos_por_refeicao['ceia']['lacteos']
        lacteo_key = random.choice(lacteos_opcoes)
        lacteo = self._ajustar_porcao(lacteo_key, cal_lacteo)
        if lacteo:
            alimentos.append(lacteo)

        # 2. Fruta leve (~40%)
        cal_fruta = calorias_alvo * 0.40
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
