from abc import ABC, abstractmethod
from typing import Dict, Any
from pytaho.parser.models import PentahoConnection

class BaseDialectAdapter(ABC):
    """
    Classe abstrata base para os adaptadores de Banco de Dados.
    Responsável por auto-detectar e traduzir configurações do Pentaho em código Python.
    """

    def __init__(self, connection: PentahoConnection):
        self.connection = connection

    @property
    @abstractmethod
    def db_type_name(self) -> str:
        """Nome do banco de dados (ex: 'Oracle', 'PostgreSQL', 'SQL Server')."""
        pass

    @property
    @abstractmethod
    def driver_package(self) -> str:
        """Nome do pacote Python recomendado para o driver (ex: 'oracledb', 'psycopg')."""
        pass

    @abstractmethod
    def generate_connection_code(self) -> str:
        """Gera trecho de código Python POO para estabelecer conexão segura com o banco."""
        pass

    @abstractmethod
    def generate_sqlalchemy_url(self) -> str:
        """Gera a URI de conexão no formato SQLAlchemy para o dialeto específico."""
        pass

    def adapt_sql_query(self, sql_query: str) -> str:
        """Adapta consultas SQL nativas do Pentaho para particularidades do dialeto (ex: paginação, funções)."""
        return sql_query

