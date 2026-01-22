"""
Base de dados simplificada de alimentos brasileiros
Valores nutricionais por 100g (baseado em TACO - Tabela Brasileira de Composição de Alimentos)

Cada alimento tem:
- nome: str
- grupo: str (cereal, proteina, fruta, verdura, legume, gordura, lacteo, leguminosa)
- kcal: float
- carb_g: float
- prot_g: float
- gord_g: float
- fibra_g: float
- porcao_usual: str (medida caseira)
- gramas_porcao: float
- ig: int (índice glicêmico aproximado: baixo <55, médio 55-70, alto >70)
"""

ALIMENTOS = {
    # ==================== CEREAIS E PÃES ====================
    'arroz_branco_cozido': {
        'nome': 'Arroz branco cozido',
        'grupo': 'cereal',
        'kcal': 128,
        'carb_g': 28.1,
        'prot_g': 2.5,
        'gord_g': 0.2,
        'fibra_g': 1.6,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 90,
        'ig': 73
    },
    'arroz_integral_cozido': {
        'nome': 'Arroz integral cozido',
        'grupo': 'cereal',
        'kcal': 124,
        'carb_g': 25.8,
        'prot_g': 2.6,
        'gord_g': 1.0,
        'fibra_g': 2.7,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 90,
        'ig': 50
    },
    'arroz_parboilizado_cozido': {
        'nome': 'Arroz parboilizado cozido',
        'grupo': 'cereal',
        'kcal': 123,
        'carb_g': 27.1,
        'prot_g': 2.5,
        'gord_g': 0.3,
        'fibra_g': 1.1,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 90,
        'ig': 47
    },
    'pao_frances': {
        'nome': 'Pão francês',
        'grupo': 'cereal',
        'kcal': 300,
        'carb_g': 58.6,
        'prot_g': 9.4,
        'gord_g': 3.1,
        'fibra_g': 2.3,
        'porcao_usual': '1/2 unidade',
        'gramas_porcao': 25,
        'ig': 95
    },
    'pao_integral': {
        'nome': 'Pão integral',
        'grupo': 'cereal',
        'kcal': 253,
        'carb_g': 49.9,
        'prot_g': 9.4,
        'gord_g': 3.4,
        'fibra_g': 6.9,
        'porcao_usual': '1 fatia',
        'gramas_porcao': 30,
        'ig': 53
    },
    'pao_forma_integral': {
        'nome': 'Pão de forma integral',
        'grupo': 'cereal',
        'kcal': 246,
        'carb_g': 41.3,
        'prot_g': 9.3,
        'gord_g': 5.0,
        'fibra_g': 5.8,
        'porcao_usual': '2 fatias',
        'gramas_porcao': 50,
        'ig': 53
    },
    'tapioca': {
        'nome': 'Tapioca (goma hidratada)',
        'grupo': 'cereal',
        'kcal': 68,
        'carb_g': 17.1,
        'prot_g': 0.0,
        'gord_g': 0.0,
        'fibra_g': 0.0,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 30,
        'ig': 70
    },
    'aveia_flocos': {
        'nome': 'Aveia em flocos',
        'grupo': 'cereal',
        'kcal': 394,
        'carb_g': 66.6,
        'prot_g': 13.9,
        'gord_g': 8.5,
        'fibra_g': 9.1,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 30,
        'ig': 55
    },
    'macarrao_cozido': {
        'nome': 'Macarrão cozido',
        'grupo': 'cereal',
        'kcal': 102,
        'carb_g': 19.9,
        'prot_g': 3.4,
        'gord_g': 1.2,
        'fibra_g': 1.4,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 90,
        'ig': 50
    },
    'macarrao_integral_cozido': {
        'nome': 'Macarrão integral cozido',
        'grupo': 'cereal',
        'kcal': 124,
        'carb_g': 23.5,
        'prot_g': 5.0,
        'gord_g': 1.3,
        'fibra_g': 4.5,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 90,
        'ig': 40
    },
    'batata_doce_cozida': {
        'nome': 'Batata doce cozida',
        'grupo': 'cereal',
        'kcal': 77,
        'carb_g': 18.4,
        'prot_g': 0.6,
        'gord_g': 0.1,
        'fibra_g': 2.2,
        'porcao_usual': '1 unidade média',
        'gramas_porcao': 100,
        'ig': 44
    },
    'mandioca_cozida': {
        'nome': 'Mandioca/Aipim cozida',
        'grupo': 'cereal',
        'kcal': 125,
        'carb_g': 30.1,
        'prot_g': 0.6,
        'gord_g': 0.3,
        'fibra_g': 1.6,
        'porcao_usual': '2 pedaços médios',
        'gramas_porcao': 80,
        'ig': 46
    },
    'inhame_cozido': {
        'nome': 'Inhame cozido',
        'grupo': 'cereal',
        'kcal': 97,
        'carb_g': 23.2,
        'prot_g': 2.0,
        'gord_g': 0.1,
        'fibra_g': 1.7,
        'porcao_usual': '1 pedaço médio',
        'gramas_porcao': 80,
        'ig': 37
    },
    'milho_cozido': {
        'nome': 'Milho verde cozido',
        'grupo': 'cereal',
        'kcal': 138,
        'carb_g': 28.6,
        'prot_g': 6.6,
        'gord_g': 0.8,
        'fibra_g': 3.9,
        'porcao_usual': '1 espiga média',
        'gramas_porcao': 100,
        'ig': 52
    },

    # ==================== PROTEÍNAS (CARNES E OVOS) ====================
    'frango_peito_grelhado': {
        'nome': 'Frango peito grelhado',
        'grupo': 'proteina',
        'kcal': 159,
        'carb_g': 0.0,
        'prot_g': 32.0,
        'gord_g': 3.6,
        'fibra_g': 0.0,
        'porcao_usual': '1 filé médio',
        'gramas_porcao': 100,
        'ig': 0
    },
    'frango_coxa_assada': {
        'nome': 'Frango coxa/sobrecoxa assada',
        'grupo': 'proteina',
        'kcal': 215,
        'carb_g': 0.0,
        'prot_g': 26.8,
        'gord_g': 11.8,
        'fibra_g': 0.0,
        'porcao_usual': '1 unidade',
        'gramas_porcao': 80,
        'ig': 0
    },
    'carne_bovina_patinho': {
        'nome': 'Carne bovina (patinho) grelhada',
        'grupo': 'proteina',
        'kcal': 219,
        'carb_g': 0.0,
        'prot_g': 35.9,
        'gord_g': 7.3,
        'fibra_g': 0.0,
        'porcao_usual': '1 bife médio',
        'gramas_porcao': 100,
        'ig': 0
    },
    'carne_bovina_acem': {
        'nome': 'Carne bovina (acém) cozida',
        'grupo': 'proteina',
        'kcal': 215,
        'carb_g': 0.0,
        'prot_g': 26.7,
        'gord_g': 11.4,
        'fibra_g': 0.0,
        'porcao_usual': '2 pedaços médios',
        'gramas_porcao': 100,
        'ig': 0
    },
    'carne_suina_lombo': {
        'nome': 'Carne suína (lombo) assada',
        'grupo': 'proteina',
        'kcal': 210,
        'carb_g': 0.0,
        'prot_g': 32.0,
        'gord_g': 8.5,
        'fibra_g': 0.0,
        'porcao_usual': '1 fatia média',
        'gramas_porcao': 80,
        'ig': 0
    },
    'peixe_tilapia': {
        'nome': 'Tilápia grelhada',
        'grupo': 'proteina',
        'kcal': 128,
        'carb_g': 0.0,
        'prot_g': 26.2,
        'gord_g': 2.7,
        'fibra_g': 0.0,
        'porcao_usual': '1 filé médio',
        'gramas_porcao': 100,
        'ig': 0
    },
    'peixe_sardinha_assada': {
        'nome': 'Sardinha assada',
        'grupo': 'proteina',
        'kcal': 164,
        'carb_g': 0.0,
        'prot_g': 32.0,
        'gord_g': 5.0,
        'fibra_g': 0.0,
        'porcao_usual': '2 unidades',
        'gramas_porcao': 80,
        'ig': 0
    },
    'peixe_atum_lata': {
        'nome': 'Atum em conserva (água)',
        'grupo': 'proteina',
        'kcal': 116,
        'carb_g': 0.0,
        'prot_g': 26.2,
        'gord_g': 0.8,
        'fibra_g': 0.0,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 0
    },
    'ovo_cozido': {
        'nome': 'Ovo cozido',
        'grupo': 'proteina',
        'kcal': 146,
        'carb_g': 0.6,
        'prot_g': 13.3,
        'gord_g': 9.5,
        'fibra_g': 0.0,
        'porcao_usual': '1 unidade',
        'gramas_porcao': 50,
        'ig': 0
    },
    'ovo_mexido': {
        'nome': 'Ovo mexido',
        'grupo': 'proteina',
        'kcal': 170,
        'carb_g': 1.0,
        'prot_g': 12.0,
        'gord_g': 13.0,
        'fibra_g': 0.0,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 0
    },

    # ==================== LEGUMINOSAS ====================
    'feijao_carioca_cozido': {
        'nome': 'Feijão carioca cozido',
        'grupo': 'leguminosa',
        'kcal': 76,
        'carb_g': 13.6,
        'prot_g': 4.8,
        'gord_g': 0.5,
        'fibra_g': 8.5,
        'porcao_usual': '1 concha média',
        'gramas_porcao': 80,
        'ig': 42
    },
    'feijao_preto_cozido': {
        'nome': 'Feijão preto cozido',
        'grupo': 'leguminosa',
        'kcal': 77,
        'carb_g': 14.0,
        'prot_g': 4.5,
        'gord_g': 0.5,
        'fibra_g': 8.4,
        'porcao_usual': '1 concha média',
        'gramas_porcao': 80,
        'ig': 30
    },
    'lentilha_cozida': {
        'nome': 'Lentilha cozida',
        'grupo': 'leguminosa',
        'kcal': 93,
        'carb_g': 16.3,
        'prot_g': 6.3,
        'gord_g': 0.5,
        'fibra_g': 7.9,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 50,
        'ig': 26
    },
    'grao_de_bico_cozido': {
        'nome': 'Grão de bico cozido',
        'grupo': 'leguminosa',
        'kcal': 130,
        'carb_g': 18.6,
        'prot_g': 8.9,
        'gord_g': 2.6,
        'fibra_g': 9.9,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 50,
        'ig': 28
    },
    'ervilha_cozida': {
        'nome': 'Ervilha cozida',
        'grupo': 'leguminosa',
        'kcal': 63,
        'carb_g': 10.6,
        'prot_g': 5.0,
        'gord_g': 0.4,
        'fibra_g': 6.3,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 50,
        'ig': 48
    },

    # ==================== FRUTAS ====================
    'banana_prata': {
        'nome': 'Banana prata',
        'grupo': 'fruta',
        'kcal': 98,
        'carb_g': 26.0,
        'prot_g': 1.3,
        'gord_g': 0.1,
        'fibra_g': 2.0,
        'porcao_usual': '1 unidade média',
        'gramas_porcao': 65,
        'ig': 52
    },
    'maca': {
        'nome': 'Maçã',
        'grupo': 'fruta',
        'kcal': 63,
        'carb_g': 16.6,
        'prot_g': 0.2,
        'gord_g': 0.0,
        'fibra_g': 2.0,
        'porcao_usual': '1 unidade média',
        'gramas_porcao': 130,
        'ig': 38
    },
    'pera': {
        'nome': 'Pera',
        'grupo': 'fruta',
        'kcal': 53,
        'carb_g': 14.0,
        'prot_g': 0.6,
        'gord_g': 0.1,
        'fibra_g': 3.0,
        'porcao_usual': '1 unidade média',
        'gramas_porcao': 133,
        'ig': 38
    },
    'laranja': {
        'nome': 'Laranja',
        'grupo': 'fruta',
        'kcal': 46,
        'carb_g': 11.5,
        'prot_g': 0.8,
        'gord_g': 0.1,
        'fibra_g': 1.8,
        'porcao_usual': '1 unidade média',
        'gramas_porcao': 150,
        'ig': 43
    },
    'mamao_papaia': {
        'nome': 'Mamão papaia',
        'grupo': 'fruta',
        'kcal': 40,
        'carb_g': 10.4,
        'prot_g': 0.5,
        'gord_g': 0.1,
        'fibra_g': 1.0,
        'porcao_usual': '1/2 unidade',
        'gramas_porcao': 150,
        'ig': 59
    },
    'mamao_formosa': {
        'nome': 'Mamão formosa',
        'grupo': 'fruta',
        'kcal': 45,
        'carb_g': 11.6,
        'prot_g': 0.8,
        'gord_g': 0.1,
        'fibra_g': 1.8,
        'porcao_usual': '1 fatia média',
        'gramas_porcao': 150,
        'ig': 59
    },
    'melancia': {
        'nome': 'Melancia',
        'grupo': 'fruta',
        'kcal': 33,
        'carb_g': 8.1,
        'prot_g': 0.9,
        'gord_g': 0.0,
        'fibra_g': 0.1,
        'porcao_usual': '1 fatia média',
        'gramas_porcao': 200,
        'ig': 72
    },
    'melao': {
        'nome': 'Melão',
        'grupo': 'fruta',
        'kcal': 29,
        'carb_g': 7.5,
        'prot_g': 0.7,
        'gord_g': 0.0,
        'fibra_g': 0.3,
        'porcao_usual': '1 fatia média',
        'gramas_porcao': 150,
        'ig': 65
    },
    'abacaxi': {
        'nome': 'Abacaxi',
        'grupo': 'fruta',
        'kcal': 48,
        'carb_g': 12.3,
        'prot_g': 0.9,
        'gord_g': 0.1,
        'fibra_g': 1.0,
        'porcao_usual': '1 fatia média',
        'gramas_porcao': 100,
        'ig': 59
    },
    'manga': {
        'nome': 'Manga',
        'grupo': 'fruta',
        'kcal': 64,
        'carb_g': 16.7,
        'prot_g': 0.4,
        'gord_g': 0.3,
        'fibra_g': 1.6,
        'porcao_usual': '1/2 unidade média',
        'gramas_porcao': 100,
        'ig': 51
    },
    'morango': {
        'nome': 'Morango',
        'grupo': 'fruta',
        'kcal': 30,
        'carb_g': 6.8,
        'prot_g': 0.9,
        'gord_g': 0.3,
        'fibra_g': 1.7,
        'porcao_usual': '10 unidades médias',
        'gramas_porcao': 150,
        'ig': 40
    },
    'uva': {
        'nome': 'Uva',
        'grupo': 'fruta',
        'kcal': 53,
        'carb_g': 13.7,
        'prot_g': 0.7,
        'gord_g': 0.2,
        'fibra_g': 0.9,
        'porcao_usual': '1 cacho pequeno',
        'gramas_porcao': 100,
        'ig': 46
    },
    'goiaba': {
        'nome': 'Goiaba',
        'grupo': 'fruta',
        'kcal': 54,
        'carb_g': 13.0,
        'prot_g': 1.1,
        'gord_g': 0.4,
        'fibra_g': 6.2,
        'porcao_usual': '1 unidade média',
        'gramas_porcao': 100,
        'ig': 12
    },
    'kiwi': {
        'nome': 'Kiwi',
        'grupo': 'fruta',
        'kcal': 51,
        'carb_g': 11.5,
        'prot_g': 1.3,
        'gord_g': 0.6,
        'fibra_g': 2.7,
        'porcao_usual': '1 unidade média',
        'gramas_porcao': 75,
        'ig': 50
    },
    'abacate': {
        'nome': 'Abacate',
        'grupo': 'fruta',
        'kcal': 96,
        'carb_g': 6.0,
        'prot_g': 1.2,
        'gord_g': 8.4,
        'fibra_g': 6.3,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 50,
        'ig': 15
    },
    'acerola': {
        'nome': 'Acerola',
        'grupo': 'fruta',
        'kcal': 33,
        'carb_g': 8.0,
        'prot_g': 0.9,
        'gord_g': 0.2,
        'fibra_g': 1.5,
        'porcao_usual': '10 unidades',
        'gramas_porcao': 100,
        'ig': 20
    },

    # ==================== VERDURAS E FOLHAS ====================
    'alface': {
        'nome': 'Alface',
        'grupo': 'verdura',
        'kcal': 11,
        'carb_g': 1.7,
        'prot_g': 1.3,
        'gord_g': 0.2,
        'fibra_g': 1.8,
        'porcao_usual': 'À vontade',
        'gramas_porcao': 50,
        'ig': 15
    },
    'rucula': {
        'nome': 'Rúcula',
        'grupo': 'verdura',
        'kcal': 17,
        'carb_g': 2.2,
        'prot_g': 2.6,
        'gord_g': 0.3,
        'fibra_g': 1.6,
        'porcao_usual': 'À vontade',
        'gramas_porcao': 30,
        'ig': 15
    },
    'agriao': {
        'nome': 'Agrião',
        'grupo': 'verdura',
        'kcal': 17,
        'carb_g': 2.3,
        'prot_g': 2.7,
        'gord_g': 0.2,
        'fibra_g': 2.1,
        'porcao_usual': 'À vontade',
        'gramas_porcao': 30,
        'ig': 15
    },
    'espinafre': {
        'nome': 'Espinafre',
        'grupo': 'verdura',
        'kcal': 17,
        'carb_g': 2.6,
        'prot_g': 2.0,
        'gord_g': 0.2,
        'fibra_g': 2.1,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 15
    },
    'couve_manteiga': {
        'nome': 'Couve manteiga',
        'grupo': 'verdura',
        'kcal': 27,
        'carb_g': 4.3,
        'prot_g': 2.9,
        'gord_g': 0.5,
        'fibra_g': 3.1,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 15
    },
    'repolho': {
        'nome': 'Repolho',
        'grupo': 'verdura',
        'kcal': 17,
        'carb_g': 3.7,
        'prot_g': 0.9,
        'gord_g': 0.1,
        'fibra_g': 1.9,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 10
    },

    # ==================== LEGUMES ====================
    'tomate': {
        'nome': 'Tomate',
        'grupo': 'legume',
        'kcal': 15,
        'carb_g': 3.1,
        'prot_g': 1.1,
        'gord_g': 0.2,
        'fibra_g': 1.2,
        'porcao_usual': '4 fatias',
        'gramas_porcao': 60,
        'ig': 15
    },
    'pepino': {
        'nome': 'Pepino',
        'grupo': 'legume',
        'kcal': 10,
        'carb_g': 2.0,
        'prot_g': 0.9,
        'gord_g': 0.0,
        'fibra_g': 1.1,
        'porcao_usual': '4 fatias',
        'gramas_porcao': 60,
        'ig': 15
    },
    'cenoura_crua': {
        'nome': 'Cenoura crua',
        'grupo': 'legume',
        'kcal': 34,
        'carb_g': 7.7,
        'prot_g': 1.3,
        'gord_g': 0.2,
        'fibra_g': 3.2,
        'porcao_usual': '1 unidade média',
        'gramas_porcao': 80,
        'ig': 16
    },
    'cenoura_cozida': {
        'nome': 'Cenoura cozida',
        'grupo': 'legume',
        'kcal': 30,
        'carb_g': 6.7,
        'prot_g': 0.8,
        'gord_g': 0.2,
        'fibra_g': 2.6,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 50,
        'ig': 49
    },
    'beterraba_cozida': {
        'nome': 'Beterraba cozida',
        'grupo': 'legume',
        'kcal': 32,
        'carb_g': 7.2,
        'prot_g': 1.2,
        'gord_g': 0.1,
        'fibra_g': 1.9,
        'porcao_usual': '2 fatias médias',
        'gramas_porcao': 50,
        'ig': 64
    },
    'brocolis_cozido': {
        'nome': 'Brócolis cozido',
        'grupo': 'legume',
        'kcal': 25,
        'carb_g': 4.4,
        'prot_g': 2.1,
        'gord_g': 0.5,
        'fibra_g': 3.4,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 10
    },
    'couve_flor_cozida': {
        'nome': 'Couve-flor cozida',
        'grupo': 'legume',
        'kcal': 19,
        'carb_g': 3.9,
        'prot_g': 1.2,
        'gord_g': 0.2,
        'fibra_g': 2.4,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 15
    },
    'chuchu_cozido': {
        'nome': 'Chuchu cozido',
        'grupo': 'legume',
        'kcal': 17,
        'carb_g': 3.9,
        'prot_g': 0.6,
        'gord_g': 0.1,
        'fibra_g': 1.4,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 15
    },
    'abobrinha_cozida': {
        'nome': 'Abobrinha cozida',
        'grupo': 'legume',
        'kcal': 15,
        'carb_g': 3.0,
        'prot_g': 0.9,
        'gord_g': 0.1,
        'fibra_g': 1.6,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 15
    },
    'berinjela_cozida': {
        'nome': 'Berinjela cozida',
        'grupo': 'legume',
        'kcal': 19,
        'carb_g': 4.5,
        'prot_g': 0.7,
        'gord_g': 0.1,
        'fibra_g': 2.9,
        'porcao_usual': '3 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 10
    },
    'vagem_cozida': {
        'nome': 'Vagem cozida',
        'grupo': 'legume',
        'kcal': 25,
        'carb_g': 4.8,
        'prot_g': 1.6,
        'gord_g': 0.2,
        'fibra_g': 2.4,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 50,
        'ig': 15
    },
    'quiabo_cozido': {
        'nome': 'Quiabo cozido',
        'grupo': 'legume',
        'kcal': 22,
        'carb_g': 4.6,
        'prot_g': 1.4,
        'gord_g': 0.2,
        'fibra_g': 2.6,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 15
    },
    'abobora_cozida': {
        'nome': 'Abóbora cozida',
        'grupo': 'legume',
        'kcal': 28,
        'carb_g': 6.3,
        'prot_g': 0.8,
        'gord_g': 0.1,
        'fibra_g': 1.6,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 60,
        'ig': 75
    },

    # ==================== LATICÍNIOS ====================
    'leite_desnatado': {
        'nome': 'Leite desnatado',
        'grupo': 'lacteo',
        'kcal': 35,
        'carb_g': 4.9,
        'prot_g': 3.4,
        'gord_g': 0.1,
        'fibra_g': 0.0,
        'porcao_usual': '1 copo (200ml)',
        'gramas_porcao': 200,
        'ig': 32
    },
    'leite_integral': {
        'nome': 'Leite integral',
        'grupo': 'lacteo',
        'kcal': 60,
        'carb_g': 4.5,
        'prot_g': 3.2,
        'gord_g': 3.2,
        'fibra_g': 0.0,
        'porcao_usual': '1 copo (200ml)',
        'gramas_porcao': 200,
        'ig': 27
    },
    'iogurte_natural': {
        'nome': 'Iogurte natural desnatado',
        'grupo': 'lacteo',
        'kcal': 42,
        'carb_g': 5.6,
        'prot_g': 4.1,
        'gord_g': 0.3,
        'fibra_g': 0.0,
        'porcao_usual': '1 pote (170g)',
        'gramas_porcao': 170,
        'ig': 36
    },
    'iogurte_grego': {
        'nome': 'Iogurte grego natural',
        'grupo': 'lacteo',
        'kcal': 90,
        'carb_g': 4.0,
        'prot_g': 9.0,
        'gord_g': 5.0,
        'fibra_g': 0.0,
        'porcao_usual': '1 pote (100g)',
        'gramas_porcao': 100,
        'ig': 11
    },
    'queijo_branco': {
        'nome': 'Queijo branco/minas frescal',
        'grupo': 'lacteo',
        'kcal': 264,
        'carb_g': 3.2,
        'prot_g': 17.4,
        'gord_g': 20.2,
        'fibra_g': 0.0,
        'porcao_usual': '1 fatia média',
        'gramas_porcao': 30,
        'ig': 0
    },
    'queijo_cottage': {
        'nome': 'Queijo cottage',
        'grupo': 'lacteo',
        'kcal': 98,
        'carb_g': 3.4,
        'prot_g': 11.1,
        'gord_g': 4.3,
        'fibra_g': 0.0,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 50,
        'ig': 0
    },
    'ricota': {
        'nome': 'Ricota',
        'grupo': 'lacteo',
        'kcal': 140,
        'carb_g': 3.8,
        'prot_g': 12.6,
        'gord_g': 8.1,
        'fibra_g': 0.0,
        'porcao_usual': '2 colheres de sopa',
        'gramas_porcao': 50,
        'ig': 0
    },
    'requeijao_light': {
        'nome': 'Requeijão light',
        'grupo': 'lacteo',
        'kcal': 166,
        'carb_g': 3.5,
        'prot_g': 10.0,
        'gord_g': 12.7,
        'fibra_g': 0.0,
        'porcao_usual': '1 colher de sopa',
        'gramas_porcao': 30,
        'ig': 0
    },

    # ==================== GORDURAS SAUDÁVEIS ====================
    'azeite_oliva': {
        'nome': 'Azeite de oliva extra virgem',
        'grupo': 'gordura',
        'kcal': 884,
        'carb_g': 0.0,
        'prot_g': 0.0,
        'gord_g': 100.0,
        'fibra_g': 0.0,
        'porcao_usual': '1 colher de sopa',
        'gramas_porcao': 13,
        'ig': 0
    },
    'oleo_coco': {
        'nome': 'Óleo de coco',
        'grupo': 'gordura',
        'kcal': 862,
        'carb_g': 0.0,
        'prot_g': 0.0,
        'gord_g': 100.0,
        'fibra_g': 0.0,
        'porcao_usual': '1 colher de sopa',
        'gramas_porcao': 13,
        'ig': 0
    },
    'castanha_para': {
        'nome': 'Castanha do Pará',
        'grupo': 'gordura',
        'kcal': 656,
        'carb_g': 3.4,
        'prot_g': 14.5,
        'gord_g': 66.4,
        'fibra_g': 7.9,
        'porcao_usual': '2 unidades',
        'gramas_porcao': 10,
        'ig': 15
    },
    'castanha_caju': {
        'nome': 'Castanha de caju',
        'grupo': 'gordura',
        'kcal': 570,
        'carb_g': 29.1,
        'prot_g': 18.5,
        'gord_g': 42.0,
        'fibra_g': 3.7,
        'porcao_usual': '10 unidades',
        'gramas_porcao': 15,
        'ig': 22
    },
    'amendoim': {
        'nome': 'Amendoim torrado',
        'grupo': 'gordura',
        'kcal': 606,
        'carb_g': 12.5,
        'prot_g': 27.2,
        'gord_g': 49.6,
        'fibra_g': 8.0,
        'porcao_usual': '1 colher de sopa',
        'gramas_porcao': 15,
        'ig': 14
    },
    'nozes': {
        'nome': 'Nozes',
        'grupo': 'gordura',
        'kcal': 620,
        'carb_g': 9.6,
        'prot_g': 14.0,
        'gord_g': 60.0,
        'fibra_g': 5.2,
        'porcao_usual': '2 unidades',
        'gramas_porcao': 10,
        'ig': 15
    },
    'amendoas': {
        'nome': 'Amêndoas',
        'grupo': 'gordura',
        'kcal': 581,
        'carb_g': 19.0,
        'prot_g': 18.6,
        'gord_g': 47.3,
        'fibra_g': 11.6,
        'porcao_usual': '10 unidades',
        'gramas_porcao': 15,
        'ig': 0
    },
    'linhaça': {
        'nome': 'Semente de linhaça',
        'grupo': 'gordura',
        'kcal': 495,
        'carb_g': 43.3,
        'prot_g': 14.1,
        'gord_g': 32.3,
        'fibra_g': 33.5,
        'porcao_usual': '1 colher de sopa',
        'gramas_porcao': 10,
        'ig': 35
    },
    'chia': {
        'nome': 'Semente de chia',
        'grupo': 'gordura',
        'kcal': 486,
        'carb_g': 42.1,
        'prot_g': 16.5,
        'gord_g': 30.7,
        'fibra_g': 34.4,
        'porcao_usual': '1 colher de sopa',
        'gramas_porcao': 10,
        'ig': 1
    },

    # ==================== BEBIDAS ====================
    'cafe_sem_acucar': {
        'nome': 'Café sem açúcar',
        'grupo': 'bebida',
        'kcal': 2,
        'carb_g': 0.0,
        'prot_g': 0.2,
        'gord_g': 0.0,
        'fibra_g': 0.0,
        'porcao_usual': '1 xícara (50ml)',
        'gramas_porcao': 50,
        'ig': 0
    },
    'cha_verde': {
        'nome': 'Chá verde',
        'grupo': 'bebida',
        'kcal': 0,
        'carb_g': 0.0,
        'prot_g': 0.0,
        'gord_g': 0.0,
        'fibra_g': 0.0,
        'porcao_usual': '1 xícara (200ml)',
        'gramas_porcao': 200,
        'ig': 0
    },
    'agua_coco': {
        'nome': 'Água de coco',
        'grupo': 'bebida',
        'kcal': 22,
        'carb_g': 5.3,
        'prot_g': 0.0,
        'gord_g': 0.0,
        'fibra_g': 0.0,
        'porcao_usual': '1 copo (200ml)',
        'gramas_porcao': 200,
        'ig': 0
    },
}

