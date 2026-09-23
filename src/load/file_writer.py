from pathlib import Path
from typing import Literal, Union
import polars as pl
"""
file_writer.py - Geração de Arquivos Finais.
Equivalente aos steps 'Text file output', 'Microsoft Excel output' e 'Parquet Output' do Pentaho Kettle.
"""

class FileWriter:
    """
    Equivalente aos steps 'Text file output', 'Parquet Output' e 'Microsoft Excel output' do Pentaho.
    Salva dados transformados em formatos otimizados para Data Lakes e relatórios.
    """
    @staticmethod
    def write_parquet(
        df: pl.DataFrame,
        output_path: Union[str, Path],
        compression: Literal["snappy", "gzip", "brotli", "zstd", "lz4", "uncompressed"] = "zstd",
    ) -> Path:
        """Salva como Parquet (recomendado para Data Lake e DW moderno)."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(path, compression=compression)
        return path

    @staticmethod
    def write_csv(
        df: pl.DataFrame,
        output_path: Union[str, Path],
        separator: str = ",",
    ) -> Path:
        """Salva como CSV estruturado."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(path, separator=separator)
        return path

    @staticmethod
    def write_excel(
        df: pl.DataFrame,
        output_path: Union[str, Path],
        worksheet: str = "Sheet1",
    ) -> Path:
        """Salva como planilha Excel (.xlsx)."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.write_excel(path, worksheet=worksheet)
        return path

    """Escritor de arquivos estruturados (Parquet, CSV, Excel, etc.)."""
    pass
