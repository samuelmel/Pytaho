import polars as pl
from src.extract.file_reader import FileReader
"""
test_extract.py - Testes unitários para os módulos de extração de dados.
"""

def test_read_csv(tmp_path):
    # Cria arquivo CSV temporário de teste
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("id,nome,valor\n1,Alice,100.50\n2,Bob,200.00\n", encoding="utf-8")

    df = FileReader.read_csv(csv_file)
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (2, 3)
    assert df["id"].to_list() == [1, 2]
    assert df["nome"].to_list() == ["Alice", "Bob"]

def test_extract_placeholder():
    """Placeholder de teste de extração."""
    assert True
