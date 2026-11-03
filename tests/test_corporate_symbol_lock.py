"""Negative tests for the one corporate emblem rule."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.check_corporate_symbol import (
    CANONICAL_FILE, CANONICAL_GIT_BLOB_SHA1, POLICY_ID,
    BrandIntegrityError, git_blob_hash, verify_brand_lock
)


class CorporateSymbolLockTests(unittest.TestCase):
    def test_original_emblem_is_pinned(self):
        proof=verify_brand_lock()
        self.assertTrue(proof["canonical_emblem_verified"])
        self.assertEqual(proof["git_blob_sha1_verified"],CANONICAL_GIT_BLOB_SHA1)
        self.assertFalse(proof["cross_repository_enforcement_verified"])

    def make_fixture(self):
        t=TemporaryDirectory()
        self.addCleanup(t.cleanup)
        root=Path(t.name)
        (root/"brand").mkdir()
        (root/"assets").mkdir()
        actual=Path(CANONICAL_FILE).read_bytes()
        (root/CANONICAL_FILE).write_bytes(actual)
        m=json.loads(Path("brand/corporate-symbol-lock.json").read_text())
        (root/"brand"/"corporate-symbol-lock.json").write_text(json.dumps(m))
        return root,m

    def test_rejects_another_symbol(self):
        root,m=self.make_fixture()
        (root/CANONICAL_FILE).write_bytes(b"RIFF....WEBP" + b"changed")
        with self.assertRaisesRegex(BrandIntegrityError,"CORPORATE_EMBLEM_BYTES_CHANGED"):
            verify_brand_lock(root=root)

    def test_rejects_substituted_asset_path(self):
        root,m=self.make_fixture()
        m["approved_symbol"]["path"]="assets/random-generated-eye-logo.webp"
        (root/"brand"/"corporate-symbol-lock.json").write_text(json.dumps(m))
        with self.assertRaisesRegex(BrandIntegrityError,"UNAPPROVED_CORPORATE_EMBLEM"):
            verify_brand_lock(root=root)

    def test_rejects_logo_randomization_rule(self):
        root,m=self.make_fixture()
        m["allowed_variation"]["official_corporate_symbol"]=True
        (root/"brand"/"corporate-symbol-lock.json").write_text(json.dumps(m))
        with self.assertRaisesRegex(BrandIntegrityError,"CORPORATE_SYMBOL_VARIATION_FORBIDDEN"):
            verify_brand_lock(root=root)

    def test_rejects_missing_symbol(self):
        root,m=self.make_fixture()
        (root/CANONICAL_FILE).unlink()
        with self.assertRaisesRegex(BrandIntegrityError,"MISSING_OR_LINKED"):
            verify_brand_lock(root=root)

    def test_asset_has_webp_magic(self):
        raw=Path(CANONICAL_FILE).read_bytes()
        self.assertEqual(raw[:4],b"RIFF")
        self.assertEqual(raw[8:12],b"WEBP")
        self.assertEqual(len(CANONICAL_GIT_BLOB_SHA1),40)

    def test_agent_avatar_can_change_without_brand_change(self):
        brand=json.loads(Path("brand/corporate-symbol-lock.json").read_text())
        variations=brand["allowed_variation"]
        self.assertTrue(variations["nca_avatar_subject"])
        self.assertTrue(variations["nca_agent_name"])
        self.assertTrue(variations["location_and_background"])
        self.assertFalse(variations["official_corporate_symbol"])


if __name__=="__main__":
    unittest.main()
