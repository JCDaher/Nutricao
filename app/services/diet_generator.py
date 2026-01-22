"""
Gerador de dieta formatada usando Claude
Objetivo: Usar mínimo de tokens (~1.000 entrada, ~3.000 saída)
Python calcula TUDO → Claude apenas formata em Markdown
"""
import os
from anthropic import Anthropic

from app.models import DietPlan
from app.data.substituicoes import formatar_todas_tabelas_markdown


class DietGenerator:
    """
    Gera dieta formatada usando Claude com prompt MÍNIMO
    """

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-5-20250929"

    def generate(self, diet_plan: DietPlan) -> str:
        """
        Envia plano estruturado para Claude formatar

        Args:
            diet_plan: Objeto completo com todos os cálculos e refeições

        Returns:
            String Markdown formatada para download
        """
        # Monta prompt MÍNIMO
        prompt = self._build_minimal_prompt(diet_plan)

        # Chama API
        message = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return message.content[0].text

    def _build_minimal_prompt(self, plan: DietPlan) -> str:
        """
        Constrói prompt mínimo com dados estruturados

        OBJETIVO: Usar ~1.000 tokens no máximo
        """
        # Converter objetos Pydantic para dicts
        paciente = plan.paciente.model_dump()
        calculos = plan.calculos.model_dump()
        refeicoes_formatadas = self._format_meals_for_prompt(plan.refeicoes)

        # Obter tabelas de substituição pré-formatadas
        tabelas_substituicao = formatar_todas_tabelas_markdown()

        # Determinar classificação do IMC
        imc = calculos['imc']
        if imc < 18.5:
            classificacao_imc = "Abaixo do peso"
        elif imc < 25:
            classificacao_imc = "Peso normal"
        elif imc < 30:
            classificacao_imc = "Sobrepeso"
        elif imc < 35:
            classificacao_imc = "Obesidade grau I"
        elif imc < 40:
            classificacao_imc = "Obesidade grau II"
        else:
            classificacao_imc = "Obesidade grau III"

        # Info glicêmica
        info_glicemica = ""
        if paciente.get('hba1c'):
            info_glicemica = f"HbA1c: {paciente['hba1c']}%"
        elif paciente.get('glicemia'):
            info_glicemica = f"Glicemia de jejum: {paciente['glicemia']} mg/dL"

        # Tratamento formal
        tratamento = "Sr." if paciente['sexo'] == 'M' else "Sra."

        prompt = f"""Você é assistente do Dr. Jorge Cecílio Daher Jr (CRMGO 6108 RQE5769, 5772).

Formate este plano alimentar em Markdown profissional. Use tratamento formal "{tratamento} {paciente['nome'].split()[0]}".

# PLANO ALIMENTAR PERSONALIZADO

## APRESENTAÇÃO DO PLANO
[Escreva 2-3 parágrafos PERSONALIZADOS apresentando o plano para o(a) {tratamento} {paciente['nome']}, mencionando:
- Importância do controle glicêmico para diabetes
- Benefícios da alimentação equilibrada para saúde intestinal
- Como os alimentos brasileiros escolhidos ajudam no controle metabólico
Use tom educativo, humano e profissional]

## INFORMAÇÕES DO PACIENTE
- **Nome:** {paciente['nome']}
- **Idade:** {paciente['idade']} anos
- **Sexo:** {"Masculino" if paciente['sexo'] == 'M' else "Feminino"}
- **Peso atual:** {paciente['peso']:.1f} kg
- **Altura:** {paciente['altura']:.0f} cm
- **IMC:** {calculos['imc']:.1f} kg/m² ({classificacao_imc})
{f"- **{info_glicemica}**" if info_glicemica else ""}

## NECESSIDADES CALÓRICAS CALCULADAS
- **Taxa Metabólica Basal (TMB):** {calculos['tmb']:.0f} kcal/dia
- **Necessidade Calórica Total:** {calculos['necessidade_calorica']:.0f} kcal/dia
- **Meta Calórica (para controle glicêmico):** {calculos['meta_calorica']:.0f} kcal/dia

### Distribuição de Macronutrientes
| Macronutriente | Gramas/dia | % do VET |
|----------------|------------|----------|
| Carboidratos | {calculos['macros']['carb_g']:.0f}g | {calculos['macros']['carb_percent']}% |
| Proteínas | {calculos['macros']['prot_g']:.0f}g | {calculos['macros']['prot_percent']}% |
| Gorduras | {calculos['macros']['gord_g']:.0f}g | {calculos['macros']['gord_percent']}% |

## PLANO DE REFEIÇÕES DIÁRIAS

{refeicoes_formatadas}

{tabelas_substituicao}

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
- Beba **{(paciente['peso'] * 35 / 1000):.1f} litros de água por dia** (35ml/kg)
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
        return prompt

    def _format_meals_for_prompt(self, refeicoes: list) -> str:
        """
        Formata refeições estruturadas para o prompt
        """
        output = ""

        for refeicao in refeicoes:
            # Calcular total real da refeição
            total_kcal = sum(a.kcal for a in refeicao.alimentos)
            total_carb = sum(a.carb for a in refeicao.alimentos)
            total_prot = sum(a.prot for a in refeicao.alimentos)
            total_gord = sum(a.gord for a in refeicao.alimentos)

            output += f"### {refeicao.nome} ({refeicao.horario})\n"
            output += f"**Meta:** ~{refeicao.calorias_alvo:.0f} kcal\n\n"
            output += "| Alimento | Porção | Kcal | Carb | Prot | Gord |\n"
            output += "|----------|--------|------|------|------|------|\n"

            for alimento in refeicao.alimentos:
                output += f"| {alimento.nome} | {alimento.porcao} | {alimento.kcal:.0f} | {alimento.carb:.1f}g | {alimento.prot:.1f}g | {alimento.gord:.1f}g |\n"

            output += f"| **TOTAL** | | **{total_kcal:.0f}** | **{total_carb:.1f}g** | **{total_prot:.1f}g** | **{total_gord:.1f}g** |\n\n"

        return output


def generate_diet_offline(diet_plan: DietPlan) -> str:
    """
    Gera dieta formatada sem usar a API Claude (modo offline/fallback)
    Útil para testes ou quando a API não está disponível

    Args:
        diet_plan: Objeto completo com todos os cálculos e refeições

    Returns:
        String Markdown formatada
    """
    paciente = diet_plan.paciente
    calculos = diet_plan.calculos
    refeicoes = diet_plan.refeicoes

    # Classificação do IMC
    imc = calculos.imc
    if imc < 18.5:
        classificacao_imc = "Abaixo do peso"
    elif imc < 25:
        classificacao_imc = "Peso normal"
    elif imc < 30:
        classificacao_imc = "Sobrepeso"
    elif imc < 35:
        classificacao_imc = "Obesidade grau I"
    elif imc < 40:
        classificacao_imc = "Obesidade grau II"
    else:
        classificacao_imc = "Obesidade grau III"

    tratamento = "Sr." if paciente.sexo == 'M' else "Sra."
    primeiro_nome = paciente.nome.split()[0]

    # Info glicêmica
    info_glicemica = ""
    if paciente.hba1c:
        info_glicemica = f"- **HbA1c:** {paciente.hba1c}%\n"
    elif paciente.glicemia:
        info_glicemica = f"- **Glicemia de jejum:** {paciente.glicemia} mg/dL\n"

    # Formatar refeições
    refeicoes_md = ""
    for refeicao in refeicoes:
        total_kcal = sum(a.kcal for a in refeicao.alimentos)
        total_carb = sum(a.carb for a in refeicao.alimentos)
        total_prot = sum(a.prot for a in refeicao.alimentos)
        total_gord = sum(a.gord for a in refeicao.alimentos)

        refeicoes_md += f"### {refeicao.nome} ({refeicao.horario})\n"
        refeicoes_md += f"**Meta:** ~{refeicao.calorias_alvo:.0f} kcal\n\n"
        refeicoes_md += "| Alimento | Porção | Kcal | Carb | Prot | Gord |\n"
        refeicoes_md += "|----------|--------|------|------|------|------|\n"

        for alimento in refeicao.alimentos:
            refeicoes_md += f"| {alimento.nome} | {alimento.porcao} | {alimento.kcal:.0f} | {alimento.carb:.1f}g | {alimento.prot:.1f}g | {alimento.gord:.1f}g |\n"

        refeicoes_md += f"| **TOTAL** | | **{total_kcal:.0f}** | **{total_carb:.1f}g** | **{total_prot:.1f}g** | **{total_gord:.1f}g** |\n\n"

    # Obter tabelas de substituição
    tabelas = formatar_todas_tabelas_markdown()

    markdown = f"""# PLANO ALIMENTAR PERSONALIZADO

