from pytaho.dialects.base_dialect import BaseDialectAdapter

class PostgreSQLDialectAdapter(BaseDialectAdapter):
    """Adaptador para Banco de Dados PostgreSQL (psycopg3)."""

    @property
    def db_type_name(self) -> str:
        return "PostgreSQL"

    @property
    def driver_package(self) -> str:
        return "psycopg"

    def generate_connection_code(self) -> str:
        host = self.connection.server or "localhost"
        port = self.connection.port or "5432"
        db = self.connection.database or "postgres"
        user = self.connection.username or "postgres"
        pwd = self.connection.password or "postgres"

        return f'''class PostgresDatabaseConnection:
    """Gerenciador de conexão PostgreSQL usando psycopg e SQLAlchemy 2.0."""

    def __init__(self, host: str = "{host}", port: str = "{port}", database: str = "{db}", user: str = "{user}", password: str = "{pwd}"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def get_sqlalchemy_engine(self):
        from sqlalchemy import create_engine
        url = f"postgresql+psycopg://{{self.user}}:{{self.password}}@{{self.host}}:{{self.port}}/{{self.database}}"
        return create_engine(url, pool_pre_ping=True)
'''

    def generate_sqlalchemy_url(self) -> str:
        host = self.connection.server or "localhost"
        port = self.connection.port or "5432"
        db = self.connection.database or "postgres"
        user = self.connection.username or "postgres"
        pwd = self.connection.password or "postgres"
        return f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"

