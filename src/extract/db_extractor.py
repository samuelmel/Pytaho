from typing import Optional
import polars as pl
from sqlalchemy import Engine
from config.database import db_manager
"""
db_extractor.py - Extração de Bancos Relacionais.
Equivalente ao step 'Table Input' do Pentaho Kettle.
"""

class DatabaseExtractor:
    """
    Equivalente ao step 'Table Input' do Pentaho Kettle.
    Extrai dados de bancos relacionais usando Polars diretamente via SQLAlchemy ou ConnectorX/ADBC.
    """
    def __init__(self, engine: Optional[Engine] = None):
        self.engine = engine or db_manager.source_engine

    def query_to_polars(self, query: str) -> pl.DataFrame:
        """
        Executa uma consulta SQL e carrega diretamente em um DataFrame Polars.
        Substitui queries manuais do Pentaho.
        """
        return pl.read_database(query=query, connection=self.engine)

    def extract_table(self, table_name: str, columns: Optional[list[str]] = None, condition: Optional[str] = None) -> pl.DataFrame:
        """Extrai colunas específicas de uma tabela com filtro opcional."""
        cols = ", ".join(columns) if columns else "*"
        sql = f"SELECT {cols} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        return self.query_to_polars(sql)

    """Extração de dados de bancos relacionais (Postgres, MySQL, SQL Server, etc.)."""
    pass
