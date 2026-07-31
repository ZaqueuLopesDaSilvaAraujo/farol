---
name: fw-init
description: >
  Instala o Claude Context Framework: cria estrutura de contexto, detecta
  stack, preserva arquivos existentes com backup. Invocado pelo usuário com
  /fw-init. Nunca modifica código-fonte.
disable-model-invocation: true
---

# /fw-init — Instalador do framework

Execute na ordem (alvos antes de referências: nenhum passo pode deixar o
projeto em estado inconsistente se interrompido). Nunca toque em código-fonte.

## 1. Pré-checagens

- Confirme a raiz do projeto (existe `.git/` ou o usuário confirma).
- Anote se há git disponível E repositório inicializado → define
  `anchor_mode`: `"git"` (ideal) ou `"date"` (degradado; avise que a
  atualização incremental fica limitada — recomende `git init`).
- Se `.claude/context/manifest.json` já existe: framework instalado. Informe
  a versão e pare (sugira /fw-update ou UPGRADE.md).

## 2. Estrutura e índice-stub (antes de qualquer referência a eles)

- Crie (se ausentes): `.claude/context/{modules,decisions}/` e
  `.claude/context/memory.md` a partir de `_templates/memory.md`.
- Crie `.claude/context/index.md` a partir de `_templates/index.md` com as
  seções em `_(pendente: /fw-contextualize)_`. Existir vazio > não existir:
  o import do CLAUDE.md jamais aponta para arquivo inexistente.

## 3. Detecção rápida de stack (orçamento: só manifestos)

Leia APENAS manifestos e configs na raiz (e raízes de workspaces, se
monorepo): `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`,
`Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`/`*.sln`,
`composer.json`, `Gemfile`, `Dockerfile`, `docker-compose*`, CI. NÃO leia
código-fonte nem lockfiles.

Determine: linguagens, gerenciador de pacotes, frameworks, tipo de aplicação
(API, web, desktop, mobile, lib, CLI, monorepo, microsserviços) e comandos
prováveis de build/teste/execução (marque `(inferido)`).

## 4. Preencher o índice

Atualize `index.md` com o que a detecção descobriu; mantenha
`_(pendente: /fw-contextualize)_` no que faltar.

## 5. CLAUDE.md (backup e mesclagem)

- Se existir `CLAUDE.md`: copie para `.claude/backups/CLAUDE.md.<data>`.
  Depois MESCLE: preserve todo o conteúdo do time e acrescente o bloco entre
  `ccf:managed-start` e `ccf:managed-end` de `CLAUDE.md.ccf` (se o bloco já
  existir, substitua apenas o bloco).
- Se não existir: renomeie `CLAUDE.md.ccf` para `CLAUDE.md`.
- Jamais sobrescreva arquivos preexistentes em `.claude/context/`.

## 6. Manifesto

Crie `.claude/context/manifest.json`:

```json
{
  "framework": "farol",
  "version": "1.1.0",
  "installed_at": "<ISO-8601>",
  "contextualized_at": null,
  "anchor_mode": "git | date",
  "anchor_commit": null,
  "inventory": {}
}
```

## 7. Relatório final

Até 15 linhas: criado, preservado/backupeado, stack detectada, `anchor_mode`,
e o próximo passo: **`/fw-contextualize`**. Ofereça (sem ativar sem
confirmação) os hooks opcionais de `.claude/hooks/README.md`. Sugira ao
usuário adicionar `.claude/backups/` ao `.gitignore` e commitar `.claude/` +
`CLAUDE.md` (ver INSTALL.md, passo 4) — sem executar comandos git por ele.
