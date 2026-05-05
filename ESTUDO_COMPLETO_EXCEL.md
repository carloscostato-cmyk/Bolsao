# ESTUDO COMPLETO DO ARQUIVO: "Controle de Licenças Fortinet (estudo) 1.xlsx"

---

## VISÃO GERAL DO SISTEMA

Este arquivo Excel é um **SISTEMA DE CONTROLE E CONCILIAÇÃO DE LICENÇAS FORTINET** que gerencia a alocação, consumo e saldo de "Pontos" de licenciamento Fortinet. Ele funciona como um módulo de cálculo integrado que:

1. **Gerencia "Point Packs"** (pacotes de pontos comprados)
2. **Calcula consumo diário** de equipamentos FortiGate
3. **Concilia** dados da base Fortinet com o controle interno
4. **Gera Dashboard** de acompanhamento por equipe/projeto

---

## ABA 1: "Dashboard" (103 linhas × 11 colunas)

### ═══ ESTRUTURA ═══

É o **painel principal de acompanhamento** com 3 blocos visuais:

| Região | Colunas | Título | Conteúdo |
|--------|---------|--------|----------|
| D4:E5 | D-E | "VISÃO FORTINET" | Células mescladas (título) |
| F4:H5 | F-H | "VISÃO ANALÍTICA" | Células mescladas (título) |
| J4:K5 | J-K | "% DE UTILIZAÇÃO" | Células mescladas (título) |
| Linha 4 | B | Filtro "Responsável" | Combo box com (Tudo) |
| Linhas 6+ | B-K | Tabela de dados | Métricas por equipe |

### ═══ CABEÇALHOS (Linha 6) ═══

| Col | Título | Descrição |
|-----|--------|-----------|
| B | Rótulos de Linha | Nome da equipe/responsável |
| C | Pontos Totais | Total de pontos contratados |
| D | Used Totais | Total de pontos usados (fortinet) |
| E | Remaining Totais | Saldo restante (C - D) |
| F | Pontos Utilizados | Consumo calculado internamente |
| G | Faltantes | Pontos restantes (C - F) |
| H | Previsão Utilização | Previsão futura de consumo |
| J | % FORTINET | % de uso pela ótica Fortinet (D/C) |
| K | % ANALÍTICO | % de uso pela ótica interna (F/C) |

### ═══ REGISTROS COM DADOS (linhas 7-12) ═══

| Linha | Equipe | Pontos Totais | Used (Fortinet) | Pontos Usados (Controle) | Faltantes |
|-------|--------|:------------:|:--------------:|:-----------------:|:--------:|
| 7 | Delivery (Aeronáltica) | 70.000 | 0 | 177,12 | 69.822,88 |
| 8 | Delivery (Pull) | 200.000 | 49.838,42 | 4.078,09 | 195.921,91 |
| 9 | Produtos (Pull) | 50.000 | 0 | 627,48 | 49.372,52 |
| 10 | Produtos (SIEM) | 110.000 | 0 | 5.171,80 | 104.828,20 |
| 11 | Projetos Especiais (MPM) | 260.000 | 0 | 5.441,25 | 254.558,75 |
| 12 | Projetos Especiais (Proderj) | 130.000 | 130.000 | 0 | 130.000 |

**TOTAIS GERAIS:** **820.000 pontos** contratados

### ═══ FÓRMULAS CRÍTICAS ═══

**Coluna F (Pontos Utilizados):**
```
=IF($B7="","",SUMIF('Pontos utilizados'!A:A,$B7,'Pontos utilizados'!L:L))
```
> Soma todos os "Pontos Consumidos" (coluna L da aba "Pontos utilizados") filtrando pela equipe na coluna A

**Coluna G (Faltantes):**
```
=IFERROR(C7-F7,"")
```
> Pontos Totais - Pontos Utilizados (controle interno)

**Coluna H (Previsão Utilização):**
```
=IF($B7="","",SUMIF('Pontos utilizados'!$A:$A,$B7,'Pontos utilizados'!$R:$R))
```
> Soma "Repetição Serial" (coluna R) - **NÃO ESTÁ SENDO USADA** (zeros)

