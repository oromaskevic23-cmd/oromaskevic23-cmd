"""Regenerate the static, localized IMPERIAL Core showcase on gh-pages."""

import hashlib
from html import escape
import json
from pathlib import Path
import re

from content import COPY, FEATURED, FEATURE_TEXT, LANGUAGES, MORE, MORE_TEXT, PORTFOLIO_LABELS, REFERENCE_LABELS

from founder import BIOGRAPHIES, ROLE, ROLE_RU, render_biography

ROOT = Path(__file__).resolve().parents[2]
PUBLICATION = ROOT / "imperial-core"
HOST = "https://oromaskevic23-cmd.github.io"
SHOWCASE = "/oromaskevic23-cmd/imperial-core/"
LEGACY_REFERENCE = "/Capital-Core-Public/reference/"
ASSETS = LEGACY_REFERENCE + "assets/"
SHOWCASE_ASSETS = SHOWCASE + "assets/"
DUBAI = ASSETS + "dubai/"
ART = ASSETS + "showcase/"
FOUNDER = HOST + "/oromaskevic23-cmd/"
GIT = "https://github.com/oromaskevic23-cmd"
CONTEST = GIT + "/IMPERIAL-DUBAI-2027-Public"
STUDIO = LEGACY_REFERENCE + "constructor-ai/studio/studio.html"
LANDSCAPES = ("aerial", "waterfront", "atrium", "intelligence", "night")
TOKENS = (
    ("NDB", "N.D.B", 760, 1060),
    ("IMPERIUM", "IMPERIUM", 720, 1280),
    ("NZT", "NZT-", 760, 760),
)
FOUNDER_LOCALES = {"en", "uk", "ru", "de", "fr", "es", "pt", "ar", "ja", "zh"}
PROOF_DETAILS = {
    "en": (
        "Engineering you can reproduce",
        "See the pinned source, commands and results for Alexander Romaskevich’s engineering portfolio.",
        ("Three application ZIPs matched across two builds. All six tests passed after clean extraction.",
         "A signed local mission returned a valid audit chain with zero external actions.",
         "The signed evidence summary verified and all ten verifier tests passed."),
    ),
    "ru": (
        "Инженерные результаты, которые можно повторить",
        "Исходники, команды и результаты проверок инженерных проектов Александра Ромаскевича.",
        ("Две сборки дали три побайтно одинаковых ZIP. Все шесть тестов распакованных приложений прошли.",
         "Подписанная локальная задача сохранила целостную цепочку аудита с нулём внешних действий.",
         "Проверка подтвердила подпись опубликованного отчёта. Все десять тестов проверяющего модуля прошли."),
    ),
}
PROOF_PROJECTS = (
    ("CONSTRUCTOR AI", "constructor-ai-reproduction"),
    ("HANTER", "hanter-reproduction"),
    ("IMPERIAL ONE", "imperial-one-reproduction"),
)
CARD_ICONS = ("gem", "stack-2", "topology-star-3", "shield-check", "id", "topology-star-3")
ALT_NAMES = ("Alexander Nikolaevich Romaskevich", "Александр Николаевич Ромаскевич", "Олександр Ромаскевич", "RomaskevicH")


def suffix(lang):
    return "" if lang == "en" else f"{lang}/"


def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="{ASSETS}showcase-icons.svg?v=3#{name}"/></svg>'


def link(label, href, style="text-link", arrow=True, extra=""):
    mark = f'<span class="arrow">{icon("arrow-up-right")}</span>' if arrow else ""
    classes = f' class="{style}"' if style else ""
    return f'<a{classes} href="{escape(href, quote=True)}"{extra}>{escape(label)}{mark}</a>'


def identity(lang, url, title, description):
    person = FOUNDER + "#person"
    organization = HOST + SHOWCASE + "#organization"
    website = HOST + SHOWCASE + "#website"
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title,
             "description": description, "inLanguage": lang, "isPartOf": {"@id": website},
             "about": {"@id": organization}, "author": {"@id": person}},
            {"@type": "Organization", "@id": organization, "name": "IMPERIAL Core",
             "url": HOST + SHOWCASE, "founder": {"@id": person},
             "logo": FOUNDER + "assets/imperial-core-emblem.webp"},
            {"@type": "Person", "@id": person, "name": "Alexander Romaskevich", "alternateName": ALT_NAMES,
             "url": FOUNDER, "jobTitle": founder_role(lang),
             "image": FOUNDER + "assets/alexander-romaskevich-portrait.jpeg", "sameAs": [GIT],
             "affiliation": {"@id": organization},
             "subjectOf": {"@id": FOUNDER + "engineering/#page"}},
            {"@type": "WebSite", "@id": website, "name": "IMPERIAL Core", "url": HOST + SHOWCASE,
             "publisher": {"@id": organization}},
        ],
    }


