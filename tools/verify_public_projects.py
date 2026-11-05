#!/usr/bin/env python3
"""Check that the portfolio's declared repositories remain public and reachable."""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from verify_pages_seo import PUBLIC_PROJECTS

OWNER = "oromaskevic23-cmd"


class NoRedirect(HTTPRedirectHandler):
    """Never send the GitHub token to a redirect destination."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check_project(name: str, opener, token: str = "") -> str | None:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "imperial-public-project-audit",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request(f"https://api.github.com/repos/{OWNER}/{name}", headers=headers)
    try:
        with opener.open(request, timeout=12) as response:
            if response.status != 200:
                return f"{name}: API returned HTTP {response.status}; availability is unknown"
            repo = json.load(response)
    except HTTPError as error:
        if error.code in (301, 302, 307, 308):
            return f"{name}: repository URL redirected; check whether it was renamed"
        if error.code == 404:
            return f"{name}: GitHub did not return a public repository (HTTP 404)"
        return f"{name}: GitHub API returned HTTP {error.code}; availability is unknown"
    except (URLError, TimeoutError, OSError, ValueError):
        return f"{name}: GitHub API could not be checked; availability is unknown"

    if not isinstance(repo, dict):
        return f"{name}: unexpected GitHub response; availability is unknown"
    owner = repo.get("owner")
    if not isinstance(owner, dict) or owner.get("login", "").lower() != OWNER:
        return f"{name}: repository owner does not match the portfolio"
    if repo.get("name") != name or repo.get("html_url") != f"https://github.com/{OWNER}/{name}":
        return f"{name}: canonical repository URL does not match the portfolio"
    if repo.get("private") is not False or repo.get("disabled") is not False:
        return f"{name}: repository is private, disabled, or its visibility is unknown"
    return None


def main() -> int:
    opener = build_opener(NoRedirect())
    token = os.environ.get("GITHUB_TOKEN", "")
    errors = [result for name in sorted(PUBLIC_PROJECTS)
              if (result := check_project(name, opener, token))]
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    if errors:
        print(f"Public project check failed for {len(errors)} of {len(PUBLIC_PROJECTS)} repositories.",
              file=sys.stderr)
        return 1
    print(f"All {len(PUBLIC_PROJECTS)} portfolio repositories are public and reachable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
