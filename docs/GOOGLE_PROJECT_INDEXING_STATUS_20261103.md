# IMPERIAL Core — Google Discoverability & Public Project Index
**Checkpoint:** 2026-11-03 · **Status:** SOURCE AND NAVIGATION VERIFIED; GOOGLE INDEXATION UNVERIFIED.
**Founder:** Alexander Nikolaevich Romaskevich (RomaskevicH), Founder • Owner • CEO • Chief Systems Architect and final architectural decision authority.

## Scope verified through authorized GitHub connector

| Metric | Evidence and classification |
|---|---|
| Owned repositories inspected | 32 repositories in authenticated owner inventory |
| Public repositories | 25 (visible to search engines subject to normal crawling) |
| Private repositories | 7 (excluded; never linked to public registry) |
| Distinct public technology/business project repositories listed | 23 |
| Founder profile repo | 1, public identity site and landing page (not a separate product) |
| Separate public governance / U.S. holding-company planning blueprint | 1, not a technology product and not promoted in the SEO catalog; legal planning only, no incorporation or share-status claims |
| Published project catalogs | Founder `projects/index.html` and company `reference/projects/index.html` on their respective `gh-pages` branches |
| Project JSON-LD `ItemList` | 23 entries, consistent project URLs and 1-based positions on both published sources |
| Sitemap / robots.txt | Present on both `gh-pages` branches, canonical host URLs declared; HTTP 200 independently checked on 2026-11-03 |
| Private source visibility | 7 private repositories excluded from all public project catalog items |
| Search Console property owner | NOT VERIFIED (Google Contacts access is unrelated) |
| Google sitemap submission | NOT VERIFIED (requires Google Search Console authenticated property) |
| Actual Google crawl/index presence | NOT VERIFIED (requires URL Inspection / Performance evidence) |
| Verified ranking or Knowledge Graph | NOT VERIFIED (do not fabricate) |

## Canonical properties and authoritative sitemap URLs

Each path is a distinct GitHub Pages URL-prefix property, even though both share `oromaskevic23-cmd.github.io`. Canonical links must remain self-referential for separately indexable, substantively distinct pages.

**Founder website:**
- Homepage: https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/
- Project portfolio: https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/projects/
- Sitemap: https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/sitemap.xml
- Robots: https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/robots.txt

**IMPERIAL Core company website:**
- Homepage: https://oromaskevic23-cmd.github.io/Capital-Core-Public/
- Project directory: https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/projects/
- Sitemap: https://oromaskevic23-cmd.github.io/Capital-Core-Public/sitemap.xml
- Supplementary reference sitemap: https://oromaskevic23-cmd.github.io/Capital-Core-Public/reference/sitemap.xml
- Robots: https://oromaskevic23-cmd.github.io/Capital-Core-Public/robots.txt

**Important:** the sitemap hosted on a GitHub Pages project site contains **only canonical pages hosted within that site's URL subtree**; GitHub.com repository links remain normal crawlable HTML anchors and `ItemList` structured references, not off-host URLs inserted into a foreign sitemap. A private repository, a proposed legal entity, an internal control plane, or a speculative product URL must not be added to a public sitemap.

## Release notes — applied changes

1. Reconciled the GitHub owner inventory with the public portfolio: 20 -> **23** public technology projects, adding `IMPERIAL-CRM-Autopilot`, `IMPERIAL-Skill`, `Supabase`.
2. Updated both published GitHub Pages project directory HTML files and their schema.org JSON-LD `ItemList` to the same 23 public project URLs.
3. Updated the first-party [canonical public project registry](FOUNDER_PUBLIC_PROJECT_REGISTRY_20261031.md) and profile README backlinks.
4. Strengthened [source SEO verification](../tools/verify_pages_seo.py) to reject stale portfolio counts, missing visible anchor links, JSON-LD mismatch and leaks of any of the seven private repository URLs.
5. Extended [GitHub Actions published-source verification](../.github/workflows/search-indexability.yml) to check public HTTP responses as an independent publishing gate. This is **not** a Google crawl or ranking test.

### Evidence IDs (specific revisions)

- Founder public portfolio change: `fe0b5a67571091188536e040215250a56f5f1709`, `gh-pages`.
- Corporate public portfolio change: `63aed247292630963185695d49fd58b1a40d2a0e`, `gh-pages`.
- Founder identity/project registry: `9b26b268298281ba4f6624a194db30a93ad96aac`, `main`.
- Source SEO CI success: https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/actions/runs/41702255715 (prior to adding live HTTP probe).
- Source audit and live HTTP probe: **PASS** at https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/actions/runs/41702530969 (commit `b6c358b8bf389746a0af21fdb14d8336431c96f6`). This run validated **12 founder-site** and **25 corporate-site** XML sitemap URLs in published source, and fetched both site homepages, both portfolio directories and both root sitemap URLs with HTTP **200** from a GitHub-hosted runner. This is site availability evidence only, not Google indexation.

## Remaining Google-only steps

The user must have actual ownership/authorized OAuth access to the two Google Search Console URL-prefix properties. Google Contacts cannot submit or inspect URLs.

1. Sign into https://search.google.com/search-console/ using the intended verified account.
2. Add or select each actual GitHub Pages URL-prefix property; complete a Google-supported ownership verification route.
3. In `Indexing > Sitemaps`, submit the exact sitemap of that property. Do not misrepresent submitting a GitHub.com repository URL as a sitemap.
4. Use `URL Inspection` on both main homes and both project catalogs to record first observed crawl/index state and request indexing when eligible.
5. After Google processes the submitted sitemap, record its actual `Success` or `Couldn't fetch` status; use URL Inspection and Pages report to troubleshoot `Discovered - currently not indexed`, `Crawled - currently not indexed` or canonicalization issues. Never fabricate a submission acknowledgment, indexed count or ranking.

**Google Search Central guidance:** https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap . Sitemap submission signals discovery and does **not** guarantee indexing or higher search ranking.

## Protected identity and project boundaries

The public architecture uses Federated Multi-Orchestrator Architecture, HANTER, ORION, VELION, NCA, Guardian Core, Approval Gateway, Audit Ledger, Zero Trust, AI Passport, Enterprise Skills, and Public / Private Boundary. Third-party code and brands retain their rightful ownership. IMPERIUM remains a long-term architectural digital currency proposed for AI agents worldwide; there is no proof of current global agent adoption or listed-market status. Founder residential details, private repositories, customer data and private licensing infrastructure are intentionally not exposed in the SEO catalog.

**Next actual production checkpoint:** Google Search Console ownership verification and recorded submission receipts, then Google-reported page indexing—not a simulated or inferred PASS.