## APRESENTAÇÃO DO PLANO

{tratamento} {primeiro_nome}, este plano alimentar foi desenvolvido especialmente para você, considerando suas necessidades nutricionais e o controle adequado do diabetes. A alimentação equilibrada é fundamental para manter os níveis de glicose estáveis e prevenir complicações a longo prazo.

Os alimentos selecionados são típicos da culinária brasileira, tornando mais fácil seguir o plano no dia a dia. Priorizamos alimentos com baixo índice glicêmico, ricos em fibras e com boa qualidade nutricional, que ajudam tanto no controle metabólico quanto na saúde intestinal.

Lembre-se: a consistência é mais importante que a perfeição. Siga o plano da melhor forma possível e, aos poucos, os bons hábitos se tornarão parte natural da sua rotina.

## INFORMAÇÕES DO PACIENTE

- **Nome:** {paciente.nome}
- **Idade:** {paciente.idade} anos
- **Sexo:** {"Masculino" if paciente.sexo == 'M' else "Feminino"}
- **Peso atual:** {paciente.peso:.1f} kg
- **Altura:** {paciente.altura:.0f} cm
- **IMC:** {calculos.imc:.1f} kg/m² ({classificacao_imc})
{info_glicemica}

## NECESSIDADES CALÓRICAS CALCULADAS

