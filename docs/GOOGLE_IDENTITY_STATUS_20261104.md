# Public Google identity — evidence checkpoint

**Observation date:** 2026-11-04 UTC. This is a dated operator record, not a live ranking report.

The public identity describes Alexander Nikolaevich Romaskevich, also known as
Alexander Romaskevich and RomaskevicH, as Founder, Owner, CEO of IMPERIAL Core. These are founder-declared project roles.

## Search Console observations

The authorized owner account's Google Search Console showed the following:

| Item | Observed state on 2026-11-04 UTC |
|---|---|
| [Founder site property](https://search.google.com/search-console?resource_id=https%3A%2F%2Foromaskevic23-cmd.github.io%2Foromaskevic23-cmd%2F) | Ownership verified using the public HTML verification tag. |
| [IMPERIAL Core property](https://search.google.com/search-console?resource_id=https%3A%2F%2Foromaskevic23-cmd.github.io%2FCapital-Core-Public%2F) | Ownership verified using the public HTML verification tag. |
| Founder homepage | The Google index inspection said the URL was unknown before the request. A live test said the page was indexable and recognized one valid ProfilePage item. Google accepted an indexing request. |
| Founder sitemap | Submitted. The sitemap report initially showed **Could not fetch**; a separate live inspection reported crawl allowed and page fetch successful. Processing by the sitemap report was not confirmed. |
| IMPERIAL Core sitemap | Submitted. The sitemap report initially showed **Could not fetch**; a separate live inspection reported crawl allowed and page fetch successful. Processing by the sitemap report was not confirmed. |

These are observations made in the owner-only Search Console interface; a
reader without property access cannot independently inspect that interface.
An accepted request is not evidence of indexing, ranking, entity recognition
or a Knowledge Panel. Those outcomes remain unverified at this checkpoint.

## Published pages and source validation

- [Founder homepage](https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/)
  and [IMPERIAL Core reference](https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/)
  describe the same Person and link to the controlled GitHub profile.
- The founder site has ten language routes, a canonical Person identifier,
  language alternates and a sitemap. The visible identity includes full Latin
  and Cyrillic names and the public signature.
- Google's live ProfilePage inspection initially flagged a date-only value.
  The source was corrected to an ISO 8601 date and time with timezone; the
  subsequent Google live test showed one valid item without that warning.
- The engineering evidence page had the same date-only problem and was
  corrected using its last substantive source commit timestamp.
- The source audit validated 12 founder and 25 IMPERIAL Core sitemap URLs,
  including canonical URLs, language clusters, structured identity and
  privacy checks. HTTP success, crawlability, submission and indexing are
  separate states.
- GitHub Pages does not host a user-site robots file at the domain root here;
  the observed root request returned HTTP 404. Project-subdirectory robots
  files do not replace a host-root robots file. Google documents that a 404
  robots response is treated as no robots file, with no crawl restrictions.
  The two sitemap URLs were submitted directly through Search Console.

## Recheck

Revisit both sitemap reports after Google has had time to process them. If
**Could not fetch** persists, inspect each sitemap's Google live fetch and
Search Console details before making changes. Recheck the founder URL in URL
Inspection for Google-reported indexing. Do not resubmit repeatedly or claim
search placement without a dated observation.

References: [Google sitemap troubleshooting](https://support.google.com/webmasters/answer/7451001),
[Google ProfilePage structured data](https://developers.google.com/search/docs/appearance/structured-data/profile-page),
and [Google robots.txt handling](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec).
