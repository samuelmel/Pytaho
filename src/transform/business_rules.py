import polars as pl
"""
business_rules.py - Regras de Negócio e Cálculos Derivados.
Equivalente aos steps 'Calculator', 'Modified Java Script Value', 'Formula' e 'Filter rows' do Pentaho Kettle.
"""

def apply_business_rules(df: pl.DataFrame) -> pl.DataFrame:
    """
    Substitui steps complexos como 'Calculator', 'Modified Java Script Value',
    'Switch / Case' e 'Formula' do Pentaho Kettle.
    """
    # Exemplo: cálculo de valor total, classificação por faixa de ticket e flag de status
    transformed = df.with_columns([
        # Cálculo de valor líquido: (quantidade * preco) - desconto
        (
            (pl.col("quantidade") * pl.col("preco_unitario")) - pl.col("desconto").fill_null(0.0)
        ).round(2).alias("valor_liquido"),

        # Regra condicional tipo CASE WHEN (Pentaho Switch/Case ou JavaScript)
        pl.when(pl.col("status").is_in(["CONCLUIDO", "ENTREGUE"]))
          .then(pl.lit("FINALIZADO"))
          .when(pl.col("status").is_in(["CANCELADO", "ESTORNADO"]))
          .then(pl.lit("CANCELADO"))
          .otherwise(pl.lit("EM_PROCESSAMENTO"))
          .alias("categoria_status"),
    ])

    return transformed

def filter_active_records(df: pl.DataFrame, status_column: str = "categoria_status") -> pl.DataFrame:
    """
    Substitui o step 'Filter rows' do Pentaho.
    """
    return df.filter(pl.col(status_column) != "CANCELADO")

# TODO: Implementar regras de negócio e validações específicas da empresa
