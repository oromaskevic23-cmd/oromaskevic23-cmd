#!/usr/bin/env python3
"""Reproducible, offline verification for the public IMPERIAL Core founder README."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import re
import sys

README = Path(__file__).resolve().parents[1] / "README.md"
EXPECTED_SECTIONS = (
    "Founder introduction",
    "IMPERIAL Core — ecosystem overview",
    "Flagship engineering projects",
    "Architecture & technology stack",
    "Zero Trust, AI Governance & Verified Engineering",
    "Public technical evidence",
    "Engineering roadmap",
    "Collaboration and business inquiries",
    "Authorship — RomaskevicH",
)
PROJECTS = ("IMPERIAL Core", "VELION", "HANTER", "CONSTRUCTOR AI",
            "LEGION", "CYBER HAK", "NDB & IMPERIUM")
CHECKS = []
def check(name, condition):
    CHECKS.append((name, bool(condition)))

text = README.read_text(encoding="utf-8")
sections = re.findall(r"^## ([^\r\n]+)$", text, flags=re.MULTILINE)
check("Founder title and identity", text.lstrip().startswith('<p align="center">')
      and '<h2 align="center">Alexander Romaskevich</h2>' in text
      and "RomaskevicH" in text and "Ukraine" not in text)
photo_paths = [
    "assets/imperial-core-skyline-original-20261029.jpg",
    "assets/alexander-romaskevich-portrait-original-20261029.jpg",
]
other_images = [
    "https://raw.githubusercontent.com/oromaskevic23-cmd/IMPERIUM/main/assets/imperium-hero-20261029.jpg",
    "assets/hanter-banner-original-20261029.jpg",
    "https://raw.githubusercontent.com/oromaskevic23-cmd/N.D.B/main/assets/ndb-hero-20261029.jpg",
]
positions = [text.find('src="' + path + '"') for path in photo_paths]
all_images = re.findall(r'<img\s+src="([^"]+)"', text)
check("Exactly two separate owner-provided presentation photos",
      all_images == photo_paths + other_images
      and all((README.parent / path).is_file()
              and (README.parent / path).stat().st_size >= 100_000
              and (README.parent / path).read_bytes()[:3] == bytes.fromhex("ffd8ff")
              for path in photo_paths)
      and (README.parent / other_images[1]).is_file()
      and (README.parent / other_images[1]).read_bytes()[:3] == bytes.fromhex("ffd8ff"))
check("Skyline -> corporate text -> founder photo -> founder statement",
      positions[0] >= 0
      and positions[0] < text.find("### Our vision") < positions[1]
      and positions[1] < text.find("### Founder statement"))
check("All approved ordered sections", sections == ["IMPERIUM & NDB · Explore the CRYPTO IMPERIAL Ecosystem", "Official multilingual websites", *EXPECTED_SECTIONS])
check("Public technology portfolio", all(name in text for name in PROJECTS))
check("Owner-approved public roles", "Founder • Owner • CEO of IMPERIAL Core" in text and "Chief Systems Architect" not in text and not re.search(r"(?:\bshares\b|\bshareholder\b)", text, re.I))
check("Founder final authority", "retain final architectural decision authority" in text)
check("Architecture governance", all(s in text for s in
      ("Zero Trust", "Approval Gateway", "Public / Private Boundary")))
check("Engineering proof", "Verified Engineering Milestones" in text
      and "TESTED" in text and "SPECIFIED" in text)
check("Clear reference versus production limits",
      "not establish product deployment" in text and
      "No production agent-payment service is assigned DEPLOYED or LIVE VERIFIED" in text)
check("Business inquiry route", "Collaboration and business inquiries" in text
      and "sign in to GitHub to open a new issue" in text
      and "https://github.com/oromaskevic23-cmd/Capital-Core-Public/issues" in text)
check("Preserved upstream attribution", "Third-party models, libraries" in text
      and "retain their original attribution" in text)
check("Free of template filler", "## Hi there 👋" not in text
      and "I'm currently learning" not in text)
links = re.findall(r"\]\(([^)\s]+)\)", text) + re.findall(r'href="([^"]+)"', text)
check("At least ten useful destination links", len(links) >= 10)
check("Links are absolute HTTPS or local anchor",
      all((urlparse(u).scheme == "https" and urlparse(u).netloc)
          or u.startswith("#") for u in links))
OFFICIAL_PAGES = {
    "https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/",
    "https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/",
    "https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/#infrastructure",
    "https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/#capital-core",
    "https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/projects/",
    "https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/velion/",
    "https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/projects/",
}
TRUSTED_RAW_GRAPHICS = {
    "https://raw.githubusercontent.com/oromaskevic23-cmd/IMPERIUM/main/assets/imperium-hero-20261029.jpg",
    "https://raw.githubusercontent.com/oromaskevic23-cmd/N.D.B/main/assets/ndb-hero-20261029.jpg",
}
def allowed_public_link(link):
    if link.startswith("#"):
        return True
    parsed = urlparse(link)
    if link in OFFICIAL_PAGES or link in TRUSTED_RAW_GRAPHICS:
        return True
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.query:
        return False
    if parsed.fragment and not re.fullmatch(r"[a-z0-9-]{1,80}", parsed.fragment):
        return False
    if parsed.netloc != "github.com":
        return False
    decoded = unquote(parsed.path)
    parts = decoded.split("/")
    return len(parts) >= 2 and parts[1] == "oromaskevic23-cmd" and all(
        part not in ("", ".", "..") for part in parts[2:]
    ) and chr(92) not in decoded
check("Official Pages plus safe GitHub namespace", all(allowed_public_link(u) for u in links))
check("No sign-in-only direct issue form", "/issues/new" not in text)
check("No obsolete Val Town website in published README", "imperialcore.val.run" not in text)
check("Public milestone PR/CI references with honest private HANTER boundary",
      all(f"/{repo}/pull/{pr}" in text and f"/{repo}/actions/runs/" in text
          for repo,pr in (("VELION-LLM-Public",1),
                          ("CONSTRUCTOR-AI",1),("CYBER-HAK-Public",1)))
      and "Private historical checkpoint" in text
      and "not independently inspectable" in text)
patterns = [
    r"ghp_[A-Za-z0-9]{36}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"-----BEGIN (?:OPENSSH|RSA|EC|PRIVATE) KEY-----",
    r"sk-[A-Za-z0-9_-]{20,}",
]
check("No common credential token patterns",
      not any(re.search(pattern, text) for pattern in patterns))
for name, success in CHECKS:
    print(("PASS" if success else "FAIL") + ": " + name)
print(f"Profile integrity: {sum(ok for _, ok in CHECKS)}/{len(CHECKS)} PASS")
sys.exit(0 if all(ok for _, ok in CHECKS) else 1)
