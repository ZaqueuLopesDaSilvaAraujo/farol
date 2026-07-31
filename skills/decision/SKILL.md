---
name: decision
description: >
  Registra uma decisão arquitetural ou técnica como ADR curto em
  .claude/context/decisions/. Use quando o usuário pedir /farol:decision, ou
  sugira ao final de discussões em que uma decisão com trade-offs foi tomada
  nesta conversa.
---

# /farol:decision — Registro de decisão (ADR)

ADRs guardam o **porquê** — a categoria de conhecimento mais cara de perder e
a única que o código não consegue expressar. São append-only: nunca edite um
ADR aceito; substitua-o com um novo que o referencia.

## Procedimento

1. Determine o próximo número: maior `NNN` em `.claude/context/decisions/` + 1.
2. Crie `decisions/NNN-<slug-do-titulo>.md` com o template
   `_templates/decision.md`. Teto: 25 linhas. Preencha a partir da conversa
   atual; pergunte ao usuário apenas o que não estiver claro (contexto e
   alternativas rejeitadas são os campos que mais valem).
3. Se a decisão altera fato documentado (ex.: troca de lib, novo padrão),
   atualize a linha correspondente em `index.md`/`conventions.md` apontando
   `(ver ADR NNN)` — o detalhe fica no ADR, não duplicado.
4. Se substitui decisão anterior, marque a antiga como
   `Status: Substituída por NNN` (única edição permitida em ADR antigo).
5. Confirme em 3 linhas: número, título, arquivos de contexto tocados.
