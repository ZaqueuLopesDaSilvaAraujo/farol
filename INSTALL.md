# Instalação — Farol v1.1.0

Guia de uma página. Tempo total: ~10 minutos (a maior parte é a
contextualização, que roda sozinha).

## O que é (em 3 linhas)

Um conjunto de arquivos de configuração que o **Claude Code lê nativamente**.
Não é um programa: nada aqui "executa" por conta própria. Ele ensina o Claude
a conhecer o SEU projeto — arquitetura, comandos, convenções — gastando o
mínimo de tokens e sem nunca tocar no código-fonte.

## Pré-requisitos

- Claude Code instalado (https://docs.claude.com/en/docs/claude-code/overview)
- Projeto em um repositório git (recomendado; sem git funciona, mas perde a
  atualização incremental)

## Passos

**1. Extraia o zip na raiz do projeto**

```bash
cd /caminho/do/seu-projeto
unzip farol-v1.1.0.zip
```

Isso adiciona `.claude/`, `CLAUDE.md.ccf` e documentação. Seu código não é
tocado. Já tem `CLAUDE.md` ou `.claude/` próprios? Sem problema — o passo 2
preserva tudo com backup e mesclagem.

**2. Instale**

```bash
claude
```

Dentro da sessão, digite: `/fw-init`

O Claude detecta a stack (lendo só manifestos), cria a estrutura de contexto,
mescla/renomeia o `CLAUDE.md` com backup e grava o manifesto.

**3. Contextualize**

Digite: `/fw-contextualize`

O subagent `fw-scout` explora o projeto em rodadas com orçamento de leitura e
preenche `.claude/context/`. Ao final, o Claude pede validação de 3–5 fatos.
**Valide com atenção** — é o momento mais barato de corrigir um erro.

**4. Suba no git (é assim que o time inteiro herda o contexto)**

```bash
echo ".claude/backups/" >> .gitignore
git add .claude/ CLAUDE.md .gitignore
git commit -m "chore: instala Farol v1.1.0 + contexto inicial"
```

Commitar: `.claude/` (agents, skills, hooks, **context/**) e `CLAUDE.md`.
Ignorar: apenas `.claude/backups/`. O `.claude/context/` é o ativo mais
valioso — versionado, ele evolui por PR como qualquer código.

**5. (Opcional, recomendado) Ative o guardrail de segurança**

Siga `.claude/hooks/README.md` (2 minutos: `chmod +x` + bloco no
`settings.json`). Bloqueia deterministicamente `git push`, `rm -rf`, `DROP
TABLE` etc. Windows: requer Git Bash ou WSL.

## Pronto — uso no dia a dia

Não há nada para invocar: toda sessão do Claude Code nesta pasta já carrega o
contexto automaticamente. Os comandos abaixo são só manutenção:

| Quando | Comando |
|---|---|
| Depois de mudanças grandes no projeto | `/fw-update` |
| Quer checar se o contexto está em dia | `/fw-status` |
| Tomaram uma decisão técnica que vale registrar | `/fw-decision "título"` |
| `memory.md` passou de 150 linhas | `/fw-consolidate` |

Dúvidas de arquitetura e filosofia: `README.md`. Atualização de versão do
framework: `UPGRADE.md`.
