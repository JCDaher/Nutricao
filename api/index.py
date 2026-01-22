"""
Vercel serverless function entry point
Exposes the FastAPI app for Vercel deployment
"""
import sys
from pathlib import Path

# Add the parent directory to the path so we can import app
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app

# Export for Vercel
handler = app
