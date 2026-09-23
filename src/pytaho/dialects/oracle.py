from pytaho.dialects.base_dialect import BaseDialectAdapter

class OracleDialectAdapter(BaseDialectAdapter):
    """
    Adaptador específico para Banco de Dados Oracle.
    Traduz conexões JDBC Oracle do Pentaho para `oracledb` (Thin Mode) e SQLAlchemy 2.0.
    """

    @property
    def db_type_name(self) -> str:
        return "Oracle"

    @property
    def driver_package(self) -> str:
        return "oracledb"

    def generate_connection_code(self) -> str:
        host = self.connection.server or "localhost"
        port = self.connection.port or "1521"
        db = self.connection.database or "ORCL"
        user = self.connection.username or "system"
        pwd = self.connection.password or "oracle"

        return f'''class OracleDatabaseConnection:
    """Gerenciador de conexão com Banco de Dados Oracle usando oracledb em Thin Mode."""

    def __init__(self, host: str = "{host}", port: str = "{port}", service_name: str = "{db}", user: str = "{user}", password: str = "{pwd}"):
        self.host = host
        self.port = port
        self.service_name = service_name
        self.user = user
        self.password = password

    def get_dsn(self) -> str:
        return f"{{self.host}}:{{self.port}}/{{self.service_name}}"

    def get_connection(self):
        import oracledb
        # Inicia a conexão oracledb em Thin Mode (não exige Oracle Instant Client)
        return oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.get_dsn()
        )

    def get_sqlalchemy_engine(self):
        from sqlalchemy import create_engine
        url = f"oracle+oracledb://{{self.user}}:{{self.password}}@{{self.host}}:{{self.port}}/?service_name={{self.service_name}}"
        return create_engine(url, pool_pre_ping=True)
'''

    def generate_sqlalchemy_url(self) -> str:
        host = self.connection.server or "localhost"
        port = self.connection.port or "1521"
        db = self.connection.database or "ORCL"
        user = self.connection.username or "system"
        pwd = self.connection.password or "oracle"
        return f"oracle+oracledb://{user}:{pwd}@{host}:{port}/?service_name={db}"

    def adapt_sql_query(self, sql_query: str) -> str:
        """Adapta consultas nativas Oracle do Pentaho para o código gerado."""
        query = sql_query.strip()
        # Tratamento simples de quebras ou maiúsculas para manter compatibilidade
        return query