# Grupos de alimentos para montagem de refeições
GRUPOS_REFEICOES = {
    'cafe_manha': ['cereal', 'lacteo', 'fruta', 'gordura', 'proteina'],
    'almoco': ['cereal', 'proteina', 'leguminosa', 'verdura', 'legume', 'gordura'],
    'lanche': ['cereal', 'lacteo', 'fruta', 'gordura'],
    'jantar': ['cereal', 'proteina', 'verdura', 'legume', 'gordura'],
    'ceia': ['lacteo', 'fruta']
}

# Alimentos recomendados por refeição (chaves do dicionário ALIMENTOS)
ALIMENTOS_POR_REFEICAO = {
    'cafe_manha': {
        'cereais': ['pao_integral', 'pao_forma_integral', 'tapioca', 'aveia_flocos'],
        'lacteos': ['leite_desnatado', 'iogurte_natural', 'queijo_branco', 'requeijao_light'],
        'frutas': ['banana_prata', 'mamao_papaia', 'maca', 'morango'],
        'gorduras': ['azeite_oliva', 'castanha_para', 'chia', 'linhaça'],
        'proteinas': ['ovo_cozido', 'ovo_mexido']
    },
    'almoco': {
        'cereais': ['arroz_integral_cozido', 'arroz_parboilizado_cozido', 'batata_doce_cozida', 'mandioca_cozida'],
        'proteinas': ['frango_peito_grelhado', 'peixe_tilapia', 'carne_bovina_patinho', 'ovo_cozido'],
        'leguminosas': ['feijao_carioca_cozido', 'feijao_preto_cozido', 'lentilha_cozida', 'grao_de_bico_cozido'],
        'verduras': ['alface', 'rucula', 'couve_manteiga', 'agriao'],
        'legumes': ['tomate', 'cenoura_crua', 'brocolis_cozido', 'abobrinha_cozida', 'berinjela_cozida'],
        'gorduras': ['azeite_oliva']
    },
    'lanche': {
        'cereais': ['pao_integral', 'tapioca', 'aveia_flocos'],
        'lacteos': ['iogurte_natural', 'iogurte_grego', 'queijo_branco'],
        'frutas': ['maca', 'pera', 'banana_prata', 'morango', 'goiaba'],
        'gorduras': ['castanha_para', 'castanha_caju', 'amendoas', 'nozes']
    },
    'jantar': {
        'cereais': ['arroz_integral_cozido', 'batata_doce_cozida', 'inhame_cozido'],
        'proteinas': ['frango_peito_grelhado', 'peixe_tilapia', 'peixe_sardinha_assada', 'ovo_cozido'],
        'verduras': ['alface', 'rucula', 'espinafre', 'repolho'],
        'legumes': ['tomate', 'pepino', 'couve_flor_cozida', 'vagem_cozida', 'chuchu_cozido'],
        'gorduras': ['azeite_oliva']
    },
    'ceia': {
        'lacteos': ['iogurte_natural', 'leite_desnatado'],
        'frutas': ['maca', 'pera', 'morango', 'kiwi'],
        'bebidas': ['cha_verde']
    }
}


