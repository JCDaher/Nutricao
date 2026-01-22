"""
Formatador de dietas em Markdown usando templates Python
SEM uso de API - Custo: $0
"""
from typing import List

from app.models import PatientData, NutritionData, Meal
from app.data.substituicoes import formatar_todas_tabelas_markdown


class MarkdownFormatter:
    """
    Gera dietas completas em Markdown usando templates
    100% Python - Custo $0
    """

    def format_complete_diet(
        self,
        patient: PatientData,
        nutrition: NutritionData,
        meals: List[Meal],
        custom_presentation: str = None
    ) -> str:
        """
        Gera documento Markdown completo

        Args:
            patient: Dados do paciente
            nutrition: Dados nutricionais
            meals: Lista de refeições
            custom_presentation: Apresentação da API (opcional)
        """

        titulo = "# PLANO ALIMENTAR PERSONALIZADO\n\n"

        apresentacao = (
            custom_presentation if custom_presentation
            else self._get_apresentacao_template(patient, nutrition)
        )

        dados = self._format_patient_data(patient, nutrition)
        calculos = self._format_nutrition_calculations(nutrition)
        refeicoes = self._format_meals(meals)
        substituicoes = self._get_substituicoes_completas()
        orientacoes = self._get_orientacoes_template(patient)
        suplementos = self._get_suplementos_template()
        dicas = self._get_dicas_template()
        assinatura = self._get_assinatura()

        return (
            f"{titulo}"
            f"{apresentacao}\n\n"
            f"{dados}\n\n"
            f"{calculos}\n\n"
            f"{refeicoes}\n\n"
            f"{substituicoes}\n\n"
            f"{orientacoes}\n\n"
            f"{suplementos}\n\n"
            f"{dicas}\n\n"
            f"{assinatura}"
        )

    def _get_apresentacao_template(
        self,
        patient: PatientData,
        nutrition: NutritionData
    ) -> str:
        """Template de apresentação Python"""

        tratamento = "Sr." if patient.sexo == "M" else "Sra."

        if nutrition.imc >= 30:
            objetivo = "controle do diabetes com perda de peso gradual e sustentável"
        elif nutrition.imc >= 25:
            objetivo = "controle do diabetes e perda moderada de peso"
        else:
            objetivo = "manutenção de peso saudável e controle glicêmico otimizado"

        # Personalizar conforme tipo de dieta
        tipo_dieta_desc = {
            'personalizado': 'balanceada, com proporção adequada de macronutrientes',
            'low_carb': 'com baixo teor de carboidratos para melhor controle glicêmico',
            'low_carb_moderado': 'com redução moderada de carboidratos',
            'mediterraneo': 'no estilo mediterrâneo, rica em gorduras saudáveis',
            'high_protein': 'com alto teor proteico para preservar massa muscular'
        }
        dieta_desc = tipo_dieta_desc.get(patient.tipo_dieta, tipo_dieta_desc['personalizado'])

        return f"""## APRESENTAÇÃO DO PLANO

Caro(a) {tratamento} {patient.nome},

Este plano alimentar personalizado foi desenvolvido especialmente para atender às suas necessidades nutricionais individuais, considerando seus dados antropométricos e o objetivo de {objetivo}. A dieta é {dieta_desc}. O plano prioriza alimentos brasileiros tradicionais e ingredientes funcionais que contribuem para a saúde digestiva e metabólica.

O planejamento nutricional visa proporcionar equilíbrio entre macronutrientes, promover saciedade adequada e facilitar o controle glicêmico através da escolha de alimentos de baixo índice glicêmico e alto teor de fibras. As tabelas de substituições permitem flexibilidade e variedade no dia a dia.

Este é um plano inicial que poderá ser ajustado conforme sua resposta individual e acompanhamento dos exames laboratoriais. Recomenda-se acompanhamento médico e nutricional periódico para otimizar os resultados."""

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

        risco_cv_line = ""
        if nutrition.risco_cardiovascular:
            risco_cv_line = f"- **Risco Cardiovascular:** {nutrition.risco_cardiovascular}\n"

        return f"""## INFORMAÇÕES DO PACIENTE

- **Nome:** {patient.nome}
- **Idade:** {patient.idade} anos
- **Sexo:** {"Masculino" if patient.sexo == "M" else "Feminino"}
- **Peso atual:** {patient.peso:.1f} kg
- **Altura:** {patient.altura:.0f} cm
- **IMC:** {nutrition.imc:.1f} kg/m² ({classif_imc})
{hba1c_line}{risco_cv_line}- **Condição:** Diabetes Mellitus"""

    def _format_nutrition_calculations(self, nutrition: NutritionData) -> str:
        """Formata cálculos nutricionais"""

        m = nutrition.macros

        return f"""## NECESSIDADES CALÓRICAS CALCULADAS

- **Taxa Metabólica Basal (TMB):** {nutrition.tmb:.0f} kcal/dia
- **Necessidade Calórica Total:** {nutrition.necessidade_calorica:.0f} kcal/dia
- **Meta Calórica (para controle glicêmico):** {nutrition.meta_calorica:.0f} kcal/dia

### Distribuição de Macronutrientes

| Macronutriente | Gramas/dia | % do VET |
|----------------|------------|----------|
| Carboidratos | {m['carb_g']:.0f}g | {m['carb_percent']}% |
| Proteínas | {m['prot_g']:.0f}g | {m['prot_percent']}% |
| Gorduras | {m['gord_g']:.0f}g | {m['gord_percent']}% |"""

    def _format_meals(self, meals: List[Meal]) -> str:
        """Formata refeições em tabelas"""

        output = "## PLANO DE REFEIÇÕES DIÁRIAS\n"

        for meal in meals:
            total_kcal = sum(a.kcal for a in meal.alimentos)
            total_carb = sum(a.carb for a in meal.alimentos)
            total_prot = sum(a.prot for a in meal.alimentos)
            total_gord = sum(a.gord for a in meal.alimentos)

            output += f"\n### {meal.nome} ({meal.horario})\n"
            output += f"**Meta:** ~{meal.calorias_alvo:.0f} kcal\n\n"
            output += "| Alimento | Porção | Kcal | Carb | Prot | Gord |\n"
            output += "|----------|--------|------|------|------|------|\n"

            for alimento in meal.alimentos:
                output += f"| {alimento.nome} | {alimento.porcao} | {alimento.kcal:.0f} | {alimento.carb:.1f}g | {alimento.prot:.1f}g | {alimento.gord:.1f}g |\n"

            output += f"| **TOTAL** | | **{total_kcal:.0f}** | **{total_carb:.1f}g** | **{total_prot:.1f}g** | **{total_gord:.1f}g** |\n"

        return output

    def _get_substituicoes_completas(self) -> str:
        """Retorna tabelas de substituições do módulo de substituições"""
        return formatar_todas_tabelas_markdown()

    def _get_orientacoes_template(self, patient: PatientData) -> str:
        """Orientações completas personalizadas"""

        agua_litros = (patient.peso * 35) / 1000

        return f"""## ORIENTAÇÕES ESPECÍFICAS

### Controle Glicêmico
- Combinar carboidratos com fibras ou proteínas para reduzir pico glicêmico
- Preferir carboidratos integrais (arroz integral, pão integral, aveia)
- Distribuir carboidratos ao longo do dia em porções moderadas
- Monitorar glicemia conforme orientação médica
- Evitar jejum prolongado (máximo 3-4 horas entre refeições)

### Saúde Intestinal
- **Fibras solúveis:** Aveia, frutas com casca, leguminosas
- **Fibras insolúveis:** Verduras, cereais integrais, cascas
- **Alimentos fermentados:** Iogurte natural, kefir, coalhada
- **Prebióticos:** Alho, cebola, banana verde, chicória

### Hidratação
- Beba **{agua_litros:.1f} litros de água por dia** (35ml/kg)
- Água auxilia no funcionamento intestinal e controle glicêmico
- Evite líquidos em excesso durante as refeições principais

### Mastigação e Digestão
- Mastigue cada porção 20-30 vezes
- Faça refeições com calma, sentado, sem distrações
- Não deite imediatamente após as refeições (espere 2 horas)"""

    def _get_suplementos_template(self) -> str:
        """Suplementos recomendados"""

        return """## SUPLEMENTOS E ALIMENTOS FUNCIONAIS RECOMENDADOS

| Suplemento | Benefício | Como usar |
|------------|-----------|-----------|
| Semente de chia | Fibras, ômega-3, saciedade | 1 colher de sopa/dia |
| Semente de linhaça | Fibras, lignanas, ômega-3 | 1 colher de sopa/dia (triturada) |
| Castanha do Pará | Selênio, gorduras boas | 2 unidades/dia |
| Canela | Auxilia controle glicêmico | 1/2 colher de chá/dia |
| Psyllium | Fibra solúvel, saciedade | 1 colher de chá antes das refeições |
| Cúrcuma | Anti-inflamatório natural | 1/2 colher de chá/dia |

**Observação:** Consulte seu médico antes de iniciar qualquer suplementação."""

    def _get_dicas_template(self) -> str:
        """Dicas importantes"""

        return """## DICAS IMPORTANTES

1. **Mastigue bem os alimentos** - a digestão começa na boca
2. **Faça refeições em horários regulares** - evite pular refeições
3. **Evite líquidos durante as refeições** - beba 30 min antes ou depois
4. **Não deite logo após comer** - espere pelo menos 2 horas
5. **Pratique atividade física regular** - caminhadas de 30 min ajudam
6. **Monitore sua glicemia** - especialmente em jejum e pós-prandial
7. **Durma bem** - o sono adequado ajuda no controle metabólico

## ALIMENTOS A EVITAR

- Açúcar refinado e doces em geral
- Refrigerantes e sucos industrializados
- Pães brancos e massas refinadas
- Frituras e alimentos ultraprocessados
- Bebidas alcoólicas
- Embutidos (salsicha, presunto, mortadela)

## SINAIS DE ALERTA

### Hipoglicemia (açúcar baixo)
- Sintomas: tremores, suor frio, tontura, fome intensa
- Ação: consumir 15g de carboidrato rápido (1 colher de sopa de mel ou 150ml de suco)

### Hiperglicemia (açúcar alto)
- Sintomas: sede excessiva, cansaço, visão turva
- Ação: verificar glicemia e seguir orientação médica"""

    def _get_assinatura(self) -> str:
        """Assinatura do médico"""

        return """---

**Dr. Jorge Cecílio Daher Jr**
CRMGO 6108 | RQE 5769, 5772
Endocrinologia e Metabologia

*Este plano alimentar foi elaborado de forma personalizada. Consulte sempre seu médico antes de fazer alterações significativas na alimentação.*"""
