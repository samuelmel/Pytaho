import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union
from pytaho.parser.models import PentahoHop, PentahoJob, PentahoJobEntry

class KJBParser:
    """
    Parser para arquivos de Job do Pentaho (.kjb).
    Extrai entradas (entries) do job e fluxo de controle.
    """

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)

    def parse(self) -> PentahoJob:
        """Lê o arquivo XML .kjb e gera o modelo de dados AST."""
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        name = root.findtext("./name", default=self.file_path.stem)
        description = root.findtext("./description", default="")

        entries = self._parse_entries(root)
        hops = self._parse_hops(root)

        return PentahoJob(
            name=name,
            description=description,
            entries=entries,
            hops=hops,
        )

    def _parse_entries(self, root: ET.Element) -> list[PentahoJobEntry]:
        entries = []
        for entry_elem in root.findall("./entries/entry"):
            name = entry_elem.findtext("name", default="")
            entry_type = entry_elem.findtext("type", default="")
            filename = entry_elem.findtext("filename", default="")
            transname = entry_elem.findtext("transname", default="")

            entries.append(
                PentahoJobEntry(
                    name=name,
                    type=entry_type,
                    filename=filename,
                    transname=transname,
                )
            )
        return entries

    def _parse_hops(self, root: ET.Element) -> list[PentahoHop]:
        hops = []
        for hop_elem in root.findall("./hops/hop"):
            from_entry = hop_elem.findtext("from", default="")
            to_entry = hop_elem.findtext("to", default="")
            enabled_str = hop_elem.findtext("enabled", default="Y")
            enabled = enabled_str.upper() in ["Y", "TRUE", "1"]

            if from_entry and to_entry:
                hops.append(
                    PentahoHop(
                        from_step=from_entry,
                        to_step=to_entry,
                        enabled=enabled,
                    )
                )
        return hops

