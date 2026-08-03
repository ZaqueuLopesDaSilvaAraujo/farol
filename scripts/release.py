#!/usr/bin/env python3
"""release.py — empacotamento deterministico do Farol.

Uso: python3 scripts/release.py [saida.zip]
Multiplataforma (Windows/Linux/macOS): usa apenas stdlib, sem shell.
Falha (exit != 0) em qualquer inconsistencia. So arquivos entram no zip —
diretorio vazio nunca e empacotado (a licao da release 1.1.0).
"""
import filecmp, os, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules"}
REQUIRED = [
    "VERSION", "README.md", "INSTALL.md", "CHANGELOG.md", "UPGRADE.md",
    "LICENSE", "CLAUDE.md.ccf",
    ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
    "agents/fw-scout.md", "agents/fw-reviewer.md", "agents/fw-debugger.md",
    "skills/init/SKILL.md", "skills/contextualize/SKILL.md",
    "skills/update/SKILL.md", "skills/consolidate/SKILL.md",
    "skills/decision/SKILL.md", "skills/status/SKILL.md",
    "templates/index.md", "templates/policies.md", "hooks/fw-guard.sh",
    "assets/banner.png", "scripts/release.py", "tests/PROTOCOL.md",
    ".gitattributes",
]


def slurp(rel):
    """Leitura SEMPRE em utf-8. O default do open() e o encoding do locale —
    no Windows, cp1252 — e o conteudo do Farol e acentuado: sem isto o portao
    de release morre com UnicodeDecodeError na plataforma do proprio autor."""
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()

def validate_versions():
    """Achado nº 1 do quinto relato: versão espalhada com bump manual é bug
    de processo. Falha a release se qualquer fonte divergir do VERSION —
    em especial plugin.json/marketplace.json, os arquivos que o Claude Code
    LE para decidir updates (equivalente ao `claude plugin tag`)."""
    import json as _json, re as _re
    v = slurp("VERSION").strip()
    errs = []
    pj = _json.loads(slurp(".claude-plugin/plugin.json"))
    if pj.get("version") != v:
        errs.append(f"plugin.json version={pj.get('version')} != VERSION={v}")
    mp = _json.loads(slurp(".claude-plugin/marketplace.json"))
    for p in mp.get("plugins", []):
        if p.get("version") != v:
            errs.append(f"marketplace.json '{p.get('name')}' version={p.get('version')} != {v}")
    if f"ccf:managed-start v{v}" not in slurp("CLAUDE.md.ccf"):
        errs.append(f"CLAUDE.md.ccf: marcador ccf:managed-start != v{v}")
    if f"# Farol — v{v}" not in slurp("README.md"):
        errs.append(f"README.md: titulo != v{v}")
    if f"# Instalação — Farol v{v}" not in slurp("INSTALL.md"):
        errs.append(f"INSTALL.md: titulo != v{v}")
    init = slurp("skills/init/SKILL.md")
    if _re.search(r'"version":\s*"\d', init):
        errs.append("skills/init: versao literal no template do manifesto (deve referenciar plugin.json)")
    return errs


def collect():
    files = []
    for root, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for n in names:
            p = os.path.relpath(os.path.join(root, n), ROOT)
            files.append(p.replace(os.sep, "/"))
    return sorted(files)

def validate_names(files):
    errs = []
    for p in files:
        if any(c in p for c in "{}\\"):
            errs.append(f"caractere invalido no caminho: {p}")
        if len(p) > 200:
            errs.append(f"caminho longo demais ({len(p)}): {p}")
    for r in REQUIRED:
        if r not in files:
            errs.append(f"arquivo obrigatorio ausente: {r}")
    return errs

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows: console/pipe cp1252
    except Exception:
        pass
    version = slurp("VERSION").strip()
    out = sys.argv[1] if len(sys.argv) > 1 else f"farol-v{version}.zip"

    errs = validate_versions()
    if errs:
        print("FALHA na consistencia de versoes:")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    files = collect()
    errs = validate_names(files)
    if errs:
        print("FALHA na validacao pre-empacotamento:")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(os.path.join(ROOT, p), p)

    with tempfile.TemporaryDirectory() as d:
        with zipfile.ZipFile(out) as z:
            bad = [n for n in z.namelist() if any(c in n for c in "{}\\")]
            if bad:
                print("FALHA: caminhos invalidos dentro do zip:", bad)
                sys.exit(1)
            z.extractall(d)
        extracted = []
        for root, dirs, names in os.walk(d):
            for n in names:
                extracted.append(
                    os.path.relpath(os.path.join(root, n), d).replace(os.sep, "/"))
        extracted.sort()
        if extracted != files:
            print("FALHA: estrutura extraida diverge da origem")
            print("  faltando:", sorted(set(files) - set(extracted)))
            print("  sobrando:", sorted(set(extracted) - set(files)))
            sys.exit(1)
        for p in files:
            if not filecmp.cmp(os.path.join(ROOT, p), os.path.join(d, p), shallow=False):
                print("FALHA: conteudo divergente apos extracao:", p)
                sys.exit(1)

    print(f"OK: {out} — {len(files)} arquivos; nomes, extracao e conteudo validados")

if __name__ == "__main__":
    main()
