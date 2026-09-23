from typing import Type
from pytaho.dialects.base_dialect import BaseDialectAdapter
from pytaho.dialects.oracle import OracleDialectAdapter
from pytaho.dialects.postgresql import PostgreSQLDialectAdapter
from pytaho.dialects.mssql import MSSQLDialectAdapter
from pytaho.dialects.mysql import MySQLDialectAdapter
from pytaho.parser.models import PentahoConnection

def get_dialect_adapter(connection: PentahoConnection) -> BaseDialectAdapter:
    """
    Fábrica que auto-detecta o tipo do banco de dados a partir da conexão Pentaho
    e retorna o adaptador correspondente.
    """
    db_type = connection.normalized_type

    if db_type == "ORACLE":
        return OracleDialectAdapter(connection)
    elif db_type == "POSTGRESQL":
        return PostgreSQLDialectAdapter(connection)
    elif db_type == "MSSQL":
        return MSSQLDialectAdapter(connection)
    elif db_type == "MYSQL":
        return MySQLDialectAdapter(connection)
    else:
        # Fallback genérico para PostgreSQL / SQLAlchemy
        return PostgreSQLDialectAdapter(connection)

__all__ = [
    "BaseDialectAdapter",
    "OracleDialectAdapter",
    "PostgreSQLDialectAdapter",
    "MSSQLDialectAdapter",
    "MySQLDialectAdapter",
    "get_dialect_adapter",
]