def founder_role(lang):
    return {"en": ROLE, "en-US": ROLE, "ru": ROLE_RU}.get(lang, COPY[lang]["role"])


def render_proof(lang, label):
    if lang not in PROOF_DETAILS:
        return ""
    title, intro, summaries = PROOF_DETAILS[lang]
    cards = "".join(
        f'<article class="entry"><h3>{name}</h3><p>{escape(summary)}</p>'
        f'{link(label, FOUNDER + "engineering/#" + section)}</article>'
        for (name, section), summary in zip(PROOF_PROJECTS, summaries, strict=True)
    )
    return f"""<section class="wrap section" id="engineering-proof" aria-labelledby="engineering-proof-title">
  <div class="section-head"><h2 id="engineering-proof-title">{escape(title)}</h2>
  {link(label, FOUNDER + "engineering/#reproduction")}</div>
  <p class="section-lead">{escape(intro)}</p>
  <div class="entries">{cards}</div>
</section>"""



def render(lang):
    t = COPY[lang]
    labels = REFERENCE_LABELS[lang].split(" | ")
    highlights, capabilities = labels[:2]
    capabilities_labels = labels[2:6]
    feature_labels = labels[6:12]
    capabilities_details = labels[12:]
    repo_heading, supabase_detail, listing_status = PORTFOLIO_LABELS[lang]
    current = suffix(lang)
    url = HOST + SHOWCASE + current
    title = ("IMPERIAL Core | Ecosistema sovrano di IA" if lang == "it"
             else f"IMPERIAL Core | {t['hero1']} {t['hero2']}")
    direction = "rtl" if lang == "ar" else "ltr"
    desc = f"{t['intro']} Alexander Romaskevich · IMPERIAL Core."
    archived_lang = lang if lang in FOUNDER_LOCALES or lang == "de-CH" else "en"
    archived = LEGACY_REFERENCE + "technical/" + suffix(archived_lang)
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{code}" href="{HOST}{SHOWCASE}{suffix(code)}">'
        for code in LANGUAGES
    )
    language_links = "\n".join(
        link(name, SHOWCASE + suffix(code), "", False,
             f' lang="{code}" hreflang="{code}"' + (' aria-current="page"' if lang == code else ""))
        for code, name in LANGUAGES.items()
    )
    navigation = (
        (t["portfolio"], "official-projects"), (t["architecture"], "architecture"),
        (t["dubai"], "dubai-2027"), (t["founder"], "architect"),
    )
    nav = "".join(link(label, "#" + target, "", False) for label, target in navigation)
    principles = [
        ("HANTER", feature_labels[0], "gem"),
        (t["federation"], "", "stack-2"),
        (t["scope"], "", "cpu"),
        ("Zero Trust", "", "shield-check"),
        ("Audit Ledger", "", "database"),
        (capabilities_labels[1], "", "topology-star-3"),
    ]
    principle_items = "".join(
        f'<li>{icon(symbol)}<span>{escape(label)}'
        f'{f"<small>{escape(subtitle)}</small>" if subtitle else ""}</span></li>'
        for label, subtitle, symbol in principles
    )
    projects = [
        (name, f"{GIT}/{repo}{dest}", description)
        for (name, repo, dest), description in zip(FEATURED, FEATURE_TEXT[lang], strict=True)
    ]
    cards = []
    for (name, href, _), caption, symbol in zip(projects[:len(CARD_ICONS)], feature_labels, CARD_ICONS, strict=True):
        cid = name.lower().replace(" ", "-")
        cards.append(f"""<a class="product" id="{cid}" href="{href}">
<img src="{ART}{cid}.webp" width="590" height="442" alt="" loading="lazy" decoding="async">
<div class="product-copy">{icon(symbol)}<h3>{escape(name)}</h3><p>{escape(caption)}</p></div>
<span class="arrow">{icon("arrow-up-right")}</span></a>""")
    projects.extend(
        (name, f"{GIT}/{repo}", description)
        for (name, repo), description in zip(MORE, MORE_TEXT[lang].split(" | "), strict=True)
    )
    projects.extend((
        ("Supabase", GIT + "/Supabase", supabase_detail),
        (t["dubai"], CONTEST, t["dubaiIntro"]),
    ))
    repository_items = "\n".join(
        f'<li><a href="{href}"><strong>{escape(name)}{icon("arrow-up-right")}</strong>'
        f'<span>{escape(description)}</span></a></li>'
        for name, href, description in projects
    )
    landscapes = "\n".join(
        f'<img class="landscape-frame" src="{DUBAI}{scene}-800.webp" '
        f'srcset="{DUBAI}{scene}-800.webp 800w, {DUBAI}{scene}.webp 1536w" '
        'sizes="100vw" width="1536" height="864" loading="lazy" decoding="async" alt="">'
        for scene in LANDSCAPES
    )
    points = "".join(
        f'<li>{icon(symbol)}<span><strong>{escape(t[key])}</strong><small>{escape(detail)}</small></span></li>'
        for key, symbol, detail in (
            ("federation", "stack-2", capabilities_details[1]),
            ("scope", "gem", capabilities_details[0]),
            ("identity", "shield-check", capabilities_details[2]),
            ("audit", "database", "Audit Ledger"),
        )
    )
    capability_cards = "".join(
        f'<li>{icon(symbol)}<span><strong>{escape(label)}</strong><small>{escape(detail)}</small></span></li>'
        for label, detail, symbol in zip(
            capabilities_labels, capabilities_details,
            ("rocket", "topology-star-3", "shield-check", "gem"), strict=True
        )
    )
    candidate_links = {
        "business": CONTEST + "/blob/main/PRODUCT_BRIEF.md",
        "personal": CONTEST + "/blob/main/TRIPLE_CROWN.md#personal",
        "societal": CONTEST + "/blob/main/TRIPLE_CROWN.md#societal",
    }
    entries = "\n".join(f"""<article class="entry"><span class="track">{escape(t[track])}</span>
<h3>{escape(t[track + "Title"])}</h3><p>{escape(t[track + "Body"])}</p>
{link(t["evidence"], href)}</article>""" for track, href in candidate_links.items())
    token_cards = "\n".join(
        f'<li><a href="{GIT}/{repo}"><img src="{ART}tokens/{symbol.lower()}.webp" '
        f'width="{width}" height="{height}" loading="lazy" decoding="async" alt="">'
        f'<span><strong>{symbol}</strong>{icon("arrow-up-right")}</span></a></li>'
        for symbol, repo, width, height in TOKENS
    )
    crypto_links = " ".join(link(name, f"{GIT}/{repo}") for name, repo in (
        ("CRYPTO IMPERIAL", "CRYPTO-IMPERIAL-Ecosystem-Public"), ("LISA", "Lisa-"),
    ))
    founder_locale = lang.split("-")[0]
    founder_locale = founder_locale if founder_locale in FOUNDER_LOCALES else "en"
    founder_link = FOUNDER + suffix(founder_locale)
    graph = json.dumps(identity(lang, url, title, desc), ensure_ascii=False, separators=(",", ":"))
    biography_lang = "en" if lang == "en-US" else lang
    biography = BIOGRAPHIES.get(biography_lang)
    founder_statement = f'<p class="founder-statement">{escape(biography["statement"])}</p>' if biography else ""
    founder_intro = escape(biography["intro"] if biography else t["founderBody"])
    founder_story = render_biography(biography_lang) if biography else ""
    proof = render_proof(biography_lang, t["evidence"])
    proof_link = "#engineering-proof" if proof else FOUNDER + "engineering/#reproduction"
    language_badge = "EN-US" if lang == "en-US" else lang.split("-")[0].upper()
    t = {k: escape(v) for k, v in t.items()}
    return f"""<!doctype html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="author" content="Alexander Romaskevich">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0d0f12">
<link rel="canonical" href="{url}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{HOST}{SHOWCASE}">
<link rel="icon" href="{ASSETS}showcase-gem.svg" type="image/svg+xml">
<link rel="stylesheet" href="{ASSETS}showcase.css?v=5">
<link rel="stylesheet" href="{SHOWCASE_ASSETS}founder.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="IMPERIAL Core">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{HOST}{DUBAI}terrace.webp">
<meta property="og:image:width" content="1536">
<meta property="og:image:height" content="864">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{graph}</script>
<script defer src="{ASSETS}showcase.js?v=5"></script>
</head>
<body>
<a href="#main-content" class="skip">{t["skip"]}</a>
<header class="masthead" id="top"><div class="wrap">
<a class="brand" href="{SHOWCASE}{current}"><img src="{ASSETS}showcase-gem.svg" width="39" height="39" alt=""><span>IMPERIAL <em>Core</em></span></a>
<nav class="main-nav" aria-label="{t["nav"]}">{nav}</nav>
<div class="bar-actions">
<details class="language"><summary aria-label="{t["languages"]} · {LANGUAGES[lang]}"><bdi>{language_badge}</bdi></summary>
<div class="language-panel">{language_links}</div></details>
<details class="mobile-menu"><summary aria-label="{t["nav"]}">{icon("menu-2")}</summary><nav>{nav}{link(COPY[lang]["github"], GIT, "", False)}</nav></details>
{link(COPY[lang]["github"], GIT, "profile-link")}
</div>
</div></header>
<main id="main-content" tabindex="-1">
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-media" aria-hidden="true">
    <img src="{DUBAI}terrace.webp" srcset="{DUBAI}terrace-800.webp 800w, {DUBAI}terrace.webp 1536w" sizes="100vw" width="1536" height="864" alt="" fetchpriority="high">
  </div>
  <div class="wrap hero-inner"><h1 id="hero-title">{t["hero1"]} <span>{t["hero2"]}</span></h1>
    <p>{t["intro"]}</p>
    <div class="actions">{link(COPY[lang]["explore"], "#official-projects", "btn btn-gold")}
    {link(COPY[lang]["evidence"], proof_link, "btn btn-outline")}</div>
  </div>
</section>
<ul class="wrap principles" aria-label="{t["architecture"]}">{principle_items}</ul>
<section class="wrap section" id="official-projects">
  <div class="section-head"><h2>{t["portfolioTitle"].replace("IMPERIAL Core", "<em>IMPERIAL Core</em>")}</h2>{link(COPY[lang]["all"], "#all-projects")}</div>
  <div class="cards">{"".join(cards)}</div>
</section>
{proof}
<section class="wrap section" id="architecture">
  <div class="architecture">
  <figure class="architecture-art"><img src="{ART}architecture.webp" width="1160" height="580" alt="" loading="lazy" decoding="async"></figure>
  <div><p class="eyebrow">{escape(highlights)}</p><h2>{t["architectureTitle"]}</h2><p>{t["architectureBody"]}</p>
  <ul class="architecture-points">{points}</ul></div></div>
</section>
<section class="wrap section capabilities" id="capabilities">
  <div class="section-head"><h2>{escape(capabilities)}</h2></div>
  <ul class="capability-grid">{capability_cards}</ul>
</section>
<section class="landscape-catalogue" id="dubai-gallery" aria-labelledby="repository-heading">
  <div class="landscape-window" aria-hidden="true">{landscapes}</div>
  <div class="wrap section catalogue-content" id="all-projects">
    <div class="section-head"><h2 id="repository-heading">{escape(repo_heading)}</h2>{link("Template Studio", STUDIO)}</div>
    <p class="section-lead">{t["moreIntro"]}</p>
    <ul class="repository-grid">{repository_items}</ul>
    <p class="governance-boundaries"><bdi>AI Passport · Enterprise Skills · Guardian Core · Approval Gateway · Audit Ledger · Zero Trust · Owner Kill Switch · Public/Private Boundary · CRYPTO IMPERIAL Ecosystem Boundary</bdi></p>
  </div>
</section>
<section class="wrap section crypto" id="crypto-imperial" aria-labelledby="token-heading">
  <h2 id="token-heading">{t["cryptoTitle"]}</h2>
  <p class="section-lead">{t["cryptoBody"]}</p>
  <p class="listing-status">{escape(listing_status)}</p>
  <ul class="token-grid">{token_cards}</ul>
  <nav aria-label="{t["cryptoTitle"]}">{crypto_links}</nav>
</section>
<section class="dubai" id="dubai-2027"><div class="wrap section">
  <h2>{t["dubaiTitle"]}</h2><p class="section-lead">{t["dubaiIntro"]}</p>
  <div class="entries">{entries}</div>
  <div class="actions">{link(COPY[lang]["walkthrough"], FOUNDER + "dubai-2027/", "btn btn-gold")}
  {link(COPY[lang]["candidateEvidence"], CONTEST + "/blob/main/TRIPLE_CROWN.md", "btn btn-outline")}</div>
</div></section>
<section class="wrap section founder" id="architect">
  <figure class="portrait"><img src="{FOUNDER}assets/alexander-romaskevich-portrait.jpeg" srcset="{DUBAI}alexander-romaskevich.webp 900w, {FOUNDER}assets/alexander-romaskevich-portrait.jpeg 1122w" sizes="(max-width: 430px) 92vw, 400px" width="1122" height="1402" alt="Alexander Romaskevich" loading="lazy" decoding="async"></figure>
  <div class="founder-bio"><p class="founder-title">{t["founderTitle"]}</p><h2><bdi>Alexander Romaskevich</bdi></h2>
  <p class="founder-role">{escape(founder_role(lang))}</p>{founder_statement}
  <p class="founder-intro">{founder_intro}</p>
  <div class="actions">{link(COPY[lang]["founderProfile"], founder_link, "btn btn-outline", True, f' rel="author" hreflang="{founder_locale}"')}
  {link(COPY[lang]["engineering"], FOUNDER + "engineering/", "btn btn-outline")}</div></div>
  {founder_story}
</section>
<section class="diamond-finale" id="contact" aria-labelledby="finale-heading">
  <div class="diamond-backdrop" aria-hidden="true"></div>
  <div class="wrap finale-copy">
    <h2 id="finale-heading">{t["digitalQuote"]}</h2>
    <p>{t["digitalBody"]}</p>
    {link(COPY[lang]["contact"], "mailto:oromaskevic23@gmail.com", "btn btn-gold")}
  </div>
</section>
</main>
<footer class="site-footer"><div class="wrap">
<p><bdi>IMPERIAL Core</bdi> · {t["footerArchitecture"]}</p>
<nav aria-label="{t["reference"]}">{link(COPY[lang]["reference"], archived, extra=f' data-legacy hreflang="{archived_lang}"')}
{link(COPY[lang]["github"], GIT)} {link(COPY[lang]["evidence"], GIT + "/oromaskevic23-cmd/blob/main/docs/UNIFIED_ECOSYSTEM_EVIDENCE.md")}</nav>
</div></footer>
</body>
</html>
"""