- **Taxa Metabólica Basal (TMB):** {calculos.tmb:.0f} kcal/dia
- **Necessidade Calórica Total:** {calculos.necessidade_calorica:.0f} kcal/dia
- **Meta Calórica (para controle glicêmico):** {calculos.meta_calorica:.0f} kcal/dia

### Distribuição de Macronutrientes

| Macronutriente | Gramas/dia | % do VET |
|----------------|------------|----------|
| Carboidratos | {calculos.macros['carb_g']:.0f}g | {calculos.macros['carb_percent']}% |
| Proteínas | {calculos.macros['prot_g']:.0f}g | {calculos.macros['prot_percent']}% |
| Gorduras | {calculos.macros['gord_g']:.0f}g | {calculos.macros['gord_percent']}% |

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

### Prebióticos
- Alho, cebola, alho-poró
- Banana verde
- Aveia
- Linhaça e chia

### Hidratação
- Beba **{(paciente.peso * 35 / 1000):.1f} litros de água por dia** (35ml/kg)

## SUPLEMENTOS E ALIMENTOS FUNCIONAIS RECOMENDADOS

| Suplemento | Benefício | Como usar |
|------------|-----------|-----------|
| Semente de chia | Fibras, ômega-3, saciedade | 1 colher de sopa/dia |
| Semente de linhaça | Fibras, lignanas, ômega-3 | 1 colher de sopa/dia (triturada) |
| Castanha do Pará | Selênio, gorduras boas | 2 unidades/dia |
| Canela | Auxilia controle glicêmico | 1/2 colher de chá/dia |

## DICAS IMPORTANTES

1. **Mastigue bem os alimentos** - a digestão começa na boca
2. **Faça refeições em horários regulares** - evite pular refeições
3. **Evite líquidos durante as refeições** - beba 30 min antes ou depois
4. **Não deite logo após comer** - espere pelo menos 2 horas
5. **Pratique atividade física regular** - caminhadas de 30 min ajudam
6. **Monitore sua glicemia** - especialmente em jejum e pós-prandial

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
"""

    return markdown
