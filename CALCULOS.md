# Lógica de Cálculo — Sistema de Controle de Licenças Fortinet

---

## Conceito base

O sistema calcula o consumo de pontos de cada equipamento FortiGate com base em **quantos dias ele ficou ativo** multiplicado pelo **custo diário em pontos** daquele modelo.

```
Pontos Consumidos = Valor Pontos Dia × Dias Consumidos
```

---

## 1. Dias Consumidos

O cálculo dos dias depende se o equipamento ainda está ativo ou já foi encerrado.

### Equipamento ainda ativo (sem Data Fim)

```
Dias Consumidos = Data de Hoje − Data Aplicação
```

**Exemplo:**
```
Data Aplicação : 01/01/2026
Hoje           : 05/05/2026
Dias Consumidos: 124 dias
```

### Equipamento encerrado (com Data Fim no passado)

```
Dias Consumidos = Data Fim − Data Aplicação
```

**Exemplo:**
```
Data Aplicação : 01/01/2026
Data Fim       : 01/03/2026
Dias Consumidos: 59 dias
```

### Equipamento com Data Fim futura

```
Dias Consumidos = Data de Hoje − Data Aplicação
```
> Ainda não encerrou, então conta até hoje — igual ao equipamento ativo.

---

## 2. Pontos Consumidos

```
Pontos Consumidos = Valor Pontos Dia × Dias Consumidos
```

**Exemplo:**
```
Modelo         : FG120G
Valor Pontos Dia: 5,75 pts/dia
Dias Consumidos : 124 dias

Pontos Consumidos = 5,75 × 124 = 713,00 pontos
```

### Referência de custo por modelo (valores do Excel de estudo)

| Modelo | Pts/Dia |
|---|---|
| FG120G | 5,75 |
| FG2H0G | 12,66 |
| FG90G | 4,12 |
| FG100E | 3,34 |
| FG100F | ~3,50 |
| FG60F | ~1,80 |
| FMG-VM | variável |
| FAZ-VM | variável |

> ⚠️ O valor exato de cada modelo deve ser consultado na tabela oficial da Fortinet e informado no campo **Valor Pontos Dia** ao cadastrar o equipamento.

---

## 3. Previsão de consumo futuro

Quando o equipamento tem uma **Data Fim futura**, o sistema também calcula quanto ainda vai consumir.

```
Tempo Faltante (dias) = Data Fim − Data de Hoje
Pontos a Consumir     = Valor Pontos Dia × Tempo Faltante
```

**Exemplo:**
```
Hoje           : 05/05/2026
Data Fim       : 31/12/2026
Tempo Faltante : 240 dias
Valor Pontos Dia: 5,75

Pontos a Consumir = 5,75 × 240 = 1.380,00 pontos
```

Se não houver Data Fim, o campo fica em branco (consumo indefinido).

---

## 4. Saldo do Bolsão (Remaining)

```
Remaining = Pontos Totais − Used Amount (Fortinet)
```

**Exemplo:**
```
Pontos Totais : 50.000
Used Amount   : 49.838,42
Remaining     : 161,58 pontos
```

---

## 5. Dashboard — Consolidado por Grupo

O Dashboard agrega todos os equipamentos de um mesmo grupo (Responsável + Projeto).

### Pontos Utilizados (Visão Analítica)

```
Pontos Utilizados do Grupo = Σ Pontos Consumidos de todos os equipamentos do grupo
```

### Faltantes (Visão Analítica)

```
Faltantes = Pontos Totais do Grupo − Pontos Utilizados do Grupo
```

### % Fortinet

```
% Fortinet = Used Totais (Fortinet) / Pontos Totais × 100
```

### % Analítico

```
% Analítico = Pontos Utilizados (calculado) / Pontos Totais × 100
```

**Exemplo completo de um grupo:**
```
Grupo          : Delivery (Pull)
Pontos Totais  : 200.000
Used (Fortinet): 49.838,42
Calculado      :  4.078,09

Remaining      : 200.000 − 49.838,42 = 150.161,58
Faltantes      : 200.000 −  4.078,09 = 195.921,91
% Fortinet     : 49.838,42 / 200.000 = 24,92%
% Analítico    :  4.078,09 / 200.000 =  2,04%
```

---

## 6. Conciliação

A conciliação compara o que o sistema calculou com o que a Fortinet registrou oficialmente.

```
Pontos Fortinet (por serial) = Σ Points da base de conciliação WHERE serial = serial do equipamento
Diferença = Pontos Calculados − Pontos Fortinet
```

| Resultado | Interpretação |
|---|---|
| Diferença ≈ 0 | Controle interno alinhado com a Fortinet ✔ |
| Diferença > 0 | Sistema calculou **mais** do que a Fortinet registrou — possível equipamento com data errada ou modelo com custo diferente |
| Diferença < 0 | Sistema calculou **menos** do que a Fortinet registrou — possível equipamento não cadastrado ou Data Aplicação posterior ao real |

---

## 7. Validação de Serial Duplicado

O sistema verifica se o mesmo Serial Number foi cadastrado mais de uma vez em Pontos Utilizados.

```
SE CONTAR(serial_number na tabela) > 1 → "Duplicado"
SE CONTAR(serial_number na tabela) = 1 → "OK"
```

> Um serial duplicado significa que o mesmo equipamento está sendo contado duas vezes, inflando o consumo calculado.

---

## Resumo das fórmulas

| Cálculo | Fórmula |
|---|---|
| Dias consumidos (ativo) | `hoje − data_aplicacao` |
| Dias consumidos (encerrado) | `data_fim − data_aplicacao` |
| Pontos consumidos | `valor_pontos_dia × dias_consumidos` |
| Tempo faltante | `data_fim − hoje` (se data_fim futura) |
| Pontos a consumir | `valor_pontos_dia × tempo_faltante` |
| Remaining bolsão | `pontos − used_amount` |
| Faltantes grupo | `pontos_totais − pontos_utilizados` |
| % Fortinet | `used_totais / pontos_totais × 100` |
| % Analítico | `pontos_utilizados / pontos_totais × 100` |
| Conciliação | `Σ points (base Fortinet) por serial` |
| Diferença | `pontos_calculados − pontos_fortinet` |
