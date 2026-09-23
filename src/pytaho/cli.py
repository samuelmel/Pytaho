import sys
from pathlib import Path
import typer
from pytaho.parser.ktr_parser import KTRParser
from pytaho.parser.kjb_parser import KJBParser
from pytaho.generator.code_builder import PythonCodeBuilder

app = typer.Typer(
    name="pytaho",
    help="Transpilador de XML Pentaho (.ktr/.kjb) para Scripts Python POO com auto-detecção de banco de dados.",
    no_args_is_help=True
)

@app.command("convert")
def convert(
    file_path: str = typer.Argument(..., help="Caminho do arquivo Pentaho .ktr ou .kjb"),
    output: str = typer.Option(None, "--output", "-o", help="Caminho do arquivo Python de saída (.py)"),
):
    """
    Converte um arquivo Pentaho XML (.ktr/.kjb) em um script Python POO modular.
    """
    input_path = Path(file_path)
    if not input_path.exists():
        typer.secho(f"Erro: Arquivo '{file_path}' não encontrado.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    if not output:
        output = input_path.with_suffix(".py")

    output_path = Path(output)
    typer.echo(f"🔍 Analisando arquivo Pentaho: {input_path.name}...")

    if input_path.suffix.lower() == ".ktr":
        parser = KTRParser(input_path)
        transformation = parser.parse()

        typer.echo(f"✅ Transformação '{transformation.name}' analisada com sucesso.")
        typer.echo(f"   - Conexões detectadas: {len(transformation.connections)}")
        for conn in transformation.connections:
            typer.echo(f"     • Conexão '{conn.name}' -> Banco: {conn.normalized_type}")
        typer.echo(f"   - Steps detectados: {len(transformation.steps)}")

        builder = PythonCodeBuilder(transformation)
        result_file = builder.write_to_file(output_path)
        typer.secho(f"🚀 Script Python POO gerado com sucesso em: {result_file}", fg=typer.colors.GREEN)

    elif input_path.suffix.lower() == ".kjb":
        parser = KJBParser(input_path)
        job = parser.parse()
        typer.echo(f"✅ Job '{job.name}' analisado com sucesso.")
        typer.echo(f"   - Entradas no Job: {len(job.entries)}")

    else:
        typer.secho("Erro: O arquivo fornecido precisa ter extensão .ktr ou .kjb", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

@app.command("version")
def version():
    """Exibe a versão atual do Pytaho."""
    typer.echo("Pytaho Converter v0.1.0")

def main():
    app()

if __name__ == "__main__":
    main()
