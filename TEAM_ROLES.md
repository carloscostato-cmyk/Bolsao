Equipe e regras de permissão — SISTEMA BOLSAO

Objetivo:
- Garantir que apenas os dois especialistas designados alterem estilos (cores/brand) do dashboard e campos relacionados.

Papéis:
- Time 1 — Frontend: alterações seguras (estrutura, markup). NÃO modificar cores ou estilos globais sem aprovação.
- Time 2 — Backend/Conciliação: responsável por aplicar cores do Excel no dashboard (apenas CSS/temas). Em progresso.
- Keeper: mantém requisitos e aprova mudanças de alto impacto.

Regras operacionais:
1. Somente os 2 especialistas do Time 2 podem alterar arquivos em `static/*.css` e os cabeçalhos em `templates/*.html` relacionados às classes `.fortinet-col`, `.analitica-col`, `.percent-col`.
2. Qualquer outra mudança deve ser tratada via pull request com aprovação do Keeper.
3. Para alterações de cores, informar no PR: cores (hex), local (arquivo e linhas), motivo e screenshot.

Arquivos sob controle restrito (exemplos):
- `static/claro.css`
- `templates/index.html`
- `templates/pontos_bolsao.html`
- `templates/pontos_utilizados.html`

Observação:
- Este arquivo é apenas uma convenção de equipe; para enforcement real, crie regras de proteção de branch e CODEOWNERS no repositório remoto.
