# Gerador de Dietas para Diabetes

Sistema otimizado que gera planos alimentares personalizados usando **mínimo de tokens da API Anthropic**.

## Arquitetura

O sistema segue o princípio: **Python calcula TUDO → Claude apenas formata em Markdown**

```
Formulário (6 campos)
→ Python calcula TMB, calorias, macros
→ Python busca alimentos TACO e monta refeições
→ Python gera JSON estruturado completo
→ Claude recebe JSON + prompt mínimo (~1.000 tokens)
→ Claude retorna Markdown formatado (~3.000 tokens)
→ Download arquivo .md
```

### Economia de Tokens

| Método | Tokens/dieta |
|--------|-------------|
| Sem otimização | ~20.500 |
| Com otimização | ~4.000 |
| **Economia** | **80%** |

## Estrutura do Projeto

```
dieta-diabetes/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── services/
│   │   ├── nutrition_calc.py   # Cálculos nutricionais (TMB, macros)
│   │   ├── meal_builder.py     # Monta refeições com TACO
│   │   └── diet_generator.py   # Integração Claude (prompt mínimo)
│   └── data/
│       ├── alimentos_base.py   # 80+ alimentos brasileiros
│       └── substituicoes.py    # Tabelas de substituição
├── static/
│   ├── css/style.css           # Design clean e responsivo
│   └── js/app.js               # Validação frontend + download
├── templates/
│   └── index.html              # Formulário simples
├── requirements.txt
├── vercel.json                 # Configuração deploy Vercel
└── .env.example
```

## Funcionalidades

### Cálculos Nutricionais (Python)
- **TMB**: Equação de Mifflin-St Jeor
- **IMC**: Cálculo e classificação
- **Necessidade Calórica**: Baseada em atividade física
- **Macros**: Distribuição personalizada (50% carb, 20% prot, 30% gord)
- **Refeições**: 5 refeições com distribuição ideal

### Base de Alimentos
- 80+ alimentos brasileiros
- Valores nutricionais baseados na Tabela TACO
- Índice glicêmico para cada alimento
- Porções em medidas caseiras

### Tabelas de Substituição
- Cereais e pães (20+ opções)
- Carnes e proteínas (20+ opções)
- Frutas (25+ opções)
- Verduras e legumes (20+ opções)
- Óleos e gorduras saudáveis
- Leguminosas
- Laticínios

## Deploy

### Local

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env e adicionar ANTHROPIC_API_KEY

# Executar
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000

### Vercel

1. Fazer push do código para o GitHub
2. Conectar repositório no Vercel
3. Adicionar variável de ambiente `ANTHROPIC_API_KEY`
4. Deploy!

```bash
vercel --prod
```

## Uso

1. Acesse a aplicação
2. Preencha o formulário:
   - Nome completo
   - Sexo
   - Idade
   - Peso (kg)
   - Altura (cm)
   - HbA1c ou Glicemia (opcional)
3. Clique em "Gerar Dieta Personalizada"
4. Download automático do arquivo `.md`
5. Importe no Google Docs para impressão profissional

## API Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Página principal |
| `/gerar-dieta` | POST | Gera dieta personalizada |
| `/api/calcular-preview` | GET | Preview dos cálculos |
| `/health` | GET | Health check |

## Tecnologias

- **Backend**: Python 3.11+, FastAPI
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI**: Claude API (Anthropic)
- **Deploy**: Vercel

## Licença

Desenvolvido para uso exclusivo do consultório:

**Dr. Jorge Cecílio Daher Jr**
CRMGO 6108 | RQE 5769, 5772
Endocrinologia e Metabologia
