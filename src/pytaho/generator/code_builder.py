from pathlib import Path
from typing import Union
from pytaho.parser.models import PentahoTransformation
from pytaho.dialects import get_dialect_adapter
from pytaho.generator.step_mappers import StepCodeMapper

class PythonCodeBuilder:
    """
    Construtor principal de Código Python POO a partir da AST do Pentaho.
    Gerencia imports, conexões de banco (auto-detectando Oracle, Postgres, etc.),
    classes POO de extratores, transformadores, joiners, carregadores e a pipeline orquestradora.
    """

    def __init__(self, transformation: PentahoTransformation):
        self.transformation = transformation

    def build_python_script(self) -> str:
        """Gera o script Python POO completo em formato de texto."""
        sections = []
        sections.append(self._build_header())
        sections.append(self._build_database_connections())
        sections.append(self._build_step_classes())
        sections.append(self._build_pipeline_runner())
        sections.append(self._build_main_block())
        return "\n\n".join(sections)

    def write_to_file(self, output_path: Union[str, Path]) -> Path:
        """Salva o script Python gerado em um arquivo físico."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        code = self.build_python_script()
        path.write_text(code, encoding="utf-8")
        return path

    def _build_header(self) -> str:
        return f'''# ==============================================================================
# Script Python POO Gerado Automaticamente pelo Pytaho Converter
# Origem Pentaho: {self.transformation.name}
# ==============================================================================
import os
import logging
import polars as pl
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Configuração de Logger Estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s - %(message)s"
)
logger = logging.getLogger("pytaho_pipeline")'''

    def _build_database_connections(self) -> str:
        code_blocks = []
        for conn in self.transformation.connections:
            adapter = get_dialect_adapter(conn)
            code_blocks.append(adapter.generate_connection_code())

        if not code_blocks:
            return "# Nenhum banco de dados configurado explicitamente no XML."
        return "\n\n".join(code_blocks)

    def _build_step_classes(self) -> str:
        code_blocks = []
        for step in self.transformation.steps:
            stype = step.type.lower()
            if "tableinput" in stype or "input" in stype:
                code_blocks.append(StepCodeMapper.generate_extractor_class(step, self.transformation))
            elif "tableoutput" in stype or "output" in stype:
                code_blocks.append(StepCodeMapper.generate_loader_class(step, self.transformation))
            elif "lookup" in stype or "join" in stype or "merge" in stype:
                code_blocks.append(StepCodeMapper.generate_joiner_class(step))
            else:
                code_blocks.append(StepCodeMapper.generate_transformer_class(step))
        return "\n\n".join(code_blocks)

    def _build_pipeline_runner(self) -> str:
        conn_inits = []
        for conn in self.transformation.connections:
            adapter = get_dialect_adapter(conn)
            var_name = f"db_{conn.name.lower().replace(' ', '_')}"
            if adapter.db_type_name == "Oracle":
                conn_inits.append(f"        self.{var_name} = OracleDatabaseConnection()")
            elif adapter.db_type_name == "PostgreSQL":
                conn_inits.append(f"        self.{var_name} = PostgresDatabaseConnection()")
            elif adapter.db_type_name == "SQL Server":
                conn_inits.append(f"        self.{var_name} = MSSQLDatabaseConnection()")
            elif adapter.db_type_name == "MySQL":
                conn_inits.append(f"        self.{var_name} = MySQLDatabaseConnection()")
            else:
                conn_inits.append(f"        self.{var_name} = PostgresDatabaseConnection()")

        step_inits = []
        step_execs = []
        extracted_dfs = []

        for idx, step in enumerate(self.transformation.steps):
            stype = step.type.lower()
            class_base = f"{step.name.replace(' ', '')}"
            var_conn = f"self.db_{step.connection.lower().replace(' ', '_')}" if step.connection else "None"

            if "input" in stype:
                step_inits.append(f"        self.extractor_{idx} = {class_base}Extractor({var_conn})")
                df_var = f"df_extracted_{len(extracted_dfs)}"
                step_execs.append(f"        {df_var} = self.extractor_{idx}.extract()")
                extracted_dfs.append(df_var)

            elif "lookup" in stype or "join" in stype or "merge" in stype:
                step_inits.append(f"        self.joiner_{idx} = {class_base}Joiner()")
                if len(extracted_dfs) >= 2:
                    step_execs.append(f"        df_joined = self.joiner_{idx}.join({extracted_dfs[0]}, {extracted_dfs[1]})")
                elif len(extracted_dfs) == 1:
                    step_execs.append(f"        df_joined = self.joiner_{idx}.join({extracted_dfs[0]}, {extracted_dfs[0]})")
                else:
                    step_execs.append(f"        df_joined = self.joiner_{idx}.join(df_left, df_right)")

            elif "output" in stype:
                step_inits.append(f"        self.loader_{idx} = {class_base}Loader({var_conn})")
                load_src = "df_joined" if "df_joined" in "\n".join(step_execs) else (extracted_dfs[-1] if extracted_dfs else "df_data")
                step_execs.append(f"        rows_loaded = self.loader_{idx}.load({load_src})")

            else:
                step_inits.append(f"        self.transformer_{idx} = {class_base}Transformer()")
                trans_src = "df_joined" if "df_joined" in "\n".join(step_execs) else (extracted_dfs[-1] if extracted_dfs else "df_data")
                step_execs.append(f"        df_transformed = self.transformer_{idx}.transform({trans_src})")

        inits_str = "\n".join(conn_inits + step_inits) if (conn_inits or step_inits) else "        pass"
        execs_str = "\n".join(step_execs) if step_execs else "        pass"

        return f'''class {self.transformation.name.replace(" ", "")}Pipeline:
    """
    Pipeline Principal POO responsável por orquestrar a execução do fluxo:
    Extract -> Transform / Join -> Load
    """
    def __init__(self):
{inits_str}

    def run(self):
        logger.info("Iniciando execução da Pipeline '{self.transformation.name}'...")
{execs_str}
        logger.info("Execução da Pipeline concluída com sucesso!")'''

    def _build_main_block(self) -> str:
        pipeline_class = f"{self.transformation.name.replace(' ', '')}Pipeline"
        return f'''if __name__ == "__main__":
    pipeline = {pipeline_class}()
    pipeline.run()'''
