from typing import Literal, Optional
import polars as pl
from sqlalchemy import Engine
from config.database import db_manager
"""
db_loader.py - Carga em Bancos de Dados e Data Warehouses.
Equivalente aos steps 'Table Output' e 'Insert / Update' do Pentaho Kettle.
"""

class DatabaseLoader:
    """
    Equivalente aos steps 'Table Output' e 'Insert / Update' do Pentaho Kettle.
    Carrega DataFrames Polars diretamente no banco de dados de destino / Data Warehouse.
    """
    def __init__(self, engine: Optional[Engine] = None):
        self.engine = engine or db_manager.target_engine

    def load_polars(
        self,
        df: pl.DataFrame,
        table_name: str,
        if_table_exists: Literal["append", "replace", "fail"] = "append",
    ) -> int:
        """
        Escreve o DataFrame Polars na tabela de destino.
        Retorna a quantidade de registros carregados.
        """
        if df.is_empty():
            return 0

        # pl.DataFrame.write_database suporta SQLAlchemy Engine ou connection string URI
        df.write_database(
            table_name=table_name,
            connection=self.engine,
            if_table_exists=if_table_exists,
        )
        return len(df)

    """Carregador de dados em bancos relacionais e Data Warehouses."""
    pass
