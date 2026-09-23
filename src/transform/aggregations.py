from typing import List, Optional
import polars as pl
"""
aggregations.py - Agrupamentos e Cálculos Analíticos.
Equivalente ao step 'Group by', 'Memory Group by' e 'Analytic Query' do Pentaho Kettle.
"""

def group_and_aggregate(
    df: pl.DataFrame,
    group_by_cols: List[str],
    sum_cols: Optional[List[str]] = None,
    avg_cols: Optional[List[str]] = None,
    count_cols: Optional[List[str]] = None,
) -> pl.DataFrame:
    """
    Substitui o step 'Memory Group by' / 'Group by' do Pentaho Kettle.
    Aplica agregações paralelas altamente otimizadas via Polars.
    """
    aggs = []
    if sum_cols:
        aggs.extend([pl.col(c).sum().alias(f"{c}_total") for c in sum_cols])
    if avg_cols:
        aggs.extend([pl.col(c).mean().alias(f"{c}_media") for c in avg_cols])
    if count_cols:
        aggs.extend([pl.col(c).count().alias(f"{c}_qtd") for c in count_cols])

    return df.group_by(group_by_cols).agg(aggs)

def calculate_running_total(df: pl.DataFrame, partition_by: str, order_by: str, target_col: str) -> pl.DataFrame:
    """
    Substitui o step 'Analytic Query' (Window Functions / Soma acumulada).
    """
    return df.with_columns(
        pl.col(target_col)
        .cum_sum()
        .over(partition_by)
        .alias(f"{target_col}_acumulado")
    ).sort(order_by)

# TODO: Implementar agregações, somas, contagens e janelas analíticas
