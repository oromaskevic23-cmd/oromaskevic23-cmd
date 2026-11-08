#!/usr/bin/env python3
"""Offline integrity checks for the public IMPERIAL Core founder profile.

These checks guard selected presentation and evidence boundaries. They do not
validate live URLs, prove claims in linked material or certify a product.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
OWNER = "oromaskevic23-cmd"
CONTACT = "mailto:oromaskevic23@gmail.com"
PHOTO_SKYLINE = "assets/imperial-core-skyline-original-20261029.jpg"
EMBLEM = "assets/imperial-core-emblem.webp"
PHOTO_FOUNDER = "assets/alexander-romaskevich-portrait-original-20261029.jpg"
HANTER_BANNER = "assets/hanter-banner-original-20261029.jpg"
IMPERIUM_IMAGE = "https://raw.githubusercontent.com/oromaskevic23-cmd/IMPERIUM/main/assets/imperium-hero-20261029.jpg"
NDB_IMAGE = "https://raw.githubusercontent.com/oromaskevic23-cmd/N.D.B/main/assets/ndb-hero-20261029.jpg"
IMAGES = (PHOTO_SKYLINE, EMBLEM, PHOTO_FOUNDER, IMPERIUM_IMAGE, HANTER_BANNER, NDB_IMAGE)
ASSET_BLOBS = {
    PHOTO_SKYLINE: "3c3da53b749b0f58eaf3e88fa16e66c30daeb8cc",
    EMBLEM: "7749da03da49d4434fc826d0f26793785a3cab42",
    PHOTO_FOUNDER: "9f9267646a4b7b12eec88714e60a452ac227dde9",
    HANTER_BANNER: "64dda3398ac3b54da5a24252502d1ac85a6f5b34",
}
OWNER_SELECTED_STACK = '''<p align="center">
  <a href="https://github.com/oromaskevic23-cmd/IMPERIUM"><img src="https://raw.githubusercontent.com/oromaskevic23-cmd/IMPERIUM/main/assets/imperium-hero-20261029.jpg" alt="IMPERIUM digital emblem" width="190" /></a>
</p>

<p align="center">
  <a href="https://github.com/oromaskevic23-cmd/HANTER-Public"><img src="assets/hanter-banner-original-20261029.jpg" alt="HANTER — Nano Core Agents and IMPERIAL Core" width="100%" /></a>
</p>

<p align="center">
  <a href="https://github.com/oromaskevic23-cmd/N.D.B"><img src="https://raw.githubusercontent.com/oromaskevic23-cmd/N.D.B/main/assets/ndb-hero-20261029.jpg" alt="NDB digital emblem" width="190" /></a>
</p>'''
OFFICIAL_PAGES = {
    "https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/",
    "https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/engineering/",
    "https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/",
    "https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/constructor-ai/studio/studio.html",
}
EXPECTED_SECTIONS = (
    "Investment and pilot partnerships", "Featured product — CONSTRUCTOR AI",
    "Public engineering portfolio", "Architecture and governance",
    "CRYPTO IMPERIAL Ecosystem", "Engineering roadmap",
    "Collaboration and authorship",
)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def approved_assets(root: Path) -> bool:
    try:
        return all(
            (root / path).is_file() and not (root / path).is_symlink()
            and git_blob_sha1((root / path).read_bytes()) == digest
            for path, digest in ASSET_BLOBS.items()
        )
    except OSError:
        return False


def allowed_public_link(link: str) -> bool:
    if link == CONTACT or link in OFFICIAL_PAGES or link in (IMPERIUM_IMAGE, NDB_IMAGE):
        return True
    if link.startswith("#"):
        return bool(re.fullmatch(r"#[a-z0-9-]{1,80}", link))
    parsed = urlparse(link)
    if (parsed.scheme != "https" or parsed.netloc != "github.com"
            or parsed.username or parsed.password or parsed.query):
        return False
    if parsed.fragment and not re.fullmatch(r"[a-z0-9-]{1,80}", parsed.fragment):
        return False
    decoded = unquote(parsed.path)
    parts = decoded.split("/")
    return (len(parts) >= 2 and parts[1] == OWNER
            and all(part not in ("", ".", "..") for part in parts[2:])
            and chr(92) not in decoded)


def verify_profile(text: str, root: Path = ROOT) -> list[tuple[str, bool]]:
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, bool(condition)))

    image_paths = re.findall(r'<img\s+src="([^"]+)"', text)
    positions = [text.find('src="' + path + '"') for path in IMAGES]
    check("Approved image selection and order", image_paths == list(IMAGES))
    check("Approved image asset fingerprints", approved_assets(root))
    check("Owner-selected IMPERIUM / HANTER / NDB arrangement", OWNER_SELECTED_STACK in text)
    check("Skyline, company text, founder portrait and statement order",
          positions[0] >= 0 and positions[0] < text.find("### Our vision")
          < positions[2] < text.find("### Founder statement"))
    check("Canonical emblem has an accessible description",
          'alt="IMPERIAL Core official corporate emblem"' in text)
    sections = re.findall(r"^## ([^\r\n]+)$", text, flags=re.MULTILINE)
    check("Profile sections remain complete and ordered", sections == list(EXPECTED_SECTIONS))
    check("Founder identity, roles and authority",
          all(value in text for value in ("Alexander Nikolaevich Romaskevich", "RomaskevicH",
              "Founder · Owner · CEO", "retain final architectural decision authority")))
    check("Deprecated executive title removed", not re.search(r"chief\s+systems\s+architect", text, re.I))
    check("Personal privacy and ownership detail boundary",
          "Ukraine" not in text and not re.search(r"\b(?:shares|shareholder)\b", text, re.I))
    check("Investment route and current prototype scope",
          all(value in text for value in ("CONSTRUCTOR_AI_INVESTOR_OVERVIEW.md", CONTACT,
              "pre-seed investors", "local applications from predefined templates",
              "multi-user production hosting and customer acceptance remain development milestones")))
    check("Reproducible flagship commands and commit-bound CI evidence",
          all(value in text for value in ("898d1abe2616cb92104b64dc126e0875cc9acddf",
              "actions/runs/42001525579", "actions/runs/42001525556",
              "npm run verify", "node tools/verify-acceptance.mjs acceptance-output",
              "docs/FLAGSHIP_ACCEPTANCE.md")))
    check("Limits of product and CI evidence",
          all(value in text for value in ("project-controlled", "local, single-user",
              "do not establish a production service or external certification",
              "Human visual/accessibility review and full cross-browser acceptance remain separate")))
    check("Canonical public portfolio",
          all(value in text for value in ("IMPERIAL Core", "VELION", "HANTER", "CONSTRUCTOR AI",
              "Nano Core Agents", "LEGION", "ORION", "CYBER HAK", "Capital Core", "IMPERIUM", "NDB")))
    check("Federated governance and public/private boundary",
          all(value in text for value in ("Federated Multi-Orchestrator Architecture", "AI Passport",
              "Enterprise Skills", "Guardian Core", "Approval Gateway", "Audit Ledger",
              "Zero Trust", "Public / Private Boundary", "CRYPTO IMPERIAL Ecosystem Boundary",
              "target architecture")))
    check("IMPERIUM vision and crypto evidence boundary",
          "long-term architectural digital currency envisioned for AI agents worldwide" in text
          and "no current global adoption, liquidity, financial return or agent-payment service is claimed" in text)
    check("Third-party attribution and license boundary",
          "Third-party models, libraries and contributions retain their original attribution" in text
          and "public visibility alone does not grant a software license" in text)
    check("Business inquiry route", CONTACT in text
          and "https://github.com/oromaskevic23-cmd/Capital-Core-Public/issues" in text
          and "/issues/new" not in text)
    links = (re.findall(r"\]\(([^)\s]+)\)", text)
             + re.findall(r'href="([^"]+)"', text)
             + [path for path in image_paths if path.startswith("https://")])
    check("Useful links stay within approved destinations",
          len(links) >= 15 and all(allowed_public_link(link) for link in links))
    check("No obsolete Val Town URL or generic template filler",
          "imperialcore.val.run" not in text and "## Hi there 👋" not in text
          and "I'm currently learning" not in text)
    patterns = (r"ghp_[A-Za-z0-9]{36}", r"github_pat_[A-Za-z0-9_]{20,}",
                r"-----BEGIN (?:OPENSSH|RSA|EC|PRIVATE) KEY-----", r"sk-[A-Za-z0-9_-]{20,}")
    check("No common credential token patterns", not any(re.search(p, text) for p in patterns))
    return checks



def verify_public_reference_links(root: Path = ROOT) -> list[tuple[str, bool]]:
    """Check local document targets and canonical links without network access.

    This prevents regressions to obsolete Pages paths, but cannot validate
    the uptime or search indexing of an externally served website.
    """
    profile = (root / "README.md").read_text(encoding="utf-8")
    notice = (root / "NOTICE.md").read_text(encoding="utf-8")
    investor = (root / "docs/CONSTRUCTOR_AI_INVESTOR_OVERVIEW.md").read_text(encoding="utf-8")
    paths = (
        "docs/ENGINEERING_DUE_DILIGENCE_20261109.md",
        "docs/CONSTRUCTOR_AI_INVESTOR_OVERVIEW.md",
        "docs/FOUNDER_PUBLIC_PROJECT_REGISTRY_20261031.md",
        "brand/README.md",
    )
    base = f"https://github.com/{OWNER}/{OWNER}/blob/main/"
    return [
        ("Public reference documents are present",
         all((root / p).is_file() for p in paths)),
        ("Profile points to existing investor, due-diligence and registry files",
         all(base + p in profile for p in paths[:3])),
        ("Founder notice points to canonical tracked symbol policy",
         base + "brand/README.md" in notice),
        ("Founder notice rejects obsolete site and untracked brand links",
         "IMPERIAL-Core-Public/reference/" not in notice
         and "Capital-Core-Public/reference/brand/BRAND.md" not in notice),
        ("Investor overview links to the reproducible evidence brief",
         base + "docs/ENGINEERING_DUE_DILIGENCE_20261109.md" in investor),
    ]


def main() -> int:
    checks = (verify_profile((ROOT / "README.md").read_text(encoding="utf-8"))
              + verify_public_reference_links())
    for name, success in checks:
        print(("PASS" if success else "FAIL") + ": " + name)
    print(f"Profile integrity: {sum(ok for _, ok in checks)}/{len(checks)} PASS")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
