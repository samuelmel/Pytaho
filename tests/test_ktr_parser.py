from pathlib import Path
from pytaho.parser.ktr_parser import KTRParser

def test_parse_oracle_ktr():
    sample_file = Path("sample_pentaho_files/exemplo_oracle.ktr")
    assert sample_file.exists()

    parser = KTRParser(sample_file)
    trans = parser.parse()

    assert trans.name == "etl_vendas_oracle"
    assert len(trans.connections) == 1

    conn = trans.connections[0]
    assert conn.name == "OracleDW"
    assert conn.normalized_type == "ORACLE"
    assert conn.server == "10.0.0.50"
    assert conn.database == "ORCLDW"
    assert conn.port == "1521"

    assert len(trans.steps) == 3
    step_names = [s.name for s in trans.steps]
    assert "Extrair Vendas Oracle" in step_names
    assert "Tratar Campos Venda" in step_names
    assert "Carregar DW Oracle" in step_names

    assert len(trans.hops) == 2

