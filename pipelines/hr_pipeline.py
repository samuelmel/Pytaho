import polars as pl
from src.extract.file_reader import FileReader
from src.transform.cleaners import clean_strings, parse_dates, handle_nulls
from src.load.file_writer import FileWriter
from src.utils.logger import logger
from src.utils.notifications import NotificationService
"""
hr_pipeline.py - Pipeline de Recursos Humanos.
Equivalente ao Job (.kjb) do Pentaho para o domínio de RH.
Orquestra o fluxo completo: Extract -> Transform -> Load.
"""

def extract_hr_data(source_path: str) -> pl.DataFrame:
    logger.info(f"Extraindo dados de RH: {source_path}")
    return FileReader.read_csv(source_path)
def run_hr_pipeline():
    """Executa o pipeline de recursos humanos."""
    pass

def transform_hr_data(df: pl.DataFrame) -> pl.DataFrame:
    logger.info("Aplicando transformações em RH...")
    df = clean_strings(df, ["nome", "cargo", "departamento"])
    df = parse_dates(df, ["data_admissao"], date_format="%Y-%m-%d")
    df = handle_nulls(df, {"salario": 0.0, "departamento": "Geral"})
    return df

def load_hr_data(df: pl.DataFrame, destination_path: str) -> str:
    logger.info(f"Gravando dados consolidados de RH em: {destination_path}")
    output = FileWriter.write_parquet(df, destination_path)
    return str(output)

def run_hr_pipeline(source_path: str = "data/raw/funcionarios.csv", output_path: str = "data/processed/funcionarios.parquet") -> bool:
    try:
        logger.info("=== Iniciando Pipeline de RH ===")
        df_raw = extract_hr_data(source_path)
        df_clean = transform_hr_data(df_raw)
        load_hr_data(df_clean, output_path)
        logger.info("=== Pipeline de RH finalizada com sucesso! ===")
        return True
    except Exception as e:
        logger.error(f"Erro na Pipeline de RH: {e}", exc_info=True)
        NotificationService.send_slack(f":warning: Erro no Pipeline de RH: {e}")
        raise

if __name__ == "__main__":
    run_hr_pipeline()

