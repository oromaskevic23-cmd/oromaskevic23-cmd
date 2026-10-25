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
PROJECTS = ("IMPERIAL Core", "VELEON", "HANTER", "CONSTRUCTOR AI",
            "LEGION", "CYBER HAK", "NDB & IMPERIUM")
CHECKS = []
def check(name, condition):
    CHECKS.append((name, bool(condition)))

text = README.read_text(encoding="utf-8")
sections = re.findall(r"^## ([^\r\n]+)$", text, flags=re.MULTILINE)
check("Founder title and identity", text.startswith("# Alexander Romaskevich\n")
      and "RomaskevicH" in text and "Ukraine" in text)
check("All nine ordered sections", sections == list(EXPECTED_SECTIONS))
check("Public technology portfolio", all(name in text for name in PROJECTS))
check("Founder final authority", "Final Architectural Decision Authority" in text)
check("Architecture governance", all(s in text for s in
      ("Zero Trust", "Approval Gateway", "Public / Private Boundary")))
check("Engineering proof", "Verified Engineering Milestones" in text
      and "TESTED" in text and "SPECIFIED" in text)
check("Clear reference versus production limits",
      "not establish product deployment" in text and
      "No flagship is assigned DEPLOYED or LIVE VERIFIED" in text)
check("Business inquiry route", "Collaboration and business inquiries" in text
      and "sign in to GitHub to open a new issue" in text
      and "https://github.com/oromaskevic23-cmd/IMPERIAL-Core-Public/issues" in text)
check("Preserved upstream attribution", "Third-party models, libraries" in text
      and "retain their original attribution" in text)
check("Free of template filler", "## Hi there 👋" not in text
      and "I'm currently learning" not in text)
links = re.findall(r"\]\(([^)\s]+)\)", text)
check("At least ten useful destination links", len(links) >= 10)
check("Links are absolute HTTPS or local anchor",
      all((urlparse(u).scheme == "https" and urlparse(u).netloc)
          or u.startswith("#") for u in links))
check("Exact GitHub HTTPS host and safe owner namespace", all(
      u.startswith("#") or (
          (parsed := urlparse(u)).scheme == "https"
          and parsed.netloc == "github.com"
          and parsed.username is None
          and parsed.password is None
          and not parsed.query
          and not parsed.fragment
          and (decoded := unquote(parsed.path)).startswith("/oromaskevic23-cmd")
          and (len(decoded) == len("/oromaskevic23-cmd")
               or decoded[len("/oromaskevic23-cmd")] == "/")
          and not any(part in ("", ".", "..") for part in decoded.split("/")[2:])
          and "\\\\" not in decoded
      ) for u in links))
check("No sign-in-only direct issue form", "/issues/new" not in text)
check("No obsolete Val Town website in published README", "imperialcore.val.run" not in text)
check("All four milestone PR and CI references present",
      all(f"/{repo}/pull/{pr}" in text and f"/{repo}/actions/runs/" in text
          for repo,pr in (("HANTER",3),("VELION-LLM-Public",1),
                          ("CONSTRUCTOR-AI",1),("CYBER-HAK-Public",1))))
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
