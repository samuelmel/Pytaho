import polars as pl
from src.extract.file_reader import FileReader
from src.transform.cleaners import clean_strings, handle_nulls
from src.transform.business_rules import apply_business_rules, filter_active_records
from src.load.file_writer import FileWriter
from src.utils.logger import logger
from src.utils.notifications import NotificationService
"""
sales_pipeline.py - Pipeline de Vendas.
Equivalente ao Job (.kjb) do Pentaho para o domínio de Vendas.
Orquestra o fluxo completo: Extract -> Transform -> Load.
"""

from prefect import task, flow
def run_sales_pipeline():
    """Executa o pipeline de vendas."""
    pass


def extract_sales_data(source_path: str) -> pl.DataFrame:
    """Passo de Extração (Input)."""
    logger.info(f"Iniciando extração de vendas a partir de: {source_path}")
    return FileReader.read_csv(source_path)


def transform_sales_data(df: pl.DataFrame) -> pl.DataFrame:
    """Passo de Transformação (Transformation)."""
    logger.info(f"Transformando {len(df)} registros de vendas...")
    # Limpeza básica
    cleaned_df = clean_strings(df, ["cliente", "produto", "status"])
    cleaned_df = handle_nulls(cleaned_df, {"desconto": 0.0, "status": "PENDENTE"})

    # Aplicação de regras de negócio e cálculo de campos derivados
    enriched_df = apply_business_rules(cleaned_df)

    # Filtragem de registros inválidos/cancelados
    final_df = filter_active_records(enriched_df)
    logger.info(f"Transformação concluída. {len(final_df)} registros prontos.")
    return final_df

def load_sales_data(df: pl.DataFrame, destination_path: str) -> str:
    """Passo de Carga (Output / Load)."""
    logger.info(f"Gravando arquivo Parquet otimizado em: {destination_path}")
    output = FileWriter.write_parquet(df, destination_path)
    return str(output)

def run_sales_pipeline(source_path: str = "data/raw/vendas.csv", output_path: str = "data/processed/vendas.parquet") -> bool:
    """
    Job principal de Vendas: Equivalente a um .kjb do Pentaho.
    Coordena Extração -> Transformação -> Carga -> Notificação.
    """
    try:
        logger.info("=== Iniciando Pipeline de Vendas ===")
        raw_df = extract_sales_data(source_path)
        processed_df = transform_sales_data(raw_df)
        dest = load_sales_data(processed_df, output_path)

        logger.info(f"=== Pipeline de Vendas finalizado com sucesso! Arquivo gerado: {dest} ===")
        return True
    except Exception as e:
        error_msg = f"Falha na execução da Sales Pipeline: {str(e)}"
        logger.error(error_msg, exc_info=True)
        NotificationService.send_slack(f":rotating_light: {error_msg}")
        raise

if __name__ == "__main__":
    run_sales_pipeline()

