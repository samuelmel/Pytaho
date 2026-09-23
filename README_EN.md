🇧🇷 [Português](README.md) | 🇺🇸 English

<div align="center">

# 🚀 Pytaho
### *Pentaho XML (`.ktr` / `.kjb`) to Modern Python OOP Transpiler*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Engine: Polars](https://img.shields.io/badge/Data%20Engine-Polars-CD7F32.svg)](https://pola.rs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Migrate your legacy Pentaho Data Integration (PDI) pipelines to modular, high-performance, and readable Python code in seconds.**

</div>

---

## 🌟 Main Features

1. **Pentaho XML File Parser (`.ktr` / `.kjb`)**:
   - Reads and analyzes the structure of transformations and jobs, extracting database connections (`<connection>`), steps (`<step>`), data flow (`<order>` / hops), and variables.

2. **Automatic Database & Dialect Detection**:
   - Automatically identifies the database configured in Pentaho (e.g., `ORACLE`, `POSTGRESQL`, `MSSQL`, `MYSQL`).
   - **Native Oracle Support**: Converts Pentaho JDBC connections into modern Python code using the **`oracledb`** library (in *Thin Mode*, eliminating the need to install the Oracle Instant Client) and **SQLAlchemy 2.0**.

3. **Python Code Generation with Object-Oriented Programming (OOP)**:
   - Translates Pentaho steps into decoupled, readable, and modular classes:
     - **Connections**: Session management classes (e.g., `OracleDatabaseConnection`).
     - **Input Steps**: Extractor classes (e.g., `ExtrairVendasExtractor`).
     - **Transform Steps**: Transformer classes (e.g., `TratarCamposTransformer`).
     - **Output Steps**: Loader classes (e.g., `CarregarDWLoader`).
     - **Pipeline Orchestrator**: Main orchestration class (e.g., `PipelineVendas`).
   - Uses the **Polars** analytical engine in the generated code for high-performance in-memory processing.

4. **Command-Line Interface (CLI)**:
   - Transpile your Pentaho files in seconds through the terminal:

```bash
pytaho convert sample_pentaho_files/exemplo_oracle.ktr -o pipelines/vendas_oracle.py
````

---

## 📌 Why use Pytaho?

* **Zero Lock-in:** Move away from heavy graphical interfaces and run your pipelines natively in Docker containers, Airflow, or GitHub Actions.
* **High Performance:** Replace Pentaho's Java processing with the native speed of the Rust-based **Polars** engine.
* **Clean Code & OOP:** Generate fully decoupled classes (Extractors, Transformers, Loaders) with static typing.
* **Native Security:** Connection variables and secrets are automatically parameterized as environment variables (`.env`).

---


## ⚡ Quickstart

### 1. Installing Dependencies

We recommend using [`uv`](https://github.com/astral-sh/uv) for its speed, but you can also use traditional `pip`:

```bash
# Clone the repository
git clone https://github.com/seu-usuario/pytaho.git
cd pytaho

# Using uv:
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Or using pip:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Converting a `.ktr` or `.kjb` Pentaho File

Run the `convert` command by providing the source file and the desired Python output file:

```bash
python -m pytaho.cli convert sample_pentaho_files/exemplo_oracle.ktr -o pipelines/vendas_oracle.py
```

---

## 💻 Generated Code Example (OOP Output)

When transpiling a `.ktr` file using **Oracle**, Pytaho automatically generates a structured, safe, and readable OOP script:

```python
import os
import logging
import polars as pl
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
logger = logging.getLogger("pytaho_pipeline")


class OracleDatabaseConnection:
    """Decoupled Oracle connection manager (oracledb Thin Mode)."""
    
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
    """Data extraction generated from the Pentaho step: 'Extrair Vendas Oracle'"""
    
    def __init__(self, db_conn: OracleDatabaseConnection):
        self.db = db_conn
        self.query = "SELECT id_venda, cd_cliente, vl_total FROM tb_vendas WHERE status = 'APROVADO'"

    def extract(self) -> pl.DataFrame:
        logger.info("Starting extraction from Oracle database...")
        return pl.read_database(query=self.query, connection=self.db.get_engine())


class TratarCamposTransformer:
    """Data transformation generated from the Pentaho step: 'Tratar Campos Venda'"""
    
    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        logger.info("Applying data transformations...")
        return df.rename({"id_venda": "venda_id", "cd_cliente": "cliente_id"})


class CarregarDWLoader:
    """Data loading generated from the Pentaho step: 'Carregar DW Oracle'"""
    
    def __init__(self, db_conn: OracleDatabaseConnection):
        self.db = db_conn
        self.target_table = "fact_vendas"

    def load(self, df: pl.DataFrame) -> int:
        logger.info(f"Loading {len(df)} records into table {self.target_table}...")
        df.write_database(
            table_name=self.target_table,
            connection=self.db.get_engine(),
            if_table_exists="append"
        )
        return len(df)


class PipelineVendas:
    """Data Flow Orchestrator (DAG)."""
    
    def __init__(self):
        self.db = OracleDatabaseConnection()
        self.extractor = ExtrairVendasExtractor(self.db)
        self.transformer = TratarCamposTransformer()
        self.loader = CarregarDWLoader(self.db)

    def run(self):
        logger.info("Starting pipeline execution...")
        df_raw = self.extractor.extract()
        df_clean = self.transformer.transform(df_raw)
        rows_inserted = self.loader.load(df_clean)
        logger.info(f"Pipeline completed successfully. Records inserted: {rows_inserted}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pipeline = PipelineVendas()
    pipeline.run()
```

---

## 🛠️ Supported Connectors & Dialects

| Database       | Native Python Driver   | Pytaho Support |
| -------------- | ---------------------- | -------------- |
| **Oracle**     | `oracledb` (Thin Mode) | ✅ Native       |
| **PostgreSQL** | `psycopg3`             | ✅ Native       |
| **SQL Server** | `pyodbc` / `pymssql`   | ✅ Native       |
| **MySQL**      | `pymysql`              | ✅ Native       |

---

## 🧪 Running Automated Tests

To validate the XML parser, dialect detection, and generated code syntax:

```bash
pytest -v
```

---

## 👨‍💻 Author

**Samuel Santos**

Pytaho was created by **Samuel Santos** with the goal of making life easier in corporate environments and also serving as a study project focused on Data Engineering, Python, automation, databases, and the modernization of legacy pipelines.