**Coluna J (% FORTINET):**
```
=IFERROR(D7/C7,"")
```
> Used Totais / Pontos Totais (ótica Fortinet)

**Coluna K (% ANALÍTICO):**
```
=IFERROR(F7/C7,"")
```
> Pontos Utilizados / Pontos Totais (ótica interna)

> **⚠️ Observação:** As linhas 13-103 têm fórmulas previamente arrastadas para baixo aguardando novos dados.

---

## ABA 2: "Pontos Bolsão" (100 linhas × 20 colunas)

### ═══ ESTRUTURA ═══

Duas tabelas lado a lado:

**TABELA PRINCIPAL (cols A-K):** "Tabela1" - Point Packs individuais
**TABELA RESUMO (cols N-T):** Subtotais por Responsável

### ═══ CABEÇALHOS (Linha 1) ═══

| Col | Título | Descrição |
|-----|--------|-----------|
| A | Point Pack Number | Identificador único do pacote (ex: ELAVM4715259066) |
| B | Responsável | Equipe responsável (Delivery, Produtos, Projetos Especiais) |
| C | Projetos | Subprojeto (Pull, SIEM, Aeronáltica, Proderj, MPM) |
| D | Resp + Projetos | Concatenação: "Responsável (Projeto)" |
| E | Pontos | Total de pontos do pacote |
| F | Used Amount | Quantidade já utilizada |
| G | Remaining Amount | Saldo remanescente |
| H | Registration Date | Data de registro do pacote |
| I | Expiration Date | Data de expiração |
| J | Previsão Início | Previsão de início de uso |
| K | Tempo Projeto (meses) | Duração prevista em meses |

### ═══ REGISTROS DE POINT PACKS (20 pacotes) ═══

| # | Point Pack | Responsável | Projeto | Pontos | Used | Remaining | Registro | Expira |
|---|-----------|-------------|---------|:-----:|:---:|:--------:|----------|--------|
| 1 | ELAVM4715259066 | Projetos Especiais | Proderj | 50.000 | 50.000 | 0 | 04/11/2024 | 03/11/2029 |
| 2 | ELAVM4715358765 | Projetos Especiais | Proderj | 50.000 | 50.000 | 0 | 28/01/2025 | 27/01/2030 |
| 3 | ELAVM4715519871 | Projetos Especiais | Proderj | 10.000 | 10.000 | 0 | 04/08/2025 | 03/08/2030 |
| 4 | ELAVM4715519872 | Projetos Especiais | Proderj | 10.000 | 10.000 | 0 | 04/08/2025 | 03/08/2030 |
| 5 | ELAVM4715519873 | Projetos Especiais | Proderj | 10.000 | 10.000 | 0 | 04/08/2025 | 03/08/2030 |
| 6 | ELAVM4715519864 | Delivery | Pull | 50.000 | 49.838,42 | 161,58 | 05/08/2025 | 04/08/2030 |
| 7 | ELAVM4715519865 | Delivery | Pull | 50.000 | 0 | 50.000 | 05/08/2025 | 04/08/2030 |
| 8 | ELAVM4715519866 | Delivery | Pull | 50.000 | 0 | 50.000 | 05/08/2025 | 04/08/2030 |
| 9 | ELAVM4715519867 | Delivery | Pull | 50.000 | 0 | 50.000 | 05/08/2025 | 04/08/2030 |
| 10 | ELAVM4715519868 | Produtos | Pull | 50.000 | 0 | 50.000 | 05/08/2025 | 04/08/2030 |
| 11 | ELAVM4715519869 | Produtos | SIEM | 50.000 | 0 | 50.000 | 05/08/2025 | 04/08/2030 |
| 12 | ELAVM4715519870 | Produtos | SIEM | 50.000 | 0 | 50.000 | 05/08/2025 | 04/08/2030 |
| 13 | ELAVM4715514536 | Delivery | Aeronáltica | 50.000 | 0 | 50.000 | 30/09/2025 | 29/09/2030 |
| 14 | ELAVM4715580631 | Delivery | Aeronáltica | 10.000 | 0 | 10.000 | 01/12/2025 | 30/11/2030 |
| 15 | ELAVM4715580632 | Delivery | Aeronáltica | 10.000 | 0 | 10.000 | 01/12/2025 | 30/11/2030 |
| 16 | ELAVM4715580633 | Produtos | SIEM | 10.000 | 0 | 10.000 | 01/12/2025 | 30/11/2030 |
| 17 | ELAVM4715636002 | Projetos Especiais | MPM | 10.000 | 0 | 10.000 | 06/03/2026 | 05/03/2029 |
| 18 | ELAVM4715636001 | Projetos Especiais | MPM | 50.000 | 0 | 50.000 | 06/03/2026 | 05/03/2029 |
| 19 | ELAVM4715636016 | Projetos Especiais | MPM | 100.000 | 0 | 100.000 | 06/03/2026 | 05/03/2029 |
| 20 | ELAVM4715636017 | Projetos Especiais | MPM | 100.000 | 0 | 100.000 | 06/03/2026 | 05/03/2029 |

