# Sistema de Controle de Licenças Fortinet

Sistema web para gerenciamento, controle de consumo e conciliação de licenças Fortinet baseadas em pontos. Desenvolvido em Python/Flask com banco de dados SQLite.

---

## Funcionalidades

- **Dashboard** — visão consolidada por grupo (Responsável + Projeto) com pontos totais, consumidos, saldo e percentual de utilização
- **Pontos Bolsão** — cadastro e listagem dos Point Packs adquiridos
- **Pontos Utilizados** — registro de equipamentos FortiGate com cálculo automático de consumo diário
- **Conciliação** — upload da base oficial da Fortinet (.xlsx) e cruzamento automático por Serial Number

---

## Tecnologias

- Python 3.14
- Flask 3.0.3
- SQLite (via módulo nativo `sqlite3`)
- openpyxl 3.1.2 (leitura de arquivos Excel)
- Gunicorn (produção)

---

## Instalação e execução local

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd sistema_py
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicialize o banco de dados

```bash
python database.py
```

### 5. Rode o servidor

```bash
python app.py
```

Acesse em: **http://127.0.0.1:5000**

---

## Estrutura do projeto

```
sistema_py/
├── app.py                  # Rotas e lógica principal (Flask)
├── database.py             # Criação das tabelas SQLite
├── wsgi.py                 # Entry point para produção (Gunicorn)
├── requirements.txt        # Dependências Python
├── sistema.db              # Banco de dados SQLite (gerado automaticamente)
├── static/
│   ├── claro.css           # Estilos globais
│   └── claro_empresas2.jpg # Logo Claro Empresas
└── templates/
    ├── index.html              # Dashboard
    ├── pontos_bolsao.html      # Listagem de Point Packs
    ├── novo_bolsao.html        # Formulário de novo bolsão
    ├── pontos_utilizados.html  # Listagem de equipamentos
    ├── novo_ponto_utilizado.html # Formulário de novo consumo
    └── conciliacao.html        # Upload e resultado da conciliação
```

---

## Banco de dados

### `pontos_bolsao`
Armazena os pacotes de pontos adquiridos (Point Packs).

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| point_pack_number | TEXT | Identificador único do pacote (ex: ELAVM...) |
| responsavel | TEXT | Equipe: Delivery, Projetos Especiais, Produtos |
| projetos | TEXT | Subprojeto: Pull, SIEM, Aeronáltica, etc. |
| pontos | INTEGER | Total de pontos do pacote |
| used_amount | REAL | Pontos já utilizados (base Fortinet) |
| registration_date | TEXT | Data de registro |
| expiration_date | TEXT | Data de expiração |

### `pontos_utilizados`
Registra cada equipamento FortiGate e seu consumo diário.

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| bolsao_id | INTEGER | FK para `pontos_bolsao` |
| serial_number | TEXT | Serial do equipamento |
| dados_cliente | TEXT | Nome do cliente/site |
| product_model | TEXT | Modelo (FG120G, FG2H0G, etc.) |
| valor_pontos_dia | REAL | Custo em pontos por dia |
| data_aplicacao | TEXT | Data de início do consumo |
| data_fim | TEXT | Data de término (opcional) |

### `base_conciliacao`
Base oficial exportada da Fortinet. Substituída a cada upload.

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| serial_number | TEXT | Serial do equipamento |
| description | TEXT | Descrição |
| usage_date | TEXT | Data do consumo registrado |
| points | REAL | Pontos consumidos na data |

---

## Lógica de cálculo

```
Dias Consumidos  = hoje - data_aplicacao  (ou data_fim - data_aplicacao se encerrado)
Pontos Calculados = valor_pontos_dia × dias_consumidos

Conciliação = SUM(points) da base_conciliacao WHERE serial_number = serial do equipamento
Diferença   = Pontos Calculados - Pontos Fortinet
```

---

## Deploy (produção)

O projeto inclui `Procfile` para deploy em plataformas como Heroku/Railway:

```
web: gunicorn wsgi:app
```

---

## Responsáveis

| Área | Responsável |
|---|---|
| Delivery | Equipe Delivery |
| Projetos Especiais | Equipe Projetos Especiais |
| Produtos | Equipe Produtos |
