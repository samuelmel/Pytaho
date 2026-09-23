from pytaho.parser.models import PentahoConnection
from pytaho.dialects import get_dialect_adapter, OracleDialectAdapter

def test_oracle_dialect_autodetect():
    conn = PentahoConnection(
        name="ProdOracle",
        type="ORACLE",
        server="oracle.empresa.com",
        database="PRODDW",
        port="1521",
        username="db_user",
        password="secret_password"
    )

    adapter = get_dialect_adapter(conn)
    assert isinstance(adapter, OracleDialectAdapter)
    assert adapter.db_type_name == "Oracle"
    assert adapter.driver_package == "oracledb"

    code = adapter.generate_connection_code()
    assert "class OracleDatabaseConnection" in code
    assert "oracledb.connect" in code
    assert "oracle.empresa.com" in code
    assert "oracle+oracledb://" in code

