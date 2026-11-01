#!/usr/bin/env python3
"""IMPERIAL Core cross-repository, zero-dependency pre-release error gate.

Static protection for *new/changed tracked files* in the caller repository.
Does not grant agent authority, attest a deployment or replace product tests.
Exit 1 on a violation, with no signing keys, network or external side effects.
Copyright (c) 2026 Alexander Nikolaevich Romaskevich (RomaskevicH).
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

MAX_TEXT_BYTES = 2_000_000
SOURCE_SUFFIXES = frozenset({".py", ".js", ".mjs", ".cjs", ".json", ".jsonl", ".yml", ".yaml"})
PY_SUFFIXES = frozenset({".py"})
JS_SUFFIXES = frozenset({".js", ".mjs", ".cjs"})
SECRET_FILE = re.compile(
    r"(^|/)(\.env(\..+)?|id_rsa|id_ed25519|wallet\.key|"
    r"service-account\.json|credentials\.json|[^/]+\.(pem|p12|pfx|key))$",
    re.IGNORECASE,
)
SECRET_VALUE = [
    ("PRIVATE_KEY_MATERIAL", re.compile(rb"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("GITHUB_ACCESS_TOKEN", re.compile(rb"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("GITHUB_FINE_GRAINED_TOKEN", re.compile(rb"github_pat_[A-Za-z0-9_]{45,}")),
    ("OPENAI_API_KEY", re.compile(rb"sk-(?:proj-)?[A-Za-z0-9_-]{30,}")),
]
USES = re.compile(r"^\s*(?:-\s*)?uses:\s*['\"]?([^\s'\"#]+)", re.MULTILINE)
PINNED_SHA = re.compile(r"^[a-fA-F0-9]{40}$")
ZERO = "0" * 40


class GateError(Exception):
    pass


def git(root: Path, *args: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False,
        timeout=30,
    )
    if proc.returncode:
        raise GateError("GIT_COMMAND_FAILED: " + " ".join(args[:2]))
    return proc.stdout


def tracked_files(root: Path) -> set[str]:
    return {p.decode("utf-8") for p in git(root, "ls-files", "-z").split(b"\0") if p}


def changed_files(root: Path, base: str, head: str, tracked: set[str]) -> set[str]:
    if not base or base == ZERO:
        return tracked
    if not re.fullmatch(r"[0-9a-fA-F]{40}", base):
        raise GateError("INVALID_BASE_SHA")
    if not head or not re.fullmatch(r"[0-9a-fA-F]{40}", head):
        raise GateError("INVALID_HEAD_SHA")
    return {
        p.decode("utf-8")
        for p in git(root, "diff", "--name-only", "--diff-filter=ACMR", "-z", base, head).split(b"\0")
        if p and p.decode("utf-8") in tracked
    }


def strict_json(raw: bytes) -> None:
    def unique(pairs):
        result = {}
        for k, value in pairs:
            if k in result:
                raise ValueError("DUPLICATE_JSON_KEY")
            result[k] = value
        return result

    def no_nonfinite(_):
        raise ValueError("NONFINITE_JSON_NUMBER")

    json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=no_nonfinite)


def check_workflow(text: str, name: str) -> list[str]:
    findings = []
    if not re.search(r"^permissions:\s*(?:\n|$)", text, re.MULTILINE):
        findings.append("WORKFLOW_MISSING_EXPLICIT_PERMISSIONS")
    for ref in USES.findall(text):
        if ref.startswith("./"):
            continue
        if ref.startswith("docker://"):
            if "@sha256:" not in ref:
                findings.append("UNPINNED_DOCKER_ACTION")
            continue
        if "@" not in ref or not PINNED_SHA.fullmatch(ref.rsplit("@", 1)[1]):
            findings.append("UNPINNED_GITHUB_ACTION")
    return findings


def scan(root: Path, files: set[str]) -> tuple[list[str], dict]:
    findings: list[str] = []
    checks = {"changed": len(files), "python": 0, "javascript": 0,
              "json": 0, "workflow": 0, "secrets": 0}
    for rel in sorted(files):
        path = PurePosixPath(rel)
        if path.is_absolute() or ".." in path.parts:
            findings.append(f"{rel}: INVALID_TRACKED_PATH")
            continue
        on_disk = root / rel
        if not on_disk.exists() or on_disk.is_symlink() or not on_disk.is_file():
            findings.append(f"{rel}: MISSING_OR_SYMLINK")
            continue
        if SECRET_FILE.search(rel) and not rel.endswith((".example", ".sample", ".template")):
            findings.append(f"{rel}: POTENTIAL_SECRET_FILENAME")
        raw = on_disk.read_bytes()
        if len(raw) > MAX_TEXT_BYTES:
            if path.suffix in SOURCE_SUFFIXES:
                findings.append(f"{rel}: SOURCE_FILE_TOO_LARGE_TO_VALIDATE")
            continue
        checks["secrets"] += 1
        for label, regex in SECRET_VALUE:
            if regex.search(raw):
                findings.append(f"{rel}: {label}")
        suffix = path.suffix.lower()
        if suffix == ".py":
            checks["python"] += 1
            try:
                ast.parse(raw.decode("utf-8-sig"), filename=rel)
            except (UnicodeError, SyntaxError, ValueError) as exc:
                findings.append(f"{rel}: PYTHON_SYNTAX_INVALID ({type(exc).__name__})")
        if suffix in JS_SUFFIXES:
            checks["javascript"] += 1
            try:
                res = subprocess.run(
                    ["node", "--check", str(on_disk)], capture_output=True,
                    check=False, timeout=20,
                )
                if res.returncode:
                    findings.append(f"{rel}: JAVASCRIPT_SYNTAX_INVALID")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                findings.append(f"{rel}: JAVASCRIPT_CHECK_UNAVAILABLE")
        if suffix in {".json", ".jsonl"}:
            checks["json"] += 1
            try:
                if suffix == ".json":
                    strict_json(raw)
                else:
                    for line in raw.splitlines():
                        if line.strip():
                            strict_json(line)
            except (UnicodeError, ValueError, RecursionError) as exc:
                findings.append(f"{rel}: JSON_INVALID ({type(exc).__name__})")
        if len(path.parts) == 3 and path.parts[:2] == (".github", "workflows") and suffix in {".yml", ".yaml"}:
            checks["workflow"] += 1
            try:
                findings.extend(f"{rel}: {f}" for f in check_workflow(raw.decode("utf-8"), rel))
            except UnicodeError:
                findings.append(f"{rel}: WORKFLOW_UTF8_INVALID")
    return findings, checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--base", default=os.getenv("IMPERIAL_CI_BASE", ""))
    parser.add_argument("--head", default=os.getenv("IMPERIAL_CI_HEAD", ""))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        tracked = tracked_files(root)
        changed = changed_files(root, args.base, args.head, tracked)
        findings, counters = scan(root, changed)
    except (GateError, OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
        print(f"IMPERIAL_GATE_BLOCKED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print("IMPERIAL_ENTERPRISE_GATE_V1", json.dumps(counters, sort_keys=True))
    print(f"TRACKED_FILES={len(tracked)} CHANGED_SCANNED={len(changed)}")
    for finding in findings:
        print("BLOCK: " + finding, file=sys.stderr)
    print("VERDICT=" + ("FAIL" if findings else "PASS"))
    print("SCOPE=CHANGED_FILES_STATIC_ONLY; production and whole-repo certification NOT claimed")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
