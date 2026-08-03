#!/usr/bin/env python3
"""Audita o contexto do Farol.

Verifica regras obrigatorias do framework (bloco always-on enxuto,
task router T0-T3, ausencia da regra de delegacao por quantidade de
arquivos, execution budget, workspace temporario, criterio de parada
do Scout, limite de hipoteses do Debugger, gatilho de risco do
Reviewer, politica de modelos, telemetria opcional) e reporta
OK/AVISO/ERRO por checagem.

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


def check_model_policy(report, root):
    categorias = re.compile(r"economical|balanced|deep-reasoning", re.IGNORECASE)
    policies_path = os.path.join(root, "templates", "policies.md")
    text = read(policies_path)
    if text and categorias.search(text):
        report.add(OK, "model-policy-categorias", "categorias de modelo documentadas em %s" % policies_path)
    else:
        report.add(WARN, "model-policy-categorias", "nenhuma categoria de modelo (economical/balanced/deep-reasoning) encontrada em %s" % policies_path)

    init_path = os.path.join(root, "skills", "init", "SKILL.md")
    init_text = read(init_path)
    schema = re.compile(r"modelPolicy", re.IGNORECASE)
    if init_text and schema.search(init_text):
        report.add(OK, "model-policy-schema", "bloco modelPolicy presente no manifesto de %s" % init_path)
    else:
        report.add(ERROR, "model-policy-schema", "%s nao declara o bloco modelPolicy no manifesto" % init_path)

    status_path = os.path.join(root, "skills", "status", "SKILL.md")
    status_text = read(status_path)
    if status_text and schema.search(status_text):
        report.add(OK, "model-policy-status-check", "verificacao de politica de modelo presente em %s" % status_path)
    else:
        report.add(WARN, "model-policy-status-check", "%s nao verifica modelPolicy/model: (transparencia de custo)" % status_path)


def check_model_policy_project(report, manifest_path):
    text = read(manifest_path)
    if text is None:
        return
    try:
        data = json.loads(text)
    except ValueError:
        return
    if "modelPolicy" in data:
        report.add(OK, "model-policy-manifest", "presente em %s" % manifest_path)
    else:
        report.add(WARN, "model-policy-manifest", "%s sem campo modelPolicy (schema anterior ao Commit 6 - nao bloqueante)" % manifest_path)


def check_telemetry(report, root):
    policies_path = os.path.join(root, "templates", "policies.md")
    text = read(policies_path)
    campos = re.compile(r"telemetria", re.IGNORECASE)
    proibidos = re.compile(r"proibidos", re.IGNORECASE)
    if text and campos.search(text) and proibidos.search(text):
        report.add(OK, "telemetry-policy", "secao de telemetria com campos permitidos/proibidos em %s" % policies_path)
    else:
        report.add(WARN, "telemetry-policy", "nenhuma secao de telemetria (campos permitidos/proibidos) encontrada em %s" % policies_path)

    # Escritor e leitor: telemetria sem escritor e campo morto; sem leitor e
    # dado gravado e nunca lido (o defeito que a v2.2.0 corrigiu).
    writer = os.path.join(root, "hooks", "fw-telemetry.py")
    if os.path.isfile(writer):
        report.add(OK, "telemetry-writer", "%s encontrado" % writer)
    else:
        report.add(ERROR, "telemetry-writer", "%s nao encontrado (telemetria sem escritor deterministico)" % writer)
    reader = os.path.join(root, "scripts", "report_telemetry.py")
    if os.path.isfile(reader):
        report.add(OK, "telemetry-reader", "%s encontrado" % reader)
    else:
        report.add(ERROR, "telemetry-reader", "%s nao encontrado (dado gravado e nunca lido)" % reader)

    # A lista de campos permitidos da secao h precisa de implementacao
    # EXECUTAVEL. Ja se perdeu uma vez ao reescrever a checagem 17 do status:
    # a regra continuou no texto e ficou sem ninguem verificando.
    leitor_txt = read(reader)
    if leitor_txt and re.search(r"CAMPOS_PERMITIDOS", leitor_txt):
        report.add(OK, "telemetry-lista-executavel",
                   "lista de campos permitidos implementada em %s" % reader)
    else:
        report.add(ERROR, "telemetry-lista-executavel",
                   "%s nao implementa CAMPOS_PERMITIDOS: a regra da secao h ficaria so declarativa" % reader)

    # Guarda contra escrita dupla: com o hook como escritor unico, o always-on
    # NAO pode voltar a instruir o modelo a gravar a linha.
    claude = read(os.path.join(root, "CLAUDE.md.ccf"))
    escrita_modelo = re.compile(r"registre uma linha JSONL", re.IGNORECASE)
    if claude and escrita_modelo.search(claude):
        report.add(ERROR, "telemetry-escrita-dupla",
                   "CLAUDE.md.ccf instrui o modelo a gravar a linha: com o hook instalado isso duplica registro")
    else:
        report.add(OK, "telemetry-escrita-dupla", "always-on nao instrui escrita pelo modelo")

    init_path = os.path.join(root, "skills", "init", "SKILL.md")
    init_text = read(init_path)
    schema = re.compile(r"\"telemetry\"", re.IGNORECASE)
    if init_text and schema.search(init_text):
        report.add(OK, "telemetry-schema", "bloco telemetry presente no manifesto de %s" % init_path)
    else:
        report.add(ERROR, "telemetry-schema", "%s nao declara o bloco telemetry no manifesto" % init_path)

    status_path = os.path.join(root, "skills", "status", "SKILL.md")
    status_text = read(status_path)
    if status_text and re.search(r"telemetry", status_text, re.IGNORECASE):
        report.add(OK, "telemetry-status-check", "verificacao de telemetria presente em %s" % status_path)
    else:
        report.add(WARN, "telemetry-status-check", "%s nao verifica telemetry.enabled" % status_path)


def check_telemetry_project(report, manifest_path):
    text = read(manifest_path)
    if text is None:
        return
    try:
        data = json.loads(text)
    except ValueError:
        return
    if "telemetry" in data:
        telemetry = data["telemetry"] if isinstance(data["telemetry"], dict) else {}
        enabled = bool(telemetry.get("enabled"))
        report.add(OK, "telemetry-manifest", "presente em %s (enabled=%s)" % (manifest_path, enabled))
        if "schemaVersion" not in telemetry:
            report.add(WARN, "telemetry-schema-version",
                       "%s sem telemetry.schemaVersion (linhas nao serao comparaveis entre versoes)" % manifest_path)
        if enabled:
            projeto = os.path.dirname(os.path.dirname(os.path.dirname(manifest_path)))
            hook = os.path.join(projeto, ".claude", "hooks", "fw-telemetry.py")
            if not os.path.isfile(hook):
                report.add(WARN, "telemetry-hook-instalado",
                           "telemetry.enabled=true mas %s nao existe: campo ligado sem escritor nao gera registro" % hook)
            log_path = telemetry.get("path")
            if log_path and not os.path.isfile(log_path):
                report.add(WARN, "telemetry-log", "telemetry.enabled=true mas %s nao existe ainda" % log_path)
    else:
        report.add(WARN, "telemetry-manifest", "%s sem campo telemetry (schema anterior ao Commit 8 - nao bloqueante)" % manifest_path)


def audit_framework(report, root):
    claude = check_teto(report, os.path.join(root, "CLAUDE.md.ccf"), 80, "always-on-teto")
    check_pattern(report, claude, "CLAUDE.md.ccf", THREE_FILE_RULE, "always-on-regra-3-arquivos", True)
    router = re.compile(r"\bt0\b|\bt1\b|\bt2\b|\bt3\b|menor conjunto suficiente", re.IGNORECASE)
    check_pattern(report, claude, "CLAUDE.md.ccf", router, "always-on-task-router", False)

    check_teto(report, os.path.join(root, "templates", "index.md"), 120, "index-template-teto")
    check_agents(report, os.path.join(root, "agents"))
    check_exists(report, os.path.join(root, "templates", "workspace.md"), "workspace-template", False)
    check_model_policy(report, root)
    check_telemetry(report, root)


def audit_project(report, root):
    ctx = os.path.join(root, ".claude", "context")
    check_teto(report, os.path.join(ctx, "index.md"), 120, "index-teto")
    check_teto(report, os.path.join(ctx, "memory.md"), 150, "memory-teto")
    check_execution_budget(report, os.path.join(ctx, "manifest.json"))
    check_model_policy_project(report, os.path.join(ctx, "manifest.json"))
    check_telemetry_project(report, os.path.join(ctx, "manifest.json"))
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