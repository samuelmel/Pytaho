🇧🇷 Português | [🇺🇸 English](README_EN.md)

# Pytaho - Pentaho XML to Python OOP Transpiler 🚀

O **Pytaho** é uma ferramenta open-source de **transpilação e geração automática de código Python Orientado a Objetos (POO)** a partir de transformações (`.ktr`) e jobs (`.kjb`) exportados do **Pentaho Data Integration (PDI / Kettle)**.

---

## 🌟 Principais Funcionalidades

1. **Parser de Arquivos Pentaho XML (`.ktr` / `.kjb`)**:
   - Lê e analisa a estrutura de transformações, extraindo conexões de banco de dados (`<connection>`), passos (`<step>`), fluxo de dados (`<order>` / hops) e variáveis.

2. **Auto-Detecção de Banco de Dados & Dialetos**:
   - Identifica automaticamente o banco de dados configurado no Pentaho (ex: `ORACLE`, `POSTGRESQL`, `MSSQL`, `MYSQL`).
   - **Suporte Nativo a Oracle**: Converte conexões JDBC do Pentaho em código Python moderno utilizando a biblioteca **`oracledb`** (em *Thin Mode*, dispensando instalação do Oracle Instant Client) e **SQLAlchemy 2.0**.

3. **Geração de Código Python com Orientação a Objetos (POO)**:
   - Traduz os passos do Pentaho em classes desacopladas, legíveis e modulares:
     - **Conexões**: Classes gerenciadoras de sessão (ex: `OracleDatabaseConnection`).
     - **Input Steps**: Classes Extratoras (ex: `ExtrairVendasOracleExtractor`).
     - **Transform Steps**: Classes Transformadoras (ex: `TratarCamposVendaTransformer`).
     - **Output Steps**: Classes Carregadoras (ex: `CarregarDWOracleLoader`).
     - **Pipeline Orchestrator**: Classe orquestradora principal (ex: `etl_vendas_oraclePipeline`).
   - Utiliza o motor analítico **Polars** no código gerado para processamento de alta performance em memória.

4. **Interface de Linha de Comando (CLI)**:
   - Transpile seus arquivos do Pentaho em segundos através do terminal:
     ```bash
     pytaho convert sample_pentaho_files/exemplo_oracle.ktr --output pipelines/script_vendas.py
     ```

---

## 📁 Estrutura do Projeto

```plaintext
pytaho/
├── .env.example                # Template de variáveis de ambiente
├── .gitignore                  # Regras para ignorar .env, logs e venv
├── pyproject.toml              # Empacotamento e dependências (uv / pip)
├── requirements.txt            # Lista de dependências do transpilador
├── README.md                   # Documentação oficial
│
├── src/
│   └── pytaho/
│       ├── __init__.py
│       ├── cli.py              # Interface CLI (pytaho convert ...)
│       │
│       ├── parser/             # Leitura do XML do Pentaho
│       │   ├── models.py       # Dataclasses/Pydantic que representam o AST
│       │   ├── ktr_parser.py   # Parser de Transformações (.ktr)
│       │   └── kjb_parser.py   # Parser de Jobs (.kjb)
│       │
│       ├── dialects/           # Adaptadores por Banco de Dados (Auto-Detecção)
│       │   ├── base_dialect.py # Interface abstrata dos dialetos
│       │   ├── oracle.py       # Conector e adaptadores para Oracle (oracledb)
│       │   ├── postgresql.py   # Conector para PostgreSQL (psycopg3)
│       │   ├── mssql.py        # Conector para SQL Server (pyodbc)
│       │   └── mysql.py        # Conector para MySQL (pymysql)
│       │
│       └── generator/          # Gerador de código Python POO
│           ├── step_mappers.py # Mapeia Steps Pentaho -> Classes POO
│           └── code_builder.py # Monta o script Python final
│
├── sample_pentaho_files/       # XMLs de exemplo para testes de conversão
│   └── exemplo_oracle.ktr
│
└── tests/                      # Testes automatizados do transpilador
    ├── test_ktr_parser.py
    ├── test_oracle_dialect.py
    └── test_code_generator.py
```

---

## 🚀 Como Usar

### 1. Instalação das Dependências

Utilizando [`uv`](https://github.com/astral-sh/uv) (rápido) ou `pip`:

```bash
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

## ⚡ Exemplo de Código Gerado (Output POO)

Ao transpilar um `.ktr` com banco **Oracle**, o Pytaho gera automaticamente um código estruturado em POO como este:

```python
import os
import logging
import polars as pl
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("pytaho_pipeline")

class OracleDatabaseConnection:
    """Gerenciador de conexão com Banco de Dados Oracle usando oracledb em Thin Mode."""
    def __init__(self, host: str = "10.0.0.50", port: str = "1521", service_name: str = "ORCLDW", user: str = "usr_etl", password: str = "SecretOraclePass123"):
        self.host = host
        self.port = port
        self.service_name = service_name
        self.user = user
        self.password = password

    def get_sqlalchemy_engine(self):
        from sqlalchemy import create_engine
        url = f"oracle+oracledb://{self.user}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}"
        return create_engine(url, pool_pre_ping=True)

class ExtrairVendasOracleExtractor:
    """Extrator de dados gerado a partir do step Pentaho: 'Extrair Vendas Oracle'"""
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.query = """SELECT id_venda, cd_cliente, vl_total, dt_venda FROM tb_vendas WHERE status = 'APROVADO'"""

    def extract(self) -> pl.DataFrame:
        logger.info("Executando extração...")
        engine = self.db_connection.get_sqlalchemy_engine()
        return pl.read_database(query=self.query, connection=engine)

class TratarCamposVendaTransformer:
    """Transformador de dados gerado a partir do step Pentaho: 'Tratar Campos Venda'"""
    def __init__(self):
        self.rename_mapping = {'id_venda': 'venda_id', 'cd_cliente': 'cliente_id'}

    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        if self.rename_mapping:
            df = df.rename({k: v for k, v in self.rename_mapping.items() if k in df.columns})
        return df

class CarregarDWOracleLoader:
    """Carregador de dados gerado a partir do step Pentaho: 'Carregar DW Oracle'"""
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.table_name = "fact_vendas"

    def load(self, df: pl.DataFrame) -> int:
        engine = self.db_connection.get_sqlalchemy_engine()
        df.write_database(table_name=self.table_name, connection=engine, if_table_exists="append")
        return len(df)

class etl_vendas_oraclePipeline:
    """Pipeline Principal POO"""
    def __init__(self):
        self.db_oracledw = OracleDatabaseConnection()
        self.extractor_0 = ExtrairVendasOracleExtractor(self.db_oracledw)
        self.transformer_1 = TratarCamposVendaTransformer()
        self.loader_2 = CarregarDWOracleLoader(self.db_oracledw)

    def run(self):
        df_0 = self.extractor_0.extract()
        df_1 = self.transformer_1.transform(df_0)
        self.loader_2.load(df_1)

if __name__ == "__main__":
    pipeline = etl_vendas_oraclePipeline()
    pipeline.run()
```

---

## 🧪 Executar Testes Automatizados

```bash
pytest
```
