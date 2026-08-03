# Instalação — Farol v2.2.0

Guia de uma página. A partir da v2.0, o Farol é um **plugin do Claude Code**:
instala uma vez, vale para todos os seus projetos, atualiza sozinho.

## O que é (em 3 linhas)

Um plugin que ensina o Claude Code a conhecer o SEU projeto — arquitetura,
comandos, princípios, restrições — gastando o mínimo de tokens e sem nunca
tocar no código-fonte. A inteligência (skills e agents) mora no plugin; o
conhecimento de cada projeto mora em `.claude/context/`, que é seu.

## Antes de instalar: este framework é para o seu projeto?

O `/farol:init` avalia a maturidade da sua documentação e recomenda um modo:
**adopt** (doc madura → o Farol aponta para ela e caça o que é verdade e não
está escrito), **augment** (doc parcial → preenche só as lacunas) ou
**bootstrap** (sem doc → constrói o contexto). Você pode fixar:
`/farol:init --mode adopt|augment|bootstrap`. E se nada disso fizer sentido
para o seu caso, roube só a ideia da tabela "Carregue quando" do template de
índice — núcleo sempre carregado + seções sob demanda — sem instalar nada.

## Caminho recomendado: marketplace (2 comandos)

Dentro de qualquer sessão do Claude Code:

```
/plugin marketplace add ZaqueuLopesDaSilvaAraujo/farol
/plugin install farol@farol
```

Se os comandos `/farol:*` não aparecerem em seguida, rode `/reload-plugins`
ou reinicie a sessão — skills de plugin são carregadas no arranque. Nota
para automações e agentes: `/plugin …` são comandos embutidos da interface;
fora dela, use o CLI equivalente (`claude plugin marketplace add …`,
`claude plugin install …`).

**Custo global, dito com franqueza**: o plugin em escopo de usuário
adiciona ~0,9k tokens a TODA sessão da máquina — inclusive em projetos que
não usam o Farol (antes, quem não instalava não pagava). Se você tem muitos
projetos fora do Farol, adote a prática de desativá-lo neles
(`/plugin disable farol` / `enable`) ou avalie instalar em escopo de
projeto.

## Test-drive sem instalar nada

Quer experimentar antes de instalar? Carregue o Farol só para uma sessão:

```bash
claude --plugin-url https://github.com/ZaqueuLopesDaSilvaAraujo/farol/releases/latest/download/farol-v2.1.0.zip
```

(ou baixe o zip e use `claude --plugin-dir ./farol-v2.1.0.zip`). Nada fica
instalado ao fechar a sessão.

## Caminho alternativo: instalação local (zip)

Para ambientes sem acesso ao marketplace, baixe o zip da Release e:

```bash
unzip farol-v2.1.0.zip -d ~/farol
```

E na sessão do Claude Code: `/plugin install ~/farol`

(Extraia FORA dos seus projetos — o plugin não vive mais na raiz do projeto.)

## Primeiro uso em cada projeto

Abra o Claude Code na raiz do projeto e rode:

1. `/farol:init` — detecta stack e maturidade documental, recomenda o modo,
   cria `.claude/context/` e mescla o `CLAUDE.md` com backup.
2. `/farol:contextualize` — descobre (ou aponta e caça lacunas, conforme o
   modo) e preenche o contexto. Valide os 3–5 fatos-chave que ele apresentar.

## Suba o contexto no git (é assim que o time inteiro herda)

```bash
echo ".claude/backups/" >> .gitignore
git add .claude/ CLAUDE.md .gitignore
git commit -m "chore: contexto do projeto via Farol v2"
```

O plugin em si NÃO vai para o repositório do projeto — cada dev instala o
plugin uma vez na própria máquina (2 comandos acima). O que se versiona é o
`.claude/context/` e o `CLAUDE.md`: o conhecimento, não a ferramenta.

## (Opcional) Guardrail de segurança

Siga `hooks/README.md` do plugin: copiar o `fw-guard.sh` para o projeto e
registrar no `settings.json`. É opt-in por projeto, de propósito — um plugin
que bloqueia `git push` globalmente de surpresa seria exatamente o tipo de
comportamento que o Farol condena.

## Dia a dia

| Quando | Comando |
|---|---|
| Depois de mudanças grandes no projeto | `/farol:update` |
| Checar saúde, ponteiros e orçamento de contexto | `/farol:status` |
| Registrar uma decisão técnica | `/farol:decision "título"` |
| `memory.md` passou de 150 linhas | `/farol:consolidate` |

Atualização do plugin: `/plugin` → aba do marketplace → update (ou reinstale
pelo mesmo comando). Migração da 1.x: `UPGRADE.md`.
