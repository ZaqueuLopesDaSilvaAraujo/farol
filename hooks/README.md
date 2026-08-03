# Hooks do framework

## Filosofia: hooks só onde determinismo é indispensável

Regras declarativas (CLAUDE.md) dependem do modelo obedecê-las. Três casos
merecem garantia mecânica; todo o resto fica declarativo de propósito:

1. **Segurança** (`fw-guard.sh`, PreToolUse): bloqueia comandos destrutivos
   antes de executarem, sempre.
2. **Frescor do contexto** (`fw-freshness.sh`, SessionStart): injeta 1 linha
   de aviso quando há 20+ commits desde a última contextualização — a
   detecção de "contexto que mente" não pode depender de o modelo lembrar.
3. **Telemetria** (`fw-telemetry.py`, v2.2.0): medição que o modelo faz de si
   mesmo não é medição. Contar ferramentas, agentes e duração é trabalho de
   código; ao modelo resta só a classificação T0–T3, que só ele sabe.

NÃO usamos hooks para injetar contexto de projeto (redundante com o índice
always-on) nem para atualizar memória automaticamente (mudança silenciosa em
base de conhecimento é corrupção difícil de detectar; preferimos as skills
explícitas /farol:update e /farol:consolidate).

## fw-guard.sh (opcional — requer bash; Windows: Git Bash/WSL)

- Analisa APENAS `tool_input.command` (via `jq`, ou `python3`, ou fallback
  bruto). Instale `jq` para precisão máxima.
- Exceções do time: `fw-guard-allow` ao lado do script copiado (1 regex por linha).
  Esse arquivo é do TIME e sobrevive a upgrades — nunca edite o script.
- Comando bloqueado + autorização do usuário = o usuário executa manualmente
  ou adiciona exceção. O hook não tem como saber o que foi autorizado na
  conversa; por isso bloqueia apenas o irreversível/raro (push, rm -rf,
  DROP...), não operações rotineiras como commit.

## fw-telemetry.py (opcional — requer python3; roda nativo no Windows)

Escritor determinístico da telemetria local. **Gate duplo**: só age se estiver
copiado para `.claude/hooks/` E o manifesto declarar `telemetry.enabled: true`.
Instalado com a telemetria desligada, é inerte — não escreve, não injeta nada,
sai `exit 0`.

- Diferente do guard, é Python: não depende de Git Bash/WSL no Windows.
- Nunca derruba a sessão — qualquer erro interno resulta em `exit 0`.
- Não grava prompt, código, saída de ferramenta nem trecho de arquivo.
  Arquivos fora de `.claude/context/` entram como hash (conta releitura sem
  registrar caminho). Veja a política completa em `policies.md`, seção h.
- Leitura do dado: `python3 scripts/report_telemetry.py . [--panel|--compare]`.
  Nada é agregado pelo modelo.
- **Descobrir o contrato da sua versão do Claude Code**: registre
  `--probe` em `SubagentStop`, rode uma tarefa T2 e leia
  `.claude/context/telemetry/probe.txt` — ele grava só as CHAVES do payload,
  nunca os valores. Se o seu Claude Code não expuser a identidade do
  subagente, `agents` fica anônimo e só a contagem é confiável.

## Ativação

0. Copie `fw-guard.sh` e `fw-guard-allow` (e, se quiser, `fw-freshness.sh`)
   de `${CLAUDE_PLUGIN_ROOT}/hooks/` para `.claude/hooks/` do PROJETO —
   hooks de segurança devem ser opt-in por projeto, nunca globais; por isso
   o plugin NÃO os auto-ativa via hooks.json.
1. No Windows, normalize o fim de linha após copiar (clones antigos podem
   ter extraído CRLF antes do `.gitattributes` da v2.0.1, e o shebang com
   `\r` quebra sob Git Bash): `sed -i 's/\r$//' .claude/hooks/*.sh`
2. `chmod +x .claude/hooks/fw-guard.sh .claude/hooks/fw-freshness.sh`
3. Mescle em `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "bash .claude/hooks/fw-guard.sh" } ] }
    ],
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "bash .claude/hooks/fw-freshness.sh" } ] }
    ],
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "python3 .claude/hooks/fw-telemetry.py --prompt" } ] }
    ],
    "PostToolUse": [
      { "hooks": [ { "type": "command", "command": "python3 .claude/hooks/fw-telemetry.py --tool" } ] }
    ],
    "SubagentStop": [
      { "hooks": [ { "type": "command", "command": "python3 .claude/hooks/fw-telemetry.py --subagent" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "python3 .claude/hooks/fw-telemetry.py --consolidate" } ] }
    ]
  }
}
```

Os quatro blocos de telemetria são opcionais e só fazem sentido juntos: sem
`--prompt` a tarefa não abre, sem `--consolidate` nada é gravado. No Windows,
troque `python3` por `python` se for o nome do seu executável.

4. Ajuste `BLOCK_PATTERNS` do guard à realidade do time (deploys, CLIs de
   infra, migrações) — ou, preferível, mantenha o script intacto e use
   `fw-guard-allow` para exceções.

Sem os hooks, as proibições continuam como regra declarativa no CLAUDE.md —
apenas sem garantia mecânica.
