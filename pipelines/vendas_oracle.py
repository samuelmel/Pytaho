# ==============================================================================
# Script Python POO Gerado Automaticamente pelo Pytaho Converter
# Origem Pentaho: etl_vendas_oracle
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

class OracleDatabaseConnection:
    """Gerenciador de conexão com Banco de Dados Oracle usando oracledb em Thin Mode."""

    def __init__(self, host: str = "10.0.0.50", port: str = "1521", service_name: str = "ORCLDW", user: str = "usr_etl", password: str = "SecretOraclePass123"):
        self.host = host
        self.port = port
        self.service_name = service_name
        self.user = user
        self.password = password

    def get_dsn(self) -> str:
        return f"{self.host}:{self.port}/{self.service_name}"

    def get_connection(self):
        import oracledb
        # Inicia a conexão oracledb em Thin Mode (não exige Oracle Instant Client)
        return oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.get_dsn()
        )

    def get_sqlalchemy_engine(self):
        from sqlalchemy import create_engine
        url = f"oracle+oracledb://{self.user}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}"
        return create_engine(url, pool_pre_ping=True)


class ExtrairVendasOracleExtractor:
    """
    Extrator de dados gerado a partir do step Pentaho: 'Extrair Vendas Oracle'
    Fonte de Dados: Oracle (OracleDW)
    """
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.query = """SELECT id_venda, cd_cliente, vl_total, dt_venda FROM tb_vendas WHERE status = 'APROVADO'"""

    def extract(self) -> "pl.DataFrame":
        import polars as pl
        logger.info("Executando extração do step 'Extrair Vendas Oracle'...")
        engine = self.db_connection.get_sqlalchemy_engine()
        # Lê a consulta diretamente para um DataFrame Polars
        return pl.read_database(query=self.query, connection=engine)


class TratarCamposVendaTransformer:
    """
    Transformador de dados gerado a partir do step Pentaho: 'Tratar Campos Venda' (Tipo: SelectValues)
    """
    def __init__(self):
        self.rename_mapping = {'id_venda': 'venda_id', 'cd_cliente': 'cliente_id'}

    def transform(self, df: "pl.DataFrame") -> "pl.DataFrame":
        import polars as pl
        logger.info("Aplicando transformações do step 'Tratar Campos Venda'...")
        if self.rename_mapping:
            df = df.rename({k: v for k, v in self.rename_mapping.items() if k in df.columns})
        return df


class CarregarDWOracleLoader:
    """
    Carregador de dados gerado a partir do step Pentaho: 'Carregar DW Oracle'
    Tabela Destino: fact_vendas (OracleDW)
    """
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.table_name = "fact_vendas"

    def load(self, df: "pl.DataFrame") -> int:
        import polars as pl
        if df.is_empty():
            logger.warning("DataFrame vazio. Nenhuma linha carregada.")
            return 0
        logger.info(f"Carregando {len(df)} registros na tabela {self.table_name}...")
        engine = self.db_connection.get_sqlalchemy_engine()
        df.write_database(table_name=self.table_name, connection=engine, if_table_exists="append")
        return len(df)


class etl_vendas_oraclePipeline:
    """
    Pipeline Principal POO responsável por orquestrar a execução do fluxo:
    Extract -> Transform -> Load
    """
    def __init__(self):
        self.db_oracledw = OracleDatabaseConnection()
        self.extractor_0 = ExtrairVendasOracleExtractor(self.db_oracledw)
        self.transformer_1 = TratarCamposVendaTransformer()
        self.loader_2 = CarregarDWOracleLoader(self.db_oracledw)

    def run(self):
        logger.info("Iniciando execução da Pipeline 'etl_vendas_oracle'...")
        df_0 = self.extractor_0.extract()
        df_1 = self.transformer_1.transform(df_0)
        rows_loaded = self.loader_2.load(df_1)
        logger.info("Execução da Pipeline concluída com sucesso!")

if __name__ == "__main__":
    pipeline = etl_vendas_oraclePipeline()
    pipeline.run()