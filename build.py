#!/usr/bin/env python3
"""Builds the static MyInviteQR marketing site.
Run:  python3 build.py        (writes every .html page, sitemap.xml, robots.txt, llms.txt, IMAGES.md)
Edit the constants below, the page content in content.py, then rebuild.
"""
import json, html, os, re, datetime
from content import PAGES, POSTS, HOME_FAQ, USE_CASES
import content_extra as X

# merge the second content layer
for _k, (_t, _d, _h) in X.TITLES.items():
    if _k in PAGES:
        PAGES[_k]["title"], PAGES[_k]["desc"] = _t, _d
        if _k in USE_CASES and _h:
            USE_CASES[_k]["h1"] = _h
        if _k == "home" and _h:
            PAGES[_k]["h1"] = _h
for _k, _kw in X.EXTRA_KEYWORDS.items():
    PAGES[_k]["keywords"] = _kw + ", " + PAGES[_k].get("keywords", "")
for _k, _e in X.EXTRAS.items():
    _f = _e.pop("faqs", [])
    USE_CASES[_k].update(_e)
    USE_CASES[_k]["faqs"] = USE_CASES[_k]["faqs"] + _f
USE_FILES = {"wedding": "digital-wedding-invitations.html", "birthday": "birthday-invitations.html", "baby": "baby-shower-invitations.html",
             "quince": "quinceanera-invitations.html", "corporate": "corporate-event-invitations.html", "qr": "qr-code-invitations.html", "rsvp": "online-rsvp.html"}
for _k, _n in X.NEW_PAGES.items():
    USE_FILES[_k] = _n.pop("file")
    PAGES[_k] = dict(title=_n.pop("title"), desc=_n.pop("desc"), keywords=_n.pop("keywords"))
    USE_CASES[_k] = _n
POSTS.update(X.MORE_POSTS)
# posts: put "Free" in every title
POSTS["how-to-write-wedding-invitation-wording"]["title"] = "Free Wedding Invitation Wording Examples and Tips | MyInviteQR"
POSTS["digital-vs-paper-invitations"]["title"] = "Digital vs Paper Invitations: Free Comparison | MyInviteQR"
POSTS["how-to-make-a-qr-code-invitation"]["title"] = "How to Make a Free QR Code Invitation | MyInviteQR"

SITE = "https://myinviteqr.com"            # canonical origin (no trailing slash)
APP = "https://app.myinviteqr.com"         # where the Flutter web app is hosted (sign in / create)
NAME = "MyInviteQR"
EMAIL = "support@myinviteqr.com"
TODAY = datetime.date.today().isoformat()
OG = SITE + "/assets/img/og-image.jpg"
ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = json.load(open(os.path.join(ROOT, "data/templates.json")))

IMAGES = []  # (path, w, h, alt, page) collected for IMAGES.md

# --------------------------------------------------------------------------- icons
_I = {
 "qr": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM20 14v.01M14 20h.01M17 20h4v-3"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 "sparkles": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 3v4M17 5h4M5 17v4M3 19h4"/>',
 "palette": '<circle cx="13.5" cy="6.5" r="1"/><circle cx="17.5" cy="10.5" r="1"/><circle cx="8.5" cy="7.5" r="1"/><circle cx="6.5" cy="12.5" r="1"/><path d="M12 22a10 10 0 1 1 10-10c0 3-2 4-4 4h-2a2 2 0 0 0-1.5 3.3A2 2 0 0 1 12 22z"/>',
 "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/>',
 "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
 "shield": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="m9 12 2 2 4-4"/>',
 "chart": '<path d="M3 3v18h18"/><path d="M7 15v3M12 9v9M17 5v13"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>',
 "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
 "check": '<path d="m5 12 5 5L20 7"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
 "cake": '<path d="M4 21h16v-8a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2z"/><path d="M4 16c2 2 4 2 8 0s6-2 8 0M12 11V8M12 4v.01"/>',
 "baby": '<circle cx="12" cy="12" r="10"/><path d="M8 14a5 5 0 0 0 8 0M9 9h.01M15 9h.01"/>',
 "grad": '<path d="M22 10 12 5 2 10l10 5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
 "brief": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>',
 "crown": '<path d="m2 8 5 4 5-8 5 8 5-4-2 12H4z"/>',
 "bell": '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M10.3 21a2 2 0 0 0 3.4 0"/>',
 "edit": '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
 "send": '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
 "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
 "layout": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>',
 "gift": '<rect x="3" y="8" width="18" height="4"/><path d="M12 8v13M19 12v9H5v-9M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
 "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>',
 "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "chev": '<path d="m6 9 6 6 6-6"/>',
 "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
 "leaf": '<path d="M11 20A7 7 0 0 1 4 13c0-6 6-9 16-9 0 10-3 16-9 16zM2 22c2-6 5-9 9-11"/>',
}


def ic(name, cls=""):
    return f'<svg class="ic {cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def esc(s):
    return html.escape(s, quote=True)


def img(src, w, h, alt, page="", cls="", eager=False):
    """Image with a soft gradient behind it until the real file exists. Registered for IMAGES.md."""
    IMAGES.append((src, w, h, alt, page))
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<figure class="ph {cls}" style="aspect-ratio:{w}/{h}"><img src="/{src}" width="{w}" height="{h}" '
            f'alt="{esc(alt)}" {load} onerror="this.remove()"></figure>')


def slug(n):
    return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")


# --------------------------------------------------------------------------- layout pieces
NAV_USE = [
    ("digital-wedding-invitations.html", "heart", "Wedding invitations", "Elegant, easy to share"),
    ("birthday-invitations.html", "cake", "Birthday invitations", "For kids and adults"),
    ("baby-shower-invitations.html", "baby", "Baby shower invitations", "Sweet and simple"),
    ("quinceanera-invitations.html", "crown", "Quinceañera invitations", "Sweet 15 and Sweet 16"),
    ("corporate-event-invitations.html", "brief", "Corporate event invitations", "Professional and branded"),
    ("graduation-invitations.html", "grad", "Graduation invitations", "High school and college"),
    ("anniversary-invitations.html", "heart", "Anniversary invitations", "Milestone celebrations"),
    ("gender-reveal-invitations.html", "sparkles", "Gender reveal invitations", "Boy or girl?"),
    ("holiday-party-invitations.html", "gift", "Holiday party invitations", "Family and office parties"),
]


def header(active):
    def cur(p):
        return ' aria-current="page"' if p == active else ""
    dd = "".join(
        f'<a href="/{u}"{cur(u)}>{ic(i)}<span>{t}<small>{s}</small></span></a>' for u, i, t, s in NAV_USE)
    mob = "".join(f'<a href="/{u}">{t}</a>' for u, i, t, s in NAV_USE)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container nav">
