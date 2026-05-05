# 🏗️ ESTRUTURA DO SISTEMA: Controle de Licenças Fortinet

## 📌 PROPÓSITO DO SISTEMA

Sistema de **Controle e Conciliação de Licenças Fortinet** baseado em "Pontos". Gerencia a alocação, consumo e saldo de pontos de licenciamento de equipamentos FortiGate, com conciliação automática entre o controle manual e a base oficial da Fortinet.

---

## 🗺️ MAPA GERAL - AS 6 ABAS

```
┌─────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE LICENÇAS FORTINET                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌───────────────────┐                                         │
│   │    DASHBOARD      │ ◄── Painel executivo central            │
│   │   (Aba Principal) │                                         │
│   └────────┬──────────┘                                         │
│            │                                                    │
│     ┌──────┴──────┐                                            │
│     │             │                                             │
│  ┌──▼────────┐ ┌──▼──────────────┐                              │
│  │ PONTOS    │ │ PONTOS          │                              │
│  │ BOLSÃO    │ │ UTILIZADOS      │                              │
│  │ (20       │ │ (80 Eqptos)     │                              │
│  │  Pacotes) │ │                 │                              │
│  └─────┬─────┘ └───────┬─────────┘                              │
│        │               │                                        │
│        │               │                                        │
│        │     ┌─────────▼──────────┐                              │
│        │     │ BASE DE            │                              │
│        └─────┤ CONCILIAÇÃO        │                              │
│              │ (Base Oficial      │                              │
│              │  Fortinet)         │                              │
│              └────────────────────┘                              │
│                                                                  │
│   ┌──────────────┐   ┌──────────────────┐                       │
│   │  PLANILHA3   │   │ BASES AUXILIARES │                       │
│   │  (Auxiliar)  │   │ (Lista Respons.) │                       │
│   └──────────────┘   └──────────────────┘                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📐 ABA 1: "Dashboard" - Painel Central

### ESTRUTURA FÍSICA
- **Tamanho:** 103 linhas × 11 colunas (A a K)
- **Células mescladas:** J5:K5, D5:E5, F5:H5

### ORGANIZAÇÃO VISUAL (3 blocos)

| Bloco | Colunas | Título | Função |
|-------|---------|--------|--------|
| **Esquerdo Superior** | D-E | "VISÃO FORTINET" | Dados oficiais da Fortinet |
| **Central Superior** | F-H | "VISÃO ANALÍTICA" | Dados do controle manual |
| **Direito Superior** | J-K | "% DE UTILIZAÇÃO" | Percentuais de uso |
| **Filtro** | B4 | Combo box "Responsável" | Filtro dinâmico por equipe |

### CABEÇALHOS (Linha 6)

| Coluna | Campo | Origem dos Dados |
|--------|-------|-------------------|
| B | Rótulos de Linha | Nome da equipe (informado manualmente) |
| C | Pontos Totais | Informado manualmente |
| D | Used Totais | Informado manualmente (base Fortinet) |
| E | Remaining Totais | **Fórmula:** C - D |
| F | Pontos Utilizados | **Fórmula:** SUMIF buscando na aba "Pontos utilizados" (coluna L) |
| G | Faltantes | **Fórmula:** C - F |
| H | Previsão Utilização | **Fórmula:** SUMIF buscando na aba "Pontos utilizados" (coluna R) |
| J | % FORTINET | **Fórmula:** D / C |
| K | % ANALÍTICO | **Fórmula:** F / C |

### FÓRMULAS ESTRUTURAIS

```
Coluna F =SE(B7="";"";SOMASE('Pontos utilizados'!A:A;B7;'Pontos utilizados'!L:L))
Coluna G =SEERRO(C7-F7;"")
Coluna H =SE(B7="";"";SOMASE('Pontos utilizados'!$A:$A;B7;'Pontos utilizados'!$R:$R))
Coluna J =SEERRO(D7/C7;"")
Coluna K =SEERRO(F7/C7;"")
```

### REGRAS DE NEGÓCIO
- Linhas 7 a 12 contêm os grupos ativos
- Linhas 13 a 103 são linhas de expansão (fórmulas pré-arrastadas, vazias)
- A linha 7 corresponde ao grupo "Delivery (Aeronáltica)"
- A linha 8 corresponde ao grupo "Delivery (Pull)"
- A linha 9 corresponde ao grupo "Produtos (Pull)"
- A linha 10 corresponde ao grupo "Produtos (SIEM)"
- A linha 11 corresponde ao grupo "Projetos Especiais (MPM)"
- A linha 12 corresponde ao grupo "Projetos Especiais (Proderj)"

---

## 📐 ABA 2: "Pontos Bolsão" - Catálogo de Pacotes

### ESTRUTURA FÍSICA
- **Tamanho:** 100 linhas × 20 colunas (A a T)
- **Células mescladas:** P2:Q2, R2:T2
- **Tabela estruturada:** "Tabela1"

### DUAS TABELAS LADO A LADO

**TABELA PRINCIPAL (Colunas A-K) - Point Packs Individuais**

| Coluna | Campo | Tipo | Descrição |
|--------|-------|------|-----------|
| A | Point Pack Number | Texto | Identificador único do pacote (prefixo "ELAVM...") |
| B | Responsável | Texto | Equipe: Delivery, Produtos, Projetos Especiais |
| C | Projetos | Texto | Subprojeto: Pull, SIEM, Aeronáltica, Proderj, MPM |
| D | Resp + Projetos | **Fórmula** | Concatenação de B e C: `B & " (" & C & ")"` |
| E | Pontos | Número | Quantidade total de pontos do pacote |
| F | Used Amount | Número | Pontos já utilizados (vindo da Fortinet) |
| G | Remaining Amount | Número | **Fórmula:** E - F |
| H | Registration Date | Data | Data de registro do pacote |
| I | Expiration Date | Data | Data de expiração (validade) |
| J | Previsão Início | Data | Previsão de início de uso |
| K | Tempo Projeto (meses) | Número | Duração prevista em meses |

**Fórmula da Coluna D:**
```
=Tabela1[[#This Row],[Responsável]]&" ("&Tabela1[[#This Row],[Projetos]]&")"
```
> Concatena "Responsável (Projeto)" para servir como chave de busca nas demais abas

**TABELA RESUMO (Colunas N-T) - Subtotais por Grupo**

| Coluna | Campo | Tipo | Descrição |
|--------|-------|------|-----------|
| N | Responsável | Texto | Nome do grupo |
| O | Pontos Totais | Número | Soma manual dos pacotes do grupo |
| P | Used Totais | Número | Soma manual dos Used Amount |
| Q | Remaining Totais | **Fórmula:** O - P | Saldo remanescente |
| R | Pontos Utilizados | **Fórmula:** SUMIF('Pontos utilizados'!A:A;N;'Pontos utilizados'!L:L) | Consumo calculado |
| S | Faltantes | **Fórmula:** O - R | Saldo pelo controle manual |
| T | Previsão Utilização | **Fórmula:** SUMIF('Pontos utilizados'!$A:$A;N;'Pontos utilizados'!$R:$R) | Previsão futura |

### FÓRMULAS ESTRUTURAIS DOS SUBTOTAIS

```
Coluna D (Resp+Projetos) = Tabela1[[Responsável]] & " (" & Tabela1[[Projetos]] & ")"
Coluna R (Pontos Utilizados) = SE(N4="";"";SOMASE('Pontos utilizados'!A:A;N4;'Pontos utilizados'!L:L))
Coluna S (Faltantes) = SEERRO(O4-R4;"")
Coluna T (Previsão) = SE(N4="";"";SOMASE('Pontos utilizados'!$A:$A;N4;'Pontos utilizados'!$R:$R))
```

---

## 📐 ABA 3: "Pontos utilizados" - Tabela de Consumo

### ESTRUTURA FÍSICA
- **Tamanho:** 82 linhas × 21 colunas (A a U)
- **Células mescladas:** I1:J1
- **Tabela estruturada:** "Tabela2"
- **Célula I1:** `=TODAY()` → Data base para todos os cálculos

### CABEÇALHOS (Linha 2) e TIPOS

| Coluna | Campo | Tipo | Descrição |
|--------|-------|------|-----------|
| A | Resp + Projetos | Texto | Chave do grupo (ex: "Delivery (Pull)") |
| B | Serial Number | Texto | Serial do equipamento FortiGate |
| C | Dados Do Cliente | Texto | Nome do cliente/site |
| D | Product Type | Texto | Tipo: "FortiGate Hardware", "FortiManager VM", etc. |
| E | Service Pack | Texto | Ex: "FGHWUTP" |
| F | Product Model | Texto | Modelo (FG120G, FG2H0G, FGT40F, etc.) |
| G | Company | Texto | Empresa (opcional) |
| H | Valor Pontos Dia | Número | **Parâmetro:** Custo em pontos POR DIA do equipamento |
| I | Data Aplicação | Data | Início do período de consumo |
| J | Data Fim | Data | Término do período (pode estar vazio = sem fim) |
| K | Dias Consumidos | **Fórmula** | Dias já decorridos |
| L | Pontos Consumidos | **Fórmula** | **H × K** - Total consumido até hoje |
| M | Tempo Faltante (Dias) | **Fórmula** | Dias restantes até Data Fim |
| N | Pontos a serem consumidos | **Fórmula** | **H × M** - Previsão de consumo futuro |
| O | Conciliação | **Fórmula** | **SUMIF na Base de Conciliação** - Compara com Fortinet |
| P | Dias Consumo Total | **Fórmula** | Dias totais do período |
| Q | Pontos Consumo Total | **Fórmula** | **H × P** - Pontos totais no período |
| R | Repetição Serial | **Fórmula** | Flag "OK" ou "Duplicado" |

### FÓRMULAS ESTRUTURAIS (Lógica Pura)

**Coluna K - Dias Consumidos:**
```
=SE(OU(DataFim="";DataFim>=Hoje); Hoje-DataInicio; DataFim-DataInicio)
```
> Se não tem data fim OU a data fim é futura: conta de DataInicio até HOJE
> Se a data fim já passou: conta de DataInicio até DataFim

**Coluna L - Pontos Consumidos:**
```
= H × K
```

**Coluna M - Tempo Faltante:**
```
=SE(DataFim=""; ""; SE(Hoje<=DataFim; DataFim-Hoje; 0))
```
> Se DataFim está vazia, não calcula
> Se Hoje é anterior a DataFim, calcula diferença
> Se já passou, retorna 0

**Coluna N - Pontos a serem consumidos:**
```
=SEERRO( M × H ; "")
```

**Coluna O - Conciliação (CRÍTICA):**
```
=SOMASE('Base de Conciliação'!$A:$I; SerialNumber; 'Base de Conciliação'!$I:$I)
```
> **CORAÇÃO DO SISTEMA:** Busca o Serial do equipamento na aba "Base de Conciliação" e soma todos os pontos registrados lá

**Coluna P - Dias Consumo Total:**
```
=SE(DataFim=""; Hoje-DataInicio; DataFim-DataInicio)
```

**Coluna Q - Pontos Consumo Total:**
```
= H × P
```

**Coluna R - Repetição Serial (VALIDAÇÃO):**
```
=SE(CONT.SE(B:B; Serial) > 1; "Duplicado"; "OK")
```
> Varre toda a coluna B e verifica se o Serial aparece mais de uma vez

---

## 📐 ABA 4: "Base de Conciliação" - Base Oficial Fortinet

### ESTRUTURA FÍSICA
- **Tamanho:** variável (~1664 linhas) × 9 colunas (A a I)
- **Sem células mescladas**

### CABEÇALHOS

| Coluna | Campo | Tipo | Descrição |
|--------|-------|------|-----------|
| A | Serial Number | Texto | Serial do equipamento (chave de busca) |
| B | Description | Texto | Nome descritivo do equipamento |
| C | Configuration Name | Texto | Nome de configuração do equipamento |
| D | Product Type | Texto | Tipo do produto (ex: "FortiGate Hardware") |
| E | Usage Date | Data | Data de consumo registrada |
| F | Service Pack | Texto | Service Pack do equipamento (ex: "FGHWUTP") |
| G | Device Model | Texto | Modelo do equipamento (ex: FGT40F, FG120G, FG2H0G) |
| H | Additional FPC modules | Texto | Módulos adicionais (sempre vazio na prática) |
| I | Points | Número | Pontos consumidos naquela data |

### PROPÓSITO ESTRUTURAL
- É a **fonte de verdade oficial** exportada do sistema Fortinet
- Cada Serial Number aparece **múltiplas vezes** (consumo registrado em várias datas)
- Serve como **contraprova** para validar se o cálculo manual está correto
- A coluna I (Points) é somada via SUMIF na aba "Pontos utilizados" para comparação

### REGRA DE NEGÓCIO
```
Conciliação = SUMIF(BaseConciliação[Serial]; SerialEquipamento; BaseConciliação[Points])
```
> Compara: "Quanto calculei manualmente" vs "Quanto a Fortinet registrou oficialmente"

---

## 📐 ABA 5: "Planilha3" - Tabela Auxiliar

### ESTRUTURA FÍSICA
- **Tamanho:** 11 linhas × 16 colunas (A a P)
- **Dados efetivos:** range J5:P9 (matriz 5×7)
- **Sem células mescladas, sem cabeçalhos nomeados**

### DADOS

Matriz de números sequenciais (1 a 31) dispostos em 5 linhas × 7 colunas no range J5:P9.

### FÓRMULA ISOLADA
```
[11,L] = K11 × (3/5)
```
> Cálculo simples de proporção (ponto avulso)

### PROPÓSITO ESTRUTURAL
- **Aba de rascunho/apoio** sem conexão direta com as demais abas
- Possível calculadora auxiliar, teste, ou referência para alguma funcionalidade não implementada
- **Não alimenta nem é alimentada por nenhuma outra aba**

---

## 📐 ABA 6: "Bases Auxiliares" - Lista de Responsáveis

### ESTRUTURA FÍSICA
- **Tamanho:** 4 linhas × 2 colunas (A a B)

### CONTEÚDO

| Linha | Coluna A | Coluna B |
|-------|----------|----------|
| 1 | (vazio) | "Responsável" (cabeçalho) |
| 2 | (vazio) | Delivery |
| 3 | (vazio) | Projetos Especiais |
| 4 | (vazio) | Produtos |

### PROPÓSITO ESTRUTURAL
- **Lista de 3 valores** que define as categorias de responsáveis
- Possível uso como:
  - **Fonte para validação de dados** (dropdowns nas demais abas)
  - **Tabela de dimensão** para possível integração com Power BI
  - **Referência** para garantir consistência nos nomes dos grupos

---

## 🔗 MAPA DE RELACIONAMENTO ENTRE ABAS (Fluxo de Dados)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FLUXO DE DADOS                                   │
└─────────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │                      │
                    │      DASHBOARD       │
                    │   (CONSOLIDAÇÃO)     │
                    │                      │
                    │  C ← Manual          │
                    │  D ← Manual          │
                    │  F ← ────────────┐   │
                    │  H ← ──────────┐ │   │
                    └────────────────┼─┼───┘
                                     │ │
                    ┌────────────────┼─┼──┐
                    │                │ │  │
                    │  PONTOS        │ │  │
                    │  BOLSÃO        │ │  │
                    │                │ │  │
                    │  E ← Manual    │ │  │
                    │  R ← ──────────┼─┘  │
                    │  T ← ──────────┼────┘
                    └────────────────┘
                                     │
                    ┌────────────────┼──┐
                    │                │  │
                    │  PONTOS        │  │
                    │  UTILIZADOS    │  │
                    │                │  │
                    │  H ← Manual    │  │
                    │  L = H × K     │  │
                    │  O = SUMIF ────┼──┤
                    │                │  │
                    └────────────────┘  │
                                     │  │
                    ┌────────────────┼──┘
                    │                │
                    │  BASE DE       │
                    │  CONCILIAÇÃO   │
                    │                │
                    │  Fornece       │
                    │  Points(I)     │
                    │  por Serial(A) │
                    │                │
                    └────────────────┘
```

### LEGENDA DO FLUXO

| Direção | Significado |
|---------|-------------|
| → Manual | Dado inserido manualmente pelo usuário |
| → Fórmula | Dado calculado por fórmula |
| 🔗 SUMIF | Conexão entre abas via função SOMASE |

### RESUMO DO FLUXO

```
1. BASE DE CONCILIAÇÃO (Fortinet)
   │
   │ SUMIF por Serial Number
   ▼
2. PONTOS UTILIZADOS (80 equipamentos)
   │
   │ SUMIF por Grupo (coluna A)
   ▼
3. PONTOS BOLSÃO (20 pacotes)  ← também alimenta DASHBOARD
   │
   │ Referência direta
   ▼
4. DASHBOARD (Painel final)
```

---

## 🧩 ESTRUTURA DE VALIDAÇÕES

### Validação de Duplicidade (Coluna R de "Pontos utilizados")
```
=SE(CONT.SE(B:B; SerialAtual) > 1; "Duplicado"; "OK")
```
> Sistema varre automaticamente toda a lista de equipamentos e alerta se encontrar o mesmo Serial Number duas vezes

### Proteção contra Erros
Todas as fórmulas de cálculo usam proteções:
- `SEERRO()` → Evita exibição de erros (#DIV/0!, #N/D, etc.)
- `SE(condição; valor_se_verdadeiro; "")` → Só calcula se houver dados
- Referências estruturadas `Tabela1[[#This Row];[Campo]]` → Facilitam manutenção

---

## ⚙️ 3 NÍVEIS HIERÁRQUICOS DO SISTEMA

```
NÍVEL 1 - DADOS BRUTOS
├── Base de Conciliação (fonte oficial)
├── Bases Auxiliares (lista de grupos)
└── Planilha3 (apoio)

NÍVEL 2 - PROCESSAMENTO
├── Pontos utilizados (cálculo por equipamento)
└── Pontos Bolsão (subtotais por grupo)

NÍVEL 3 - APRESENTAÇÃO
└── Dashboard (painel executivo consolidado)
```

---

## 🧮 LÓGICA MACRO DO SISTEMA

```
1. COMPRA: Cliente adquire Point Pack (N pontos)
   │
   ▼
2. ALOCAÇÃO: Point Pack é atribuído a um Grupo + Projeto
   │
   ▼
3. CONSUMO: Cada equipamento FortiGate instalado consome X pts/dia
   │  ├── DataInício → DataFim (ou indefinido)
   │  └── Cálculo: ValorPontoDia × DiasCorridos
   │
   ▼
4. CONCILIAÇÃO: O consumo calculado é comparado com a base Fortinet
   │
   ▼
5. DASHBOARD: Mostra por grupo:
   ├── Total de pontos contratados
   ├── Total de pontos utilizados (manual)
   ├── Total de pontos utilizados (Fortinet)
   ├── Saldo restante
   └── Percentuais de utilização
```

---

## 🗃️ REGRAS DE NEGÓCIO (Sem Valores)

1. **Cada Point Pack** (ELAVM...) tem validade de ~5 anos a partir do registro
2. **Cada equipamento** tem um "Valor Pontos Dia" fixo que depende do modelo
3. **Se Data Fim estiver vazia**, o consumo é calculado até a data atual (=TODAY)
4. **Se Data Fim for futura**, o sistema calcula consumo passado E previsão futura
5. **Serial Number** é a chave universal entre as abas "Pontos utilizados" e "Base de Conciliação"
6. **"Resp + Projetos"** (concatenação) é a chave entre "Pontos utilizados" e as demais abas
7. **A coluna R de "Pontos utilizados"** deveria conter valor de previsão mas estruturalmente contém flags de duplicidade (OK/Duplicado) - **INCONSISTÊNCIA ESTRUTURAL**
8. **O sistema tem 100 linhas de sobra** em "Pontos Bolsão" e "Dashboard" para novos registros