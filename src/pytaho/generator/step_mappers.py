from pytaho.parser.models import PentahoStep, PentahoTransformation
from pytaho.dialects import get_dialect_adapter

class StepCodeMapper:
    """
    Mapeador responsável por traduzir steps individuais do Pentaho
    em classes Python POO com Polars.
    """

    @staticmethod
    def generate_extractor_class(step: PentahoStep, transformation: PentahoTransformation) -> str:
        """Gera classe POO Extratora (ex: para TableInput)."""
        class_name = f"{step.name.replace(' ', '')}Extractor"
        conn_name = step.connection or ""
        conn_obj = transformation.get_connection(conn_name)

        if conn_obj:
            adapter = get_dialect_adapter(conn_obj)
            db_type = adapter.db_type_name
        else:
            db_type = "Banco de Dados"

        sql_clean = (step.sql or "SELECT * FROM dual").replace('"', '\\"').strip()

        return f'''class {class_name}:
    """
    Extrator de dados gerado a partir do step Pentaho: '{step.name}'
    Fonte de Dados: {db_type} ({conn_name})
    """
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.query = """{sql_clean}"""

    def extract(self) -> "pl.DataFrame":
        import polars as pl
        logger.info("Executando extração do step '{step.name}'...")
        engine = self.db_connection.get_sqlalchemy_engine()
        return pl.read_database(query=self.query, connection=engine)
'''

    @staticmethod
    def generate_transformer_class(step: PentahoStep) -> str:
        """Gera classe POO de Transformação (ex: para SelectValues, StringOperations)."""
        class_name = f"{step.name.replace(' ', '')}Transformer"

        renames = {}
        for f in step.fields:
            if f.get("name") and f.get("rename"):
                renames[f["name"]] = f["rename"]

        return f'''class {class_name}:
    """
    Transformador de dados gerado a partir do step Pentaho: '{step.name}' (Tipo: {step.type})
    """
    def __init__(self):
        self.rename_mapping = {renames}

    def transform(self, df: "pl.DataFrame") -> "pl.DataFrame":
        import polars as pl
        logger.info("Aplicando transformações do step '{step.name}'...")
        if self.rename_mapping:
            df = df.rename({{k: v for k, v in self.rename_mapping.items() if k in df.columns}})
        return df
'''

    @staticmethod
    def generate_joiner_class(step: PentahoStep) -> str:
        """Gera classe POO de Junção / Join (ex: para StreamLookup, MergeJoin)."""
        class_name = f"{step.name.replace(' ', '')}Joiner"
        join_key = "id_cliente"
        if step.fields and len(step.fields) > 0 and step.fields[0].get("name"):
            join_key = step.fields[0]["name"]

        return f'''class {class_name}:
    """
    Unificador/Joiner de dados gerado a partir do step Pentaho: '{step.name}' (Tipo: {step.type})
    Realiza o cruzamento (Join) em memória entre DataFrames.
    """
    def __init__(self, join_key: str = "{join_key}", how: str = "inner"):
        self.join_key = join_key
        self.how = how

    def join(self, df_left: "pl.DataFrame", df_right: "pl.DataFrame") -> "pl.DataFrame":
        import polars as pl
        logger.info(f"Executando Join entre DataFrames pela chave '{{self.join_key}}'...")
        return df_left.join(df_right, on=self.join_key, how=self.how)
'''

    @staticmethod
    def generate_loader_class(step: PentahoStep, transformation: PentahoTransformation) -> str:
        """Gera classe POO Carregadora (ex: para TableOutput)."""
        class_name = f"{step.name.replace(' ', '')}Loader"
        table = step.table_name or "tb_output"
        conn_name = step.connection or ""

        return f'''class {class_name}:
    """
    Carregador de dados gerado a partir do step Pentaho: '{step.name}'
    Tabela Destino: {table} ({conn_name})
    """
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.table_name = "{table}"

    def load(self, df: "pl.DataFrame") -> int:
        import polars as pl
        if df.is_empty():
            logger.warning("DataFrame vazio. Nenhuma linha carregada.")
            return 0
        logger.info(f"Carregando {{len(df)}} registros na tabela {{self.table_name}}...")
        engine = self.db_connection.get_sqlalchemy_engine()
        df.write_database(table_name=self.table_name, connection=engine, if_table_exists="append")
        return len(df)
'''
