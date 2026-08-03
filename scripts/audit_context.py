#!/usr/bin/env python3
"""Audita o contexto do Farol.

Verifica regras obrigatorias do framework (bloco always-on enxuto,
task router T0-T3, ausencia da regra de delegacao por quantidade de
arquivos, execution budget, workspace temporario, criterio de parada
do Scout, limite de hipoteses do Debugger, gatilho de risco do
Reviewer, politica de modelos) e reporta OK/AVISO/ERRO por checagem.

Uso:
  python3 scripts/audit_context.py [raiz]

Sem argumento, audita o proprio framework (CLAUDE.md.ccf, agents/,
templates/). Com uma raiz de projeto que tenha .claude/context/,
audita tambem o contexto instalado nesse projeto (index.md, memory.md,
manifest.json, workspace/).

Saida: codigo 1 se alguma regra obrigatoria (nivel ERRO) falhar.
"""
import json
import os
import re
import sys

ERROR = "ERRO"
WARN = "AVISO"
OK = "OK"

THREE_FILE_RULE = re.compile(
    r"3\+?\s*arquivos|tr[êe]s\s*(ou mais)?\s*arquivos", re.IGNORECASE
)


def read(path):
  if not os.path.isfile(path):
    return None
  with open(path, encoding="utf-8") as fh:
    return fh.read()


def count_lines(text):
  return len(text.splitlines()) if text else 0


class Report:
  def __init__(self):
    self.items = []

  def add(self, level, check, detail):
    self.items.append((level, check, detail))

  def has_errors(self):
    return any(item[0] == ERROR for item in self.items)

  def render(self):
    out = ["Auditoria de contexto - Farol", ""]
    for level, check, detail in self.items:
      out.append("[%s] %s: %s" % (level, check, detail))
    n_err = sum(1 for item in self.items if item[0] == ERROR)
    n_warn = sum(1 for item in self.items if item[0] == WARN)
    out.append("")
    out.append("Total: %d erro(s), %d aviso(s)" % (n_err, n_warn))
    return "\n".join(out)


def check_teto(report, path, teto, nome):
  text = read(path)
  if text is None:
    report.add(WARN, nome, "%s nao encontrado" % path)
    return None
  n = count_lines(text)
  if n > teto:
    report.add(ERROR, nome, "%s tem %d linhas (teto %d)" % (path, n, teto))
  else:
    report.add(OK, nome, "%s com %d linhas (teto %d)" % (path, n, teto))
  return text


def check_pattern(report, text, path, pattern, label, proibido):
  if text is None:
    return
  found = bool(pattern.search(text))
  if proibido and found:
    report.add(ERROR, label, "%s contem regra proibida" % path)
  elif proibido:
    report.add(OK, label, "regra proibida ausente em %s" % path)
  elif found:
    report.add(OK, label, "criterio presente em %s" % path)
  else:
    report.add(WARN, label, "%s nao contem o criterio esperado" % path)


def check_agents(report, agents_dir):
  scout = read(os.path.join(agents_dir, "fw-scout.md"))
  check_pattern(report, scout, "fw-scout.md", THREE_FILE_RULE, "scout-regra-3-arquivos", True)
  parada = re.compile(r"suficient|par(e|ar) quando", re.IGNORECASE)
  check_pattern(report, scout, "fw-scout.md", parada, "scout-criterio-parada", False)

  debugger = read(os.path.join(agents_dir, "fw-debugger.md"))
  hipoteses = re.compile(r"3\s*hip[óo]teses|m[áa]ximo de.*hip[óo]teses", re.IGNORECASE)
  check_pattern(report, debugger, "fw-debugger.md", hipoteses, "debugger-limite-hipoteses", False)

  reviewer = read(os.path.join(agents_dir, "fw-reviewer.md"))
  gatilho_tamanho = re.compile(r"ap[óo]s\s+implementa[çc][õo]es\s+significativas", re.IGNORECASE)
  check_pattern(report, reviewer, "fw-reviewer.md", gatilho_tamanho, "reviewer-gatilho-por-tamanho", True)
  criterio_risco = re.compile(r"risco", re.IGNORECASE)
  check_pattern(report, reviewer, "fw-reviewer.md", criterio_risco, "reviewer-criterio-risco", False)


def check_execution_budget(report, manifest_path):
  text = read(manifest_path)
  if text is None:
    report.add(WARN, "execution-budget", "%s nao encontrado" % manifest_path)
    return
  try:
    data = json.loads(text)
  except ValueError:
    report.add(ERROR, "manifest-json", "%s nao e JSON valido" % manifest_path)
    return
  if "executionBudget" in data:
    report.add(OK, "execution-budget", "presente em %s" % manifest_path)
  else:
    report.add(ERROR, "execution-budget", "%s sem campo executionBudget" % manifest_path)


def check_exists(report, path, nome, isdir):
  ok = os.path.isdir(path) if isdir else os.path.isfile(path)
  if ok:
    report.add(OK, nome, "%s encontrado" % path)
  else:
    report.add(ERROR, nome, "%s nao encontrado" % path)


def check_model_policy(report, paths):
  categorias = re.compile(r"economical|balanced|deep-reasoning", re.IGNORECASE)
  for path in paths:
    text = read(path)
    if text and categorias.search(text):
      report.add(OK, "model-policy", "categorias de modelo referenciadas em %s" % path)
      return
  report.add(WARN, "model-policy", "nenhuma categoria de modelo encontrada (economical/balanced/deep-reasoning)")


def audit_framework(report, root):
  claude = check_teto(report, os.path.join(root, "CLAUDE.md.ccf"), 40, "always-on-teto")
  check_pattern(report, claude, "CLAUDE.md.ccf", THREE_FILE_RULE, "always-on-regra-3-arquivos", True)
  router = re.compile(r"\bt0\b|\bt1\b|\bt2\b|\bt3\b|menor conjunto suficiente", re.IGNORECASE)
  check_pattern(report, claude, "CLAUDE.md.ccf", router, "always-on-task-router", False)
  check_teto(report, os.path.join(root, "templates", "index.md"), 120, "index-template-teto")
  check_agents(report, os.path.join(root, "agents"))
  check_exists(report, os.path.join(root, "templates", "workspace.md"), "workspace-template", False)
  check_model_policy(report, [
      os.path.join(root, "templates", "policies.md"),
      os.path.join(root, ".claude-plugin", "plugin.json"),
  ])


def audit_project(report, root):
  ctx = os.path.join(root, ".claude", "context")
  check_teto(report, os.path.join(ctx, "index.md"), 120, "index-teto")
  check_teto(report, os.path.join(ctx, "memory.md"), 150, "memory-teto")
  check_execution_budget(report, os.path.join(ctx, "manifest.json"))
  check_exists(report, os.path.join(ctx, "workspace"), "workspace-dir", True)


def main():
  root = sys.argv[1] if len(sys.argv) > 1 else "."
  report = Report()
  if os.path.isfile(os.path.join(root, "CLAUDE.md.ccf")):
    audit_framework(report, root)
  if os.path.isdir(os.path.join(root, ".claude", "context")):
    audit_project(report, root)
  print(report.render())
  sys.exit(1 if report.has_errors() else 0)


if __name__ == "__main__":
  main()
