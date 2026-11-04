"""Regression tests for Google ProfilePage timestamps and evidence states."""
import unittest

from tools.verify_pages_seo import (
    FOUNDER, SEOError, validate_google_observation, validate_profile_page_dates,
)


class ProfileMetadataTests(unittest.TestCase):
    def test_valid_datetime_and_optional_missing_date(self):
        validate_profile_page_dates(
            [{"@type": "ProfilePage", "dateModified": "2026-11-04T19:22:38Z"},
             {"@type": "ProfilePage"}], FOUNDER,
        )

    def test_google_rejects_a_date_without_a_time(self):
        with self.assertRaises(SEOError):
            validate_profile_page_dates(
                [{"@type": "ProfilePage", "dateModified": "2026-11-04"}], FOUNDER,
            )

    def test_malformed_and_timezone_free_timestamps_are_rejected(self):
        for timestamp in ("not-a-date", "2026-11-04T19:22:38", "2026-13-04T19:22:38Z"):
            with self.subTest(timestamp=timestamp), self.assertRaises(SEOError):
                validate_profile_page_dates(
                    [{"@type": "ProfilePage", "dateModified": timestamp}], FOUNDER,
                )

    def test_unrelated_webpage_date_is_outside_this_rule(self):
        validate_profile_page_dates([{"@type": "WebPage", "dateModified": "2026-11-04"}], FOUNDER)


class GoogleEvidenceTests(unittest.TestCase):
    def test_unverified_evidence_remains_valid(self):
        validate_google_observation({
            "google_indexed": "UNVERIFIED",
            "google_search_console_verified": "UNVERIFIED",
            "sitemap_submitted": "UNVERIFIED",
            "evidence_is_not_independently_ranked": True,
        })

    def test_observations_need_a_dated_property_and_source(self):
        with self.assertRaises(SEOError):
            validate_google_observation({
                "google_indexed": "NOT_INDEXED_AT_INSPECTION",
                "google_search_console_verified": "VERIFIED",
                "sitemap_submitted": "SUBMITTED",
                "evidence_is_not_independently_ranked": True,
            })

    def test_owner_observation_preserves_submission_and_fetch_states(self):
        status = {
            "google_indexed": "NOT_INDEXED_AT_INSPECTION",
            "google_search_console_verified": "VERIFIED",
            "sitemap_submitted": "SUBMITTED",
            "evidence_is_not_independently_ranked": True,
            "property": FOUNDER,
            "evidence_source": "OWNER_SEARCH_CONSOLE_UI",
            "observation_date_utc": "2026-11-04",
            "recorded_at_utc": "2026-11-04T23:17:00Z",
            "sitemap_url": FOUNDER + "sitemap.xml",
            "sitemap_report_status": "COULD_NOT_FETCH",
            "indexing_request": "SUBMITTED",
            "founder_url_live_test": "INDEXABLE",
        }
        validate_google_observation(status)
        for key, value in (
            ("observation_date_utc", "2026-11-05"),
            ("founder_url_live_test", "UNVERIFIED"),
            ("sitemap_report_status", "INDEXED"),
        ):
            invalid = dict(status)
            invalid[key] = value
            with self.subTest(field=key), self.assertRaises(SEOError):
                validate_google_observation(invalid)
        status["google_indexed"] = "INDEXED"
        with self.assertRaises(SEOError):
            validate_google_observation(status)


if __name__ == "__main__":
    unittest.main()
