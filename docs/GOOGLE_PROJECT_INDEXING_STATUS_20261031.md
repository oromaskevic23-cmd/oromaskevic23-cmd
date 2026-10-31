# IMPERIAL Core — Google Public Discoverability Register

**Snapshot: 2026-10-31. Not a claim of Search Console ownership or indexing.**

| Stage | Current evidence-based state |
| --- | --- |
| Owner public GitHub profile and verified repository links | YES — direct GitHub metadata |
| Founder identity and canonical public portfolio | Source-published |
| VELION v2 module and architecture documentation | Source-published / CI-verified on cited revision |
| Canonical public project author/source linking | Source-published |
| Published stable HTML website with verified HTTP 200 | Not independently confirmed in this review |
| Site-specific canonical/hreflang metadata | Not independently confirmed on deployed HTML |
| Deployed sitemap and robots URLs | Not independently confirmed |
| Google Search Console property ownership | Not verified |
| Authorized sitemap submission to Search Console | Not verified |
| Google crawl, indexing, Knowledge Panel, ranking | Not verified |

## Operator release checklist

Publish real HTTPS HTML landing pages and founder biography; verify exact 200 and visible content. Match names and original author records, version/source citations and lawful third-party attribution; do not claim exclusive ownership of unrelated software.

Add valid `Person`, `SoftwareSourceCode` and `ProfilePage` JSON-LD **only** to suitable real pages, with canonical equal to their actual public URL. Generate a UTF-8 sitemap containing only the real canonical pages and expose it via an appropriate root URL, discoverable from robots.txt if supported. Use Google Search Console under a confirmed authorized property to submit that URL and inspect crawl/indexing response.

Official guidance: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap · https://developers.google.com/search/docs/appearance/structured-data/profile-page

Google cannot be forced to index a page. A submitted sitemap is a hint; neither visibility nor ranking is guaranteed. Preserve privacy: do not disclose a founder's residence or infer a corporate headquarters from a server region.
