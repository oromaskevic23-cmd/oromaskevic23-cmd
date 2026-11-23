"""Negative tests for the public profile's critical disclosure boundaries."""
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
import unittest

from tools.verify_profile import ASSET_BLOBS, EMBLEM, ROOT, allowed_public_link, verify_profile, verify_public_reference_links


class ProfileIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = (ROOT / "README.md").read_text(encoding="utf-8")

    def rejected(self, changed, name, root=ROOT):
        self.assertFalse(dict(verify_profile(changed, root))[name])

    def test_current_profile_passes(self):
        self.assertTrue(all(ok for _, ok in verify_profile(self.profile)))
        self.assertTrue(all(ok for _, ok in verify_public_reference_links()))

    def test_founder_remains_the_primary_heading(self):
        changed = self.profile.replace(">Alexander Romaskevich</h1>", ">IMPERIAL Core</h1>")
        self.rejected(changed, "Profile opens with the founder")

    def test_architecture_and_passport_boundaries(self):
        self.rejected(self.profile.replace("Federated Multi-Orchestrator Architecture", "single controller"),
                      "Federated architecture and control boundaries")
        self.rejected(self.profile.replace("Identity alone never grants permission", "Identity grants permission"),
                      "Passport illustration cannot imply authorization")

    def test_synthetic_demo_and_model_failure_are_disclosed(self):
        self.rejected(self.profile.replace("fixed synthetic examples", "live examples"),
                      "Dubai walkthrough and status are bounded")
        self.rejected(self.profile.replace("browser verifier failed", "browser verifier succeeded"),
                      "Evidence, model failure and limitations disclosed")

    def test_swapped_symbol_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for path in ASSET_BLOBS:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                copyfile(ROOT / path, target)
            (root / EMBLEM).write_bytes(b"unapproved substitution")
            self.rejected(self.profile, "Owner-selected image fingerprints", root)

    def test_bad_links_and_credentials_are_rejected(self):
        self.assertFalse(allowed_public_link("https://github.com.evil.example/oromaskevic23-cmd/project"))
        self.assertFalse(allowed_public_link("docs/%2e%2e/private"))
        self.rejected(self.profile + "\n" + "ghp_" + "A" * 36,
                      "No common credential token patterns")


if __name__ == "__main__":
    unittest.main()