def update_sitemap():
    path = ROOT / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    sitemap_base = HOST + SHOWCASE
    xml = re.sub(
        rf"(?m)^[ \t]*<url>\s*<loc>{re.escape(sitemap_base)}[^<]*</loc>[\s\S]*?</url>\n?",
        "",
        xml,
    )
    urls = {lang: sitemap_base + suffix(lang) for lang in LANGUAGES}
    alternates = {**urls, "x-default": sitemap_base}
    links = "".join(
        f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{url}"/>\n'
        for lang, url in alternates.items()
    )
    entries = "".join(
        f"  <url>\n    <loc>{url}</loc>\n{links}  </url>\n"
        for url in urls.values()
    )
    path.write_text(xml.replace("</urlset>", entries + "</urlset>"), encoding="utf-8")


def main():
    for lang in LANGUAGES:
        page = PUBLICATION / suffix(lang) / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(render(lang), encoding="utf-8")
    update_sitemap()
    files = sorted(path for path in PUBLICATION.rglob("*")
                   if path.is_file() and path.name != "publication-manifest.json")
    manifest = {
        "canonical_base": HOST + SHOWCASE,
        "pages": [HOST + SHOWCASE + suffix(lang) for lang in LANGUAGES],
        "files": [
            {"path": path.relative_to(PUBLICATION).as_posix(),
             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in files
        ],
    }
    (PUBLICATION / "publication-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
