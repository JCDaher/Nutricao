"""
Tabelas de substituição para variedade na dieta
Permite trocar alimentos mantendo equivalência nutricional aproximada
"""

# Tabelas de substituições organizadas por grupo alimentar
SUBSTITUICOES = {
    'cereais_paes': {
        'titulo': 'Cereais e Pães',
        'descricao': 'Porções equivalentes em carboidratos (~15g de carboidratos)',
        'itens': [
            {'alimento': 'Arroz branco cozido', 'porcao': '2 colheres de sopa', 'gramas': 60},
            {'alimento': 'Arroz integral cozido', 'porcao': '2 colheres de sopa', 'gramas': 60},
            {'alimento': 'Arroz parboilizado', 'porcao': '2 colheres de sopa', 'gramas': 60},
            {'alimento': 'Arroz com pequi', 'porcao': '2 colheres de sopa', 'gramas': 60},
            {'alimento': 'Pão francês', 'porcao': '1/2 unidade', 'gramas': 25},
            {'alimento': 'Pão integral', 'porcao': '1 fatia', 'gramas': 30},
            {'alimento': 'Pão de forma integral', 'porcao': '1 fatia', 'gramas': 25},
            {'alimento': 'Pão sírio integral', 'porcao': '1/2 unidade', 'gramas': 30},
            {'alimento': 'Pão de centeio', 'porcao': '1 fatia', 'gramas': 30},
            {'alimento': 'Tapioca', 'porcao': '2 colheres de sopa', 'gramas': 30},
            {'alimento': 'Cuscuz', 'porcao': '2 colheres de sopa', 'gramas': 45},
            {'alimento': 'Aveia em flocos', 'porcao': '2 colheres de sopa', 'gramas': 25},
            {'alimento': 'Granola sem açúcar', 'porcao': '2 colheres de sopa', 'gramas': 25},
            {'alimento': 'Batata doce cozida', 'porcao': '1/2 unidade média', 'gramas': 80},
            {'alimento': 'Batata inglesa cozida', 'porcao': '1 unidade pequena', 'gramas': 100},
            {'alimento': 'Mandioca/Aipim cozida', 'porcao': '1 pedaço médio', 'gramas': 50},
            {'alimento': 'Inhame cozido', 'porcao': '1 pedaço médio', 'gramas': 65},
            {'alimento': 'Cará cozido', 'porcao': '1 pedaço médio', 'gramas': 70},
            {'alimento': 'Milho verde cozido', 'porcao': '1/2 espiga', 'gramas': 50},
            {'alimento': 'Pipoca (sem óleo)', 'porcao': '2 xícaras', 'gramas': 20},
            {'alimento': 'Macarrão cozido', 'porcao': '2 colheres de sopa', 'gramas': 75},
            {'alimento': 'Macarrão integral cozido', 'porcao': '2 colheres de sopa', 'gramas': 70},
            {'alimento': 'Torrada integral', 'porcao': '2 unidades', 'gramas': 15},
            {'alimento': 'Biscoito integral', 'porcao': '3 unidades', 'gramas': 20},
        ]
    },

    'proteinas_carnes': {
        'titulo': 'Carnes e Proteínas',
        'descricao': 'Porções equivalentes em proteínas (~20-25g de proteína)',
        'itens': [
            {'alimento': 'Frango peito grelhado', 'porcao': '1 filé médio', 'gramas': 100},
            {'alimento': 'Frango coxa/sobrecoxa', 'porcao': '1 unidade', 'gramas': 80},
            {'alimento': 'Carne bovina magra grelhada', 'porcao': '1 bife médio', 'gramas': 100},
            {'alimento': 'Carne bovina (patinho)', 'porcao': '1 bife médio', 'gramas': 100},
            {'alimento': 'Carne bovina (acém) cozida', 'porcao': '2 pedaços', 'gramas': 100},
            {'alimento': 'Carne bovina (coxão mole)', 'porcao': '1 bife médio', 'gramas': 100},
            {'alimento': 'Carne suína (lombo)', 'porcao': '1 fatia média', 'gramas': 80},
            {'alimento': 'Tilápia grelhada', 'porcao': '1 filé médio', 'gramas': 100},
            {'alimento': 'Salmão grelhado', 'porcao': '1 filé pequeno', 'gramas': 80},
            {'alimento': 'Sardinha assada', 'porcao': '2 unidades', 'gramas': 80},
            {'alimento': 'Atum em conserva', 'porcao': '4 colheres de sopa', 'gramas': 80},
            {'alimento': 'Peixe pintado', 'porcao': '1 filé médio', 'gramas': 100},
            {'alimento': 'Merluza', 'porcao': '1 filé médio', 'gramas': 100},
            {'alimento': 'Camarão cozido', 'porcao': '10 unidades médias', 'gramas': 100},
            {'alimento': 'Ovo cozido/pochê', 'porcao': '2 unidades', 'gramas': 100},
            {'alimento': 'Ovo mexido', 'porcao': '2 unidades', 'gramas': 100},
            {'alimento': 'Queijo branco/minas', 'porcao': '2 fatias médias', 'gramas': 60},
            {'alimento': 'Queijo cottage', 'porcao': '4 colheres de sopa', 'gramas': 100},
            {'alimento': 'Ricota', 'porcao': '4 colheres de sopa', 'gramas': 100},
            {'alimento': 'Tofu', 'porcao': '4 fatias médias', 'gramas': 120},
        ]
    },

    'frutas': {
        'titulo': 'Frutas',
        'descricao': 'Porções equivalentes (~15g de carboidratos)',
        'itens': [
            {'alimento': 'Abacaxi', 'porcao': '1 fatia média', 'gramas': 100},
            {'alimento': 'Abacate', 'porcao': '2 colheres de sopa', 'gramas': 50},
            {'alimento': 'Acerola', 'porcao': '15 unidades', 'gramas': 150},
            {'alimento': 'Ameixa fresca', 'porcao': '3 unidades médias', 'gramas': 100},
            {'alimento': 'Amora', 'porcao': '1 xícara', 'gramas': 100},
            {'alimento': 'Banana prata', 'porcao': '1/2 unidade', 'gramas': 35},
            {'alimento': 'Banana maçã', 'porcao': '1/2 unidade', 'gramas': 40},
            {'alimento': 'Caju', 'porcao': '2 unidades', 'gramas': 100},
            {'alimento': 'Caqui', 'porcao': '1/2 unidade', 'gramas': 60},
            {'alimento': 'Carambola', 'porcao': '2 unidades', 'gramas': 200},
            {'alimento': 'Framboesa', 'porcao': '1 xícara', 'gramas': 100},
            {'alimento': 'Goiaba', 'porcao': '1 unidade média', 'gramas': 100},
            {'alimento': 'Jabuticaba', 'porcao': '20 unidades', 'gramas': 100},
            {'alimento': 'Jaca', 'porcao': '4 bagos', 'gramas': 60},
            {'alimento': 'Kiwi', 'porcao': '1 unidade', 'gramas': 75},
            {'alimento': 'Laranja', 'porcao': '1 unidade média', 'gramas': 130},
            {'alimento': 'Limão', 'porcao': '4 unidades', 'gramas': 200},
            {'alimento': 'Maçã', 'porcao': '1 unidade pequena', 'gramas': 100},
            {'alimento': 'Mamão papaia', 'porcao': '1/2 unidade', 'gramas': 150},
            {'alimento': 'Mamão formosa', 'porcao': '1 fatia média', 'gramas': 150},
            {'alimento': 'Manga', 'porcao': '1/2 unidade', 'gramas': 100},
            {'alimento': 'Maracujá (polpa)', 'porcao': '1/2 xícara', 'gramas': 100},
            {'alimento': 'Melancia', 'porcao': '1 fatia fina', 'gramas': 200},
            {'alimento': 'Melão', 'porcao': '1 fatia média', 'gramas': 200},
            {'alimento': 'Morango', 'porcao': '10 unidades médias', 'gramas': 150},
            {'alimento': 'Pera', 'porcao': '1 unidade pequena', 'gramas': 100},
            {'alimento': 'Pêssego', 'porcao': '2 unidades médias', 'gramas': 150},
            {'alimento': 'Tangerina/Mexerica', 'porcao': '1 unidade', 'gramas': 120},
            {'alimento': 'Uva', 'porcao': '10 unidades', 'gramas': 60},
        ]
    },

    'verduras_legumes': {
        'titulo': 'Verduras e Legumes',
        'descricao': 'Verduras folhosas são livres. Legumes: ~1/2 xícara cozido',
        'itens': [
            {'alimento': 'Agrião', 'porcao': 'À vontade', 'gramas': 0},
            {'alimento': 'Alface (todos os tipos)', 'porcao': 'À vontade', 'gramas': 0},
            {'alimento': 'Almeirão', 'porcao': 'À vontade', 'gramas': 0},
            {'alimento': 'Chicória', 'porcao': 'À vontade', 'gramas': 0},
            {'alimento': 'Couve manteiga', 'porcao': 'À vontade', 'gramas': 0},
            {'alimento': 'Espinafre', 'porcao': 'À vontade', 'gramas': 0},
            {'alimento': 'Repolho', 'porcao': 'À vontade', 'gramas': 0},
            {'alimento': 'Rúcula', 'porcao': 'À vontade', 'gramas': 0},
            {'alimento': 'Abobrinha cozida', 'porcao': '3 colheres de sopa', 'gramas': 60},
            {'alimento': 'Abóbora cozida', 'porcao': '2 colheres de sopa', 'gramas': 50},
            {'alimento': 'Berinjela', 'porcao': '3 colheres de sopa', 'gramas': 60},
            {'alimento': 'Beterraba cozida', 'porcao': '2 fatias médias', 'gramas': 50},
            {'alimento': 'Brócolis cozido', 'porcao': '3 colheres de sopa', 'gramas': 60},
            {'alimento': 'Cenoura crua', 'porcao': '1 unidade média', 'gramas': 80},
            {'alimento': 'Cenoura cozida', 'porcao': '2 colheres de sopa', 'gramas': 50},
            {'alimento': 'Chuchu cozido', 'porcao': '2 colheres de sopa', 'gramas': 60},
            {'alimento': 'Couve-flor cozida', 'porcao': '3 colheres de sopa', 'gramas': 60},
            {'alimento': 'Jiló', 'porcao': '2 colheres de sopa', 'gramas': 50},
            {'alimento': 'Maxixe', 'porcao': '2 colheres de sopa', 'gramas': 50},
            {'alimento': 'Pepino', 'porcao': '4 fatias', 'gramas': 60},
            {'alimento': 'Pimentão', 'porcao': '4 fatias', 'gramas': 50},
            {'alimento': 'Quiabo cozido', 'porcao': '2 colheres de sopa', 'gramas': 60},
            {'alimento': 'Tomate', 'porcao': '4 fatias', 'gramas': 60},
            {'alimento': 'Vagem cozida', 'porcao': '2 colheres de sopa', 'gramas': 50},
        ]
    },

    'oleos_gorduras': {
        'titulo': 'Óleos e Gorduras Saudáveis',
        'descricao': 'Porções equivalentes (~5g de gordura)',
        'itens': [
            {'alimento': 'Azeite de oliva extra virgem', 'porcao': '1 colher de chá', 'gramas': 5},
            {'alimento': 'Óleo de coco', 'porcao': '1 colher de chá', 'gramas': 5},
            {'alimento': 'Óleo de linhaça', 'porcao': '1 colher de chá', 'gramas': 5},
            {'alimento': 'Manteiga', 'porcao': '1/2 colher de chá', 'gramas': 3},
            {'alimento': 'Manteiga ghee', 'porcao': '1/2 colher de chá', 'gramas': 3},
            {'alimento': 'Creme de leite', 'porcao': '1 colher de sopa', 'gramas': 15},
            {'alimento': 'Castanha do Pará', 'porcao': '1 unidade', 'gramas': 5},
            {'alimento': 'Castanha de caju', 'porcao': '5 unidades', 'gramas': 10},
            {'alimento': 'Amêndoas', 'porcao': '6 unidades', 'gramas': 10},
            {'alimento': 'Nozes', 'porcao': '1 unidade', 'gramas': 5},
            {'alimento': 'Amendoim', 'porcao': '1 colher de sopa', 'gramas': 15},
            {'alimento': 'Semente de linhaça', 'porcao': '1 colher de sopa', 'gramas': 10},
            {'alimento': 'Semente de chia', 'porcao': '1 colher de sopa', 'gramas': 10},
            {'alimento': 'Semente de girassol', 'porcao': '1 colher de sopa', 'gramas': 10},
            {'alimento': 'Abacate', 'porcao': '2 colheres de sopa', 'gramas': 30},
            {'alimento': 'Azeitona preta', 'porcao': '5 unidades', 'gramas': 15},
            {'alimento': 'Azeitona verde', 'porcao': '5 unidades', 'gramas': 15},
        ]
    },

    'leguminosas': {
        'titulo': 'Leguminosas',
        'descricao': 'Porções equivalentes (~7g de proteína e ~15g de carboidrato)',
        'itens': [
            {'alimento': 'Feijão carioca cozido', 'porcao': '1 concha média', 'gramas': 80},
            {'alimento': 'Feijão preto cozido', 'porcao': '1 concha média', 'gramas': 80},
            {'alimento': 'Feijão branco cozido', 'porcao': '1 concha média', 'gramas': 80},
            {'alimento': 'Feijão fradinho cozido', 'porcao': '1 concha média', 'gramas': 80},
            {'alimento': 'Lentilha cozida', 'porcao': '3 colheres de sopa', 'gramas': 75},
            {'alimento': 'Grão de bico cozido', 'porcao': '3 colheres de sopa', 'gramas': 60},
            {'alimento': 'Ervilha cozida', 'porcao': '3 colheres de sopa', 'gramas': 75},
            {'alimento': 'Soja cozida', 'porcao': '3 colheres de sopa', 'gramas': 60},
        ]
    },

    'lacteos': {
        'titulo': 'Laticínios',
        'descricao': 'Porções equivalentes (~8g de proteína)',
        'itens': [
            {'alimento': 'Leite desnatado', 'porcao': '1 copo (200ml)', 'gramas': 200},
            {'alimento': 'Leite semidesnatado', 'porcao': '1 copo (200ml)', 'gramas': 200},
            {'alimento': 'Iogurte natural desnatado', 'porcao': '1 pote (170g)', 'gramas': 170},
            {'alimento': 'Iogurte grego natural', 'porcao': '1 pote (100g)', 'gramas': 100},
            {'alimento': 'Coalhada', 'porcao': '1 pote (170g)', 'gramas': 170},
            {'alimento': 'Kefir', 'porcao': '1 copo (200ml)', 'gramas': 200},
            {'alimento': 'Queijo minas frescal', 'porcao': '2 fatias finas', 'gramas': 50},
            {'alimento': 'Queijo cottage', 'porcao': '3 colheres de sopa', 'gramas': 75},
            {'alimento': 'Ricota', 'porcao': '3 colheres de sopa', 'gramas': 75},
            {'alimento': 'Requeijão light', 'porcao': '2 colheres de sopa', 'gramas': 40},
        ]
    }
}


