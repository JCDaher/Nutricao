"""
Vercel serverless function entry point
"""
import os
import sys
from pathlib import Path

# Configurar o caminho para importar os módulos da aplicação
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Configurar variável de ambiente para indicar que estamos no Vercel
os.environ['VERCEL'] = '1'

# Importar a aplicação FastAPI
from app.main import app

# Handler para Vercel (nome obrigatório)
app = app