### ═══ TABELA DE SUBTOTAIS (cols N-T, linhas 4-9) ═══

| Grupo | Pontos Totais | Used Totais | Remaining | Pontos Utilizados | Faltantes |
|-------|:-----------:|:---------:|:--------:|:--------------:|:--------:|
| Delivery (Aeronáltica) | 70.000 | 0 | 70.000 | 177,12 | 69.822,88 |
| Delivery (Pull) | 200.000 | 49.838,42 | 150.161,58 | 4.078,09 | 195.921,91 |
| Produtos (Pull) | 50.000 | 0 | 50.000 | 627,48 | 49.372,52 |
| Produtos (SIEM) | 110.000 | 0 | 110.000 | 5.171,80 | 104.828,20 |
| Projetos Especiais (MPM) | 260.000 | 0 | 260.000 | 5.441,25 | 254.558,75 |
| Projetos Especiais (Proderj) | 130.000 | 130.000 | 0 | 0 | 130.000 |

### ═══ FÓRMULAS ═══

**Coluna D (Resp + Projetos):**
```
=Tabela1[[#This Row],[Responsável]]&" ("&Tabela1[[#This Row],[Projetos]]&")"
```
> Concatena "Responsável (Projeto)" para uso como chave de busca

**Coluna R (Pontos Utilizados) - Subtotais:**
```
=IF($N4="","",SUMIF('Pontos utilizados'!A:A,$N4,'Pontos utilizados'!L:L))
```
> Soma Pontos Consumidos da aba "Pontos utilizados" filtrando pelo nome do grupo

**Coluna S (Faltantes):**
```
=IFERROR(O4-R4,"")
```
> Pontos Totais - Pontos Utilizados

**Coluna T (Previsão Utilização):**
```
=IF($N4="","",SUMIF('Pontos utilizados'!$A:$A,$N4,'Pontos utilizados'!$R:$R))
```
> Soma a coluna R de "Pontos utilizados" (previsão futura)

---

## ABA 3: "Pontos utilizados" (82 linhas × 21 colunas)

### ═══ ESTRUTURA ═══

É a **tabela de consumo** (Tabela2) com **~80 equipamentos FortiGate** cadastrados. Cada linha = 1 equipamento com seu consumo calculado dinamicamente.

### ═══ CABEÇALHOS (Linha 2) ═══

