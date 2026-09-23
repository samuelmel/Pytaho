from pytaho.dialects.base_dialect import BaseDialectAdapter

class MSSQLDialectAdapter(BaseDialectAdapter):
    """Adaptador para SQL Server (pyodbc)."""

    @property
    def db_type_name(self) -> str:
        return "SQL Server"

    @property
    def driver_package(self) -> str:
        return "pyodbc"

    def generate_connection_code(self) -> str:
        host = self.connection.server or "localhost"
        port = self.connection.port or "1433"
        db = self.connection.database or "master"
        user = self.connection.username or "sa"
        pwd = self.connection.password or "secret"

        return f'''class MSSQLDatabaseConnection:
    """Gerenciador de conexão com SQL Server usando pyodbc e SQLAlchemy."""

    def __init__(self, host: str = "{host}", port: str = "{port}", database: str = "{db}", user: str = "{user}", password: str = "{pwd}"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def get_sqlalchemy_engine(self):
        from sqlalchemy import create_engine
        url = f"mssql+pyodbc://{{self.user}}:{{self.password}}@{{self.host}}:{{self.port}}/{{self.database}}?driver=ODBC+Driver+17+for+SQL+Server"
        return create_engine(url, pool_pre_ping=True)
'''

    def generate_sqlalchemy_url(self) -> str:
        host = self.connection.server or "localhost"
        port = self.connection.port or "1433"
        db = self.connection.database or "master"
        user = self.connection.username or "sa"
        pwd = self.connection.password or "secret"
        return f"mssql+pyodbc://{user}:{pwd}@{host}:{port}/{db}?driver=ODBC+Driver+17+for+SQL+Server"

