import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union
from pytaho.parser.models import (
    PentahoConnection,
    PentahoHop,
    PentahoStep,
    PentahoTransformation,
)

class KTRParser:
    """
    Parser para arquivos de Transformação do Pentaho (.ktr).
    Extrai conexões de banco de dados, passos (steps) e fluxo de dados (hops).
    """

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)

    def parse(self) -> PentahoTransformation:
        """Lê o arquivo XML .ktr e gera o modelo de dados AST."""
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        name = root.findtext("./info/name", default=self.file_path.stem)
        description = root.findtext("./info/description", default="")

        connections = self._parse_connections(root)
        steps = self._parse_steps(root)
        hops = self._parse_hops(root)

        return PentahoTransformation(
            name=name,
            description=description,
            connections=connections,
            steps=steps,
            hops=hops,
        )

    def _parse_connections(self, root: ET.Element) -> list[PentahoConnection]:
        connections = []
        for conn_elem in root.findall("connection"):
            name = conn_elem.findtext("name", default="")
            server = conn_elem.findtext("server", default="")
            type_str = conn_elem.findtext("type", default="GENERIC")
            access = conn_elem.findtext("access", default="Native")
            database = conn_elem.findtext("database", default="")
            port = conn_elem.findtext("port", default="")
            username = conn_elem.findtext("username", default="")
            password = conn_elem.findtext("password", default="")

            attributes = {}
            for attr in conn_elem.findall("./attributes/attribute"):
                code = attr.findtext("code", default="")
                attribute = attr.findtext("attribute", default="")
                if code:
                    attributes[code] = attribute

            connections.append(
                PentahoConnection(
                    name=name,
                    server=server,
                    type=type_str,
                    access=access,
                    database=database,
                    port=port,
                    username=username,
                    password=password,
                    attributes=attributes,
                )
            )
        return connections

    def _parse_steps(self, root: ET.Element) -> list[PentahoStep]:
        steps = []
        for step_elem in root.findall("step"):
            name = step_elem.findtext("name", default="")
            step_type = step_elem.findtext("type", default="")
            connection = step_elem.findtext("connection", default="")
            sql = step_elem.findtext("sql", default="")
            table_name = step_elem.findtext("table", default="")
            schema_name = step_elem.findtext("schema", default="")
            commit_size_str = step_elem.findtext("commit", default="1000")

            try:
                commit_size = int(commit_size_str)
            except ValueError:
                commit_size = 1000

            # Parse de campos selecionados / alterados
            fields = []
            for field in step_elem.findall("./fields/field"):
                f_name = field.findtext("name", default="")
                f_rename = field.findtext("rename", default="")
                f_type = field.findtext("type", default="")
                fields.append({"name": f_name, "rename": f_rename, "type": f_type})

            steps.append(
                PentahoStep(
                    name=name,
                    type=step_type,
                    connection=connection,
                    sql=sql,
                    table_name=table_name,
                    schema_name=schema_name,
                    commit_size=commit_size,
                    fields=fields,
                )
            )
        return steps

    def _parse_hops(self, root: ET.Element) -> list[PentahoHop]:
        hops = []
        for hop_elem in root.findall("./order/hop"):
            from_step = hop_elem.findtext("from", default="")
            to_step = hop_elem.findtext("to", default="")
            enabled_str = hop_elem.findtext("enabled", default="Y")
            enabled = enabled_str.upper() in ["Y", "TRUE", "1"]

            if from_step and to_step:
                hops.append(
                    PentahoHop(
                        from_step=from_step,
                        to_step=to_step,
                        enabled=enabled,
                    )
                )
        return hops