<a class="brand" href="/" aria-label="{NAME} home"><img src="/assets/img/logo-wordmark.png" alt="{NAME}" width="170" height="34"></a>
<nav class="nav-links" aria-label="Main">
<div class="dd"><button class="dd-btn" aria-expanded="false" aria-haspopup="true">Invitations {ic("chev")}</button><div class="dd-menu two">{dd}</div></div>
<a href="/templates.html"{cur("templates.html")}>Templates</a>
<a href="/free-invitation-maker.html"{cur("free-invitation-maker.html")}>Free maker</a>
<a href="/how-it-works.html"{cur("how-it-works.html")}>How it works</a>
<a href="/pricing.html"{cur("pricing.html")}>Pricing</a>
<a href="/blog/"{cur("blog/")}>Blog</a>
<a href="/faq.html"{cur("faq.html")}>FAQ</a>
</nav>
<div class="nav-cta"><a class="btn btn-outline btn-sm" href="{APP}">Log in</a><a class="btn btn-primary btn-sm" href="{APP}">Create invitation</a>
<button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">{ic("menu")}</button></div>
</div></header>
<div class="mobile-menu" id="mobile-menu">
<div class="grp">Invitations</div>{mob}
<div class="grp">Explore</div>
<a href="/templates.html">Templates</a><a href="/free-invitation-maker.html">Free invitation maker</a><a href="/how-it-works.html">How it works</a><a href="/qr-code-invitations.html">QR code invitations</a><a href="/save-the-date-invitations.html">Save the date</a><a href="/send-invitations-by-text.html">Send by text</a><a href="/online-rsvp.html">Online RSVP</a><a href="/pricing.html">Pricing</a><a href="/blog/">Blog</a><a href="/faq.html">FAQ</a><a href="{APP}">Log in</a>
</div>'''


def footer():
    use = "".join(f'<li><a href="/{u}">{t}</a></li>' for u, i, t, s in NAV_USE)
    return f'''<footer class="site-footer"><div class="container">
<div class="foot-grid">
<div class="foot-brand"><img src="/assets/img/logo-wordmark.png" alt="{NAME}" width="200" height="40" loading="lazy">
<p>Digital invitations with a QR code. Design it, share one link, and track every RSVP in real time. Made for weddings, birthdays, baby showers, quinceañeras and corporate events across the United States.</p></div>
<div><h4>Product</h4><ul><li><a href="/how-it-works.html">How it works</a></li><li><a href="/templates.html">Templates</a></li><li><a href="/pricing.html">Pricing</a></li><li><a href="/free-invitation-maker.html">Free invitation maker</a></li><li><a href="/qr-code-invitations.html">QR code invitations</a></li><li><a href="/online-rsvp.html">Online RSVP</a></li><li><a href="/save-the-date-invitations.html">Save the date</a></li><li><a href="/send-invitations-by-text.html">Send invitations by text</a></li></ul></div>
<div><h4>Invitations</h4><ul>{use}</ul></div>
<div><h4>Resources</h4><ul><li><a href="/blog/">Blog</a></li><li><a href="/feed.xml">RSS feed</a></li><li><a href="/faq.html">FAQ</a></li><li><a href="/contact.html">Contact</a></li><li><a href="{APP}">Log in</a></li></ul></div>
<div><h4>Legal</h4><ul><li><a href="/privacy.html">Privacy Policy</a></li><li><a href="/terms.html">Terms of Service</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
</div>
<div class="foot-bottom"><span>&copy; <span id="year">{datetime.date.today().year}</span> {NAME}. All rights reserved.</span><span>Payments processed securely by <a href="https://stripe.com" rel="noopener nofollow" target="_blank">Stripe</a>.</span></div>
</div></footer>
<div class="sticky-cta"><a class="btn btn-primary btn-lg" href="{APP}">Create your invitation {ic("arrow","ic-arrow")}</a></div>
<script src="/assets/js/main.js" defer></script>'''


def head(p):
    url = SITE + p["url"]
    title = p["title"]
    desc = p["desc"]
    kw = p.get("keywords", "")
    og_img = p.get("og") or (SITE + "/assets/img/og/" + p["ogkey"] + ".jpg" if p.get("ogkey") and os.path.exists(os.path.join(ROOT, "assets/img/og", p["ogkey"] + ".jpg")) else OG)
    typ = "article" if p.get("article") else "website"
    web = {"@context": "https://schema.org", "@type": "CollectionPage" if p["url"] in ("/blog/", "/templates.html") else ("AboutPage" if p["url"] == "/how-it-works.html" else "WebPage"),
           "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "en-US",
           "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#organization"},
           "primaryImageOfPage": {"@type": "ImageObject", "url": og_img, "width": 1200, "height": 675},
           "dateModified": TODAY, "potentialAction": {"@type": "ReadAction", "target": [url]},
           "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".lead"]}}
    schemas = base_schemas() + [web] + p.get("schema", [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>' for s in schemas)
    return f'''<!doctype html>
<html lang="en-US" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(kw)}">
<meta name="author" content="{NAME}">
<meta name="robots" content="{p.get("robots", "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")}">
<meta name="googlebot" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-US" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="language" content="English">
<meta name="geo.region" content="US">
<meta name="geo.placename" content="United States">
<meta name="distribution" content="global">
<meta name="rating" content="general">
<meta name="theme-color" content="#E94B6F">
<meta name="format-detection" content="telephone=no">
<meta name="application-name" content="{NAME}">
<meta name="apple-mobile-web-app-title" content="{NAME}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{typ}">
<meta property="og:title" content="{esc(p.get("og_title", title))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="675">
<meta property="og:image:alt" content="{esc(p.get("og_alt", "MyInviteQR digital invitation with a QR code shown on a phone"))}">
{('<meta property="article:published_time" content="%s"><meta property="article:modified_time" content="%s"><meta property="article:author" content="%s">' % (p["date"], p["date"], NAME)) if p.get("article") else ""}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p.get("og_title", title))}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/img/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="alternate" type="application/rss+xml" title="MyInviteQR Blog" href="/feed.xml">
<link rel="dns-prefetch" href="https://fonts.gstatic.com">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta property="og:image:secure_url" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500&family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500&family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{p.get("preload", "")}
{ld}
</head>'''


def base_schemas():
    return [
        {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#organization", "name": NAME,
         "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/logo.png", "width": 715, "height": 547},
         "image": OG, "email": EMAIL, "areaServed": {"@type": "Country", "name": "United States"},
         "description": "MyInviteQR creates digital invitations with a QR code and tracks RSVPs online.",
         "contactPoint": [{"@type": "ContactPoint", "contactType": "customer support", "email": EMAIL, "availableLanguage": ["English", "Spanish"], "areaServed": "US"}]},
        {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
         "inLanguage": "en-US", "publisher": {"@id": SITE + "/#organization"},
         "description": "Digital invitations with QR code, online RSVP and guest tracking."},
    ]


def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


# --------------------------------------------------------------------------- sections
def cta_band(title="Ready to send an invitation people will remember?", text="Pick a template, add your details and share one link. Design for free and pay only when you publish."):
    return f'''<section><div class="container"><div class="cta-band reveal">
<h2>{title}</h2><p>{text}</p>
<a class="btn btn-primary btn-lg" href="{APP}">Create your invitation {ic("arrow","ic-arrow")}</a>
<p class="cta-note">Designing is free. You pay one time, only when you publish. No subscription.</p></div></div></section>'''


def faq_block(faqs, title="Frequently asked questions", sub=""):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in faqs)
    return f'''<section id="faq"><div class="container narrow"><div class="section-head reveal"><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>
