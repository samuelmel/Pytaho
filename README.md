
<div align="center">

# 🚀 Pytaho
### *Pentaho XML (`.ktr` / `.kjb`) to Modern Python OOP Transpiler*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Engine: Polars](https://img.shields.io/badge/Data%20Engine-Polars-CD7F32.svg)](https://pola.rs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Migre seus pipelines legados do Pentaho Data Integration (PDI) para código Python modular, performático e legível em segundos.**

</div>

---

## 🌟 Principais Funcionalidades

1. **Parser de Arquivos Pentaho XML (`.ktr` / `.kjb`)**:
   - Lê e analisa a estrutura de transformações e jobs, extraindo conexões de banco de dados (`<connection>`), passos (`<step>`), fluxo de dados (`<order>` / hops) e variáveis.

2. **Auto-Detecção de Banco de Dados & Dialetos**:
   - Identifica automaticamente o banco de dados configurado no Pentaho (ex: `ORACLE`, `POSTGRESQL`, `MSSQL`, `MYSQL`).
   - **Suporte Nativo a Oracle**: Converte conexões JDBC do Pentaho em código Python moderno utilizando a biblioteca **`oracledb`** (em *Thin Mode*, dispensando instalação do Oracle Instant Client) e **SQLAlchemy 2.0**.

3. **Geração de Código Python com Orientação a Objetos (POO)**:
   - Traduz os passos do Pentaho em classes desacopladas, legíveis e modulares:
     - **Conexões**: Classes gerenciadoras de sessão (ex: `OracleDatabaseConnection`).
     - **Input Steps**: Classes Extratoras (ex: `ExtrairVendasExtractor`).
     - **Transform Steps**: Classes Transformadoras (ex: `TratarCamposTransformer`).
     - **Output Steps**: Classes Carregadoras (ex: `CarregarDWLoader`).
     - **Pipeline Orchestrator**: Classe orquestradora principal (ex: `PipelineVendas`).
   - Utiliza o motor analítico **Polars** no código gerado para processamento de alta performance em memória.

4. **Interface de Linha de Comando (CLI)**:
   - Transcreva seus arquivos do Pentaho em segundos através do terminal:

```bash
pytaho convert sample_pentaho_files/exemplo_oracle.ktr -o pipelines/vendas_oracle.py
````

---

## 📌 Por que usar?

* **Zero Lock-in:** Abandone interfaces gráficas pesadas e execute seus pipelines nativamente em containers Docker, Airflow ou GitHub Actions.
* **Alta Performance:** Substitua o processamento Java do Pentaho pela velocidade nativa do motor em Rust do **Polars**.
* **Código Limpo & POO:** Geração de classes totalmente desacopladas (Extractors, Transformers, Loaders) com tipagem estática.
* **Segurança Nativa:** Variáveis de conexão e segredos são parametrizados automaticamente para variáveis de ambiente (`.env`).

---

## ⚡ Quickstart

### 1. Instalação das Dependências

Eu recomendo o uso do [`uv`](https://github.com/astral-sh/uv) pela velocidade, mas você pode utilizar o `pip` tradicional:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pytaho.git
cd pytaho

# Usando uv:
uv venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Ou usando pip:
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Converter um Arquivo `.ktr` ou `.kjb` do Pentaho

Execute o comando `convert` passando o arquivo de origem e o arquivo Python de destino desejado:

```bash
python -m pytaho.cli convert sample_pentaho_files/exemplo_oracle.ktr -o pipelines/vendas_oracle.py
```

---

## 💻 Exemplo de Código Gerado (Output POO)

Ao transcrever um `.ktr` com banco **Oracle**, o Pytaho gera automaticamente um script estruturado em POO, totalmente seguro e legível:

```python
import os
import logging
import polars as pl
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
logger = logging.getLogger("pytaho_pipeline")


class OracleDatabaseConnection:
    """Gerenciador de conexão Oracle desacoplado (oracledb Thin Mode)."""
    
    def __init__(self):
        self.host = os.getenv("ORACLE_HOST", "localhost")
        self.port = os.getenv("ORACLE_PORT", "1521")
        self.service = os.getenv("ORACLE_SERVICE", "ORCL")
        self.user = os.getenv("ORACLE_USER")
        self.password = os.getenv("ORACLE_PASSWORD")

    def get_engine(self):
        url = f"oracle+oracledb://{self.user}:{self.password}@{self.host}:{self.port}/?service_name={self.service}"
        return create_engine(url, pool_pre_ping=True)


class ExtrairVendasExtractor:
    """Extração de dados gerada a partir do step Pentaho: 'Extrair Vendas Oracle'"""
    
    def __init__(self, db_conn: OracleDatabaseConnection):
        self.db = db_conn
        self.query = "SELECT id_venda, cd_cliente, vl_total FROM tb_vendas WHERE status = 'APROVADO'"

    def extract(self) -> pl.DataFrame:
        logger.info("Iniciando extração na base Oracle...")
        return pl.read_database(query=self.query, connection=self.db.get_engine())


class TratarCamposTransformer:
    """Transformação de dados gerada a partir do step Pentaho: 'Tratar Campos Venda'"""
    
    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        logger.info("Aplicando transformações nos dados...")
        return df.rename({"id_venda": "venda_id", "cd_cliente": "cliente_id"})


class CarregarDWLoader:
    """Carga de dados gerada a partir do step Pentaho: 'Carregar DW Oracle'"""
    
    def __init__(self, db_conn: OracleDatabaseConnection):
        self.db = db_conn
        self.target_table = "fact_vendas"

    def load(self, df: pl.DataFrame) -> int:
        logger.info(f"Carregando {len(df)} registros na tabela {self.target_table}...")
        df.write_database(
            table_name=self.target_table,
            connection=self.db.get_engine(),
            if_table_exists="append"
        )
        return len(df)


class PipelineVendas:
    """Orquestrador do Fluxo de Dados (DAG)."""
    
    def __init__(self):
        self.db = OracleDatabaseConnection()
        self.extractor = ExtrairVendasExtractor(self.db)
        self.transformer = TratarCamposTransformer()
        self.loader = CarregarDWLoader(self.db)

    def run(self):
        logger.info("Iniciando execução do pipeline...")
        df_raw = self.extractor.extract()
        df_clean = self.transformer.transform(df_raw)
        rows_inserted = self.loader.load(df_clean)
        logger.info(f"Pipeline finalizado com sucesso. Registros inseridos: {rows_inserted}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pipeline = PipelineVendas()
    pipeline.run()
```

---

## 🛠️ Conectores & Dialetos Suportados

| Banco de Dados | Driver Python Nativo   | Suporte no Pytaho |
| -------------- | ---------------------- | ----------------- |
| **Oracle**     | `oracledb` (Thin Mode) | ✅ Nativo          |
| **PostgreSQL** | `psycopg3`             | ✅ Nativo          |
| **SQL Server** | `pyodbc` / `pymssql`   | ✅ Nativo          |
| **MySQL**      | `pymysql`              | ✅ Nativo          |

---

## 🧪 Executando os Testes Automatizados

Para validar o parser XML, a detecção de dialetos e a sintaxe do código gerado:

```bash
pytest -v
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
```
