import polars as pl
from src.transform.cleaners import clean_strings, handle_nulls
from src.transform.aggregations import group_and_aggregate
from src.transform.business_rules import apply_business_rules, filter_active_records
"""
test_transform.py - Testes unitários para regras de transformação e limpeza.
"""

def test_clean_strings():
    df = pl.DataFrame({"nome": ["  Alice  ", "Bob  ", " Carlos "]})
    res = clean_strings(df, ["nome"])
    assert res["nome"].to_list() == ["Alice", "Bob", "Carlos"]

def test_handle_nulls():
    df = pl.DataFrame({"valor": [10.0, None, 30.0]})
    res = handle_nulls(df, {"valor": 0.0})
    assert res["valor"].to_list() == [10.0, 0.0, 30.0]

def test_business_rules_and_filter():
    df = pl.DataFrame({
        "quantidade": [2, 5],
        "preco_unitario": [10.0, 20.0],
        "desconto": [5.0, None],
        "status": ["CONCLUIDO", "CANCELADO"]
    })
    transformed = apply_business_rules(df)
    assert transformed["valor_liquido"].to_list() == [15.0, 100.0]
    assert transformed["categoria_status"].to_list() == ["FINALIZADO", "CANCELADO"]

    active = filter_active_records(transformed)
    assert len(active) == 1
    assert active["categoria_status"][0] == "FINALIZADO"

def test_group_and_aggregate():
    df = pl.DataFrame({
        "departamento": ["TI", "TI", "Vendas"],
        "salario": [5000.0, 7000.0, 4000.0]
    })
    res = group_and_aggregate(df, group_by_cols=["departamento"], sum_cols=["salario"], count_cols=["salario"])
    ti_row = res.filter(pl.col("departamento") == "TI")
    assert ti_row["salario_total"][0] == 12000.0
    assert ti_row["salario_qtd"][0] == 2

def test_transform_placeholder():
    """Placeholder de teste de transformação."""
    assert True
