"""
Formatador especializado para contagem de carboidratos
Para pacientes em esquema basal-bolus de insulina
"""
from typing import List, Optional

from app.models import PatientData, NutritionData, Meal


class CarbCountingFormatter:
    """
    Gera dietas com foco em contagem de carboidratos
    Ideal para pacientes em insulinoterapia intensiva
    """

    # 1 porção de carboidrato = 15g
    GRAMAS_POR_PORCAO = 15

    def format_carb_counting_diet(
        self,
        patient: PatientData,
        nutrition: NutritionData,
        meals: List[Meal],
        razao_insulina_cho: Optional[float] = None
    ) -> str:
        """
        Gera documento Markdown formatado para contagem de carboidratos

        Args:
            patient: Dados do paciente
            nutrition: Dados nutricionais
            meals: Lista de refeições
            razao_insulina_cho: Razão insulina/carboidrato (UI por 15g)
        """

        titulo = "# PLANO ALIMENTAR COM CONTAGEM DE CARBOIDRATOS\n\n"

        apresentacao = self._get_apresentacao_cho(patient, nutrition)
        dados = self._format_patient_data(patient, nutrition)
        guia_cho = self._get_guia_contagem()
        calculos = self._format_nutrition_calculations(nutrition)
        refeicoes = self._format_meals_cho(meals, razao_insulina_cho)
        tabela_cho = self._get_tabela_porcoes_cho()
        orientacoes = self._get_orientacoes_cho(patient, razao_insulina_cho)
        assinatura = self._get_assinatura()

        return (
            f"{titulo}"
            f"{apresentacao}\n\n"
            f"{dados}\n\n"
            f"{guia_cho}\n\n"
            f"{calculos}\n\n"
            f"{refeicoes}\n\n"
            f"{tabela_cho}\n\n"
            f"{orientacoes}\n\n"
            f"{assinatura}"
        )

    def _get_apresentacao_cho(
        self,
        patient: PatientData,
        nutrition: NutritionData
    ) -> str:
        """Apresentação específica para contagem de CHO"""

        tratamento = "Sr." if patient.sexo == "M" else "Sra."

        return f"""## APRESENTAÇÃO

Caro(a) {tratamento} {patient.nome},

Este plano alimentar foi desenvolvido com **foco na contagem de carboidratos**, uma técnica essencial para pacientes em uso de insulina de ação rápida. A contagem de carboidratos permite maior flexibilidade alimentar e melhor controle glicêmico, pois você aprenderá a ajustar a dose de insulina conforme a quantidade de carboidratos consumida.

Neste documento, cada alimento está apresentado com sua quantidade de carboidratos em gramas e em **porções de CHO** (1 porção = 15g de carboidrato). Isso facilita o cálculo da dose de insulina necessária para cada refeição.

**Importante:** A contagem de carboidratos deve ser combinada com monitorização frequente da glicemia capilar para ajustes finos da terapia insulínica."""

    def _format_patient_data(
        self,
        patient: PatientData,
        nutrition: NutritionData
    ) -> str:
        """Formata dados do paciente"""

        # Classificação do IMC
        if nutrition.imc < 18.5:
            classif_imc = "Abaixo do peso"
        elif nutrition.imc < 25:
            classif_imc = "Peso normal"
        elif nutrition.imc < 30:
            classif_imc = "Sobrepeso"
        elif nutrition.imc < 35:
            classif_imc = "Obesidade grau I"
        elif nutrition.imc < 40:
            classif_imc = "Obesidade grau II"
        else:
            classif_imc = "Obesidade grau III"

        hba1c_line = ""
        if patient.hba1c:
            hba1c_line = f"- **HbA1c:** {patient.hba1c}%\n"
        elif patient.glicemia:
            hba1c_line = f"- **Glicemia de jejum:** {patient.glicemia} mg/dL\n"

        return f"""## INFORMAÇÕES DO PACIENTE

- **Nome:** {patient.nome}
- **Idade:** {patient.idade} anos
- **Sexo:** {"Masculino" if patient.sexo == "M" else "Feminino"}
- **Peso atual:** {patient.peso:.1f} kg
- **Altura:** {patient.altura:.0f} cm
- **IMC:** {nutrition.imc:.1f} kg/m² ({classif_imc})
{hba1c_line}- **Regime:** Contagem de Carboidratos"""

    def _get_guia_contagem(self) -> str:
        """Guia rápido de contagem de CHO"""

        return """## GUIA RÁPIDO DE CONTAGEM DE CARBOIDRATOS

### O que é uma porção de carboidrato?
**1 porção de CHO = 15 gramas de carboidrato**

### Como usar este plano:
1. Identifique os carboidratos em cada alimento
2. Some o total de carboidratos da refeição
3. Divida por 15 para saber quantas porções
4. Aplique sua razão insulina/carboidrato

### Exemplo prático:
- Refeição com 60g de carboidratos
- 60g ÷ 15 = **4 porções de CHO**
- Se sua razão é 1:15 (1 UI para cada 15g)
- Dose de insulina rápida: **4 UI**

### Dica importante:
Sempre confirme sua razão insulina/carboidrato com seu médico, pois ela pode variar conforme o horário do dia e sensibilidade individual."""

    def _format_nutrition_calculations(self, nutrition: NutritionData) -> str:
        """Formata cálculos nutricionais com destaque para CHO"""

        m = nutrition.macros
        cho_total = m['carb_g']
        porcoes_dia = cho_total / self.GRAMAS_POR_PORCAO

        return f"""## METAS NUTRICIONAIS DIÁRIAS

- **Meta Calórica:** {nutrition.meta_calorica:.0f} kcal/dia

### Carboidratos (FOCO PRINCIPAL)
- **Total:** {cho_total:.0f}g/dia
- **Porções de CHO:** {porcoes_dia:.1f} porções/dia (≈ {round(porcoes_dia)} porções)
- **Percentual:** {m['carb_percent']}% das calorias

### Outros Macronutrientes
| Nutriente | Gramas/dia | % das Calorias |
|-----------|------------|----------------|
| Proteínas | {m['prot_g']:.0f}g | {m['prot_percent']}% |
| Gorduras | {m['gord_g']:.0f}g | {m['gord_percent']}% |"""

    def _format_meals_cho(
        self,
        meals: List[Meal],
        razao_insulina_cho: Optional[float]
    ) -> str:
        """Formata refeições com destaque para carboidratos"""

        output = "## PLANO DE REFEIÇÕES COM CONTAGEM DE CHO\n"

        for meal in meals:
            total_kcal = sum(a.kcal for a in meal.alimentos)
            total_carb = sum(a.carb for a in meal.alimentos)
            total_prot = sum(a.prot for a in meal.alimentos)
            total_gord = sum(a.gord for a in meal.alimentos)
            porcoes_cho = total_carb / self.GRAMAS_POR_PORCAO

            output += f"\n### {meal.nome} ({meal.horario})\n"
            output += f"**Carboidratos:** {total_carb:.0f}g = **{porcoes_cho:.1f} porções de CHO**\n"

            if razao_insulina_cho:
                insulina_sugerida = total_carb / (15 / razao_insulina_cho)
                output += f"**Insulina sugerida:** ~{insulina_sugerida:.0f} UI (razão 1:{int(15/razao_insulina_cho)})\n"

            output += "\n| Alimento | Porção | **CHO (g)** | Porções | Kcal |\n"
            output += "|----------|--------|-------------|---------|------|\n"

            for alimento in meal.alimentos:
                porcao_cho = alimento.carb / self.GRAMAS_POR_PORCAO
                output += f"| {alimento.nome} | {alimento.porcao} | **{alimento.carb:.0f}g** | {porcao_cho:.1f} | {alimento.kcal:.0f} |\n"

            output += f"| **TOTAL** | | **{total_carb:.0f}g** | **{porcoes_cho:.1f}** | {total_kcal:.0f} |\n"

        # Resumo do dia
        total_cho_dia = sum(sum(a.carb for a in meal.alimentos) for meal in meals)
        porcoes_dia = total_cho_dia / self.GRAMAS_POR_PORCAO

        output += f"\n### RESUMO DIÁRIO DE CARBOIDRATOS\n"
        output += f"- **Total de CHO:** {total_cho_dia:.0f}g\n"
        output += f"- **Total de porções:** {porcoes_dia:.1f} porções\n"

        if razao_insulina_cho:
            insulina_total = total_cho_dia / (15 / razao_insulina_cho)
            output += f"- **Insulina rápida estimada:** ~{insulina_total:.0f} UI/dia\n"

        return output

    def _get_tabela_porcoes_cho(self) -> str:
        """Tabela de referência de porções de CHO"""

        return """## TABELA DE REFERÊNCIA - PORÇÕES DE CARBOIDRATO

### PÃES E CEREAIS (1 porção = 15g CHO)
| Alimento | Quantidade para 1 porção |
|----------|-------------------------|
| Pão francês | ½ unidade (25g) |
| Pão de forma | 1 fatia (30g) |
| Arroz branco cozido | 2 colheres de sopa (50g) |
| Arroz integral cozido | 2½ colheres de sopa (60g) |
| Macarrão cozido | 2 colheres de sopa (50g) |
| Aveia em flocos | 2 colheres de sopa (30g) |
| Batata cozida | 1 unidade pequena (70g) |
| Mandioca cozida | 2 colheres de sopa (50g) |
| Tapioca (goma) | 2 colheres de sopa (30g) |

### FRUTAS (1 porção = 15g CHO)
| Alimento | Quantidade para 1 porção |
|----------|-------------------------|
| Banana | ½ unidade média (50g) |
| Maçã | 1 unidade pequena (100g) |
| Laranja | 1 unidade média (150g) |
| Mamão papaia | 1 fatia média (150g) |
| Manga | ½ unidade pequena (70g) |
| Uva | 10 unidades (50g) |
| Melancia | 1 fatia média (200g) |
| Abacaxi | 1 fatia média (100g) |

### LEITE E DERIVADOS (1 porção = 15g CHO)
| Alimento | Quantidade para 1 porção |
|----------|-------------------------|
| Leite integral | 1 copo (200ml) |
| Iogurte natural | 1 pote (170g) |
| Leite desnatado | 1 copo (200ml) |

### LEGUMINOSAS (1 porção = 15g CHO)
| Alimento | Quantidade para 1 porção |
|----------|-------------------------|
| Feijão cozido | 1 concha média (80g) |
| Lentilha cozida | 3 colheres de sopa (60g) |
| Grão de bico cozido | 3 colheres de sopa (60g) |

### ALIMENTOS LIVRES (< 5g CHO por porção)
Podem ser consumidos com mais liberdade:
- Verduras folhosas (alface, rúcula, agrião)
- Legumes não amiláceos (pepino, tomate, abobrinha)
- Carnes, ovos, peixes
- Queijos
- Azeite, óleo
- Café e chá sem açúcar"""

    def _get_orientacoes_cho(
        self,
        patient: PatientData,
        razao_insulina_cho: Optional[float]
    ) -> str:
        """Orientações específicas para contagem de CHO"""

        razao_texto = ""
        if razao_insulina_cho:
            razao_texto = f"\n- **Sua razão I:CHO:** 1 UI para cada {int(15/razao_insulina_cho)}g de carboidrato"

        agua = (patient.peso * 35) / 1000

        return f"""## ORIENTAÇÕES PARA CONTAGEM DE CARBOIDRATOS

### Passos para cada refeição:
1. **Identifique** os alimentos que contêm carboidratos
2. **Meça ou estime** as porções (use balança de cozinha no início)
3. **Calcule** o total de carboidratos em gramas
4. **Aplique** sua razão insulina/carboidrato
5. **Ajuste** conforme glicemia pré-prandial (correção){razao_texto}

### Monitorização recomendada:
- Glicemia em jejum
- Glicemia 2h após as principais refeições
- Registre: glicemia + CHO consumidos + insulina aplicada

### Fatores que afetam a glicemia além dos CHO:
- Índice glicêmico do alimento
- Presença de fibras, proteínas e gorduras na refeição
- Atividade física
- Estresse e doenças
- Horário da refeição

### Hidratação:
- Beba **{agua:.1f} litros de água por dia** (35ml/kg)

### Sinais de hipoglicemia (glicemia < 70 mg/dL):
- Tremores, suor frio, tontura, fome intensa
- **Ação:** Consumir 15g de carboidrato rápido (1 porção):
  - 150ml de suco de laranja
  - 1 colher de sopa de mel
  - 3 balas de glicose
- Aguardar 15 minutos e medir novamente

### Quando procurar atendimento:
- Glicemias persistentemente > 300 mg/dL
- Hipoglicemias frequentes ou graves
- Sintomas de cetoacidose (náuseas, vômitos, dor abdominal)"""

    def _get_assinatura(self) -> str:
        """Assinatura do médico"""

        return """---

**Dr. Jorge Cecílio Daher Jr**
CRMGO 6108 | RQE 5769, 5772
Endocrinologia e Metabologia

*Este plano alimentar foi elaborado de forma personalizada para contagem de carboidratos.
A razão insulina/carboidrato deve ser ajustada individualmente com acompanhamento médico.*"""
