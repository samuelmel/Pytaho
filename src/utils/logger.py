import logging
import sys
from pathlib import Path
"""
logger.py - Configuração de Logs de Execução e Erros.
Substitui o sistema de logs do Pentaho Spoon / Kitchen.
"""

def setup_logger(name: str = "pytaho", log_file: str = "logs/etl.log", level: int = logging.INFO) -> logging.Logger:
    """
    Configura logger padronizado para execuções de ETL.
    Substitui os logs de console e arquivos de log do Pentaho Spoon/Kitchen.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()

# TODO: Configurar instâncias de logger estruturado (ex: Loguru ou logging padrão)
