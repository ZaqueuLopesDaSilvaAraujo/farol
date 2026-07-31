---
name: consolidate
description: >
  Consolida a memória do projeto: deduplica, promove conhecimento maduro para
  os arquivos de contexto corretos, converte justificativas em ADRs e remove
  informação efêmera. Use quando o usuário pedir /farol:consolidate ou quando
  memory.md ultrapassar 150 linhas.
disable-model-invocation: true
---

# /farol:consolidate — Manutenção da memória

`memory.md` é uma antessala, não um arquivo-destino. Conhecimento maduro migra
para o lugar certo; o resto morre. Teto pós-consolidação: 80 linhas.

## Procedimento

1. Leia `.claude/context/memory.md` e classifique cada entrada:
   - **Promover**: fato estável sobre comando/stack → `index.md`; sobre
     estrutura → `architecture.md` ou `modules/*`; sobre estilo →
     `conventions.md`. Mover = escrever lá e apagar daqui (zero duplicação).
   - **Virar ADR**: entrada que explica um *porquê* (trade-off, decisão) →
     crie ADR via procedimento do /farol:decision e apague a entrada.
   - **Manter**: aprendizado recente ainda não confirmado pelo uso
     (menos de ~30 dias na dúvida) — mantenha, 1 linha.
   - **Apagar**: efêmero (estado de tarefas, bugs já corrigidos, TODOs),
     duplicado, ou contradito por informação mais nova. Em contradição,
     vence a entrada mais recente; registre a mudança como ADR se relevante.
2. Reescreva `memory.md` apenas com as entradas mantidas, agrupadas por seção
   (Comandos e ambiente / Pegadinhas / Domínio / Outros), 1 linha cada, com
   data `(AAAA-MM)`.
3. Atualize os hashes afetados no `manifest.json`.
4. Relatório em até 8 linhas: promovidas, viraram ADR, apagadas, mantidas.