<div class="reveal">{items}</div></div></section>'''


def steps_block(title="Create your invitation in four simple steps", sub="No design skills, no printing, no app for your guests to download.", page=""):
    steps = [
        ("Create your event", "Choose the type of event, add the title, date, time and place. Everything saves automatically as a draft."),
        ("Pick a template", "Browse designer templates for every occasion and preview them on a phone before you decide."),
        ("Make it yours", "Change text, fonts and colors, drag photos where you want them and add your RSVP button and QR code."),
        ("Share and track", "Publish, then send one link or QR code by text, email or social media. Watch RSVPs arrive in real time."),
    ]
    h = "".join(f'<div class="step reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in steps)
    return f'''<section id="how"><div class="container"><div class="section-head reveal"><h2>{title}</h2><p>{sub}</p></div><div class="steps">{h}</div></div></section>'''


def features_block(title="Everything you need to invite, organize and celebrate", sub="One simple tool replaces paper cards, group texts and spreadsheets."):
    f = [
        ("qr", "QR code on every invitation", "Guests scan the code at your venue, on a save-the-date or on printed cards and land on your invitation instantly."),
        ("edit", "Free-form invitation editor", "Move, resize and rotate any text, photo or shape. Start from a template or build your own layout."),
        ("palette", "Over 130 color palettes", "Change one palette and the whole invitation recolors itself, always keeping the text readable."),
        ("users", "Online RSVP and guest list", "Guests reply yes, no or maybe with their party size. You see every answer in one clean dashboard."),
        ("chart", "Know who opened it", "See who viewed your invitation and who still needs a nudge, so you can follow up with the right people."),
        ("upload", "Import your guest list", "Upload a CSV or add guests one by one, with groups and a personal link for each guest."),
        ("phone", "Made for phones", "Guests open your invitation in the browser they already use. No app, no account, no friction."),
        ("zap", "Motion that feels premium", "Gentle animated details bring your invitation to life on every screen without slowing it down."),
    ]
    h = "".join(f'<div class="card reveal">{ic(i,"ic-lg")}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in f)
    return f'''<section class="section-soft" id="features"><div class="container"><div class="section-head reveal"><h2>{title}</h2><p>{sub}</p></div><div class="grid g4">{h}</div></div></section>'''


def occasions_block(title="Digital invitations for every occasion", sub="Find the perfect design for your celebration."):
    c = [
        ("digital-wedding-invitations.html", "heart", "Wedding", "Save-the-dates, ceremony details and RSVPs in one elegant link."),
        ("birthday-invitations.html", "cake", "Birthday", "Fun, colorful invitations for kids, teens and grown-ups."),
        ("baby-shower-invitations.html", "baby", "Baby shower", "Soft designs, gift details and a simple way to reply."),
        ("quinceanera-invitations.html", "crown", "Quinceañera", "A grand invitation for the celebration of a lifetime."),
        ("corporate-event-invitations.html", "brief", "Corporate", "Clean, branded invitations for launches, galas and team events."),
        ("qr-code-invitations.html", "qr", "QR code invitations", "Turn any invitation into a scannable code for print and screens."),
    ]
    h = "".join(f'<a class="card reveal" href="/{u}">{ic(i,"ic-lg")}<h3>{t}</h3><p>{d}</p><span class="more">Learn more {ic("arrow")}</span></a>' for u, i, t, d in c)
    return f'''<section id="occasions"><div class="container"><div class="section-head reveal"><h2>{title}</h2><p>{sub}</p></div><div class="grid g3">{h}</div></div></section>'''


def tpl_card(t, page=""):
    s = slug(t["name"])
    sw = "".join(f'<i style="background:{c}"></i>' for c in t["colors"][:3])
    cats = " ".join(t["themes"])
    return (f'<a class="tpl reveal" href="{APP}" data-cat="{cats}">'
            f'{img("assets/img/templates/" + s + ".jpg", 800, 1000, t["name"] + " digital invitation template", page)}'
            f'<h3>{esc(t["name"])}</h3><span>{t["style"].title()} style</span><div class="sw">{sw}</div></a>')


def templates_showcase(names=None, title="Designer templates you will actually want to send", sub="Fifty templates, from romantic garden arches to bold party posters. Every one is fully editable.", limit=8, link=True, page="home"):
    ts = [t for t in TEMPLATES if (names is None or t["name"] in names)][:limit]
    h = "".join(tpl_card(t, page) for t in ts)
    btn = f'<div style="text-align:center;margin-top:36px"><a class="btn btn-outline btn-lg" href="/templates.html">Browse all templates {ic("arrow")}</a></div>' if link else ""
    return f'''<section class="section-soft" id="templates"><div class="container"><div class="section-head reveal"><h2>{title}</h2><p>{sub}</p></div><div class="grid g4">{h}</div>{btn}</div></section>'''


def split(title, text, checks, image, side="", cta=True, rev=False, page=""):
    lis = "".join(f'<li>{ic("check")}<span>{c}</span></li>' for c in checks)
    src, w, h, alt = image
    btn = f'<a class="btn btn-primary" href="{APP}" style="margin-top:8px">Try it now {ic("arrow","ic-arrow")}</a>' if cta else ""
    return f'''<section><div class="container"><div class="split {"rev" if rev else ""}"><div class="reveal"><h2>{title}</h2><p>{text}</p><ul class="checks">{lis}</ul>{btn}</div><div class="reveal">{img(src, w, h, alt, page)}</div></div></div></section>'''


def compare_table():
    rows = [
        ("Setup time", "Minutes", "Days or weeks"),
        ("Cost per guest", "None. One flat price per event", "Printing plus postage for every card"),
        ("Corrections after sending", "Edit anytime, everyone sees the update", "Reprint and resend"),
        ("RSVP tracking", "Automatic and in real time", "Phone calls, texts and spreadsheets"),
        ("Reach", "One link, text, email or QR", "Mail only"),
        ("Guest count limit", "Up to 1,000 with Premium", "Limited by budget"),
        ("Environmental impact", "Paperless", "Paper, ink and shipping"),
    ]
    b = "".join(f'<tr><th scope="row">{a}</th><td class="yes">{b}</td><td class="no">{c}</td></tr>' for a, b, c in rows)
    return f'''<section id="compare"><div class="container narrow"><div class="section-head reveal"><h2>Digital invitations vs. paper invitations</h2><p>Save time and money, and make it easy for everyone to reply.</p></div>
<div class="table-wrap reveal"><table><thead><tr><th></th><th>MyInviteQR</th><th>Paper invitations</th></tr></thead><tbody>{b}</tbody></table></div></div></section>'''


def plans_block(title="Simple pricing. Pay once per event.", sub="Design for free. You only pay when you publish. No subscriptions, no hidden fees."):
    def li(items):
        return "".join(f'<li>{ic("check")}<span>{i}</span></li>' for i in items)
    ess = ["Downloadable QR code", "Online RSVP and guest management", "Up to 50 guests", "1 reminder", "Valid for 90 days from publication", "All 50 templates and the full editor"]
    pre = ["Everything in Essential", "Up to 1,000 guests", "Unlimited reminders", "Open analytics", "Custom link", "Individual link for each guest", "Shared photo album", "No MyInviteQR branding"]
    return f'''<section class="section-soft" id="pricing"><div class="container"><div class="section-head reveal"><h2>{title}</h2><p>{sub}</p></div>
