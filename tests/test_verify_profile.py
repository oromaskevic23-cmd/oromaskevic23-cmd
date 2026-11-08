"""Meaningful regression checks for founder profile integrity boundaries."""
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
import unittest

from tools.verify_profile import ASSET_BLOBS, EMBLEM, ROOT, verify_profile


class ProfileIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = (ROOT / "README.md").read_text(encoding="utf-8")

    def assert_fails(self, text, name, root=ROOT):
        self.assertFalse(dict(verify_profile(text, root))[name])

    def test_current_profile_passes(self):
        self.assertTrue(all(ok for _, ok in verify_profile(self.profile)))

    def test_missing_founder_authority_is_rejected(self):
        changed = self.profile.replace("retain final architectural decision authority", "guide the project")
        self.assert_fails(changed, "Founder identity, roles and authority")

    def test_deprecated_executive_title_is_rejected(self):
        old_title = "Chief" + " Systems" + " Architect"
        self.assert_fails(self.profile + "\n" + old_title, "Deprecated executive title removed")

    def test_missing_product_evidence_boundary_is_rejected(self):
        changed = self.profile.replace("do not establish a production service or external certification", "prove full production readiness")
        self.assert_fails(changed, "Limits of product and CI evidence")

    def test_missing_architecture_boundary_is_rejected(self):
        changed = self.profile.replace("Federated Multi-Orchestrator Architecture", "single global controller")
        self.assert_fails(changed, "Federated governance and public/private boundary")

    def test_unapproved_link_is_rejected(self):
        changed = self.profile.replace("https://github.com/oromaskevic23-cmd/CONSTRUCTOR-AI)", "https://example.invalid/CONSTRUCTOR-AI)", 1)
        self.assert_fails(changed, "Useful links stay within approved destinations")

    def test_missing_recorded_ci_is_rejected(self):
        changed = self.profile.replace("actions/runs/42001525556", "actions/runs/not-a-recorded-run")
        self.assert_fails(changed, "Reproducible flagship commands and commit-bound CI evidence")

    def test_substituted_corporate_emblem_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for asset in ASSET_BLOBS:
                target = root / asset
                target.parent.mkdir(parents=True, exist_ok=True)
                copyfile(ROOT / asset, target)
            (root / EMBLEM).write_bytes(b"substituted emblem")
            self.assert_fails(self.profile, "Approved image asset fingerprints", root)

    def test_hanter_banner_must_remain_between_token_images(self):
        changed = self.profile.replace('src="assets/hanter-banner-original-20261029.jpg"',
                                       'src="assets/unapproved-banner.jpg"')
        self.assert_fails(changed, "Owner-selected IMPERIUM / HANTER / NDB arrangement")

    def test_credential_like_token_is_rejected(self):
        token = "ghp_" + "A" * 36
        self.assert_fails(self.profile + "\n" + token, "No common credential token patterns")


if __name__ == "__main__":
    unittest.main()
