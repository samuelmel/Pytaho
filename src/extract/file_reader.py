from pathlib import Path
from typing import Optional, Union
import polars as pl
"""
file_reader.py - Leitura de Arquivos (CSV, Parquet, Excel, JSON).
Equivalente aos steps 'CSV file input', 'Microsoft Excel input' e 'JSON input' do Pentaho Kettle.
"""

class FileReader:
    """
    Equivalente aos steps 'CSV file input', 'Microsoft Excel input' e 'JSON input' do Pentaho Kettle.
    Lê arquivos locais ou de rede com alta performance utilizando Polars.
    """
    @staticmethod
    def read_csv(
        file_path: Union[str, Path],
        separator: str = ",",
        encoding: str = "utf8",
        has_header: bool = True
    ) -> pl.DataFrame:
        """Lê arquivo CSV usando o parser multi-threaded do Polars em Rust."""
        return pl.read_csv(
            source=file_path,
            separator=separator,
            encoding=encoding,
            has_header=has_header,
            infer_schema_length=10000,
            ignore_errors=True
        )

    @staticmethod
    def read_parquet(file_path: Union[str, Path], columns: Optional[list[str]] = None) -> pl.DataFrame:
        """Lê arquivo Parquet (formato colunar de alta performance para Data Lake)."""
        return pl.read_parquet(source=file_path, columns=columns)

    @staticmethod
    def read_excel(
        file_path: Union[str, Path],
        sheet_name: Optional[str] = None
    ) -> pl.DataFrame:
        """Lê arquivo Excel (.xlsx ou .xls) usando calamine/fastexcel sob o capô."""
        return pl.read_excel(source=file_path, sheet_name=sheet_name)

    @staticmethod
    def read_ndjson(file_path: Union[str, Path]) -> pl.DataFrame:
        """Lê arquivo JSON delimitado por linhas (newline-delimited JSON)."""
        return pl.read_ndjson(source=file_path)

    """Leitor de arquivos tabulares e semiestruturados."""
    pass