<div class="plans">
<div class="plan reveal"><h3>Essential</h3><p>A simple event, done right.</p><div class="price">$9.99<small>one-time payment</small></div><ul>{li(ess)}</ul><a class="btn btn-outline btn-lg" style="width:100%" href="{APP}">Choose Essential</a></div>
<div class="plan pop reveal"><span class="badge">Most popular</span><h3>Premium</h3><p>More features for memorable events.</p><div class="price">$19.99<small>one-time payment</small></div><ul>{li(pre)}</ul><a class="btn btn-primary btn-lg" style="width:100%" href="{APP}">Choose Premium</a></div>
</div>
<p class="cta-note" style="text-align:center;margin-top:24px">Need more time? Add a 6-month extension for $6.99 to keep your invitation active longer. All prices in USD.</p></div></section>'''


def hero_home():
    return f'''<section class="hero"><div class="container hero-grid">
<div class="reveal in">
<span class="eyebrow"><span class="dot"></span>Digital invitations with QR code</span>
<h1>Design <em>free</em> digital invitations with a QR code, <span class="nw">sent in minutes.</span></h1>
<p class="lead">Design a stunning online invitation, share it with one link or a QR code, and watch your RSVPs arrive in real time. No printing, no postage, no app for your guests.</p>
<div class="hero-actions"><a class="btn btn-primary btn-lg" href="{APP}">Create your invitation {ic("arrow","ic-arrow")}</a><a class="btn btn-outline btn-lg" href="/templates.html">See templates</a></div>
<ul class="hero-points"><li>{ic("check")}Free to design and preview</li><li>{ic("check")}Pay once only to publish</li><li>{ic("check")}Works on any phone</li><li>{ic("check")}Real-time RSVP tracking</li></ul>
</div>
<div class="hero-art reveal in"><img class="hero-photo" src="/assets/img/hero-preview.jpg" width="1400" height="788" alt="A digital birthday invitation with a QR code shown on a phone" fetchpriority="high"></div>
</div></section>'''


def guide_block():
    links = [("digital-wedding-invitations.html", "Digital wedding invitations"), ("birthday-invitations.html", "Birthday invitations"), ("baby-shower-invitations.html", "Baby shower invitations"),
             ("quinceanera-invitations.html", "Quinceañera invitations"), ("corporate-event-invitations.html", "Corporate event invitations"), ("graduation-invitations.html", "Graduation invitations"),
             ("anniversary-invitations.html", "Anniversary invitations"), ("gender-reveal-invitations.html", "Gender reveal invitations"), ("holiday-party-invitations.html", "Holiday party invitations"),
             ("save-the-date-invitations.html", "Save the date"), ("qr-code-invitations.html", "QR code invitations"), ("online-rsvp.html", "Online RSVP"),
             ("send-invitations-by-text.html", "Send invitations by text"), ("free-invitation-maker.html", "Free invitation maker")]
    tl = "".join(f'<a href="/{u}">{t}</a>' for u, t in links)
    return f'''<section id="guide"><div class="container narrow prose reveal"><h2>What is a digital invitation with a QR code?</h2>
<p>A <strong>digital invitation</strong> is an online invitation you send as a link, text message or email instead of by mail. With MyInviteQR every digital invitation also includes a <strong>QR code</strong>: guests point their phone camera at it and your invitation opens instantly with the date, place, photos and an <strong>online RSVP</strong> button.</p>
<h3>Free to design, pay once to publish</h3>
<p>Designing your invitation is <strong>free</strong>. You can pick from 50 templates, edit every detail, upload photos, preview on a phone and save as many drafts as you like without paying. You choose a plan only when you are ready to publish and share: Essential is $9.99 and Premium is $19.99, one time per event, with no subscription.</p>
<h3>Why hosts in the United States are switching from paper</h3>
<p>Paper invitations mean design fees, printing, envelopes and postage, then weeks of waiting and calling guests for answers. A digital invitation is ready in minutes, costs the same for 20 guests or 200, updates instantly if plans change and collects every reply in one guest list. For weddings, birthdays, baby showers, quincea&ntilde;eras, graduations and corporate events, it is the faster, cheaper and easier way to invite.</p></div>
<div class="container" style="margin-top:32px"><div class="section-head reveal" style="margin-bottom:24px"><h2 style="font-size:1.6rem">Explore invitations by occasion and feature</h2></div><div class="topic-links reveal">{tl}</div></div></section>'''


def demo_block():
    qr = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" fill="#fff"/><g fill="#2B2D42"><rect x="4" y="4" width="18" height="18"/><rect x="42" y="4" width="18" height="18"/><rect x="4" y="42" width="18" height="18"/><rect x="8" y="8" width="10" height="10" fill="#fff"/><rect x="46" y="8" width="10" height="10" fill="#fff"/><rect x="8" y="46" width="10" height="10" fill="#fff"/><rect x="11" y="11" width="4" height="4"/><rect x="49" y="11" width="4" height="4"/><rect x="11" y="49" width="4" height="4"/><rect x="28" y="6" width="6" height="6"/><rect x="28" y="20" width="10" height="6"/><rect x="6" y="28" width="8" height="6"/><rect x="20" y="30" width="8" height="8"/><rect x="34" y="30" width="6" height="10"/><rect x="46" y="28" width="12" height="6"/><rect x="28" y="44" width="8" height="8"/><rect x="42" y="42" width="6" height="6"/><rect x="52" y="44" width="8" height="10"/><rect x="40" y="54" width="10" height="6"/></g></svg>'
    return f'''<section style="padding-top:24px"><div class="container"><div class="demo reveal">
<div><span class="eyebrow">Try it right now</span><h2>See your invitation come to life</h2><p>Type a name and pick a date. Your invitation updates instantly. That is how easy it is.</p>
<form id="demo-form" autocomplete="off"><div class="field"><label for="demo-kind">Occasion</label><select id="demo-kind"><option value="birthday">Birthday</option><option value="wedding">Wedding</option><option value="baby">Baby shower</option><option value="quince">Quincea&ntilde;era</option><option value="corporate">Corporate event</option></select></div>
<div class="field"><label for="demo-name">Name or title</label><input id="demo-name" type="text" maxlength="28" placeholder="Sofia" value="Sofia"></div>
<div class="field"><label for="demo-date">Date</label><input id="demo-date" type="date"></div>
<div class="field"><label for="demo-place">Place (optional)</label><input id="demo-place" type="text" maxlength="30" placeholder="Garden Las Flores"></div></form>
<p style="margin:18px 0 0"><a class="btn btn-primary" href="{APP}">Make it real {ic("arrow","ic-arrow")}</a></p></div>
<div class="phone theme-pink" id="demo-phone" aria-label="Live invitation preview"><div class="card-prev"><small id="pv-kicker">Birthday of</small><span class="title" id="pv-title">Sofia</span><strong>you&rsquo;re invited!</strong><span class="when" id="pv-when">Saturday, Oct 19</span><span class="rsvp">Confirm attendance</span>{qr}</div></div>
</div></div></section>'''


def strip_block():
    return '''<div class="container"><div class="strip reveal"><div><b>50</b><span>designer templates</span></div><div><b>1,000</b><span>guests with Premium</span></div><div><b>$9.99</b><span>one-time, from</span></div><div><b>0</b><span>apps for guests to install</span></div></div></div>'''


# --------------------------------------------------------------------------- page builders
def crumbs(items):
    parts = []
    for i, (n, u) in enumerate(items):
        parts.append(f'<a href="{u}">{n}</a>' if i < len(items) - 1 else f"<span>{n}</span>")
    return f'<nav class="crumbs" aria-label="Breadcrumb">{" / ".join(parts)}</nav>'


def page_hero(h1, lead, bc, cta=True, key=None):
    free = f'<p class="free-badge">{ic("check")} {X.FREE_NOTE}</p>' if key else ""
    btn = f'<div class="hero-actions" style="justify-content:center"><a class="btn btn-primary btn-lg" href="{APP}">Create your invitation {ic("arrow","ic-arrow")}</a><a class="btn btn-outline btn-lg" href="/pricing.html">See pricing</a></div>' if cta else ""
    return f'''<section class="page-hero"><div class="container narrow">{crumbs(bc)}<h1>{h1}</h1><p class="lead">{lead}</p>{btn}{free}</div></section>'''


def wrap(p, body, active=""):
    return f'''{head(p)}
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