| Col | Título | Descrição |
|-----|--------|-----------|
| A | Resp + Projetos | Grupo responsável (ex: "Delivery (Pull)") |
| B | Serial Number | Serial do equipamento FortiGate |
| C | Dados Do Cliente | Nome do cliente/site |
| D | Product Type | Tipo do produto (FortiGate Hardware) |
| E | Service Pack | Service Pack do equipamento |
| F | Product Model | Modelo do equipamento |
| G | Company | Empresa (vazio na maioria) |
| H | Valor Pontos Dia | **Custo em pontos POR DIA** de cada equipamento |
| I | Data Aplicação | Data de início do consumo |
| J | Data Fim | Data de término (ou vazia) |
| K | Dias Consumidos | Dias já consumidos (calculado) |
| L | Pontos Consumidos | Total de pontos já consumidos (H × K) |
| M | Tempo Faltante (Dias) | Dias restantes até Data Fim |
| N | Pontos a serem consumidos | Previsão de consumo futuro (H × M) |
| O | Conciliação | **Conciliação com base Fortinet** |
| P | Dias Consumo Total | Dias totais (Data Fim - Data Início) |
| Q | Pontos Consumo Total | Pontos totais no período (H × P) |
| R | Repetição Serial | Flag de serial duplicado |

### ═══ FÓRMULAS DETALHADAS ═══

**Coluna K - Dias Consumidos:**
```
=IF(OR(Tabela2[[#This Row],[Data Fim]]="",Tabela2[[#This Row],[Data Fim]]>=$I$1),
    $I$1-Tabela2[[#This Row],[Data Aplicação]],
    Tabela2[[#This Row],[Data Fim]]-Tabela2[[#This Row],[Data Aplicação]])
```
> Se Data Fim está vazia OU é futura: calcula de Data Aplicação até HOJE ($I$1)
> Senão: calcula de Data Aplicação até Data Fim

**Coluna L - Pontos Consumidos:**
```
=H3*K3
```
> Valor Pontos Dia × Dias Consumidos

**Coluna M - Tempo Faltante:**
```
=IF(Tabela2[[#This Row],[Data Fim]]="","",
    IF($I$1<=Tabela2[[#This Row],[Data Fim]],
       Tabela2[[#This Row],[Data Fim]]-$I$1,0))
```
> Se Data Fim existe e é futura: calcula diferença até HOJE

**Coluna N - Pontos a serem consumidos:**
```
=IFERROR(Tabela2[[#This Row],[Tempo Faltante (Dias)]]*Tabela2[[#This Row],[Valor Pontos Dia]],"")
```

**Coluna O - Conciliação:**
```
=SUMIF('Base de Conciliação'!$A:$I,Tabela2[[#This Row],[Serial Number]],'Base de Conciliação'!$I:$I)
```
> **Busca o Serial na aba "Base de Conciliação" e soma os pontos da coluna I** (concilia com a base oficial Fortinet)

**Coluna P - Dias Consumo Total:**
```
=IF(Tabela2[[#This Row],[Data Fim]]="",$I$1-I3,Tabela2[[#This Row],[Data Fim]]-Tabela2[[#This Row],[Data Aplicação]])
```

**Coluna Q - Pontos Consumo Total:**
```
=H3*Tabela2[[#This Row],[Dias Consumo Total]]
```

**Coluna R - Repetição Serial:**
```
=IF(COUNTIF(B:B,Tabela2[[#This Row],[Serial Number]])>1,"Duplicado","OK")
```
> Verifica se o mesmo Serial aparece mais de uma vez na lista

**Célula I1 (TODAY):**
```
=TODAY()
```
> Data base para todos os cálculos (atualizada automaticamente)

### ═══ EQUIPAMENTOS CADASTRADOS (80 registros) ═══

**Distribuição por Grupo:**
| Grupo | Qtd Equipamentos | Exemplos |
|-------|:-------:|----------|
| **Delivery (Pull)** | ~27 | Open Finance, Bom Jesus, Casas Pedro, etc. |
| **Produtos (Pull)** | ~9 | Cliente Pull diversos |
| **Produtos (SIEM)** | ~10 | Equipamentos SIEM |
| **Delivery (Aeronáltica)** | ~5 | Equipamentos Aeronáltica |
| **Projetos Especiais (MPM)** | ~29 | Diversos clientes MPM |

