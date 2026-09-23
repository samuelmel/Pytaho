# ==============================================================================
# Script Python POO Gerado Automaticamente pelo Pytaho Converter
# Origem Pentaho: etl_vendas_clientes_postgres
# ==============================================================================
import os
import logging
import polars as pl
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Configuração de Logger Estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s - %(message)s"
)
logger = logging.getLogger("pytaho_pipeline")

class PostgresDatabaseConnection:
    """Gerenciador de conexão PostgreSQL usando psycopg e SQLAlchemy 2.0."""

    def __init__(self, host: str = "localhost", port: str = "5432", database: str = "db_comercial", user: str = "postgres", password: str = "secret_postgres_pass"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def get_sqlalchemy_engine(self):
        from sqlalchemy import create_engine
        url = f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return create_engine(url, pool_pre_ping=True)


class ExtrairClientesAtivosExtractor:
    """
    Extrator de dados gerado a partir do step Pentaho: 'Extrair Clientes Ativos'
    Fonte de Dados: PostgreSQL (PostgresComercialDB)
    """
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.query = """SELECT id_cliente, nm_cliente, ds_email, sg_uf FROM tb_clientes WHERE status = 'A'"""

    def extract(self) -> "pl.DataFrame":
        import polars as pl
        logger.info("Executando extração do step 'Extrair Clientes Ativos'...")
        engine = self.db_connection.get_sqlalchemy_engine()
        # Lê a consulta diretamente para um DataFrame Polars
        return pl.read_database(query=self.query, connection=engine)


class ExtrairPedidosRecentesExtractor:
    """
    Extrator de dados gerado a partir do step Pentaho: 'Extrair Pedidos Recentes'
    Fonte de Dados: PostgreSQL (PostgresComercialDB)
    """
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.query = """SELECT id_pedido, id_cliente, vl_total, dt_pedido FROM tb_pedidos WHERE dt_pedido >= CURRENT_DATE - INTERVAL '30 days'"""

    def extract(self) -> "pl.DataFrame":
        import polars as pl
        logger.info("Executando extração do step 'Extrair Pedidos Recentes'...")
        engine = self.db_connection.get_sqlalchemy_engine()
        # Lê a consulta diretamente para um DataFrame Polars
        return pl.read_database(query=self.query, connection=engine)


class JuntarClientesePedidosTransformer:
    """
    Transformador de dados gerado a partir do step Pentaho: 'Juntar Clientes e Pedidos' (Tipo: StreamLookup)
    """
    def __init__(self):
        self.rename_mapping = {}

    def transform(self, df: "pl.DataFrame") -> "pl.DataFrame":
        import polars as pl
        logger.info("Aplicando transformações do step 'Juntar Clientes e Pedidos'...")
        if self.rename_mapping:
            df = df.rename({k: v for k, v in self.rename_mapping.items() if k in df.columns})
        return df


class CarregarDWPedidosConsolidadosLoader:
    """
    Carregador de dados gerado a partir do step Pentaho: 'Carregar DW Pedidos Consolidados'
    Tabela Destino: fact_pedidos_consolidados (PostgresComercialDB)
    """
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.table_name = "fact_pedidos_consolidados"

    def load(self, df: "pl.DataFrame") -> int:
        import polars as pl
        if df.is_empty():
            logger.warning("DataFrame vazio. Nenhuma linha carregada.")
            return 0
        logger.info(f"Carregando {len(df)} registros na tabela {self.table_name}...")
        engine = self.db_connection.get_sqlalchemy_engine()
        df.write_database(table_name=self.table_name, connection=engine, if_table_exists="append")
        return len(df)


class etl_vendas_clientes_postgresPipeline:
    """
    Pipeline Principal POO responsável por orquestrar a execução do fluxo:
    Extract -> Transform -> Load
    """
    def __init__(self):
        self.db_postgrescomercialdb = PostgresDatabaseConnection()
        self.extractor_0 = ExtrairClientesAtivosExtractor(self.db_postgrescomercialdb)
        self.extractor_1 = ExtrairPedidosRecentesExtractor(self.db_postgrescomercialdb)
        self.transformer_2 = JuntarClientesePedidosTransformer()
        self.loader_3 = CarregarDWPedidosConsolidadosLoader(self.db_postgrescomercialdb)

    def run(self):
        logger.info("Iniciando execução da Pipeline 'etl_vendas_clientes_postgres'...")
        df_0 = self.extractor_0.extract()
        df_1 = self.extractor_1.extract()
        df_2 = self.transformer_2.transform(df_1)
        rows_loaded = self.loader_3.load(df_2)
        logger.info("Execução da Pipeline concluída com sucesso!")

if __name__ == "__main__":
    pipeline = etl_vendas_clientes_postgresPipeline()
    pipeline.run()