def build_home():
    p = dict(PAGES["home"], url="/", ogkey="home")
    p["preload"] = '<link rel="preload" as="image" href="/assets/img/hero-preview.jpg">'
    app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "@id": SITE + "/#app", "name": NAME,
           "applicationCategory": "LifestyleApplication", "operatingSystem": "Web, iOS, Android (browser)",
           "url": SITE + "/", "image": OG, "inLanguage": "en-US",
           "description": "Create digital invitations with a QR code, share them with one link and track RSVPs online.",
           "featureList": ["Digital invitation templates", "QR code for every invitation", "Online RSVP", "Guest list import (CSV)", "Open tracking and analytics", "Free-form invitation editor", "Photo uploads", "Custom color palettes"],
           "offers": {"@type": "AggregateOffer", "priceCurrency": "USD", "lowPrice": "9.99", "highPrice": "19.99", "offerCount": "2",
                      "offers": [
                          {"@type": "Offer", "name": "Essential", "price": "9.99", "priceCurrency": "USD", "url": SITE + "/pricing.html", "availability": "https://schema.org/InStock"},
                          {"@type": "Offer", "name": "Premium", "price": "19.99", "priceCurrency": "USD", "url": SITE + "/pricing.html", "availability": "https://schema.org/InStock"}]},
           "publisher": {"@id": SITE + "/#organization"}}
    p["schema"] = [app, faq_schema(HOME_FAQ)]
    body = (hero_home() + strip_block() + demo_block() + steps_block(page="home") + features_block() + occasions_block()
            + templates_showcase(names=["Garden Romance", "Balloon Bash", "Golden Arch", "Rose Polaroids", "Starry Night", "Bento Bloom", "Poster Bold", "Boho Arch"])
            + split("Put a QR code on everything", "Every invitation comes with its own QR code. Add it to a printed save-the-date, a welcome sign, a menu or a screen at the venue and guests can open your invitation with one scan.",
                    ["Download your QR code as an image", "Works with any phone camera", "Perfect for printed cards and signs", "The link never expires while your event is active"],
                    ("assets/img/qr-code-invitation.jpg", 900, 700, "Guest scanning a QR code invitation with a smartphone"), page="home")
            + split("Track every RSVP without chasing anyone", "Guests reply in seconds from their phone. You see who is coming, who declined and who has not answered yet, and you know exactly who opened your invitation.",
                    ["Yes, no and maybe answers with party size", "See who viewed the invitation", "Groups and individual links for each guest", "Export your guest list to CSV"],
                    ("assets/img/rsvp-dashboard.jpg", 900, 700, "MyInviteQR guest list and RSVP dashboard"), rev=True, page="home")
            + compare_table() + plans_block() + guide_block() + faq_block(HOME_FAQ) + cta_band())
    write("index.html", wrap(p, body, "/"))


def build_simple(key, out, body_fn, bc, active=""):
    p = dict(PAGES[key])
    p["ogkey"] = key
    p["url"] = "/" + out
    items = [("Home", "/")] + bc
    p["schema"] = p.get("schema", []) + [breadcrumb([(n, u) for n, u in items])]
    body, extra = body_fn(p, items)
    p["schema"] += extra
    write(out, wrap(p, body, active or out))


def b_howitworks(p, items):
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": "How to create a digital invitation with a QR code",
             "description": "Create, customize and share a digital invitation online in four steps.", "totalTime": "PT10M",
             "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "9.99"},
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": SITE + "/how-it-works.html#step-" + str(i + 1)} for i, (n, t) in enumerate([
                 ("Create your event", "Choose the event type and add the title, date, time and location."),
                 ("Choose a template", "Pick one of 50 designer templates and preview it on a phone."),
                 ("Customize your invitation", "Edit text, fonts, colors and photos, and add your RSVP button and QR code."),
                 ("Add guests and publish", "Import or add your guests, choose a plan and publish. Share your link or QR code."),
             ])]}
    det = [
        ("Create your event", "Start with the basics: the type of event (wedding, birthday, baby shower, quinceañera, corporate and more), a title, the date and time, and the venue. We use your event type to recommend the best templates. Your work saves automatically as a draft, so you can leave and come back anytime."),
        ("Choose a template", "Browse fifty designer templates filtered by style and color. Every card previews your own event name and date, and a phone preview shows exactly how guests will see it. Change your mind? Switch templates without losing your details."),
        ("Customize your invitation", "Use the free-form editor to move, resize and rotate anything. Upload photos, pick from over 130 color palettes, choose from dozens of fonts, add decorations and drop in your RSVP button and QR code. Undo and redo are always one click away."),
        ("Add guests and publish", "Add guests manually or import a CSV. Choose Essential or Premium, pay securely with Stripe and your invitation goes live instantly. Share the link by text, email or social media, or print the QR code."),
    ]
    blocks = ""
    for i, (t, d) in enumerate(det):
        rev = i % 2 == 1
        im = img(f"assets/img/how-step-{i+1}.jpg", 900, 700, f"Step {i+1}: {t} in MyInviteQR", "how-it-works")
        blocks += f'''<section id="step-{i+1}"><div class="container"><div class="split {"rev" if rev else ""}"><div class="reveal"><span class="eyebrow">Step {i+1}</span><h2>{t}</h2><p>{d}</p></div><div class="reveal">{im}</div></div></div></section>'''
    body = page_hero("Free digital invitation maker: how it works", "From idea to a shared invitation in about ten minutes. Free to design, and you pay once only when you publish.", items, key="how") + blocks + features_block("Made to be easy for you and your guests", "The details that make it feel effortless.") + faq_block(HOME_FAQ[:5]) + cta_band()
    return body, [howto, faq_schema(HOME_FAQ[:5])]