**Modelos de equipamentos encontrados:**
- FG120G (FortiGate 120G)
- FG2H0G (FortiGate 200G)
- FG100E (FortiGate 100E)
- FG100F (FortiGate 100F)
- FG60F (FortiGate 60F)
- FG90G (FortiGate 90G)
- FGT_ (diversos)
- FMG-VM (FortiManager VM)
- FAZ-VM (FortiAnalyzer VM)

**Valor de pontos por dia (coluna H):** Varia de 0,62 até 18,54 pontos/dia dependendo do modelo

---

## ABA 4: "Base de Conciliação" (1.664 linhas × 9 colunas)

### ═══ ESTRUTURA ═══

É a **base oficial exportada do sistema Fortinet** com o consumo real registrado.

### ═══ CABEÇALHOS ═══

| Col | Título | Exemplo |
|-----|--------|---------|
| A | Serial Number | FG120GTK25003745 |
| B | Description | Open Finance |
| C | Configuration Name | Openfinance120G |
| D | Product Type | FortiGate Hardware |
| E | Usage Date | 2026-01-01 |
| F | Service Pack | FGHWUTP |
| G | Device Model | FG120G |
| H | Additional FPC modules | (vazio) |
| I | Points | 5,75 |

### ═══ CARACTERÍSTICAS ═══

- **~1.663 registros de consumo** (cada linha = consumo de um equipamento em uma data)
- **Período:** Janeiro 2026 (datas como 2026-01-01, 2026-01-31, etc.)
- **Mesmo Serial aparece múltiplas vezes** (consumo em múltiplas datas)
- **Coluna H (Additional FPC modules):** SEMPRE vazia
- **Service Pack:** FGHWUTP (padrão)
- **Maioria:** FortiGate Hardware
- **Points variam por modelo:** FG120G=5,75 | FG2H0G=12,66 | FG90G=4,12 | FG100E=3,34 | etc.

### ═══ PROPÓSITO ═══

Serve como **fonte de verdade oficial da Fortinet** para conciliar com o controle manual.
A fórmula na coluna O de "Pontos utilizados" faz:
```
=SUMIF('Base de Conciliação'!$A:$I, SerialNumber, 'Base de Conciliação'!$I:$I)
```
Isso permite comparar: "Quanto eu calculei manualmente (coluna L)" vs "Quanto a Fortinet registrou (coluna O)"

---

## ABA 5: "Planilha3" (11 linhas × 16 colunas) - **AUXILIAR**

### ═══ ESTRUTURA ═══

Tabela numérica simples no range J5:P9:

```
     J   K   L   M   N   O   P
5    1   2   3   4   5   6   7
6    8   9  10  11  12  13  14
7   15  16  17  18  19  20  21
8   22  23  24  25  26  27  28
9   29  30  31
```

**Fórmula única encontrada:**
```
[11,L] =$K$11*(3/5) → 12 = 20 * 3/5
```

> ⚠️ **PROPÓSITO PROVÁVEL:** Esta aba parece ser uma **planilha de rascunho/auxiliar** com dados numéricos de exemplo. Pode ser uma tabela de apoio para validação de cálculos ou referência para alguma funcionalidade não implementada. **Não tem conexão direta com as demais abas.**

---

## ABA 6: "Bases Auxiliares" (4 linhas × 2 colunas) - **AUXILIAR**

### ═══ DADOS ═══

| Linha | A | B |
|-------|---|-----|
| 1 | - | Responsável |
| 2 | - | Delivery |
| 3 | - | Projetos Especiais |
| 4 | - | Produtos |

> ⚠️ **PROPÓSITO:** Lista simples de responsáveis (3 categorias: Delivery, Projetos Especiais, Produtos). Possivelmente usada como **fonte para dropdowns/validação de dados** ou como tabela de referência para BI.

---

## ═══ MAPA DE RELACIONAMENTO ENTRE ABAS ═══

