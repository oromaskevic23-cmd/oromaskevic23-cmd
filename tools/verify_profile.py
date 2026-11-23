#!/usr/bin/env python3
"""Check the public profile's image, architecture and evidence boundaries offline."""
from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
EMBLEM = "assets/imperial-core-diamond-20261116.jpg"
PROFILE_IMAGES = (
    "assets/imperial-core-dubai-luxury-profile-20261123.jpg",
    "assets/alexander-romaskevich-portrait-20261110.jpg",
    "assets/hanter-banner-diamond-20261116.jpg",
    "assets/ai-passport-concept-20261116.jpg",
    "assets/dubai-social-preview-20261123.jpg",
)
ASSET_BLOBS = {
    PROFILE_IMAGES[0]: "2b748cc61a9466e1910d633f020a623135b84495",
    PROFILE_IMAGES[-1]: "ea178022266c95b6d4ffe30a2a92178855eee871",
    "assets/imperial-core-banner-diamond-20261116.jpg": "83c8ec16411e5d3037b6a942f0df1c3456fc7116",
    EMBLEM: "85113c4fdd90c6c0fbe971ee14a5a6c30bb9d7aa",
    "assets/alexander-romaskevich-portrait-20261110.jpg": "9f9267646a4b7b12eec88714e60a452ac227dde9",
    "assets/hanter-banner-diamond-20261116.jpg": "cad43e21f050cd027e51e93500ddbbc94dfe3755",
    "assets/ai-passport-concept-20261116.jpg": "271a98128c51d83333b27d77ac9763245d5afad1",
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def approved_assets(root: Path) -> bool:
    try:
        return all((root / p).is_file() and not (root / p).is_symlink()
                   and git_blob_sha1((root / p).read_bytes()) == h
                   for p, h in ASSET_BLOBS.items())
    except OSError:
        return False


def allowed_public_link(link: str) -> bool:
    if link == "mailto:oromaskevic23@gmail.com":
        return True
    p = urlparse(link)
    if p.username or p.password or p.query or any(ord(c) < 32 for c in link):
        return False
    if p.scheme:
        return (p.scheme == "https" and (
            (p.netloc == "github.com" and p.path.startswith("/oromaskevic23-cmd/"))
            or p.netloc == "oromaskevic23-cmd.github.io"))
    if p.netloc or p.path.startswith("/") or "\\" in unquote(p.path):
        return False
    return all(part not in {"..", "."} for part in unquote(p.path).split("/"))


def verify_profile(text: str, root: Path = ROOT) -> list[tuple[str, bool]]:
    checks = []
    def check(name: str, condition: bool) -> None:
        checks.append((name, bool(condition)))

    images = re.findall(r'<img\s+src="([^"]+)"', text)
    check("Owner-selected assets and order", tuple(images[:len(PROFILE_IMAGES)]) == PROFILE_IMAGES)
    check("Owner-selected image fingerprints", approved_assets(root))
    check("Image descriptions present", all(re.search(r'<img\b[^>]*\balt="[^"]+"', tag)
                                              for tag in re.findall(r'<img\b[^>]*>', text)))
    check("Founder and authority", all(v in text for v in (
        "Alexander Romaskevich", "Founder · Owner · CEO", "RomaskevicH")))
    check("Federated architecture and control boundaries", all(v in text for v in (
        "Federated Multi-Orchestrator Architecture", "AI Passport", "Enterprise Skills",
        "Guardian Core", "Approval Gateway", "Audit Ledger", "Zero Trust",
        "Public/Private Boundary", "CRYPTO IMPERIAL Ecosystem Boundary")))
    check("Evidence, model failure and limitations disclosed", all(v in text for v in (
        "42001525579", "42001525556", "browser verifier failed",
        "not independent certification", "Customer revenue")))
    check("Dubai walkthrough and status are bounded", all(v in text for v in (
        "IMPERIAL-DUBAI-2027-Public", "fixed synthetic examples", "not a live agent",
        "independent review and measured customer value remain open")))
    check("Passport illustration cannot imply authorization", all(v in text for v in (
        "Identity alone never grants permission", "score, QR code and status are illustrative",
        "docs/AI_PASSPORT_CONCEPT.md")))
    check("Crypto is a long-term vision", "long-term architectural digital currency envisioned for AI agents worldwide" in text
          and "no claim of current global adoption" in text)
    check("Image QR and old labels are not operational claims", "labels and QR code do not establish operating status" in text)
    check("Third-party rights and license boundary", "Third-party components retain" in text
          and "Public visibility does not by itself grant a software license" in text)
    links = re.findall(r"\]\(([^)\s]+)\)", text) + re.findall(r'href="([^"]+)"', text)
    check("Public links stay within approved destinations", len(links) >= 15 and all(allowed_public_link(x) for x in links))
    patterns = (r"ghp_[A-Za-z0-9]{36}", r"github_pat_[A-Za-z0-9_]{20,}",
                r"-----BEGIN (?:OPENSSH|RSA|EC|PRIVATE) KEY-----", r"sk-[A-Za-z0-9_-]{20,}")
    check("No common credential token patterns", not any(re.search(p, text) for p in patterns))
    return checks


def verify_public_reference_links(root: Path = ROOT) -> list[tuple[str, bool]]:
    profile = (root / "README.md").read_text(encoding="utf-8")
    notice = (root / "NOTICE.md").read_text(encoding="utf-8")
    paths = ("docs/ENGINEERING_DUE_DILIGENCE_20261109.md", "docs/CONSTRUCTOR_AI_INVESTOR_OVERVIEW.md",
             "docs/FOUNDER_PUBLIC_PROJECT_REGISTRY_20261031.md", "docs/AI_PASSPORT_CONCEPT.md", "brand/README.md")
    return [
        ("Public reference documents are present", all((root / p).is_file() for p in paths)),
        ("Profile links to the public passport concept", "docs/AI_PASSPORT_CONCEPT.md" in profile),
        ("Founder notice points to canonical tracked symbol policy", "oromaskevic23-cmd/blob/main/brand/README.md" in notice),
    ]


def main() -> int:
    checks = verify_profile((ROOT / "README.md").read_text(encoding="utf-8")) + verify_public_reference_links()
    for name, ok in checks:
        print(("PASS" if ok else "FAIL") + ": " + name)
    print(f"Profile integrity: {sum(ok for _, ok in checks)}/{len(checks)} PASS")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
