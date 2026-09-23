from typing import Any, Dict, List
import polars as pl
"""
cleaners.py - Limpeza e Tratamento de Dados.
Equivalente a steps como 'String operations', 'Replace in string', 'Select values' (casting) e 'If field value is null'.
"""

def clean_strings(df: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
    """
    Substitui steps do Pentaho como 'String operations' e 'Trim'.
    Remove espaços nas extremidades e normaliza strings em maiúsculas/minúsculas.
    """
    exprs = [
        pl.col(col).str.strip_chars() for col in columns if col in df.columns
    ]
    return df.with_columns(exprs)

def handle_nulls(df: pl.DataFrame, defaults: Dict[str, Any]) -> pl.DataFrame:
    """
    Substitui o step 'If field value is null' do Pentaho.
    Preenche valores nulos com valores padrão definidos por coluna.
    """
    exprs = [
        pl.col(col).fill_null(val)
        for col, val in defaults.items()
        if col in df.columns
    ]
    return df.with_columns(exprs)

def parse_dates(df: pl.DataFrame, columns: List[str], date_format: str = "%Y-%m-%d") -> pl.DataFrame:
    """
    Substitui o step 'Select values' (aba Meta-data para conversão de Date).
    Converte colunas de texto para tipo Date do Polars.
    """
    exprs = [
        pl.col(col).str.to_date(format=date_format, strict=False)
        for col in columns if col in df.columns
    ]
    return df.with_columns(exprs)

def select_and_rename(df: pl.DataFrame, mapping: Dict[str, str]) -> pl.DataFrame:
    """
    Substitui 'Select values' (Rename / Select fields) do Pentaho.
    """
    return df.rename({k: v for k, v in mapping.items() if k in df.columns})

# TODO: Implementar funções de limpeza (strings, datas, nulos e tipagem)
