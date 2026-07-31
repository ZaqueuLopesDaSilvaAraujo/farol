<p align="center">
  <img src="assets/banner.png" alt="Farol — context framework para Claude Code" width="100%">
</p>

# Farol — v1.1.0

**Contexto, memória e agentes especializados para o Claude Code — em qualquer stack.**
*Farol ("lighthouse"): project context, memory and specialized agents for Claude Code, on any stack. Docs in Brazilian Portuguese.*

Como um farol: guia o Claude pelo seu projeto **sem nunca tocar no código**,
ilumina apenas o necessário (economia de tokens) e permanece aceso entre
sessões (memória persistente).

> Projeto independente, não afiliado nem endossado pela Anthropic.
> Claude Code é um produto da Anthropic.


O Farol é uma camada fina e reutilizável que transforma o Claude Code em um
assistente especializado em **qualquer** projeto, separando:

- **Inteligência** (agents e skills `fw-*`): genérica, permanente, atualizável.
- **Contexto** (`.claude/context/`): específico do projeto, propriedade do time,
  jamais tocado por upgrades do framework.

Funciona em qualquer stack (Node, Python, Java, .NET, Go, Rust, monorepos,
CLI, mobile, Electron...) porque nenhum arquivo `fw-*` contém conhecimento
de projeto: todo conhecimento específico é descoberto na contextualização.

## Instalação

1. Copie o conteúdo deste diretório para a raiz do projeto
   (o diretório `.claude/` e o arquivo `CLAUDE.md.ccf`).
2. Abra o Claude Code na raiz do projeto e execute: `/fw-init`
3. Em seguida execute: `/fw-contextualize`

Pronto. Todas as conversas futuras usam `.claude/context/` como fonte
primária de conhecimento, com carga mínima de tokens.

## Comandos

| Comando | Função |
|---|---|
| `/fw-init` | Instala o framework, detecta stack, preserva arquivos existentes com backup |
| `/fw-contextualize` | Descobre arquitetura, módulos, comandos e convenções e preenche o contexto |
| `/fw-update` | Atualização incremental do contexto (ancorada em `git diff`) |
| `/fw-consolidate` | Consolida a memória: deduplica, promove decisões, remove efêmeros |
| `/fw-decision "título"` | Registra uma decisão arquitetural (ADR curto) |
| `/fw-status` | Verifica frescor e saúde do contexto |

## Subagents

- `fw-scout` — explora o repositório em contexto isolado e devolve resumos.
- `fw-reviewer` — revisa mudanças sob 4 lentes: qualidade, segurança, performance, testes.
- `fw-debugger` — investiga falhas com ciclo de hipóteses, sem poluir a conversa.

Implementação e arquitetura acontecem na **sessão principal** (que conhece a
conversa inteira). Subagents existem apenas onde o isolamento de contexto é
vantagem: tarefas que leem muito e devolvem pouco.

## Segurança

O framework nunca altera código-fonte, instala dependências, faz commit/push
ou executa comandos destrutivos sem autorização explícita. Além das regras
declarativas, o hook opcional `fw-guard.sh` (PreToolUse) **bloqueia**
deterministicamente comandos destrutivos. Veja `.claude/hooks/README.md`.

## Atualização do framework

Tudo que é do framework tem prefixo `fw-`. Para atualizar para uma nova
versão: substitua `.claude/agents/fw-*` e `.claude/skills/fw-*` e siga
`UPGRADE.md`. **Nunca** substitua `.claude/context/` — ele é seu.

## Economia de tokens (mecanismos)

1. Always-on = apenas `context/index.md` (~1–2k tokens), via import no CLAUDE.md.
2. Todo o resto carrega sob demanda, guiado pela tabela "carregue quando" do índice.
3. Leituras pesadas rodam no `fw-scout` (contexto isolado, retorna só resumo).
4. Contextualização com orçamento duro de leitura e lista de exclusão obrigatória.
5. Atualização incremental ancorada no commit registrado em `manifest.json`.
6. `memory.md` com teto de 150 linhas + consolidação periódica.
