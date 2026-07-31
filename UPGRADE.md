# Atualização e migração

## Era do plugin (v2.0+)

Atualizar o Farol é operação nativa do Claude Code: `/plugin` → marketplace
`farol` → update. Nada no seu projeto é tocado pela atualização do plugin.

## Modelo de propriedade

| Área | Dono | Em atualização |
|---|---|---|
| Plugin (skills, agents, hooks, templates-fonte) | Framework | Atualizado via /plugin |
| `.claude/context/**` do projeto | **Time** | **Nunca tocado** |
| `.claude/context/_templates/` do projeto | Time (cópia customizável) | Só substituída se você rodar /farol:init de novo e aceitar |
| CLAUDE.md fora do bloco `ccf:managed-*` | **Time** | **Nunca tocado** |
| Bloco `ccf:managed-*` | Framework | Atualizado só pelo /farol:init, com backup |
| Hooks copiados para `.claude/hooks/` + `fw-guard-allow` | Time (opt-in) | Nunca tocados; recopie do plugin se quiser a versão nova |

## Migração 1.x → 2.0

1. Instale o plugin (2 comandos — ver INSTALL.md).
2. Em cada projeto que usava o zip da 1.x, remova a cópia embutida do
   framework: `.claude/skills/fw-*`, `.claude/agents/fw-*` e, se não
   customizou, `.claude/hooks/fw-*`. **NÃO remova** `.claude/context/` nem o
   CLAUDE.md — são seus.
3. Os comandos mudaram de nome: `/fw-<skill>` → `/farol:<skill>`
   (ex.: `/fw-status` → `/farol:status`). Os agents mantêm os nomes
   (`fw-scout`, `fw-reviewer`, `fw-debugger`).
4. Rode `/farol:status` — ele valida manifesto, bloco gerenciado e ponteiros.
5. Manifesto: se vier da 1.2.x, aplique também a migração abaixo.

## Migração 1.2.x → 1.3.x (manifesto)

No `.claude/context/manifest.json`: substitua `"adopt_mode": true|false` por
`"mode": "adopt"` (se era true) ou `"bootstrap"`/`"augment"`, e adicione o
bloco `contextBudget` com `bytesPerToken` calibrado (ver /farol:init §6b).

## Customização sem conflito

Skills/agents próprios do time: crie normalmente em `.claude/` do projeto,
com qualquer nome sem o namespace `farol:` — plugin e projeto convivem sem
colisão (é para isso que o namespace existe). Para mudar o comportamento de
uma skill do plugin, não edite o plugin: copie o SKILL.md para
`.claude/skills/<nome>/` do projeto com outro nome e use a sua versão.
