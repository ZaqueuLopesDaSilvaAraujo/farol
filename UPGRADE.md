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

## Migração 2.1.0 → 2.2.0 (opcional)

A v2.2.0 adiciona **telemetria local determinística**, desligada por padrão.
**Nada muda sem ação sua** — atualizar o plugin não passa a registrar nada.

O que o upgrade faz sozinho: ao rodar `/farol:init` (modo atualização), o
bloco gerenciado do `CLAUDE.md.ccf` perde 4 linhas de instrução de telemetria
que a v2.1.0 mantinha always-on — **devolve ~106 tokens em toda sessão**,
mesmo para quem nunca usar o recurso.

Para adotar a telemetria (3 passos, todos opt-in):

1. Acrescente o bloco ao `.claude/context/manifest.json`:
   ```json
   "telemetry": {
     "enabled": true,
     "path": ".claude/context/telemetry/log.jsonl",
     "schemaVersion": 1, "recordFilePaths": false,
     "retainDays": 90, "maxLines": 5000
   }
   ```
   `path` aceita caminho absoluto — útil para medir um repositório sem sujar
   o diff dele (o arquivo transitório da tarefa segue o mesmo diretório).
2. Copie `hooks/fw-telemetry.py` para `.claude/hooks/` e registre os 4
   eventos no `settings.json` (ver `hooks/README.md`). Sem o hook, o campo
   ligado **não gera registro** — não existe caminho alternativo pelo modelo.
3. Adicione o diretório da telemetria ao `.gitignore`: é registro
   operacional local, não conhecimento de projeto.

Leitura: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/report_telemetry.py .` — ou
`--panel` para as 3 linhas que o `/farol:status` exibe. O relatório valida
cada linha contra a lista de campos permitidos da seção h do `policies.md` e
denuncia violação de política.

Manifesto sem o bloco `telemetry` continua válido: a auditoria trata a
ausência como AVISO, nunca ERRO.

## Migração 2.0.x → 2.1.0 (opcional)

A v2.1.0 adiciona políticas por projeto e o fluxo colaborativo. Nada muda
sem ação sua. Para adotar: rode `/farol:init` (modo atualização) — ele cria
`.claude/context/policies.md` do template com tudo em padrão; preencha os
campos que o time já decidiu e commite junto do contexto.

## Migração 1.x → 2.0

1. Instale o plugin (2 comandos — ver INSTALL.md; agentes e automações usam
   o CLI: `claude plugin marketplace add …` / `claude plugin install …`).
2. Em cada projeto que usava o zip da 1.x, remova a cópia embutida:
   `.claude/skills/fw-*`, `.claude/agents/fw-*`, `.claude/hooks/fw-*` (se
   não customizados — compare IGNORANDO fim de linha, pois o git converte
   CRLF no Windows e o hash acusa customização falsa), o
   `.claude/hooks/README.md` da 1.x, e os diretórios `.claude/skills/` e
   `.claude/agents/` se ficarem vazios. **NÃO remova** `.claude/context/`
   nem o CLAUDE.md — são seus. A remoção dos agents antigos não é só
   higiene: agents em `.claude/agents/` do projeto SOBRESCREVEM agents
   homônimos do plugin (comportamento documentado do Claude Code) — um
   `fw-scout` da 1.x esquecido no projeto silenciaria o do plugin.
3. **Rode `/farol:init`** — em modo atualização, ele substitui o bloco
   gerenciado do CLAUDE.md (que ainda ensina comandos `/fw-*` mortos) e
   oferece refrescar `.claude/context/_templates/`, tudo com backup. Este
   passo NÃO é opcional: sem ele, o arquivo always-on continua mentindo.
4. Os comandos mudaram: `/fw-<skill>` → `/farol:<skill>`. Agents mantêm os
   nomes (`fw-scout`, `fw-reviewer`, `fw-debugger`).
5. Rode `/farol:status` — as checagens 9 e 13 confirmam bloco na versão
   certa e manifesto no esquema novo; se vier da 1.2.x, aplique também a
   migração de manifesto abaixo.
6. Revise o `git status` e commite o resultado — a migração mexe em vários
   arquivos do `.claude/` e no CLAUDE.md.

## Clones anteriores à v2.0.1 (Windows/CRLF)

O `.gitattributes` (LF em scripts) só vale para arquivos re-extraídos; um
clone antigo mantém CRLF em arquivos que não mudaram desde então. Para
normalizar de uma vez: `git add --renormalize . ` no clone — ou simplesmente
atualize para a v2.0.2+, cujos hooks foram tocados de propósito para forçar
a re-extração com LF.

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
