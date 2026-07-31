---
name: init
description: >
  Instala o Claude Context Framework: cria estrutura de contexto, detecta
  stack, preserva arquivos existentes com backup. Invocado pelo usuário com
  /farol:init. Nunca modifica código-fonte.
disable-model-invocation: true
---

# /farol:init — Instalador do framework

Execute na ordem (alvos antes de referências: nenhum passo pode deixar o
projeto em estado inconsistente se interrompido). Nunca toque em código-fonte.

## 1. Pré-checagens

- Confirme a raiz do projeto (existe `.git/` ou o usuário confirma).
- Anote se há git disponível E repositório inicializado → define
  `anchor_mode`: `"git"` (ideal) ou `"date"` (degradado; avise que a
  atualização incremental fica limitada — recomende `git init`).
- Se `.claude/context/manifest.json` já existe: framework instalado. Informe
  a versão e pare (sugira /farol:update ou UPGRADE.md).

## 2. Estrutura e índice-stub (antes de qualquer referência a eles)

- Copie os templates do plugin (`${CLAUDE_PLUGIN_ROOT}/templates/`) para
  `.claude/context/_templates/` do projeto — cópia local permite ao time
  customizá-los; o /farol:contextualize sempre usa a cópia do projeto.
- Crie (se ausentes): `.claude/context/{modules,decisions}/` e
  `.claude/context/memory.md` a partir de `_templates/memory.md`.
- Crie `.claude/context/index.md` a partir de `_templates/index.md` com as
  seções em `_(pendente: /farol:contextualize)_`. Existir vazio > não existir:
  o import do CLAUDE.md jamais aponta para arquivo inexistente.

## 3. Detecção rápida de stack (orçamento: só manifestos)

Procure manifestos e configs na raiz E até 2 níveis de profundidade (fora
das exclusões): `package.json`, `pyproject.toml`, `requirements.txt`,
`go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`/`*.sln`,
`composer.json`, `Gemfile`, `Dockerfile`, `docker-compose*`, CI. Nomes não
são universais: reconheça variantes localizadas (ex.: `requisitos.txt`) e,
na dúvida, identifique pelo CONTEÚDO (um txt com linhas `pacote==versão` é
um manifesto pip, seja qual for o nome). Um subdiretório com manifesto
próprio (`sidecar/`, `api/`) é um runtime do produto — nunca o omita da
stack. NÃO leia código-fonte nem lockfiles.

Determine: linguagens, gerenciador de pacotes, frameworks e comandos
prováveis (marque `(inferido)`). Tipo de aplicação: preencha SOMENTE se
inequívoco pelos manifestos; caso contrário escreva `a confirmar` — um chute
errado no índice vale menos que uma lacuna honesta (o /farol:contextualize
confirma na primeira rodada).

## 3b. Seleção do modo (adopt | augment | bootstrap)

O usuário pode fixar o modo: `/farol:init --mode adopt|augment|bootstrap`.
Sem `--mode`, avalie a maturidade documental por sinais objetivos —
presença E substância de: AGENTS.md/CLAUDE.md, CONTRIBUTING.md, docs de
arquitetura, registros de decisão, princípios de produto, comandos
documentados, hierarquia de autoridade explícita. Um arquivo isolado não
basta; avalie cobertura.

- Cobertura ampla → recomende **adopt**: índice de ponteiros; a doc do time
  é a fonte.
- Cobertura parcial (ex.: README com comandos, sem regras de produto) →
  recomende **augment**: aproveitar o que existe e preencher só as lacunas.
- Sem documentação relevante → recomende **bootstrap**: construir o contexto.

Sinais claros → prossiga anunciando o modo escolhido e o porquê (1 linha).
Dúvida relevante entre dois modos → PERGUNTE ao usuário; nunca escolha em
silêncio. Registre o modo no manifesto.

## 4. Preencher o índice

Atualize `index.md` com o que a detecção descobriu; mantenha
`_(pendente: /farol:contextualize)_` no que faltar.

## 5. CLAUDE.md (backup e mesclagem)

- Se existir `CLAUDE.md`: copie para `.claude/backups/CLAUDE.md.<data>`.
  Depois MESCLE: preserve todo o conteúdo do time e acrescente o bloco entre
  `ccf:managed-start` e `ccf:managed-end` de
  `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md.ccf` (se o bloco já existir, substitua
  apenas o bloco).
- Se não existir: crie `CLAUDE.md` copiando
  `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md.ccf`.
- Jamais sobrescreva arquivos preexistentes em `.claude/context/`.

## 6. Manifesto

Crie `.claude/context/manifest.json`:

```json
{
  "framework": "farol",
  "version": "2.0.0",
  "installed_at": "<ISO-8601>",
  "contextualized_at": null,
  "anchor_mode": "git | date",
  "mode": "adopt | augment | bootstrap",
  "contextBudget": {
    "alwaysOnEstimatedTokens": null,
    "bytesPerToken": 3.0,
    "warningThresholdTokens": 1800,
    "hardLimitTokens": 2500
  },
  "anchor_commit": null,
  "inventory": {}
}
```

## 6b. Calibração da razão bytes/token

`bytes ÷ 4` subestima idiomas acentuados (medição de campo em pt-BR:
~2,6 bytes/token — erro de ~55%). Defina `bytesPerToken` no manifesto:
- Melhor opção — calibrar: se existir um documento com contagem de tokens
  conhecida (ex.: medida via `/context`), use `bytes ÷ tokens` dele.
- Sem calibração — escolha pelo idioma dominante do contexto:
  pt-BR/es/acentuados ≈ **2,6** · inglês ≈ **4,0** · misto/código ≈ **3,0**.
Na dúvida, use o valor MENOR: um guarda de orçamento deve superestimar o
custo (alarme cedo), nunca subestimá-lo (luz verde falsa).

## 7. Relatório final

Até 15 linhas: criado, preservado/backupeado, stack detectada, `anchor_mode`,
modo selecionado ou recomendado (com o porquê), e o próximo passo: **`/farol:contextualize`**. Ofereça (sem ativar sem
confirmação) os hooks opcionais de `.claude/hooks/README.md`. Sugira ao
usuário adicionar `.claude/backups/` ao `.gitignore` e commitar `.claude/` +
`CLAUDE.md` (ver INSTALL.md, passo 4) — sem executar comandos git por ele.
