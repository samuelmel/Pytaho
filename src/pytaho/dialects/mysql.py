from pytaho.dialects.base_dialect import BaseDialectAdapter

class MySQLDialectAdapter(BaseDialectAdapter):
    """Adaptador para MySQL / MariaDB."""

    @property
    def db_type_name(self) -> str:
        return "MySQL"

    @property
    def driver_package(self) -> str:
        return "pymysql"

    def generate_connection_code(self) -> str:
        host = self.connection.server or "localhost"
        port = self.connection.port or "3306"
        db = self.connection.database or "mysql"
        user = self.connection.username or "root"
        pwd = self.connection.password or "root"

        return f'''class MySQLDatabaseConnection:
    """Gerenciador de conexão com MySQL usando PyMySQL e SQLAlchemy."""

    def __init__(self, host: str = "{host}", port: str = "{port}", database: str = "{db}", user: str = "{user}", password: str = "{pwd}"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def get_sqlalchemy_engine(self):
        from sqlalchemy import create_engine
        url = f"mysql+pymysql://{{self.user}}:{{self.password}}@{{self.host}}:{{self.port}}/{{self.database}}"
        return create_engine(url, pool_pre_ping=True)
'''

    def generate_sqlalchemy_url(self) -> str:
        host = self.connection.server or "localhost"
        port = self.connection.port or "3306"
        db = self.connection.database or "mysql"
        user = self.connection.username or "root"
        pwd = self.connection.password or "root"
        return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"

