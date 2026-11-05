"""Regression checks for public repository status and inconclusive API errors."""

import io
import json
from pathlib import Path
import sys
import unittest
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from verify_public_projects import NoRedirect, check_project


class Response(io.BytesIO):
    status = 200

    def __init__(self, value):
        super().__init__(json.dumps(value).encode("utf-8"))


class Opener:
    def __init__(self, value=None, code=None):
        self.value, self.code = value, code
        self.request = None

    def open(self, request, timeout):
        self.request = request
        if self.code:
            raise HTTPError(request.full_url, self.code, "error", {}, None)
        return Response(self.value)


def repo():
    return {"name": "Example", "owner": {"login": "oromaskevic23-cmd"},
            "html_url": "https://github.com/oromaskevic23-cmd/Example",
            "private": False, "disabled": False}


class PublicProjectTests(unittest.TestCase):
    def test_public_project_passes(self):
        self.assertIsNone(check_project("Example", Opener(repo())))

    def test_private_or_moved_project_does_not_pass(self):
        private = repo()
        private["private"] = True
        self.assertIn("private", check_project("Example", Opener(private)))
        moved = repo()
        moved["name"] = "Renamed"
        self.assertIn("canonical", check_project("Example", Opener(moved)))
        self.assertIn("redirected", check_project("Example", Opener(code=301)))

    def test_api_errors_do_not_claim_a_repository_is_private(self):
        self.assertIn("HTTP 404", check_project("Example", Opener(code=404)))
        limited = check_project("Example", Opener(code=403))
        self.assertIn("availability is unknown", limited)
        self.assertNotIn("private", limited)

    def test_token_is_sent_only_to_the_fixed_github_api(self):
        opener = Opener(repo())
        self.assertIsNone(check_project("Example", opener, "test-token"))
        self.assertEqual(opener.request.full_url,
                         "https://api.github.com/repos/oromaskevic23-cmd/Example")
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, "", {},
                                                        "https://example.com/"))


if __name__ == "__main__":
    unittest.main()
