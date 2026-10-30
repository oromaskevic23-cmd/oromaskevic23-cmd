#!/usr/bin/env python3
"""Read-only public GitHub licensing inventory; not legal clearance or a license grant.

Public endpoint only. Never retrieves private repository data, uses payment APIs,
posts customer material, or changes repository settings.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OWNER = "oromaskevic23-cmd"
FOUNDER = "Alexander Nikolaevich Romaskevich"
SIGNATURE = "RomaskevicH"
LICENSE = re.compile(r"^(?:LICENSE|LICENCE|COPYING)(?:\.[A-Za-z0-9_-]+)?$", re.I)
API = "https://api.github.com"


def api_json(path: str, token: str = ""):
    if not path.startswith("/") or ".." in path or "//" in path:
        raise ValueError("UNSAFE_API_PATH")
    url = API + path
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "imperial-ip-audit/1",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15) as response:
        return json.load(response)


def audit_public_repo(repo: dict, contents: list[dict], author_record: str | None):
    name = repo["name"]
    files = {entry["name"] for entry in contents
             if entry.get("type") == "file" and isinstance(entry.get("name"), str)}
    licenses = sorted(f for f in files if LICENSE.fullmatch(f))
    result = {"repo": name, "url": repo["html_url"], "public": not repo.get("private", False),
              "fork": bool(repo.get("fork", False)),
              "license_files": licenses, "founder_record": "UNVERIFIED",
              "license_status": "UNRESOLVED", "release_authorized": False}
    if result["fork"]:
        result["license_status"] = "UPSTREAM_LICENSES_REQUIRE_REVIEW"
        return result
    if "AUTHORS.md" not in files:
        result["founder_record"] = "MISSING"
    elif author_record is None:
        result["founder_record"] = "UNREADABLE"
    elif FOUNDER in author_record and SIGNATURE in author_record and any(
            x in author_record.lower() for x in ("git history", "git contribution", "contributor")):
        result["founder_record"] = "FOUNDER_DECLARED_CONTRIBUTIONS_PRESERVED"
    else:
        result["founder_record"] = "INCOMPLETE"
    result["license_status"] = ("ROOT_LICENSE_PRESENT_THIRD_PARTY_RIGHTS_UNVERIFIED"
                                if licenses else "NO_ROOT_LICENSE_GRANT")
    return result


def collect_public(owner: str, token: str = ""):
    if owner != OWNER:
        raise ValueError("OWNER_SCOPE_DENIED")
    records = []
    for page in range(1, 11):
        listing = api_json("/users/" + owner + "/repos?type=owner&per_page=100&page=" + str(page), token)
        if not isinstance(listing, list):
            raise RuntimeError("UNEXPECTED_REPOSITORY_RESPONSE")
        for repo in listing:
            if repo.get("owner", {}).get("login", "").lower() != owner.lower() or repo.get("private"):
                continue
            name = repo.get("name", "")
            if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", name):
                raise ValueError("UNSAFE_REPOSITORY_NAME")
            prefix = "/repos/" + owner + "/" + name + "/contents/"
            listing_contents = api_json(prefix, token)
            if not isinstance(listing_contents, list):
                raise RuntimeError("UNEXPECTED_ROOT_CONTENTS: " + name)
            files = {entry["name"] for entry in listing_contents
                     if entry.get("type") == "file" and isinstance(entry.get("name"), str)}
            author_record = None
            if "AUTHORS.md" in files:
                author_data = api_json(prefix + "AUTHORS.md", token)
                if author_data.get("encoding") == "base64" and isinstance(author_data.get("content"), str):
                    author_record = base64.b64decode(author_data["content"], validate=False).decode("utf-8")
                else:
                    raise RuntimeError("UNREADABLE_AUTHOR_RECORD: " + name)
            records.append(audit_public_repo(repo, listing_contents, author_record))
        if len(listing) < 100:
            break
    else:
        raise RuntimeError("PAGINATION_LIMIT_REACHED")
    return sorted(records, key=lambda x: x["repo"].lower())


def summarize(records):
    return {"public_repos_checked": len(records),
            "founder_records_verified": sum(x["founder_record"] == "FOUNDER_DECLARED_CONTRIBUTIONS_PRESERVED" for x in records),
            "root_license_absent": sum(x["license_status"] == "NO_ROOT_LICENSE_GRANT" for x in records),
            "root_license_present_rights_unverified": sum(x["license_status"] == "ROOT_LICENSE_PRESENT_THIRD_PARTY_RIGHTS_UNVERIFIED" for x in records),
            "releases_authorized": 0,
            "private_repositories_included": False,
            "complete_copyright_clearance": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="license-audit.json")
    parser.add_argument("--offline-fixture", default="")
    args = parser.parse_args()
    if args.offline_fixture:
        fixture = json.loads(Path(args.offline_fixture).read_text(encoding="utf-8"))
        records = [audit_public_repo(x["repo"], x["contents"], x.get("author_record")) for x in fixture]
    else:
        # Deliberately use only public API; do not accept a wide-scope private PAT.
        records = collect_public(OWNER, os.environ.get("GITHUB_TOKEN", ""))
    report = {"schema": "imperial.ip.public-inventory.v1", "owner": OWNER,
              "observed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "summary": summarize(records), "repositories": records,
              "limits": ["PUBLIC_REPOSITORIES_ONLY", "ROOT_FILES_ONLY",
                         "DEPENDENCY_AND_MODEL_LICENSES_NOT_CLEARED", "NO_RELEASE_AUTHORIZATION",
                         "NO_PRIVATE_SOURCE_EXPOSURE"]}
    Path(args.out).write_text(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
    print(json.dumps(report["summary"], sort_keys=True))
    for row in records:
        print(row["repo"] + ": " + row["license_status"] + " / " + row["founder_record"])
    if any(x["founder_record"] in ("MISSING", "INCOMPLETE", "UNREADABLE") for x in records):
        print("REMEDIATION_REQUIRED: one or more founder records need owner-reviewed repair")
    print("REPORT_WRITTEN: " + args.out)
    print("NOT_A_LICENSE_GRANT_OR_A_LEGAL_CERTIFICATION")


if __name__ == "__main__":
    try:
        main()
    except (urllib.error.URLError, ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print("INVENTORY_FAILED_CLOSED: " + str(exc), file=sys.stderr)
        sys.exit(1)