def get_alimento(key: str) -> dict:
    """Retorna os dados de um alimento pela chave"""
    return ALIMENTOS.get(key, None)


def get_alimentos_por_grupo(grupo: str) -> dict:
    """Retorna todos os alimentos de um grupo específico"""
    return {k: v for k, v in ALIMENTOS.items() if v['grupo'] == grupo}


def calcular_nutricao_porcao(key: str, gramas: float = None) -> dict:
    """
    Calcula os valores nutricionais para uma porção específica

    Args:
        key: Chave do alimento
        gramas: Quantidade em gramas (se None, usa porção usual)

    Returns:
        Dict com valores nutricionais ajustados
    """
    alimento = ALIMENTOS.get(key)
    if not alimento:
        return None

    if gramas is None:
        gramas = alimento['gramas_porcao']

    fator = gramas / 100

    return {
        'nome': alimento['nome'],
        'porcao': alimento['porcao_usual'] if gramas == alimento['gramas_porcao'] else f"{gramas:.0f}g",
        'gramas': gramas,
        'kcal': alimento['kcal'] * fator,
        'carb': alimento['carb_g'] * fator,
        'prot': alimento['prot_g'] * fator,
        'gord': alimento['gord_g'] * fator,
        'fibra': alimento['fibra_g'] * fator
    }
