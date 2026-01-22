"""
Tracking de custos e estatísticas de uso
Armazena dados em JSON local (quando possível)
No Vercel, usa memória apenas (stats são perdidos entre requests)
"""
from datetime import datetime
from typing import Dict
from pydantic import BaseModel
import json
import os

from app.config.settings import settings

# Detectar ambiente Vercel (read-only filesystem)
IS_VERCEL = os.environ.get('VERCEL', False)


class DietGeneration(BaseModel):
    """Registro de uma geração de dieta"""
    timestamp: datetime
    patient_name: str
    mode: str  # python_only, api_minimal, api_full
    tokens_used: int
    cost_usd: float
    complexity_score: int


class CostTracker:
    """
    Rastreia custos e estatísticas
    No Vercel: apenas memória (não persiste entre requests)
    Local: salva em arquivo JSON
    """

    def __init__(self, storage_path: str = "data/usage_stats.json"):
        self.storage_path = storage_path
        self.is_readonly = IS_VERCEL
        self.stats = self._load_stats()

    def record_generation(
        self,
        patient_name: str,
        mode: str,
        tokens_used: int,
        complexity_score: int
    ):
        """Registra uma geração de dieta"""

        # Calcular custo baseado no modo
        cost_map = {
            'python_only': settings.cost_python_only,
            'api_minimal': settings.cost_api_minimal,
            'api_full': settings.cost_api_full
        }
        cost = cost_map.get(mode, 0.0)

        generation = DietGeneration(
            timestamp=datetime.now(),
            patient_name=patient_name,
            mode=mode,
            tokens_used=tokens_used,
            cost_usd=cost,
            complexity_score=complexity_score
        )

        # Atualizar estatísticas
        self.stats['generations'].append(generation.model_dump())
        self.stats['total_diets'] += 1
        self.stats['total_cost_usd'] += cost
        self.stats['total_tokens'] += tokens_used

        # Contadores por modo
        if mode not in self.stats['by_mode']:
            self.stats['by_mode'][mode] = {'count': 0, 'cost': 0.0}

        self.stats['by_mode'][mode]['count'] += 1
        self.stats['by_mode'][mode]['cost'] += cost

        self._save_stats()

    def get_monthly_stats(self, year: int, month: int) -> Dict:
        """Retorna estatísticas do mês"""

        monthly_gens = [
            g for g in self.stats['generations']
            if datetime.fromisoformat(str(g['timestamp'])).year == year
            and datetime.fromisoformat(str(g['timestamp'])).month == month
        ]

        if not monthly_gens:
            return {
                'total_diets': 0,
                'total_cost': 0.0,
                'by_mode': {},
                'average_cost': 0.0
            }

        by_mode = {}
        for gen in monthly_gens:
            mode = gen['mode']
            if mode not in by_mode:
                by_mode[mode] = {'count': 0, 'cost': 0.0}
            by_mode[mode]['count'] += 1
            by_mode[mode]['cost'] += gen['cost_usd']

        total_cost = sum(g['cost_usd'] for g in monthly_gens)

        return {
            'total_diets': len(monthly_gens),
            'total_cost': total_cost,
            'by_mode': by_mode,
            'average_cost': total_cost / len(monthly_gens) if monthly_gens else 0.0
        }

    def get_all_time_stats(self) -> Dict:
        """Retorna estatísticas totais"""
        return {
            'total_diets': self.stats['total_diets'],
            'total_cost_usd': self.stats['total_cost_usd'],
            'total_tokens': self.stats['total_tokens'],
            'by_mode': self.stats['by_mode'],
            'average_cost': (
                self.stats['total_cost_usd'] / self.stats['total_diets']
                if self.stats['total_diets'] > 0 else 0.0
            )
        }

    def _load_stats(self) -> Dict:
        """Carrega estatísticas do arquivo (se disponível)"""

        # Em ambiente Vercel, sempre começar vazio
        if self.is_readonly:
            return self._empty_stats()

        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return self._empty_stats()
        else:
            return self._empty_stats()

    def _empty_stats(self) -> Dict:
        """Estrutura vazia de estatísticas"""
        return {
            'generations': [],
            'total_diets': 0,
            'total_cost_usd': 0.0,
            'total_tokens': 0,
            'by_mode': {}
        }

    def _save_stats(self):
        """Salva estatísticas no arquivo (apenas em ambiente local)"""

        # Não salvar em ambiente Vercel (read-only filesystem)
        if self.is_readonly:
            return

        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(self.stats, f, indent=2, default=str)
        except (OSError, IOError) as e:
            # Ignorar erros de escrita silenciosamente
            print(f"Aviso: Não foi possível salvar estatísticas: {e}")
