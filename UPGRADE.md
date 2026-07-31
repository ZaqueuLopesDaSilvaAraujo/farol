# Atualização do framework

## Modelo de propriedade (a regra que torna upgrades seguros)

| Área | Dono | Em upgrade |
|---|---|---|
| `.claude/agents/fw-*` | Framework | Substituir |
| `.claude/skills/fw-*` | Framework | Substituir |
| `.claude/hooks/fw-*` | Framework | Substituir (preserve seus BLOCK_PATTERNS customizados) |
| `.claude/context/_templates/` | Framework | Substituir |
| Bloco `ccf:managed-*` no CLAUDE.md | Framework | Substituir só o bloco |
| `.claude/context/**` (exceto `_templates`) | **Time** | **Nunca tocar** |
| CLAUDE.md fora do bloco gerenciado | **Time** | **Nunca tocar** |
| Agents/skills do time (sem prefixo `fw-`) | **Time** | **Nunca tocar** |

## Procedimento de upgrade (v1 → vN)

1. Leia o `CHANGELOG` da nova versão; verifique se há passos de migração de
   formato de contexto (raros; quando existirem, virão como skill
   `/fw-migrate` na própria versão nova).
2. Substitua os arquivos das quatro primeiras linhas da tabela.
3. Substitua apenas o bloco `ccf:managed-start … ccf:managed-end` do CLAUDE.md.
4. Atualize `"version"` no `.claude/context/manifest.json`.
5. Rode `/fw-status` para validar integridade.

## Migração 1.2.x → 1.3.0

No `.claude/context/manifest.json`: substitua `"adopt_mode": true|false` por
`"mode": "adopt"` (se era true) ou `"bootstrap"`/`"augment"` (conforme o
projeto), e adicione o bloco `contextBudget` (ver template no /fw-init).
Depois rode `/fw-status` — a checagem 11 valida os obrigatórios do modo.

## Customização sem conflito

Precisa de um agente/skill próprio do time? Crie **sem** o prefixo `fw-`
(ex.: `.claude/agents/dba.md`, `.claude/skills/deploy/`). Precisa mudar o
comportamento de um `fw-*`? Não edite o original: copie com outro nome e
desative o original removendo o arquivo — assim o upgrade nunca reverte sua
mudança silenciosamente.

## Extensão por stack

O framework não tem variação por tecnologia — a especificidade vive no
contexto gerado. Se o seu time precisar de procedimentos específicos de stack
(ex.: playbook de migração Django), o ponto de extensão é uma skill do time,
não um fork dos arquivos `fw-*`.

## Futuro: distribuição como plugin

A estrutura já é compatível com o formato de plugins do Claude Code (que
empacotam skills, agents e hooks em uma unidade instalável). Quando houver
múltiplos times consumindo o framework, publique-o como plugin em um
marketplace interno — o fluxo de instalação/atualização passa a ser nativo e
este documento vira apenas a política de propriedade.
