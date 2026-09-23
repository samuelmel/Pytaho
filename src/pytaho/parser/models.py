from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PentahoConnection(BaseModel):
    """Modelo que representa uma conexão de banco de dados do Pentaho."""
    name: str
    server: Optional[str] = None
    type: str  # ORACLE, POSTGRESQL, MSSQL, MYSQL, SQLITE, etc.
    access: Optional[str] = "Native"  # Native (JDBC), OCI, JNDI
    database: Optional[str] = None
    port: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    attributes: Dict[str, str] = Field(default_factory=dict)

    @property
    def normalized_type(self) -> str:
        """Retorna o tipo de banco de dados padronizado em maiúsculas."""
        t = (self.type or "").upper().strip()
        if "ORACLE" in t:
            return "ORACLE"
        elif "POSTGRES" in t:
            return "POSTGRESQL"
        elif "MSSQL" in t or "SQLSERVER" in t:
            return "MSSQL"
        elif "MYSQL" in t or "MARIADB" in t:
            return "MYSQL"
        return t or "GENERIC"

class PentahoStep(BaseModel):
    """Modelo que representa um passo (Step) de uma transformação Pentaho."""
    name: str
    type: str  # TableInput, TableOutput, SelectValues, FilterRows, Dummy, ExecSQL, REST, etc.
    connection: Optional[str] = None
    sql: Optional[str] = None
    table_name: Optional[str] = None
    schema_name: Optional[str] = None
    commit_size: Optional[int] = 1000
    fields: List[Dict[str, str]] = Field(default_factory=list)
    raw_xml_attributes: Dict[str, str] = Field(default_factory=dict)

class PentahoHop(BaseModel):
    """Modelo que representa a transição (Hop) entre dois passos ou jobs no Pentaho."""
    from_step: str
    to_step: str
    enabled: bool = True

class PentahoTransformation(BaseModel):
    """Modelo AST completo de uma Transformação Pentaho (.ktr)."""
    name: str = "transformation"
    description: Optional[str] = None
    connections: List[PentahoConnection] = Field(default_factory=list)
    steps: List[PentahoStep] = Field(default_factory=list)
    hops: List[PentahoHop] = Field(default_factory=list)

    def get_connection(self, name: str) -> Optional[PentahoConnection]:
        """Busca conexão pelo nome."""
        for conn in self.connections:
            if conn.name == name:
                return conn
        return None

class PentahoJobEntry(BaseModel):
    """Modelo que representa uma entrada de Job (.kjb) do Pentaho."""
    name: str
    type: str  # SPECIAL (START), TRANS, JOB, EVAL, MAIL, DUMMY
    filename: Optional[str] = None
    transname: Optional[str] = None
    raw_xml: Dict[str, str] = Field(default_factory=dict)

class PentahoJob(BaseModel):
    """Modelo AST completo de um Job Pentaho (.kjb)."""
    name: str = "job"
    description: Optional[str] = None
    connections: List[PentahoConnection] = Field(default_factory=list)
    entries: List[PentahoJobEntry] = Field(default_factory=list)
    hops: List[PentahoHop] = Field(default_factory=list)

