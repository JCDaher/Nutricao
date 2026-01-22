# Nutricao
Nutrição
# Gerador de Dietas para Diabetes

Sistema otimizado que gera planos alimentares personalizados usando **mínimo de tokens da API Anthropic**.

## Arquitetura

- **Python faz**: Todos os cálculos nutricionais + montagem de refeições
- **Claude faz**: Apenas formatação em Markdown profissional

## Economia de Tokens

- **Sem bibliotecas**: ~20.500 tokens/dieta
- **Com bibliotecas**: ~4.000 tokens/dieta
- **Economia**: 80% 💰

## Deploy

### Local
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload

Vercel
vercel --prod

Adicionar ANTHROPIC_API_KEY nas variáveis de ambiente do Vercel.
Uso
Acesse a aplicação
Preencha o formulário (6 campos)
Clique em "Gerar Dieta"
Download automático do arquivo .md
Importe no Google Docs para impressão
Dr. Jorge Cecílio Daher Jr
CRMGO 6108 RQE5769, 5772 Endocrinologia, Metabologia
