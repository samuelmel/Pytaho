import os
from contextlib import contextmanager
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
"""
database.py - Instâncias do SQLAlchemy / Pool de conexões.
Configura e gerencia conexões com bancos de dados relacionais e Data Warehouses.
"""

# Carrega variáveis do arquivo .env
load_dotenv()

class DatabaseManager:
    """
    Gerenciador de conexões de banco de dados (Origem e Destino/DW).
    Substitui as conexões JDBC/ODBC do Pentaho Kettle.
    """
    def __init__(self):
        self._source_engine: Engine | None = None
        self._target_engine: Engine | None = None

    @staticmethod
    def get_connection_uri(prefix: str = "DB_SOURCE") -> str:
        """Monta a URI de conexão ou lê diretamente do .env."""
        direct_url = os.getenv(f"{prefix}_URL")
        if direct_url:
            return direct_url

        host = os.getenv(f"{prefix}_HOST", "localhost")
        port = os.getenv(f"{prefix}_PORT", "5432")
        db = os.getenv(f"{prefix}_NAME", "postgres")
        user = os.getenv(f"{prefix}_USER", "postgres")
        pwd = os.getenv(f"{prefix}_PASSWORD", "postgres")
        driver = os.getenv(f"{prefix}_DRIVER", "postgresql+psycopg")
        return f"{driver}://{user}:{pwd}@{host}:{port}/{db}"

    @property
    def source_engine(self) -> Engine:
        """Engine para o banco de dados de origem."""
        if self._source_engine is None:
            uri = self.get_connection_uri("DB_SOURCE")
            self._source_engine = create_engine(
                uri,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
            )
        return self._source_engine

    @property
    def target_engine(self) -> Engine:
        """Engine para o banco de destino / Data Warehouse."""
        if self._target_engine is None:
            uri = self.get_connection_uri("DB_TARGET")
            self._target_engine = create_engine(
                uri,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
            )
        return self._target_engine

    @contextmanager
    def get_source_session(self) -> Generator[Session, None, None]:
        """Context manager para sessão segura do banco de origem."""
        session_factory = sessionmaker(bind=self.source_engine)
        session: Session = session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def get_target_session(self) -> Generator[Session, None, None]:
        """Context manager para sessão segura do banco de destino."""
        session_factory = sessionmaker(bind=self.target_engine)
        session: Session = session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

db_manager = DatabaseManager()

# TODO: Configurar engine e sessões do SQLAlchemy