def get_substituicoes_grupo(grupo: str) -> dict:
    """
    Retorna tabela de substituições para um grupo específico

    Args:
        grupo: Nome do grupo (cereais_paes, proteinas_carnes, frutas, etc.)

    Returns:
        Dict com título, descrição e lista de itens
    """
    return SUBSTITUICOES.get(grupo, {})


def get_todas_substituicoes() -> dict:
    """
    Retorna todas as tabelas de substituições

    Returns:
        Dict completo de substituições
    """
    return SUBSTITUICOES


def formatar_tabela_markdown(grupo: str) -> str:
    """
    Formata a tabela de substituições de um grupo em Markdown

    Args:
        grupo: Nome do grupo

    Returns:
        String formatada em Markdown
    """
    dados = SUBSTITUICOES.get(grupo)
    if not dados:
        return ""

    output = f"### {dados['titulo']}\n"
    output += f"*{dados['descricao']}*\n\n"
    output += "| Alimento | Porção |\n"
    output += "|----------|--------|\n"

    for item in dados['itens']:
        porcao = item['porcao']
        if item['gramas'] > 0:
            porcao += f" ({item['gramas']}g)"
        output += f"| {item['alimento']} | {porcao} |\n"

    output += "\n"
    return output


def formatar_todas_tabelas_markdown() -> str:
    """
    Formata todas as tabelas de substituições em Markdown

    Returns:
        String com todas as tabelas formatadas
    """
    output = "## TABELAS DE SUBSTITUIÇÕES ALIMENTARES\n\n"
    output += "Use estas tabelas para variar sua alimentação mantendo o equilíbrio nutricional.\n\n"

    for grupo in SUBSTITUICOES.keys():
        output += formatar_tabela_markdown(grupo)

    return output
