"""Offline tests for read-only, fail-closed IP inventory classification."""
import importlib.util
import pathlib
import json
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "imperial_license_audit", pathlib.Path(__file__).with_name("imperial_license_audit.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

RECORD = ("Founder: Alexander Nikolaevich Romaskevich (RomaskevicH).\n"
          "Git history and contributors are preserved and licenses are independently reviewed.")


def repo(name="IMPERIAL", fork=False):
    return {"name": name, "html_url": "https://github.com/oromaskevic23-cmd/" + name,
            "private": False, "fork": fork}


def files(*names):
    return [{"name": n, "type": "file"} for n in names]


class GuardTests(unittest.TestCase):
    def test_founder_present_unlicensed_is_not_approved(self):
        result = audit.audit_public_repo(repo(), files("AUTHORS.md", "README.md"), RECORD)
        self.assertEqual(result["license_status"], "NO_ROOT_LICENSE_GRANT")
        self.assertEqual(result["founder_record"], "FOUNDER_DECLARED_CONTRIBUTIONS_PRESERVED")
        self.assertFalse(result["release_authorized"])

    def test_license_present_does_not_certify_rights(self):
        result = audit.audit_public_repo(repo(), files("LICENSE", "AUTHORS.md"), RECORD)
        self.assertEqual(result["license_status"], "ROOT_LICENSE_PRESENT_THIRD_PARTY_RIGHTS_UNVERIFIED")
        self.assertFalse(result["release_authorized"])

    def test_notice_is_not_a_license(self):
        result = audit.audit_public_repo(repo(), files("NOTICE.md", "LICENSE_INVENTORY.md", "AUTHORS.md"), RECORD)
        self.assertEqual(result["license_files"], [])

    def test_missing_author_fail_closed(self):
        result = audit.audit_public_repo(repo(), files("README.md"), None)
        self.assertEqual(result["founder_record"], "MISSING")

    def test_incomplete_author_fail_closed(self):
        result = audit.audit_public_repo(repo(), files("AUTHORS.md"), "Invented founder")
        self.assertEqual(result["founder_record"], "INCOMPLETE")

    def test_forks_preserve_upstream_authority(self):
        result = audit.audit_public_repo(repo(fork=True), files("AUTHORS.md", "LICENSE"), RECORD)
        self.assertEqual(result["license_status"], "UPSTREAM_LICENSES_REQUIRE_REVIEW")
        self.assertFalse(result["release_authorized"])

    def test_noassertion_summary_even_when_license_present(self):
        result = audit.audit_public_repo(repo(), files("LICENSE", "AUTHORS.md"), RECORD)
        summary = audit.summarize([result])
        self.assertEqual(summary["releases_authorized"], 0)
        self.assertFalse(summary["complete_copyright_clearance"])
        self.assertFalse(summary["private_repositories_included"])

    def test_cli_founder_regression_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = pathlib.Path(folder)
            fixture = folder / "data.json"
            report = folder / "result.json"
            fixture.write_text(json.dumps([
                {"repo": repo("OK"), "contents": files("README.md", "AUTHORS.md"),
                 "author_record": RECORD},
                {"repo": repo("BROKEN"), "contents": files("README.md")}
            ]), encoding="utf-8")
            process = subprocess.run([
                sys.executable, str(pathlib.Path(__file__).with_name("imperial_license_audit.py")),
                "--offline-fixture", str(fixture), "--out", str(report)
            ], capture_output=True, text=True)
            self.assertEqual(process.returncode, 2)
            self.assertIn("FOUNDER_PROVENANCE_GUARD_FAILED_CLOSED", process.stderr)
            self.assertTrue(report.is_file())
            self.assertEqual(json.loads(report.read_text())["summary"]["founder_records_verified"], 1)

    def test_cli_clean_founder_inventory_passes_without_license_grant(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = pathlib.Path(folder)
            fixture = folder / "data.json"
            report = folder / "result.json"
            fixture.write_text(json.dumps([
                {"repo": repo("OK"), "contents": files("README.md", "AUTHORS.md"),
                 "author_record": RECORD}
            ]), encoding="utf-8")
            process = subprocess.run([
                sys.executable, str(pathlib.Path(__file__).with_name("imperial_license_audit.py")),
                "--offline-fixture", str(fixture), "--out", str(report)
            ], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0)
            self.assertIn("NOT_A_LICENSE_GRANT_OR_A_LEGAL_CERTIFICATION", process.stdout)
            self.assertEqual(json.loads(report.read_text())["summary"]["releases_authorized"], 0)

    def test_scope_rejects_wrong_owner(self):
        with self.assertRaises(ValueError):
            audit.collect_public("another-owner")

    def test_unsafe_api_paths_blocked_before_network(self):
        for path in ("https://evil.example/", "/repos/../secrets", "/repos//test"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                audit.api_json(path)


if __name__ == "__main__":
    unittest.main()