def b_pricing(p, items):
    faqs = [
        ("How much do MyInviteQR digital invitations cost?", "Essential is $9.99 and Premium is $19.99 per event, paid once. There is no subscription. Designing your invitation is free; you only pay when you publish."),
        ("What is the difference between Essential and Premium?", "Essential includes up to 50 guests, a downloadable QR code, RSVP management, 1 reminder and 90 days of validity. Premium adds up to 1,000 guests, unlimited reminders, open analytics, a custom link, individual links for each guest, a shared photo album and no MyInviteQR branding."),
        ("Can I extend my invitation after 90 days?", "Yes. A 6-month extension costs $6.99 and keeps your invitation active longer. You can add it when you publish or later from your event page."),
        ("Is there a monthly fee?", "No. Every plan is a one-time payment for one event."),
        ("Which payment methods do you accept?", "Payments are processed securely by Stripe. You can pay with major credit and debit cards."),
    ]
    prod = [{"@context": "https://schema.org", "@type": "Product", "name": f"{NAME} {n}", "description": d, "image": OG, "brand": {"@type": "Brand", "name": NAME},
             "offers": {"@type": "Offer", "price": pr, "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": SITE + "/pricing.html", "priceValidUntil": "2027-12-31",
                        "shippingDetails": None}} for n, pr, d in [("Essential", "9.99", "Digital invitation with QR code for one event. Up to 50 guests, RSVP management and 90 days of validity."), ("Premium", "19.99", "Digital invitation with QR code for one event. Up to 1,000 guests, unlimited reminders, analytics, custom link and no branding.")]]
    for pr in prod:
        pr["offers"].pop("shippingDetails")
    body = (page_hero("Design free, pay once to publish", "One price per event and no subscription. Build and preview your invitation for free, then pick a plan when you are ready to share it.", items, cta=False)
            + plans_block(title="Choose your plan", sub="Every plan includes the full editor, all 50 templates, a QR code and online RSVP.")
            + compare_features() + faq_block(faqs, "Pricing questions") + cta_band())
    return body, prod + [faq_schema(faqs)]


def compare_features():
    rows = [("Templates and full editor", "Yes", "Yes"), ("Guests", "Up to 50", "Up to 1,000"), ("QR code", "Yes", "Yes"), ("Online RSVP", "Yes", "Yes"), ("Reminders", "1", "Unlimited"),
            ("Validity", "90 days", "90 days"), ("Open analytics", "No", "Yes"), ("Custom link", "No", "Yes"), ("Individual link per guest", "No", "Yes"), ("Shared photo album", "No", "Yes"),
            ("Co-hosts", "No", "Up to 3"), ("MyInviteQR branding removed", "No", "Yes"), ("Price", "$9.99", "$19.99")]
    b = "".join(f'<tr><th scope="row">{a}</th><td class="{"yes" if x not in ("No",) else "no"}">{x}</td><td class="yes">{y}</td></tr>' for a, x, y in rows)
    return f'''<section><div class="container narrow"><div class="section-head reveal"><h2>Compare plans</h2></div><div class="table-wrap reveal"><table><thead><tr><th>Feature</th><th>Essential</th><th>Premium</th></tr></thead><tbody>{b}</tbody></table></div></div></section>'''


def b_templates(p, items):
    cats = [("all", "All"), ("wedding", "Wedding"), ("birthday", "Birthday"), ("baby_shower", "Baby shower"), ("quinceanera", "Quinceañera"), ("corporate", "Corporate"),
            ("anniversary", "Anniversary"), ("graduation", "Graduation"), ("gender_reveal", "Gender reveal"), ("dinner_gathering", "Dinner"), ("trip", "Trip")]
    chips = "".join(f'<button class="chip" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in cats)
    grid = "".join(tpl_card(t, "templates") for t in TEMPLATES)
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "name": "Digital invitation templates", "numberOfItems": len(TEMPLATES),
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t["name"], "url": SITE + "/templates.html"} for i, t in enumerate(TEMPLATES)]}
    body = (page_hero("50 free digital invitation templates", "Fifty designer templates for weddings, birthdays, baby showers, quinceañeras and more. Pick one, then make it completely yours.", items, key="templates")
            + f'<section style="padding-top:24px"><div class="container"><div class="filters" role="group" aria-label="Filter templates">{chips}</div><div class="grid g4">{grid}</div></div></section>'
            + features_block("Every template is fully editable", "Change anything you like.") + cta_band())
    return body, [itemlist]


RELATED = {
    "wedding": ["savedate", "rsvp", "qr", "anniversary"], "birthday": ["text", "rsvp", "baby", "maker"], "baby": ["gender", "birthday", "text", "rsvp"],
    "quince": ["wedding", "savedate", "rsvp", "qr"], "corporate": ["holiday", "rsvp", "qr", "maker"], "qr": ["wedding", "birthday", "rsvp", "maker"],
    "rsvp": ["qr", "text", "wedding", "corporate"], "graduation": ["birthday", "text", "rsvp", "qr"], "anniversary": ["wedding", "savedate", "rsvp", "text"],
    "gender": ["baby", "birthday", "text", "rsvp"], "holiday": ["corporate", "birthday", "rsvp", "text"], "maker": ["wedding", "birthday", "qr", "rsvp"],
    "savedate": ["wedding", "rsvp", "qr", "text"], "text": ["birthday", "wedding", "rsvp", "qr"],
}


def related_block(key):
    cards = "".join(
        f'<a class="card reveal" href="/{USE_FILES[k]}" title="{esc(USE_CASES[k]["h1"])}"><h3>{USE_CASES[k]["crumb"]}</h3><p>{esc(PAGES[k]["desc"][:118].rsplit(" ", 1)[0])}...</p><span class="more">Explore {ic("arrow")}</span></a>'
        for k in RELATED.get(key, []))
    return f'''<section class="section-soft"><div class="container"><div class="section-head reveal"><h2>Keep exploring</h2><p>More ways to invite, organize and celebrate.</p></div><div class="grid g4">{cards}</div></div></section>'''


def tips_block(u):
    lis = "".join(f"<li>{t}</li>" for t in u["tips"])
    return f'''<section class="section-soft"><div class="container narrow prose reveal"><h2>{u["tips_title"]}</h2><ul>{lis}</ul></div></section>'''


def what_block(u):
    ps = "".join(f"<p>{t}</p>" for t in u["what"])
    return f'''<section><div class="container narrow prose reveal"><h2>{u["what_title"]}</h2>{ps}<p class="meta">{X.FREE_NOTE}</p></div></section>'''


def b_usecase(key):
    def fn(p, items):
        u = USE_CASES[key]
        why = "".join(f'<div class="card reveal">{ic(i,"ic-lg")}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in u["why"])
        wording = "".join(f"<blockquote>{w}</blockquote>" for w in u["wording"])
        body = (page_hero(u["h1"], u["lead"], items, key=key)
                + what_block(u)
                + f'<section class="section-soft"><div class="container"><div class="section-head reveal"><h2>{u["why_title"]}</h2><p>{u["why_sub"]}</p></div><div class="grid g3">{why}</div></div></section>'
                + steps_block(u["steps_title"], "Simple enough to finish in one sitting.")
                + templates_showcase(names=u.get("templates"), title=u["tpl_title"], sub=u["tpl_sub"], limit=4, page=key)
                + features_block(f'Everything you need for your {u["name"].lower()} invitation', "One tool for the design, the link, the QR code and the guest list.")
                + tips_block(u)
                + f'<section><div class="container narrow prose reveal"><h2>{u["wording_title"]}</h2><p>{u["wording_intro"]}</p>{wording}</div></section>'
                + split(u["split_title"], u["split_text"], u["split_checks"], (f"assets/img/{key}-feature.jpg", 900, 700, u["split_alt"]), page=key)
                + related_block(key)
                + faq_block(u["faqs"], f'{u["name"]} invitation questions') + cta_band(u["cta_title"], u["cta_text"]))
        howto = {"@context": "https://schema.org", "@type": "HowTo", "name": f'How to create a {u["name"].lower()} invitation online',
                 "description": u["lead"], "totalTime": "PT10M", "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": "0"},
                 "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate([
                     ("Create your event", "Choose the event type and add the title, date, time and place."),
                     ("Pick a template", "Browse designer templates and preview them on a phone."),
                     ("Make it yours", "Edit text, fonts, colors and photos, then add your RSVP button and QR code."),
                     ("Share and track", "Publish, share the link or QR code and watch RSVPs arrive in real time.")])]}
        prod = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": f'{NAME} {u["crumb"]}', "applicationCategory": "LifestyleApplication",
                "operatingSystem": "Web", "url": SITE + "/" + USE_FILES[key], "description": PAGES[key]["desc"], "image": SITE + f"/assets/img/{key}-feature.jpg",
                "offers": {"@type": "AggregateOffer", "priceCurrency": "USD", "lowPrice": "9.99", "highPrice": "19.99", "offerCount": "2"}}
        return body, [faq_schema(u["faqs"]), howto, prod]
    return fn


