import httpx
from typing import Any, Dict, List, Optional
import polars as pl
"""
api_client.py - Extração de APIs REST.
Equivalente aos steps de REST Client / HTTP Client do Pentaho Kettle.
"""

class APIClient:
    """
    Equivalente ao step 'REST Client' / 'HTTP Client' do Pentaho Kettle.
    Utiliza HTTPX para requisições rápidas e síncronas/assíncronas com retry.
    """
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # Se for dict com chave de lista (ex: {"data": [...]})
                for val in data.values():
                    if isinstance(val, list):
                        return val
                return [data]
            return []

    def get_as_polars(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> pl.DataFrame:
        """Extrai os dados da API e converte diretamente para Polars DataFrame."""
        records = self.get(endpoint, params=params)
        if not records:
            return pl.DataFrame()
        return pl.DataFrame(records)

    """Cliente para extração e consumo de APIs REST."""
    pass
