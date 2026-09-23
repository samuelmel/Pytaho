import ast
from pathlib import Path
from pytaho.parser.ktr_parser import KTRParser
from pytaho.generator.code_builder import PythonCodeBuilder

def test_generate_python_code_from_oracle_ktr():
    sample_file = Path("sample_pentaho_files/exemplo_oracle.ktr")
    parser = KTRParser(sample_file)
    trans = parser.parse()

    builder = PythonCodeBuilder(trans)
    python_code = builder.build_python_script()

    # Validação de Sintaxe do código gerado usando AST
    parsed_ast = ast.parse(python_code)
    assert parsed_ast is not None

    assert "class OracleDatabaseConnection:" in python_code
    assert "class ExtrairVendasOracleExtractor:" in python_code
    assert "class TratarCamposVendaTransformer:" in python_code
    assert "class CarregarDWOracleLoader:" in python_code
    assert "oracledb" in python_code

def test_generate_python_code_from_postgres_join_ktr():
    sample_file = Path("sample_pentaho_files/exemplo_postgres_join.ktr")
    parser = KTRParser(sample_file)
    trans = parser.parse()

    builder = PythonCodeBuilder(trans)
    python_code = builder.build_python_script()

    # Validação de Sintaxe
    parsed_ast = ast.parse(python_code)
    assert parsed_ast is not None

    assert "class PostgresDatabaseConnection:" in python_code
    assert "class ExtrairClientesAtivosExtractor:" in python_code
    assert "class ExtrairPedidosRecentesExtractor:" in python_code
    assert "class JuntarClientesePedidosJoiner:" in python_code
    assert "class CarregarDWPedidosConsolidadosLoader:" in python_code
    assert "psycopg" in python_code
