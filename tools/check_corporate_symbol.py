"""IMPERIAL Core immutable corporate symbol integrity reference.

Pins the actual canonical GitHub asset by its Git blob object hash.
This check does not replace active protected-branch rulesets or Owner approval.
Python standard library only; FREE_ONLY.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "brand" / "corporate-symbol-lock.json"

CANONICAL_REPO = "oromaskevic23-cmd/oromaskevic23-cmd"
CANONICAL_FILE = "assets/imperial-core-emblem.webp"
CANONICAL_GIT_BLOB_SHA1 = "7749da03da49d4434fc826d0f26793785a3cab42"
POLICY_ID = "IMPERIAL-CORE-CORPORATE-SYMBOL-LOCK-001"


class BrandIntegrityError(ValueError):
    pass


def git_blob_hash(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise BrandIntegrityError("INVALID_EMBLEM_BYTES")
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def verify_brand_lock(*, root: Path = ROOT) -> dict:
    root = Path(root)
    path = root / "brand" / "corporate-symbol-lock.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if (type(manifest) is not dict or manifest.get("schema_version") != 1
            or manifest.get("policy_id") != POLICY_ID
            or manifest.get("status") != "CANONICAL_GITHUB_REFERENCE"):
        raise BrandIntegrityError("INVALID_BRAND_POLICY")
    symbol = manifest.get("approved_symbol")
    if (type(symbol) is not dict
            or symbol.get("repository") != CANONICAL_REPO
            or symbol.get("path") != CANONICAL_FILE
            or symbol.get("git_blob_sha1") != CANONICAL_GIT_BLOB_SHA1
            or symbol.get("role") != "corporate_primary_symbol"):
        raise BrandIntegrityError("UNAPPROVED_CORPORATE_EMBLEM")
    variation = manifest.get("allowed_variation")
    if (type(variation) is not dict or
            variation.get("official_corporate_symbol") is not False or
            variation.get("nca_agent_name") is not True or
            variation.get("location_and_background") is not True):
        raise BrandIntegrityError("CORPORATE_SYMBOL_VARIATION_FORBIDDEN")
    asset = root / CANONICAL_FILE
    if asset.is_symlink() or not asset.is_file():
        raise BrandIntegrityError("MISSING_OR_LINKED_CORPORATE_EMBLEM")
    content = asset.read_bytes()
    if not content.startswith(b"RIFF") or content[8:12] != b"WEBP":
        raise BrandIntegrityError("INVALID_CORPORATE_EMBLEM_FORMAT")
    actual = git_blob_hash(content)
    if actual != CANONICAL_GIT_BLOB_SHA1:
        raise BrandIntegrityError("CORPORATE_EMBLEM_BYTES_CHANGED")
    return {
        "policy": POLICY_ID,
        "asset": CANONICAL_FILE,
        "git_blob_sha1_verified": actual,
        "canonical_emblem_verified": True,
        "cross_repository_enforcement_verified": False,
        "github_branch_protection_verified": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(verify_brand_lock(), sort_keys=True, indent=2))
