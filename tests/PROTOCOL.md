# Protocolo de validação — Farol

Cenários reproduzíveis para validar uma release. O cenário 8 é automatizado por `scripts/release.py`; os demais são executados com projetos-fixture mínimos e as skills reais, comparando o resultado ao esperado. Nenhum cenário altera código-fonte do projeto de teste.

| # | Cenário | Setup mínimo | Resultado esperado |
|---|---|---|---|
| 1 | Projeto vazio | 1 stack simples, sem docs | `/farol:init` recomenda bootstrap; contexto criado; zero comando inventado (só Confirmado/Não identificado); `/farol:status` sem erros |
| 2 | Doc parcial | README com comandos, sem regras de produto | Recomenda augment; README apontado, não copiado; só lacunas criadas; relatório separa coberto × criado × pendente |
| 3 | Doc madura | AGENTS.md + docs de decisão + hierarquia explícita | Recomenda adopt; índice de ponteiros; nenhuma paráfrase extensa; acréscimo always-on mínimo; autoridade do time preservada |
| 4 | Stack híbrida | package.json + sidecar/requisitos.txt | Node E Python detectados; sidecar reconhecido como runtime; nenhum omitido |
| 5 | Pasta ignorada | diretório grande no disco, listado no .gitignore | Nunca afirmado como versionado/distribuído; marcado (local, fora do repo) |
| 6 | Ponteiro morto | índice referenciando arquivo inexistente | `/farol:status` reporta ERRO com o caminho e recomendação de correção |
| 7 | Conflito de autoridade | CLAUDE.md do time divergindo do bloco do Farol | Precedência explícita aplicada (time vence); nada decidido por ordem física no arquivo |
| 8 | Empacotamento | `python3 scripts/release.py` | Zip sem diretórios literais de expansão; extração comparada byte a byte; exit 0 |
| 9 | Descoberta pós-install | instalar o plugin numa sessão aberta | INSTALL.md instrui `/reload-plugins` ou sessão nova; nenhuma promessa de descoberta imediata |
| 10 | Custo de contexto | rodar `/farol:status` após contextualizar em cada modo | Bytes + estimativa de tokens reportados vs `contextBudget`; adopt com acréscimo mínimo; alerta acima do warning |
| 11 | Política de modelo declarada sem override | manifest com `modelPolicy.declared: true` e categorias preenchidas; nenhum agent com `model:` distinto de `inherit` | `/farol:status` reporta a divergência (intenção declarada, sem efeito real); `scripts/audit_context.py` não falha (nível AVISO, não ERRO) |
| 12 | Telemetria desligada por padrão | projeto recém-inicializado, `telemetry.enabled` ausente ou `false` | Nenhum arquivo em `telemetry.path` é criado; `/farol:status` não alerta; `scripts/audit_context.py` não falha |
| 13 | Telemetria habilitada | manifest com `telemetry.enabled: true` + hook instalado; tarefas T0–T3 executadas | Linhas JSONL só com os campos permitidos (política h); nenhum campo proibido (prompt completo, código-fonte, segredo, dado pessoal); **todas** as classes registram, inclusive T0 sem nenhuma chamada de ferramenta |
| 14 | Telemetria ligada sem hook | `telemetry.enabled: true`, `fw-telemetry.py` ausente de `.claude/hooks/` | Nenhum registro é criado (não há caminho alternativo pelo modelo); `/farol:status` #17 e `audit_context.py` reportam AVISO "campo ligado sem escritor"; nada falha |
| 15 | Ausência de escrita dupla | framework com o hook como escritor único | `CLAUDE.md.ccf` não contém instrução de gravar linha JSONL; `audit_context.py` reporta ERRO (`telemetry-escrita-dupla`) se ela reaparecer |
| 16 | Leitura e comparação | log com linhas de duas `framework_version` | `report_telemetry.py --panel` cabe em 3 linhas; `--compare vA vB` produz delta por classificação; com dados de um só lado, RECUSA declarar economia; linha corrompida é contada e ignorada, nunca fatal (exit 0) |

Critério de release: cenário 8 automatizado passando + amostragem manual de pelo menos os cenários 3, 4 e 6 (os três que falharam na v1.1.0).

## Comparação A/B (Fluxo A vs Fluxo B) — item 14 da especificação

Metodologia para comparar consumo antes/depois desta série de 8 commits, sem declarar economia sem medição:

- Fluxo A ("Farol atual"): estado do framework antes do Commit 1 (regra de delegação por quantidade de arquivos, sem Execution Budget, sem Model Routing).
- Fluxo B ("Farol econômico"): estado após o Commit 7 (Task Router T0–T3, Execution Budget, Model Routing opt-in, workspace temporário).
- Suíte fixa de tarefas por classificação: T0 (corrigir texto, explicar comando, localizar símbolo), T1 (alterar propriedade, corrigir comportamento localizado, adicionar teste), T2 (investigar bug sem causa, localizar acoplamentos, confirmar regressão), T3 (alterar arquitetura, revisar persistência, mapear impacto transversal).
- Métricas a registrar por execução: agentes acionados, chamadas de ferramentas, arquivos lidos/relidos, documentos de contexto carregados, tamanho da resposta final, diagnóstico correto (sim/não), testes aprovados, decisões preservadas. A partir da v2.2.0 as seis primeiras saem medidas pelo hook — habilite a telemetria nos dois fluxos e agregue com `python3 scripts/report_telemetry.py . --compare <vA> <vB>`; as demais continuam manuais.
- Execução: rodar a mesma tarefa nos dois fluxos, mesmo projeto-fixture, mesma versão de modelo, registrar as métricas acima para ambos.
- Este protocolo descreve o procedimento reproduzível; nenhum número de economia deve ser declarado publicamente sem essas execuções terem sido de fato realizadas e registradas. O `--compare` recusa produzir delta quando falta dado de um dos lados — a regra é mecanizada, não apenas escrita.