def b_faq(p, items):
    allf = HOME_FAQ + [
        ("Do my guests need an account or an app?", "No. Guests open your invitation in the web browser on their phone or computer and reply without creating an account."),
        ("Can I edit my invitation after I send it?", "Yes. Any change you make appears for everyone right away, because guests always see the latest version at the same link."),
        ("How do I log in?", "Enter your email and we send you an 8-digit code. There is no password to remember."),
        ("What languages are supported?", "You can create invitations in English and Spanish, and the templates work with any text you write."),
        ("How many photos can I upload?", "You can upload as many photos as your design needs. Each photo can be up to 5 MB in JPG, PNG, WebP or GIF format."),
    ]
    body = page_hero("Frequently asked questions", "Everything you want to know about digital invitations, QR codes and RSVPs.", items, cta=False) + faq_block(allf, "Your questions, answered") + cta_band()
    return body, [faq_schema(allf)]


def b_contact(p, items):
    body = page_hero("Contact us", "Questions about your invitation, your order or how MyInviteQR works? We are happy to help.", items, cta=False) + f'''<section style="padding-top:0"><div class="container narrow"><div class="grid g2">
<div class="card reveal">{ic("mail","ic-lg")}<h3>Email support</h3><p>Write to us at <a href="mailto:{EMAIL}">{EMAIL}</a>. We reply within one business day.</p></div>
<div class="card reveal">{ic("sparkles","ic-lg")}<h3>In your account</h3><p>Already have an invitation? Open the Help menu inside the app to send us a message about your event.</p><a class="more" href="{APP}">Open the app {ic("arrow")}</a></div></div></div></section>'''
    return body, []


def b_legal(kind):
    def fn(p, items):
        body = page_hero(p["h1"], p["lead"], items, cta=False) + f'<section style="padding-top:0"><div class="container narrow prose">{LEGAL[kind]}</div></section>'
        return body, []
    return fn


LEGAL = {
    "privacy": f'''<p class="meta">Last updated: {TODAY}</p>
<h2>What we collect</h2><ul><li><strong>Account data:</strong> your email address and, optionally, your name.</li><li><strong>Event data:</strong> the events, invitations and photos you create, and the guest details you add (name, email, phone, group).</li><li><strong>Guest responses:</strong> RSVP answers and messages guests send through your invitation.</li><li><strong>Usage data:</strong> basic analytics such as when an invitation is opened.</li><li><strong>Payment data:</strong> payments are handled by Stripe. We never see or store your full card number.</li></ul>
<h2>How we use it</h2><p>We use your data to provide the service, show RSVPs, send sign-in codes and support messages, process payments and improve the product. We do not sell your personal information.</p>
<h2>Sharing</h2><p>We share data only with service providers that help us run MyInviteQR (hosting, email delivery, payments) and when required by law.</p>
<h2>Your choices</h2><p>You can edit or delete your events and guests at any time from the app. To request a copy or deletion of your data, email <a href="mailto:{EMAIL}">{EMAIL}</a>. California residents can exercise their CCPA rights through the same address.</p>
<h2>Children</h2><p>MyInviteQR is intended for adults. We do not knowingly collect data from children under 13.</p>
<h2>Contact</h2><p>Questions about this policy: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''',
    "terms": f'''<p class="meta">Last updated: {TODAY}</p>
<h2>The service</h2><p>MyInviteQR lets you design digital invitations, share them by link or QR code and collect RSVPs. By using the service you agree to these terms.</p>
<h2>Your account</h2><p>You are responsible for the events and guest information you add and for having the right to share it. Do not upload unlawful, hateful or infringing content.</p>
<h2>Payments and validity</h2><p>Each plan is a one-time payment for a single event, in US dollars, processed by Stripe. Your invitation stays active for the validity period of your plan and can be extended for an additional fee. Prices may change for future purchases.</p>
<h2>Content</h2><p>You keep ownership of the content you upload. You grant us a license to host and display it so the service works. We may remove content that violates these terms.</p>
<h2>Availability</h2><p>We work hard to keep MyInviteQR available but do not guarantee uninterrupted service.</p>
<h2>Liability</h2><p>To the extent permitted by law, MyInviteQR is provided &ldquo;as is&rdquo; and our liability is limited to the amount you paid for the affected event.</p>
<h2>Contact</h2><p>Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''',
}


def build_blog():
    cards = "".join(
        f'<a class="card post-card reveal" href="/blog/{s}.html">{img(f"assets/img/blog/{s}.jpg", 1200, 630, po["title"], "blog", "")}<h3 style="margin-top:16px">{esc(po["h1"])}</h3><p>{esc(po["desc"])}</p><span class="meta">{po["date_h"]} &middot; {po["read"]} min read</span></a>'
        for s, po in POSTS.items())
    p = dict(PAGES["blog"], url="/blog/", ogkey="blog")
    items = [("Home", "/"), ("Blog", "/blog/")]
    blog_ld = {"@context": "https://schema.org", "@type": "Blog", "name": f"{NAME} Blog", "url": SITE + "/blog/", "inLanguage": "en-US", "publisher": {"@id": SITE + "/#organization"}}
    p["schema"] = [breadcrumb(items), blog_ld]
    body = page_hero("Invitation ideas and guides", "Wording ideas, etiquette and step-by-step guides to help you plan the perfect event.", items, cta=False) + f'<section style="padding-top:0"><div class="container"><div class="grid g3">{cards}</div></div></section>' + cta_band()
    write("blog/index.html", wrap(p, body, "blog/"))
    for s, po in POSTS.items():
        pp = dict(po, url=f"/blog/{s}.html", article=True, og_title=po["title"], ogkey="blog-" + s)
        items2 = [("Home", "/"), ("Blog", "/blog/"), (po["h1"], f"/blog/{s}.html")]
        art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": po["h1"], "description": po["desc"], "inLanguage": "en-US",
               "datePublished": po["date"], "dateModified": po["date"], "mainEntityOfPage": SITE + f"/blog/{s}.html",
               "image": SITE + f"/assets/img/blog/{s}.jpg", "author": {"@type": "Organization", "name": NAME, "url": SITE + "/"},
               "publisher": {"@id": SITE + "/#organization"}}
        pp["schema"] = [art, breadcrumb(items2)]
        body = (f'<section class="page-hero" style="padding-bottom:12px"><div class="container narrow">{crumbs(items2)}<h1>{esc(po["h1"])}</h1><p class="meta">{po["date_h"]} &middot; {po["read"]} min read</p></div></section>'
                f'<section style="padding-top:12px"><div class="container narrow">{img(f"assets/img/blog/{s}.jpg", 1200, 630, po["h1"], "blog", "", True)}<article class="prose" style="margin-top:32px">{po["body"]}</article></div></section>' + cta_band())
        write(f"blog/{s}.html", wrap(pp, body, "blog/"))


