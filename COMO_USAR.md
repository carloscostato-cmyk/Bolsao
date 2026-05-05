# Como usar o Sistema de Controle de Licenças Fortinet

---

## Acesso

Acesse **https://bolsao.onrender.com** e faça login com:

| Campo | Valor |
|---|---|
| Usuário | EstratOpera |
| Senha | Bolsao26 |

> Sem login, qualquer página redireciona automaticamente para a tela de autenticação.
> Para sair, clique em **Sair** no menu de navegação.

---

## Visão geral do fluxo

```
0. Login
        ↓
1. Cadastrar Bolsão (Point Pack)
        ↓
2. Registrar Equipamentos (Pontos Utilizados)
        ↓
3. Importar Base da Fortinet (Conciliação)
        ↓
4. Acompanhar no Dashboard
```

---

## Passo 1 — Cadastrar um Bolsão de Pontos

> Um bolsão é um pacote de pontos comprado para uma equipe/projeto.

**Onde:** Menu → **Pontos Bolsão** → botão **Adicionar Novo Point Pack**

| Campo | O que preencher |
|---|---|
| Número do Pack | Código do pacote (ex: ELAVM4715519864) |
| Responsável | Selecione: Delivery, Projetos Especiais ou Produtos |
| Projeto | Nome do subprojeto (ex: Pull, SIEM, MPM) |
| Pontos | Total de pontos do pacote (ex: 50000) |
| Usados | Pontos já consumidos segundo a Fortinet (pode ser 0) |
| Restantes | Calculado automaticamente: Pontos − Usados |
| Data Registro | Data em que o pacote foi adquirido (DD/MM/AAAA) |
| Data Expiração | Data de validade do pacote (DD/MM/AAAA) |

✅ Após salvar, o bolsão aparece na listagem de **Pontos Bolsão** com datas no formato DD/MM/AAAA.

> ⚠️ O Número do Pack deve ser único. Se tentar cadastrar um número já existente, o sistema exibe mensagem de erro sem travar.

---

## Passo 2 — Registrar um Equipamento (Ponto Utilizado)

> Cada equipamento FortiGate instalado num cliente consome X pontos por dia.

**Onde:** Menu → **Pontos Utilizados** → botão **Novo Ponto Utilizado**

| Campo | O que preencher |
|---|---|
| Bolsão | Selecione o grupo (Responsável + Projeto) — aparece apenas 1 opção por grupo, sempre o pack com maior saldo |
| Serial | Número de série do equipamento (ex: FG120GTK25003745) |
| Dados do Cliente | Nome do cliente ou site onde está instalado |
| Modelo do Produto | Modelo do equipamento (ex: FG120G, FG2H0G) |
| Valor Pontos Dia | Custo diário em pontos deste modelo (ex: 5.75) |
| Data Aplicação | Data em que o equipamento começou a consumir pontos |
| Data Fim | Data de encerramento (deixe em branco se ainda está ativo) |

✅ O sistema calcula automaticamente:
- **Dias Consumidos** — quantos dias já se passaram desde a Data Aplicação
- **Pontos Consumidos** — Valor Pontos Dia × Dias Consumidos

---

## Passo 3 — Importar a Base da Fortinet (Conciliação)

> A Fortinet gera um relatório oficial de consumo. Importe-o aqui para comparar com o seu controle.

**Onde:** Menu → **Conciliação**

### Como importar

1. Exporte o relatório de consumo do portal da Fortinet em formato **.xlsx**
2. O arquivo deve conter as colunas:
   - `Serial Number`
   - `Description`
   - `Usage Date`
   - `Points`
3. Clique em **Escolher arquivo**, selecione o .xlsx e clique em **Importar e Conciliar**

✅ O sistema irá:
- Substituir a base anterior pelos novos dados
- Cruzar automaticamente cada equipamento pelo **Serial Number**
- Exibir a tabela de conciliação com o resultado

### Como ler o resultado

| Status | Significado |
|---|---|
| ✔ OK | Seu cálculo bate com o da Fortinet (diferença < 0,01) |
| ▲ Acima | Você calculou **mais** pontos do que a Fortinet registrou |
| ▼ Abaixo | Você calculou **menos** pontos do que a Fortinet registrou |

A coluna **Diferença** mostra exatamente quanto os valores divergem.

---

## Passo 4 — Acompanhar o Dashboard

> Visão consolidada de todos os grupos com saldo e percentual de utilização.

**Onde:** Menu → **Dashboard**

### O que cada coluna mostra

| Coluna | Descrição |
|---|---|
| Grupo | Responsável + Projeto (ex: Delivery (Pull)) |
| Pontos Totais | Total de pontos contratados no bolsão |
| Used Totais (Fortinet) | Pontos consumidos segundo a Fortinet |
| Remaining (Fortinet) | Saldo pela ótica da Fortinet |
| Pontos Utilizados (Analítico) | Pontos calculados pelo sistema (Pts/Dia × Dias) |
| Faltantes (Analítico) | Saldo pela ótica do controle interno |
| % Fortinet | Percentual de uso segundo a Fortinet |
| % Analítico | Percentual de uso segundo o controle interno |

---

## Resumo rápido

```
┌─────────────────────────────────────────────────────────┐
│  PASSO 0   Faça login                                   │
│            https://bolsao.onrender.com                  │
├─────────────────────────────────────────────────────────┤
│  PASSO 1   Cadastre o bolsão (Point Pack)               │
│            Menu > Pontos Bolsão > Adicionar             │
├─────────────────────────────────────────────────────────┤
│  PASSO 2   Registre cada equipamento instalado          │
│            Menu > Pontos Utilizados > Novo              │
├─────────────────────────────────────────────────────────┤
│  PASSO 3   Importe o relatório .xlsx da Fortinet        │
│            Menu > Conciliação > Importar                │
├─────────────────────────────────────────────────────────┤
│  PASSO 4   Acompanhe o saldo e % de uso                 │
│            Menu > Dashboard                             │
└─────────────────────────────────────────────────────────┘
```

---

## Dicas importantes

- O **Serial Number** é a chave de ligação entre o seu controle e a base da Fortinet — cadastre-o exatamente como aparece no relatório da Fortinet.
- Se um equipamento ainda está ativo, **deixe o campo Data Fim em branco** — o sistema calcula o consumo até hoje automaticamente.
- A importação da base de conciliação **substitui** os dados anteriores. Sempre importe o relatório mais recente.
- O campo **Responsável** tem 3 opções fixas: **Delivery**, **Projetos Especiais** e **Produtos**.
- O campo **Bolsão** no formulário de novo equipamento mostra apenas **1 opção por grupo** — o sistema escolhe automaticamente o pack com maior saldo disponível.
- Datas são exibidas no formato **DD/MM/AAAA** (padrão brasileiro).
- Para sair do sistema, clique em **Sair** no menu de navegação.
