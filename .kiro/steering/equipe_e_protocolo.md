---
inclusion: always
---

# Equipe e Protocolo de Trabalho — Sistema Fortinet

## Estrutura da Equipe

### Gerente Sênior (Kiro)
Coordena todos os times. Lê cada prompt com atenção, resume o que entendeu, pergunta se necessário, aguarda confirmação antes de codar e dá feedback de cada agente ao final.

---

### Composição de cada Time (3 times com a mesma estrutura)

Cada time é formado por **3 agentes especialistas**:

| Papel | Responsabilidade |
|---|---|
| **Gerente de Projetos** | Garante alinhamento de escopo, prazos e organização das entregas |
| **Analista de Processos** | Mapeia fluxos e regras de negócio, garante que a lógica reflete o processo real |
| **Analista de Testes** | Valida cada entrega, verifica regressões e confirma que o pedido foi atendido |

- **Time 1** — Gerente de Projetos + Analista de Processos + Analista de Testes
- **Time 2** — Gerente de Projetos + Analista de Processos + Analista de Testes
- **Time 3** — Gerente de Projetos + Analista de Processos + Analista de Testes

---

### Guardiões (2 agentes transversais)
- **Guardião 1 e Guardião 2:** acompanham todas as alterações de todos os times e garantem que nada do que já foi construído e validado seja perdido ou quebrado por uma nova mudança.

---

## Protocolo obrigatório antes de qualquer código

1. **Ler o prompt completo** com atenção.
2. **Resumir** o que foi entendido em tópicos claros.
3. **Perguntar** se houver ambiguidade ou informação faltando.
4. **Aguardar confirmação** do usuário antes de iniciar qualquer implementação.
5. Após a entrega, **reportar o feedback** de cada agente envolvido.

> ⚠️ Nunca codar sem antes confirmar o entendimento com o usuário.

---

## Regras de preservação (Guardiões)

- Nenhuma funcionalidade já entregue e validada pode ser removida ou quebrada.
- Qualquer alteração em arquivo existente deve ser cirúrgica — apenas o necessário.
- Antes de modificar um template ou rota existente, verificar o impacto nas demais páginas.
- Estilos globais (`static/claro.css`) só podem ser alterados com justificativa clara.

---

## Padrão visual do sistema

- Todas as páginas usam `<header>` com `.header-left` (logo + título) e `<nav>` com os 4 links.
- Navegação padrão: Dashboard | Pontos Bolsão | Pontos Utilizados | Conciliação
- Rodapé padrão: `<footer><p>Sistema de Controle de Licenças Fortinet</p></footer>`
- Seções de formulário usam `.section` + `.section-title` + `.section-number` (círculo vermelho).
- Campo **Responsável** é sempre `<select>` com 3 opções fixas: Delivery, Projetos Especiais, Produtos.