def build_404():
    p = dict(PAGES["404"], url="/404.html")
    body = f'<section class="page-hero"><div class="container narrow"><h1>Page not found</h1><p class="lead">The page you are looking for moved or does not exist. Let&rsquo;s get you back to creating something beautiful.</p><div class="hero-actions" style="justify-content:center"><a class="btn btn-primary btn-lg" href="/">Go to the home page</a><a class="btn btn-outline btn-lg" href="/templates.html">Browse templates</a></div></div></section>'
    write("404.html", wrap(p, body))


def page_images(u):
    """Images of a built page, for the sitemap (logos and icons are skipped)."""
    f = "index.html" if u == "/" else (u.lstrip("/") + "index.html" if u.endswith("/") else u.lstrip("/"))
    try:
        h = open(os.path.join(ROOT, f), encoding="utf-8").read()
    except OSError:
        return []
    out = []
    for m in re.finditer(r'<img src="/(assets/img/[^"]+)"[^>]*alt="([^"]*)"', h):
        if any(k in m.group(1) for k in ("logo", "favicon", "icon")):
            continue
        if m.group(1) not in [o[0] for o in out]:
            out.append((m.group(1), html.unescape(m.group(2))))
    return out


def build_extras(urls):
    global IMG_BY_URL
    IMG_BY_URL = {u: page_images(u) for u, _, _ in urls}
    # sitemap
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u, pr, cf in urls:
        loc = SITE + u
        sm.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n    <xhtml:link rel="alternate" hreflang="en-US" href="{loc}"/>')
        for im in IMG_BY_URL.get(u, [])[:6]:
            sm.append(f'    <image:image>\n      <image:loc>{SITE}/{im[0]}</image:loc>\n      <image:title>{html.escape(im[1])}</image:title>\n    </image:image>')
        sm.append("  </url>")
    sm.append("</urlset>\n")
    write("sitemap.xml", "\n".join(sm))
    # RSS feed for the blog
    items = "".join(
        f"<item><title>{html.escape(po['h1'])}</title><link>{SITE}/blog/{k}.html</link><guid isPermaLink=\"true\">{SITE}/blog/{k}.html</guid>"
        f"<pubDate>Sun, 20 Sep 2026 09:00:00 GMT</pubDate><description>{html.escape(po['desc'])}</description></item>" for k, po in POSTS.items())
    write("feed.xml", f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>{NAME} Blog</title><link>{SITE}/blog/</link><description>Invitation wording ideas, etiquette and guides.</description><language>en-us</language><atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>{items}</channel></rss>
''')
    # robots
    write("robots.txt", f"""# {NAME}: https://myinviteqr.com
User-agent: *
Allow: /
Disallow: /404.html
Disallow: /*?utm_
Disallow: /*?fbclid=

# AI and search crawlers are welcome to read the public pages
User-agent: GPTBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /

Sitemap: {SITE}/sitemap.xml
Host: {SITE}
""")
    write("site.webmanifest", json.dumps({"name": NAME, "short_name": NAME, "description": "Digital invitations with QR code", "start_url": "/", "display": "standalone",
                                          "background_color": "#ffffff", "theme_color": "#E94B6F", "lang": "en-US",
                                          "icons": [{"src": "/assets/img/favicon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/favicon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    write("llms.txt", f"""# {NAME}

> {NAME} is a web app for creating digital invitations with a QR code, sharing them by link and tracking RSVPs online. It serves customers in the United States.

## Key pages
- [Home]({SITE}/): overview and live demo
- [How it works]({SITE}/how-it-works.html): four steps from event to shared invitation
- [Templates]({SITE}/templates.html): fifty designer invitation templates
- [Pricing]({SITE}/pricing.html): Essential $9.99, Premium $19.99 (one-time, USD), 6-month extension $6.99
- [QR code invitations]({SITE}/qr-code-invitations.html)
- [Online RSVP]({SITE}/online-rsvp.html)
- [FAQ]({SITE}/faq.html)

## Facts
- Designing is free; payment happens once per event when publishing (Stripe).
- Essential: up to 50 guests, 90 days. Premium: up to 1,000 guests, unlimited reminders, analytics, custom link, no branding.
- Guests need no account or app.
""")
    write("_headers", """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/sitemap.xml
  Content-Type: application/xml; charset=utf-8
""")
    write("_redirects", """/index.html / 301
/home / 301
/wedding-invitations /digital-wedding-invitations 301
/birthday /birthday-invitations 301
/blog/index.html /blog/ 301
""")
    # image checklist
    seen = {}
    for src, w, h, alt, pg in IMAGES:
        seen.setdefault(src, (w, h, alt, pg))
    lines = ["# Image inventory", "", "Every slot below is filled by `tools/make_images.py` (feature scenes, templates, OG images) or by the real app screenshots. Replace any file with your own artwork at the same path and size.", "", "| Path | Size | Used on | What to show |", "|---|---|---|---|"]
    for src, (w, h, alt, pg) in sorted(seen.items()):
        lines.append(f"| `{src}` | {w}x{h} | {pg or 'various'} | {alt} |")
    write("IMAGES.md", "\n".join(lines) + "\n")


def main():
    build_home()
    urls = [("/", "1.0", "weekly")]
    build_simple("how", "how-it-works.html", b_howitworks, [("How it works", "/how-it-works.html")])
    build_simple("pricing", "pricing.html", b_pricing, [("Pricing", "/pricing.html")])
    build_simple("templates", "templates.html", b_templates, [("Templates", "/templates.html")])
    build_simple("faq", "faq.html", b_faq, [("FAQ", "/faq.html")])
    build_simple("contact", "contact.html", b_contact, [("Contact", "/contact.html")])
    build_simple("privacy", "privacy.html", b_legal("privacy"), [("Privacy Policy", "/privacy.html")])
    build_simple("terms", "terms.html", b_legal("terms"), [("Terms of Service", "/terms.html")])
    for key, out in USE_FILES.items():
        build_simple(key, out, b_usecase(key), [(USE_CASES[key]["crumb"], "/" + out)])
    build_blog()
    build_404()
    pri = {"how-it-works.html": ("0.9", "monthly"), "pricing.html": ("0.9", "monthly"), "templates.html": ("0.9", "weekly"), "faq.html": ("0.7", "monthly"),
           "contact.html": ("0.4", "yearly"), "privacy.html": ("0.3", "yearly"), "terms.html": ("0.3", "yearly")}
    for k, out in USE_FILES.items():
        pri[out] = ("0.9" if k in ("wedding", "birthday", "baby", "quince", "corporate", "qr", "rsvp", "maker") else "0.8", "monthly")
    for k, (pr, cf) in pri.items():
        urls.append(("/" + k, pr, cf))
    urls.append(("/blog/", "0.8", "weekly"))
    for s in POSTS:
        urls.append((f"/blog/{s}.html", "0.7", "monthly"))
    build_extras(urls)
    print("built", len(urls), "pages,", len(set(i[0] for i in IMAGES)), "image slots")


if __name__ == "__main__":
    main()
