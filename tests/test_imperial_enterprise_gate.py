"""Adversarial tests for the cross-repository enterprise quality gate."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from imperial_enterprise_gate import scan, strict_json, check_workflow, changed_files, tracked_files


class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def put(self, relative, data):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data if isinstance(data, bytes) else data.encode())
        return relative

    def errors(self, *paths):
        return scan(self.root, set(paths))[0]

    def test_safe_python_and_json(self):
        p = self.put("src/module.py", "x = 2\n")
        q = self.put("data/config.json", '{"ok":true}')
        self.assertEqual(self.errors(p, q), [])

    def test_python_syntax_must_fail(self):
        p = self.put("src/invalid.py", "def oops(:\n")
        self.assertIn("PYTHON_SYNTAX_INVALID", repr(self.errors(p)))

    def test_duplicate_keys_fail_even_nested(self):
        p = self.put("data/data.json", '{"approval":{"expires":1,"expires":2}}')
        self.assertIn("JSON_INVALID", repr(self.errors(p)))

    def test_nonfinite_json_fails(self):
        p = self.put("data/invalid.json", '{"risk":NaN}')
        self.assertIn("JSON_INVALID", repr(self.errors(p)))

    def test_jsonl_each_line_validated(self):
        p = self.put("data/invalid.jsonl", '{"ok":1}\n{"ok":Infinity}\n')
        self.assertIn("JSON_INVALID", repr(self.errors(p)))

    def test_embedded_private_key_fails(self):
        marker = "-----BEGIN " + "PRIVATE KEY-----"
        p = self.put("README.md", marker + "\nFAKE\n-----END " + "PRIVATE KEY-----")
        self.assertIn("PRIVATE_KEY_MATERIAL", repr(self.errors(p)))

    def test_secret_file_name_fails(self):
        p = self.put(".env.production", "SAFE=0\n")
        self.assertIn("POTENTIAL_SECRET_FILENAME", repr(self.errors(p)))

    def test_template_secret_filename_allowed(self):
        p = self.put(".env.example", "IMPERIAL_SAMPLE=REPLACE_ME\n")
        self.assertEqual(self.errors(p), [])

    def test_unpinned_action_fails(self):
        p = self.put(
            ".github/workflows/test.yml",
            "name: Test\non: push\npermissions:\n  contents: read\njobs:\n  x:\n    steps:\n      - uses: actions/checkout@v4\n",
        )
        self.assertIn("UNPINNED_GITHUB_ACTION", repr(self.errors(p)))

    def test_pinned_workflow_passes(self):
        p = self.put(
            ".github/workflows/test.yml",
            "permissions:\n  contents: read\nsteps:\n  - uses: actions/checkout@" + "a" * 40 + "\n",
        )
        self.assertEqual(self.errors(p), [])

    def test_missing_workflow_permissions_fails(self):
        p = self.put(".github/workflows/unsafe.yml", "name: test\non: push\n")
        self.assertIn("WORKFLOW_MISSING_EXPLICIT_PERMISSIONS", repr(self.errors(p)))

    def test_invalid_js_fails(self):
        p = self.put("src/broken.mjs", "export function ( {")
        self.assertIn("JAVASCRIPT_SYNTAX_INVALID", repr(self.errors(p)))

    def test_symlink_outside_repo_fails(self):
        link = self.root / "leak.py"
        link.symlink_to(self.root / "missing")
        self.assertIn("MISSING_OR_SYMLINK", repr(self.errors("leak.py")))

    def test_diff_only_new_changed_files(self):
        def git(*args):
            return subprocess.run(
                ["git", "-C", str(self.root), *args], capture_output=True,
                text=True, check=True
            ).stdout.strip()
        git("init")
        git("config", "user.name", "IMPERIAL Test")
        git("config", "user.email", "test@example.invalid")
        self.put("src/old.py", "n = 1\n")
        git("add", ".")
        git("commit", "-m", "base")
        base = git("rev-parse", "HEAD")
        self.put("src/new.py", "n = 2\n")
        git("add", ".")
        git("commit", "-m", "head")
        head = git("rev-parse", "HEAD")
        self.assertEqual(
            changed_files(self.root, base, head, tracked_files(self.root)),
            {"src/new.py"},
        )


if __name__ == "__main__":
    unittest.main()
