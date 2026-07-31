---
name: fw-status
description: >
  Verifica a saúde do framework e o frescor do contexto: idade da âncora,
  commits acumulados, tamanho da memória, integridade dos arquivos. Use
  quando o usuário pedir /fw-status ou no início de tarefas grandes se houver
  suspeita de contexto desatualizado.
---

# /fw-status — Saúde do contexto

Somente leitura. Sem missões de scout, sem leitura de código-fonte.

## Verificações

1. `manifest.json` existe e é válido? (não → sugerir /fw-init)
2. `contextualized_at` nulo? (sim → sugerir /fw-contextualize)
3. Distância da âncora:
   - `anchor_mode` = "date" → reporte idade em dias e a limitação (sem git,
     sem incremental por diff); 30+ dias → recomendar /fw-update guiado.
   - `anchor_mode` = "git" → `git rev-list --count <anchor_commit>..HEAD`:
     0 → em dia · 1–19 → ok · 20+ → recomendar /fw-update. Âncora
     inexistente (rebase) → avisar; /fw-update resolve via fallback por data.
4. `memory.md`: linhas > 150 → recomendar /fw-consolidate.
5. Integridade: arquivos do `inventory` existem? Hash bate?
   Compare com `git hash-object <arquivo>` (mesmo método da escrita).
   (divergência = edição manual — legítima; apenas avise que o inventário
   será realinhado no próximo /fw-update.)
6. Tetos: algum arquivo de contexto estourou seu limite de linhas?

## Saída

Painel de até 12 linhas: versão do framework, idade do contexto (commits e
dias), status de cada verificação (OK/atenção), e no máximo 2 ações
recomendadas em ordem de prioridade.