```
                   ┌──────────────────┐
                   │    Dashboard     │
                   │  (Painel Geral)  │
                   └────┬─────────┬───┘
                        │         │
                        │         │
             ┌──────────▼──┐  ┌──▼────────────┐
             │Pontos Bolsão│  │Pontos utilizados│
             │(20 Pacotes) │  │ (80 Equipamentos)│
             └─────────────┘  └──┬────────────┬─┘
                                │            │
                                │            │
                     ┌──────────▼──┐   ┌────▼──────────┐
                     │Base de      │   │Planilha3      │
                     │Conciliação  │   │(Auxiliar)     │
                     │(1.663 reg.) │   └───────────────┘
                     └─────────────┘
                         
                ┌──────────────────┐
                │Bases Auxiliares  │
                │(3 responsáveis)  │
                └──────────────────┘
```

### FLUXO DE DADOS:

1. **Base de Conciliação** (Fortinet) → Alimenta coluna O de **Pontos utilizados**
2. **Pontos utilizados** (coluna L) → Alimenta coluna F do **Dashboard** e coluna R de **Pontos Bolsão**
3. **Pontos Bolsão** (coluna R-S-T) → Alimenta colunas F-G-H do **Dashboard**
4. **Dashboard** → Consolida tudo num painel visual

---

## ═══ ANÁLISE CRÍTICA E OBSERVAÇÕES ═══

### ✅ PONTOS POSITIVOS

1. **Arquitetura sólida** com separação clara entre dados brutos (Conciliação), processamento (Pontos utilizados) e apresentação (Dashboard)
2. **Uso de Tabelas Estruturadas** (Tabela1, Tabela2) que facilitam expansão
3. **Fórmulas com proteção IF/IFERROR** para evitar erros visuais
4. **Conciliação automática** entre cálculo manual e base oficial Fortinet
5. **Detecção de duplicidade** de Seriais (coluna R)

### ⚠️ PONTOS DE ATENÇÃO

1. **Coluna H do Dashboard sempre ZERO** - "Previsão Utilização" nunca está sendo preenchida (coluna R de Pontos utilizados = "Repetição Serial" está OK/Duplicado, não valor de previsão)
2. **Proderj já usou TODO seu saldo** (130.000/130.000 used) mas o controle manual mostra zero - **INCONSISTÊNCIA GRAVE**
3. **Planilha3 e Bases Auxiliares** - abas com dados residuais/parados
4. **Data base congelada em 25/03/2026** (=TODAY() na célula I1) - todos os cálculos dependem desta data
5. **Delivery (Pull)** usa Used Amount = 49.838 no Point Pack ELAVM4715519864 mas não registra consumo manual equivalente

### 🔍 INSIGHTS

1. **820.000 pontos totais contratados** divididos em 20 pacotes
2. **Consumo atual: ~15.495 pontos** (soma coluna F do Dashboard)
3. **Taxa de utilização geral: ~1,9%** (muito baixa!)
4. **Maior consumidor: Delivery (Pull)** com 4.078 pontos
5. **Proderj:** 130.000 pontos já consumidos segundo Fortinet, mas 0 no controle manual

### 🧮 LOGICA DE NEGÓCIO COMPLETA

```
1. Cliente compra Point Pack (Ex: 50.000 pontos)
2. Equipamento FortiGate é instalado no cliente
3. Cada modelo de equipamento CONSOOME X pontos POR DIA (coluna H)
   - FG120G → 5,75 pts/dia
   - FG2H0G → 12,66 pts/dia
   - FG90G → 4,12 pts/dia
   - etc.
4. Calcula-se: Pontos Consumidos = ValorDia × DiasDecorridos
5. Concilia-se com a base oficial da Fortinet
6. Dashboard mostra saldo restante + % de utilização por equipe
```

### 📊 RESUMO DOS DADOS

| Métrica | Valor |
|---------|-------|
| Total de Point Packs | 20 |
| Total de Equipamentos | ~80 |
| Total Registros Conciliação | ~1.663 |
| Pontos Totais Contratados | 820.000 |
| Pontos Utilizados (manual) | ~15.495 |
| Pontos Utilizados (Fortinet) | ~179.838 |
| Saldo Total | ~640.162 |
| % Utilização (manual) | ~1,9% |
| % Utilização (Fortinet) | ~21,9% |