#!/usr/bin/env python3
"""Verify two GitHub Pages publication branches for search-engine eligibility.

Validates published source trees, not Google indexing or Search Console ownership.
Uses only Python stdlib. Never modifies content or collects personal data.
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

FOUNDER = "https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/"
ECOSYSTEM = "https://oromaskevic23-cmd.github.io/IMPERIAL-Core-Public/"
GITHUB_PROFILE = "https://github.com/oromaskevic23-cmd"
LOCALES = {"en", "uk", "ru", "de", "fr", "es", "pt", "ja", "zh", "ar"}
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class SEOError(RuntimeError):
    pass


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.title_open = False
        self.script_open = False
        self.title = []
        self.script_data = []
        self.scripts = []
        self.head_links = []
        self.head_meta = []
        self.headings = 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "head":
            self.in_head = True
        if tag == "title" and self.in_head:
            self.title_open = True
        if tag == "meta" and self.in_head:
            self.head_meta.append(a)
        if tag == "link" and self.in_head:
            self.head_links.append(a)
        if tag == "script" and a.get("type") == "application/ld+json":
            self.script_open = True
            self.script_data = []
        if tag == "h1":
            self.headings += 1

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        if tag == "title":
            self.title_open = False
        if tag == "script" and self.script_open:
            self.scripts.append("".join(self.script_data))
            self.script_open = False

    def handle_data(self, text):
        if self.title_open:
            self.title.append(text)
        if self.script_open:
            self.script_data.append(text)


def demand(condition, message):
    if not condition:
        raise SEOError(message)


def local_page(site: Path, prefix: str, url: str) -> Path:
    demand(url.startswith(prefix) and "#" not in url and "?" not in url,
           "Unexpected or non-canonical sitemap URL: " + url)
    suffix = unquote(url[len(prefix):])
    demand("\\" not in suffix and not suffix.startswith("/") and
           all(p not in (".", "..") for p in suffix.split("/") if p),
           "Unsafe site-relative URL " + url)
    name = (suffix + "index.html") if suffix.endswith("/") or not suffix else suffix
    file = (site / name).resolve()
    demand(file.is_relative_to(site.resolve()), "Page escapes site root")
    demand(file.is_file(), "Sitemap URL lacks a published HTML file: " + url)
    return file


def validate_page(site: Path, prefix: str, url: str):
    source = local_page(site, prefix, url).read_text(encoding="utf-8")
    demand(len(source) <= 2_000_000, "Oversize indexable page " + url)
    parser = Page()
    parser.feed(source)
    title = "".join(parser.title).strip()
    demand(10 <= len(title) < 135, "Bad title " + url)
    demand(parser.headings == 1, "Expected exactly one H1 " + url)
    demand(isinstance(parser.lang, str) and
           parser.lang.split("-", 1)[0].lower() in LOCALES,
           "Unexpected document language " + url)
    descriptions = [m.get("content", "") for m in parser.head_meta
                    if m.get("name", "").lower() == "description"]
    demand(len(descriptions) == 1 and len(descriptions[0]) >= 40,
           "Missing unique meaningful meta description " + url)
    directives = ",".join(m.get("content", "") for m in parser.head_meta
                         if m.get("name", "").lower() in ("robots", "googlebot")).lower()
    demand("noindex" not in directives and "nofollow" not in directives,
           "Search bot blocked in metadata " + url)
    canon = [l.get("href") for l in parser.head_links if l.get("rel") == "canonical"]
    demand(canon == [url], "Missing or conflicting self canonical " + url)
    alt = {l.get("hreflang") for l in parser.head_links
           if l.get("rel") == "alternate"}
    demand({"x-default", "en", "ru", "uk"}.issubset(alt),
           "Missing essential international language alternatives " + url)
    demand(parser.scripts, "No JSON-LD " + url)
    graphs = []
    for text in parser.scripts:
        try:
            data = json.loads(text)
        except ValueError as e:
            raise SEOError("Invalid JSON-LD on " + url) from e
        graphs.extend(data.get("@graph", [data]) if isinstance(data, dict) else data)
    people = [g for g in graphs if isinstance(g, dict) and g.get("@type") == "Person"]
    demand(len(people) == 1, "Missing or duplicate Person entity " + url)
    person = people[0]
    demand(person.get("name") == "Alexander Romaskevich",
           "Identity name drift " + url)
    demand("RomaskevicH" in person.get("alternateName", []) and
           "Александр Николаевич Ромаскевич" in person.get("alternateName", []),
           "Official alias missing " + url)
    demand(GITHUB_PROFILE in person.get("sameAs", []),
           "Missing verified GitHub identity " + url)
    if url in {ECOSYSTEM + "reference/" + variant for variant in
               ("", "ru/", "uk/", "de-CH/", "ja/", "zh/")}:
        demand(person.get("image") ==
               FOUNDER + "assets/alexander-romaskevich-portrait.jpeg",
               "Official founder portrait missing from reference identity " + url)
        demand("CEO" in person.get("jobTitle", ""),
               "Founder role drift in reference identity " + url)
    demand(not any(k in person for k in
                   ("homeLocation", "address", "birthPlace", "nationality",
                    "streetAddress", "telephone", "email")),
           "Sensitive location or identity fields should not be published " + url)
    return parser.lang


def audit(site: Path, prefix: str, expected_minimum: int):
    sitemap = site / "sitemap.xml"
    demand(sitemap.is_file(), "Missing sitemap.xml")
    try:
        tree = ET.parse(sitemap)
    except ET.ParseError as e:
        raise SEOError("Invalid sitemap XML " + prefix) from e
    locs = [u.text for u in tree.findall("s:url/s:loc", NS)]
    demand(len(locs) >= expected_minimum, "Sitemap has fewer indexable pages than expected")
    demand(len(locs) == len(set(locs)), "Duplicate sitemap loc")
    if prefix == ECOSYSTEM:
        reference_sitemap = site / "reference" / "sitemap.xml"
        demand(reference_sitemap.is_file(), "Primary reference sitemap missing")
        reference_urls = [u.text for u in ET.parse(reference_sitemap).findall("s:url/s:loc", NS)]
        demand(len(reference_urls) >= 9, "Expected nine published reference routes")
        demand(set(reference_urls).issubset(set(locs)),
               "One or more primary reference URLs missing from root sitemap")
        demand(prefix + "reference/" in reference_urls,
               "Main IMPERIAL Core reference URL is absent")
        for main_language in ("ru", "uk", "de-CH", "ja", "zh"):
            demand(prefix + "reference/" + main_language + "/" in reference_urls,
                   "Localized reference route missing: " + main_language)
        demand(prefix + "reference/constructor-ai/" in reference_urls,
               "CONSTRUCTOR AI reference route missing")
    langs = set()
    for url in locs:
        langs.add(validate_page(site, prefix, url).split("-", 1)[0].lower())
    demand(LOCALES.issubset(langs), "Missing one or more languages from sitemap")
    robots = (site / "robots.txt").read_text(encoding="utf-8").lower()
    demand("disallow: /" not in robots and
           ("sitemap: " + prefix.lower() + "sitemap.xml") in robots,
           "Unexpected project sitemap or robots directives")
    demand((site / "index.html").is_file(), "Missing home page")
    return len(locs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--founder-tree", type=Path, required=True)
    parser.add_argument("--ecosystem-tree", type=Path, required=True)
    args = parser.parse_args()
    n1 = audit(args.founder_tree, FOUNDER, 10)
    n2 = audit(args.ecosystem_tree, ECOSYSTEM, 10)
    print(f"PASS: {n1} founder site URLs + {n2} ecosystem site URLs, "
          "canonicals, language clusters, structured identity and privacy.")
    print("BOUNDARY: verified GitHub Pages published source trees, NOT Google crawl,"
          " indexing, rankings, Search Console ownership or sitemap submission.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (SEOError, OSError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
