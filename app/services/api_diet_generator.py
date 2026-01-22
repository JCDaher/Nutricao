"""
Gerador via API Anthropic
Modos: minimal (só apresentação) e full (dieta completa)
"""
from typing import Tuple

from anthropic import Anthropic

from app.models import DietPlan, PatientData, NutritionData
from app.config.settings import settings
from app.data.substituicoes import formatar_todas_tabelas_markdown


class APIDietGenerator:
    """
    Gera dietas usando API Anthropic
    """

    def __init__(self):
        api_key = settings.anthropic_api_key
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada")

        self.client = Anthropic(api_key=api_key)
        self.model = settings.anthropic_model

    def generate_minimal(
        self,
        patient: PatientData,
        nutrition: NutritionData
    ) -> Tuple[str, int]:
        """
        Gera APENAS apresentação humanizada

        Returns:
            (texto_apresentacao, tokens_usados)
        """

        prompt = self._build_minimal_prompt(patient, nutrition)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=settings.max_tokens_minimal,
            messages=[{"role": "user", "content": prompt}]
        )

        apresentacao = message.content[0].text

        # Usar tokens reais da resposta
        tokens = message.usage.input_tokens + message.usage.output_tokens

        return (apresentacao, tokens)

    def generate_full(self, diet_plan: DietPlan) -> Tuple[str, int]:
        """
        Gera dieta COMPLETA

        Returns:
            (markdown_completo, tokens_usados)
        """

        prompt = self._build_full_prompt(diet_plan)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=settings.max_tokens_full,
            messages=[{"role": "user", "content": prompt}]
        )

        markdown = message.content[0].text

        # Usar tokens reais da resposta
        tokens = message.usage.input_tokens + message.usage.output_tokens

        return (markdown, tokens)

    def _build_minimal_prompt(
        self,
        patient: PatientData,
        nutrition: NutritionData
    ) -> str:
        """Prompt mínimo para apresentação"""

        tratamento = "Sr." if patient.sexo == "M" else "Sra."

        if nutrition.imc >= 30:
            objetivo = "controle do diabetes com perda de peso gradual"
        elif nutrition.imc >= 25:
            objetivo = "controle do diabetes e perda moderada de peso"
        else:
            objetivo = "manutenção de peso saudável e controle glicêmico"

        tipo_dieta_desc = {
            'personalizado': 'balanceada',
            'low_carb': 'com baixo teor de carboidratos',
            'low_carb_moderado': 'com redução moderada de carboidratos',
            'mediterraneo': 'no estilo mediterrâneo',
            'high_protein': 'com alto teor proteico'
        }
        dieta = tipo_dieta_desc.get(patient.tipo_dieta, 'balanceada')

        return f"""Escreva 3 parágrafos de apresentação para um plano alimentar personalizado:

Paciente: {tratamento} {patient.nome}
Idade: {patient.idade} anos
IMC: {nutrition.imc:.1f} kg/m²
Meta calórica: {nutrition.meta_calorica:.0f} kcal/dia
Tipo de dieta: {dieta}
Objetivo: {objetivo}

INSTRUÇÕES:
- Tom formal, acolhedor e educativo
- Mencionar: diabetes, alimentos brasileiros, saúde intestinal
- 3 parágrafos de 3-4 linhas cada
- 300-400 palavras total
- Use o título "## APRESENTAÇÃO DO PLANO" no início
- Responda APENAS os parágrafos formatados, sem explicações adicionais"""

    def _build_full_prompt(self, plan: DietPlan) -> str:
        """Prompt completo para dieta inteira"""

        p = plan.paciente
        c = plan.calculos

        # Classificação do IMC
        if c.imc < 18.5:
            classif_imc = "Abaixo do peso"
        elif c.imc < 25:
            classif_imc = "Peso normal"
        elif c.imc < 30:
            classif_imc = "Sobrepeso"
        elif c.imc < 35:
            classif_imc = "Obesidade grau I"
        elif c.imc < 40:
            classif_imc = "Obesidade grau II"
        else:
            classif_imc = "Obesidade grau III"

        # Formatar refeições
        refeicoes_md = ""
        for meal in plan.refeicoes:
            total_kcal = sum(a.kcal for a in meal.alimentos)
            total_carb = sum(a.carb for a in meal.alimentos)
            total_prot = sum(a.prot for a in meal.alimentos)
            total_gord = sum(a.gord for a in meal.alimentos)

            refeicoes_md += f"\n### {meal.nome} ({meal.horario})\n"
            refeicoes_md += f"**Meta:** ~{meal.calorias_alvo:.0f} kcal\n\n"
            refeicoes_md += "| Alimento | Porção | Kcal | Carb | Prot | Gord |\n"
            refeicoes_md += "|----------|--------|------|------|------|------|\n"

            for alimento in meal.alimentos:
                refeicoes_md += f"| {alimento.nome} | {alimento.porcao} | {alimento.kcal:.0f} | {alimento.carb:.1f}g | {alimento.prot:.1f}g | {alimento.gord:.1f}g |\n"

            refeicoes_md += f"| **TOTAL** | | **{total_kcal:.0f}** | **{total_carb:.1f}g** | **{total_prot:.1f}g** | **{total_gord:.1f}g** |\n"

        # Info glicêmica
        info_glicemica = ""
        if p.hba1c:
            info_glicemica = f"- **HbA1c:** {p.hba1c}%"
        elif p.glicemia:
            info_glicemica = f"- **Glicemia de jejum:** {p.glicemia} mg/dL"

        # Tabelas de substituição
        tabelas = formatar_todas_tabelas_markdown()

        # Água recomendada
        agua = (p.peso * 35) / 1000

        tratamento = "Sr." if p.sexo == "M" else "Sra."

        return f"""Você é assistente do Dr. Jorge Cecílio Daher Jr (CRMGO 6108 RQE5769, 5772).

Formate este plano alimentar em Markdown profissional. Use tratamento formal "{tratamento} {p.nome.split()[0]}".

# PLANO ALIMENTAR PERSONALIZADO

## APRESENTAÇÃO DO PLANO
[Escreva 2-3 parágrafos PERSONALIZADOS apresentando o plano para o(a) {tratamento} {p.nome}, mencionando:
- Importância do controle glicêmico para diabetes
- Benefícios da alimentação equilibrada para saúde intestinal
- Como os alimentos brasileiros escolhidos ajudam no controle metabólico
Use tom educativo, humano e profissional]

## INFORMAÇÕES DO PACIENTE
- **Nome:** {p.nome}
- **Idade:** {p.idade} anos
- **Sexo:** {"Masculino" if p.sexo == "M" else "Feminino"}
- **Peso atual:** {p.peso:.1f} kg
- **Altura:** {p.altura:.0f} cm
- **IMC:** {c.imc:.1f} kg/m² ({classif_imc})
{info_glicemica}

## NECESSIDADES CALÓRICAS CALCULADAS
- **Taxa Metabólica Basal (TMB):** {c.tmb:.0f} kcal/dia
- **Necessidade Calórica Total:** {c.necessidade_calorica:.0f} kcal/dia
- **Meta Calórica (para controle glicêmico):** {c.meta_calorica:.0f} kcal/dia

### Distribuição de Macronutrientes
| Macronutriente | Gramas/dia | % do VET |
|----------------|------------|----------|
| Carboidratos | {c.macros['carb_g']:.0f}g | {c.macros['carb_percent']}% |
| Proteínas | {c.macros['prot_g']:.0f}g | {c.macros['prot_percent']}% |
| Gorduras | {c.macros['gord_g']:.0f}g | {c.macros['gord_percent']}% |

## PLANO DE REFEIÇÕES DIÁRIAS

{refeicoes_md}

{tabelas}

## ORIENTAÇÕES PARA SAÚDE INTESTINAL

### Fibras Alimentares
- Consuma **25-30g de fibras por dia**
- Prefira grãos integrais (arroz integral, aveia, pão integral)
- Inclua leguminosas diariamente (feijão, lentilha, grão de bico)
- Frutas com casca e bagaço aumentam a ingestão de fibras

### Alimentos Fermentados e Probióticos
- Iogurte natural (sem açúcar)
- Kefir
- Coalhada
- Queijos frescos

### Prebióticos (alimentos que nutrem bactérias benéficas)
- Alho, cebola, alho-poró
- Banana verde
- Aveia
- Linhaça e chia

### Hidratação
- Beba **{agua:.1f} litros de água por dia** (35ml/kg)
- Água auxilia no funcionamento intestinal e controle glicêmico

## SUPLEMENTOS E ALIMENTOS FUNCIONAIS RECOMENDADOS

| Suplemento | Benefício | Como usar |
|------------|-----------|-----------|
| Semente de chia | Fibras, ômega-3, saciedade | 1 colher de sopa/dia |
| Semente de linhaça | Fibras, lignanas, ômega-3 | 1 colher de sopa/dia (triturada) |
| Castanha do Pará | Selênio, gorduras boas | 2 unidades/dia |
| Canela | Auxilia controle glicêmico | 1/2 colher de chá/dia |
| Psyllium | Fibra solúvel | 1 colher de chá antes das refeições |

## DICAS IMPORTANTES

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

---

**Dr. Jorge Cecílio Daher Jr**
CRMGO 6108 | RQE 5769, 5772
Endocrinologia e Metabologia

*Este plano alimentar foi elaborado de forma personalizada. Consulte sempre seu médico antes de fazer alterações significativas na alimentação.*

---

IMPORTANTE:
- Retorne APENAS Markdown puro
- NÃO use tags XML ou blocos de código
- NÃO adicione explicações fora do documento
"""
