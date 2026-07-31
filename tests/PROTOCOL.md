# Protocolo de validação — Farol

Cenários reproduzíveis para validar uma release. O cenário 8 é automatizado
por `scripts/release.py`; os demais são executados com projetos-fixture
mínimos e as skills reais, comparando o resultado ao esperado. Nenhum
cenário altera código-fonte do projeto de teste.

| # | Cenário | Setup mínimo | Resultado esperado |
|---|---|---|---|
| 1 | Projeto vazio | 1 stack simples, sem docs | `/fw-init` recomenda **bootstrap**; contexto criado; zero comando inventado (só Confirmado/Não identificado); `/fw-status` sem erros |
| 2 | Doc parcial | README com comandos, sem regras de produto | Recomenda **augment**; README apontado, não copiado; só lacunas criadas; relatório separa coberto × criado × pendente |
| 3 | Doc madura | AGENTS.md + docs de decisão + hierarquia explícita | Recomenda **adopt**; índice de ponteiros; nenhuma paráfrase extensa; acréscimo always-on mínimo; autoridade do time preservada |
| 4 | Stack híbrida | `package.json` + `sidecar/requisitos.txt` | Node E Python detectados; sidecar reconhecido como runtime; nenhum omitido |
| 5 | Pasta ignorada | diretório grande no disco, listado no `.gitignore` | Nunca afirmado como versionado/distribuído; marcado `(local, fora do repo)` |
| 6 | Ponteiro morto | índice referenciando arquivo inexistente | `/fw-status` reporta ERRO com o caminho e recomendação de correção |
| 7 | Conflito de autoridade | CLAUDE.md do time divergindo do bloco do Farol | Precedência explícita aplicada (time vence); nada decidido por ordem física no arquivo |
| 8 | Empacotamento | `python3 scripts/release.py` | Zip sem diretórios literais de expansão; extração comparada byte a byte; exit 0 |
| 9 | Sessão existente | instalar com sessão do Claude Code aberta | INSTALL.md instrui sessão NOVA; nenhuma promessa de descoberta imediata |
| 10 | Custo de contexto | rodar `/fw-status` após contextualizar em cada modo | Bytes + estimativa de tokens reportados vs `contextBudget`; adopt com acréscimo mínimo; alerta acima do warning |

Critério de release: cenário 8 automatizado passando + amostragem manual de
pelo menos os cenários 3, 4 e 6 (os três que falharam na v1.1.0).
