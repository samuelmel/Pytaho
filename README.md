# Pytaho - Modern ETL Framework (Pentaho to Python)

O **Pytaho** é uma estrutura de engenharia de dados em Python desenhada para substituir de forma moderna, modular e performática o ecossistema legado do **Pentaho Data Integration (PDI / Kettle, Spoon, Kitchen, Carte)**.

---

## 🎯 Por que migrar do Pentaho para Python?

| Pentaho (Kettle / Spoon) | Nova Abordagem com Python |
| :--- | :--- |
| Arquivos XML proprietários (`.ktr` / `.kjb`) difíceis de versionar e fazer merge | **Código Python puro**, versionado diretamente no **Git** com Pull Requests e code review |
| Execução pesada em máquina virtual Java (JVM) com alto consumo de memória | Motores analíticos compilados em **Rust / C++ (Polars e DuckDB)**, até **50x mais rápidos** |
| Dificuldade para criar testes automatizados de dados | Testes unitários e de integração com **Pytest** integrados a pipelines de CI/CD |
| Interface gráfica pesada e engessada | Orquestração moderna como código (*Workflows-as-Code*) com **Prefect** ou **Dagster** |
| Conexões JDBC lentas para grandes volumes | Leitura paralela ultra-rápida direto para a memória com **ConnectorX** e **Arrow** |

---

## 🗂️ Estrutura de Diretórios do Projeto

A arquitetura adota o padrão modular **E-T-L (Extract - Transform - Load)** separando responsabilidades:

```plaintext
meu_projeto_etl/
├── .env.example                # Template de variáveis de ambiente (copiar para .env)
├── .gitignore                  # Arquivos e pastas ignorados pelo Git
├── requirements.txt            # Dependências recomendadas para o ecossistema
├── pyproject.toml              # Gerenciamento de projeto e empacotamento
├── README.md                   # Documentação do projeto
│
├── config/                     # Configurações globais e infraestrutura de conexões
│   ├── database.py             # Instâncias do SQLAlchemy / Pool de conexões (Origem e DW)
│   └── settings.yaml           # Parâmetros de execução, batch sizes e mapeamento de tabelas
│
├── src/                        # Código-fonte dos componentes de dados (Core ETL)
│   ├── extract/                # Equivalente aos "Input Steps" do Pentaho
│   │   ├── api_client.py       # Extração e consumo de APIs REST
│   │   ├── db_extractor.py     # Extração de bancos relacionais (Postgres, Oracle, SQL Server, etc.)
│   │   └── file_reader.py      # Leitura otimizada de arquivos (CSV, Parquet, Excel, JSON)
│   │
│   ├── transform/              # Equivalente aos "Transform Steps" do Pentaho
│   │   ├── cleaners.py         # Tratamento de nulos, tipagem, formatação de datas e strings
│   │   ├── aggregations.py     # Agrupamentos, somas, médias e janelas analíticas (Window Functions)
│   │   └── business_rules.py   # Regras de negócio, cálculos condicionais e filtros
│   │
│   ├── load/                   # Equivalente aos "Output Steps" do Pentaho
│   │   ├── db_loader.py        # Carga em massa, inserts e upserts no Data Warehouse
│   │   └── file_writer.py      # Geração de arquivos finais (ex: Parquet para Data Lake)
│   │
│   └── utils/                  # Utilitários de infraestrutura
│       ├── logger.py           # Configuração de logs estruturados de execução e erro
│       └── notifications.py    # Alertas no Slack, Teams e E-mail (substitui o Mail Step)
│
├── pipelines/                  # Equivalente aos "Jobs" (.kjb) do Pentaho
│   ├── sales_pipeline.py       # Orquestra Extract -> Transform -> Load de Vendas
│   └── hr_pipeline.py          # Orquestra Extract -> Transform -> Load de Recursos Humanos
│
└── tests/                      # Testes automatizados (Garante confiabilidade das transformações)
    ├── test_extract.py         # Testes para validação das fontes de dados
    └── test_transform.py       # Testes unitários para as regras de negócio e transformações
```

---

## 🛠️ Mapeamento de Ferramentas (Pentaho vs. Stack Python Moderna)

| Funcionalidade Pentaho | Função no Projeto | Biblioteca Recomendada | Vantagens |
| :--- | :--- | :--- | :--- |
| **PDI / Kettle (Steps)** | Processamento e Transformação em Memória | **Polars** ou **DuckDB** | Muito superior ao Pandas em velocidade e consumo de memória; execução multi-thread nativa em Rust. |
| **Table Input (JDBC)** | Conexões com Bancos de Dados | **SQLAlchemy 2.0** + **ConnectorX** | ConnectorX aloca dados diretamente em buffers Apache Arrow sem serialização intermediária. |
| **File Inputs** | Leitura de CSV, Excel e JSON | **Polars** + **fastexcel** | Lê planilhas e arquivos grandes em frações de segundo. |
| **REST Client** | Extração de APIs | **HTTPX** | Suporte moderno a HTTP/2, pooling de conexões e execução síncrona/assíncrona. |
| **Spoon (DAG) & Kitchen** | Orquestração de Jobs e Tarefas | **Prefect** ou **Dagster** | Interface web moderna, retries automáticos, histórico de execuções e código Python puro com decorators. |
| **Carte / Scheduler** | Agendamento de Execuções | **Scheduler nativo do Prefect/Dagster** | Agendamento via CRON, triggers orientados a eventos e observabilidade visual. |
| **Mail Step** | Alertas e Notificações | **Webhooks (Slack / Teams)** + `smtplib` | Alertas instantâneos em caso de falha nos pipelines com stack trace do erro. |
| **Pentaho Reporting** | Visualização e Relatórios | **Streamlit** ou **Apache Superset** | Dashboards analíticos rápidos em Python (Streamlit) ou plataforma corporativa open-source (Superset). |

---

## 🚀 Como Iniciar

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/pytaho.git
cd pytaho
```

### 2. Configurar o ambiente virtual
Recomendado usar o gerenciador moderno [`uv`](https://github.com/astral-sh/uv) ou o `venv` padrão:

```bash
# Usando uv:
uv venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Ou usando venv padrão:
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```
Preencha as credenciais dos bancos de dados e webhooks necessários no arquivo `.env` gerado.

### 4. Executar os testes
```bash
pytest
```
