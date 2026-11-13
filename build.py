#!/usr/bin/env python3
"""Génère le portfolio de Clément Lemaine : /fr /en /es + CV (HTML → PDF + aperçu PNG via Chrome headless).

Usage : python3 build.py          (site + CV)
        python3 build.py --no-cv  (site seul, plus rapide)
"""
import html
import json
import subprocess
from urllib.parse import quote
import sys
from pathlib import Path

import segno

from content import (EDUCATION, EMAIL, EXPERIENCES, FIRST, HERO_LINE, LANGS, LAST, LINKEDIN, NAME, PHONE, ROUTE,
                     ROUTE_TARGETS, SITE_URL, T)
from legal import GITHUB_PAGES_DATA, GITHUB_PRIVACY, LEGAL, SLUGS

ROOT = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LANG_NAMES = {"fr": "Français", "en": "English", "es": "Español"}
# sans JavaScript, les éléments animés restent visibles (lecteurs sans JS, agents, impression)
NOSCRIPT = ('<noscript><style>[data-reveal],.hero-name .l,.hero-cities,.hero-bio,.hero-top,.hero-bottom,.nav-pill'
            '{opacity:1!important;transform:none!important;filter:none!important}'
            '.odo-col{transform:translateY(calc(var(--n) * -.9em))}</style></noscript>')

e = html.escape

ARROW = '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
DOWN = '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 2v10M4 8l4 4 4-4M3 14h10"/></svg>'
PHONE_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M10.5 18.5h3"/></svg>'
LI_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>'
QR_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3.5" y="3.5" width="6" height="6" rx="1"/><rect x="14.5" y="3.5" width="6" height="6" rx="1"/><rect x="3.5" y="14.5" width="6" height="6" rx="1"/><path d="M14.5 14.5h2.5v2.5M20.5 14.5v.01M14.5 20.5h.01M17.5 20.5h3v-3" stroke-linecap="round"/></svg>'
MOON = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 14.5A8 8 0 019.5 4a8 8 0 1010.5 10.5z"/></svg>'


def pdf_name(lang):
    return f"Clement-Lemaine-CV-{lang.upper()}.pdf"


def qr_code():
    """QR code vers le site : SVG pour la page, PNG haute résolution pour le CV (imprimable partout) et le partage."""
    qr = segno.make(SITE_URL, error="q")
    # noir sur blanc avec la marge standard de 4 modules : le plus lisible pour l'appareil photo d'un téléphone
    qr.save(ROOT / "assets" / "qr.svg", scale=10, border=4, dark="#000000", light="#ffffff")
    qr.save(ROOT / "assets" / "qr.png", scale=24, border=4, dark="#000000", light="#ffffff")


def ver(name):
    """Empreinte du fichier, ajoutée à son URL : le navigateur recharge le CSS/JS dès qu'il change."""
    import hashlib
    return hashlib.md5((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]


def tr(v, lang):
    return v[lang] if isinstance(v, dict) else v


def odometer(value):
    """Chiffres sur rouleaux : chaque colonne défile de 0 jusqu'au bon chiffre."""
    digits = "".join(f"<span>{d}</span>" for d in range(10))
    return f'<span class="sr-only">{e(value)}</span>' + "".join(f'<span class="odo-col" style="--n:{c}" aria-hidden="true">{digits}</span>' for c in value)


def letters(word, start):
    return "".join(f'<span class="l" style="--i:{start + i}">{e(c)}</span>' for i, c in enumerate(word))


# ---------------------------------------------------------------- morceaux communs

def head_links(lang, slug):
    """URL canonique + versions dans les autres langues (adresses complètes, comme le veut Google)."""
    path = f"{slug}/" if slug else ""
    links = [f'<link rel="canonical" href="{SITE_URL}{lang}/{path}">']
    links += [f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}{l}/{path}">' for l in LANGS]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}en/{path}">')
    return "\n".join(links)


def mail_link(user, domain, cls="mail"):
    """Adresse assemblée par main.js ; sans JavaScript, elle reste lisible sous la forme « nom (at) domaine »."""
    return f'<a class="{cls}" data-u="{e(user)}" data-d="{e(domain)}" href="#">{e(user)} (at) {e(domain)}</a>'


def site_footer(lang, base, current=""):
    """Pied de page : liens vers les pages légales. base = chemin vers la racine de la langue."""
    lg = LEGAL[lang]
    here = ' aria-current="page"'
    links = "".join(f'<li><a href="{base}{s}/"{here if s == current else ""}>{e(lg["titles"][s])}</a></li>' for s in SLUGS)
    return f"""<footer class="wrap legal-foot">
  <nav aria-label="{e(lg['nav'])}"><ul class="legal-links">{links}</ul></nav>
  <p class="copyright">© 2026 {e(NAME)}. {e(T[lang]['footer'])}</p>
</footer>"""


# ---------------------------------------------------------------- pages légales

def legal_page(lang, slug):
    t, lg = T[lang], LEGAL[lang]
    title = lg["titles"][slug]
    user, domain = EMAIL.split("@")
    body = lg[slug].format(mail=mail_link(user, domain), gh_pages=GITHUB_PAGES_DATA, gh_privacy=GITHUB_PRIVACY,
                           **{s: f"../{s}/" for s in SLUGS})
    cur = ' aria-current="true"'
    langs = "".join(f'<a href="../../{l}/{slug}/" hreflang="{l}" lang="{l}" aria-label="{LANG_NAMES[l]}"{cur if l == lang else ""}>{l.upper()}</a>'
                    for l in LANGS)
    return f"""<!doctype html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — {e(NAME)}</title>
<meta name="description" content="{e(title)} — {e(NAME)}">
{head_links(lang, slug)}
<link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
<script>try{{var s=localStorage.getItem('cl-theme');if(s)document.documentElement.dataset.theme=s;}}catch(_){{}}</script>
<link rel="stylesheet" href="../../assets/fonts/fonts.css?v={ver('fonts/fonts.css')}">
<link rel="stylesheet" href="../../assets/style.css?v={ver('style.css')}">
{NOSCRIPT}
</head>
<body>
<a class="skip" href="#main">{e(t['skip'])}</a>
<header class="nav-wrap">
  <nav class="nav-pill" aria-label="Navigation">
    <a class="nav-name" href="../">{e(NAME)}</a>
    <span class="seg">{langs}</span>
    <button class="theme" type="button" aria-label="{e(t['theme'])}">{MOON}</button>
  </nav>
</header>
<main id="main" class="legal">
  <p class="eyebrow">{e(lg['nav'])}</p>
  <h1>{e(title)}</h1>
  <p class="updated">{e(lg['updated'])}</p>
  {body}
  <p style="margin-top:40px"><a class="btn btn-quiet" href="../">{e(lg['back'])}</a></p>
</main>
{site_footer(lang, "../", slug)}
<script src="../../assets/main.js?v={ver('main.js')}"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- pour les moteurs et les agents IA

def sitemap():
    urls = [f"{SITE_URL}{l}/" for l in LANGS] + [f"{SITE_URL}{l}/{s}/" for l in LANGS for s in SLUGS]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")


def llms_txt():
    """Résumé en Markdown du site, lisible directement par un agent IA (convention llms.txt)."""
    t = T["en"]
    exps = "\n".join(f"- {x['year']['en']} · {x['role']['en']} — {tr(x['venue'], 'en')}, {x['city']['en']}. {x['desc']['en']}" for x in EXPERIENCES)
    edus = "\n".join(f"- {x['years']['en']} · {x['school']} — {x['prog']['en']}" for x in EDUCATION)
    pages = "\n".join(f"- [Portfolio ({LANG_NAMES[l]})]({SITE_URL}{l}/)" for l in LANGS)
    cvs = "\n".join(f"- [CV ({LANG_NAMES[l]}, PDF)]({SITE_URL}cv/{pdf_name(l)})" for l in LANGS)
    legal = "\n".join(f"- [{LEGAL['en']['titles'][s]}]({SITE_URL}en/{s}/)" for s in SLUGS)
    return f"""# {NAME}

> {t['meta']}

{t['cv_profile']}

## Pages
{pages}

## CV
{cvs}

## Experience
{exps}

## Education
{edus}

## Languages
{", ".join(f"{a} ({b})" for a, b in t['langs'])}

## Contact
- Email: {EMAIL}
- LinkedIn: {LINKEDIN}
- Based in Madrid, Spain. {t['contact_p']}

## Legal
{legal}
"""


# ---------------------------------------------------------------- site

def page(lang):
    t = T[lang]
    cv_href = f"../cv/{pdf_name(lang)}"
    cur = ' aria-current="true"'
    langs = "".join(f'<a href="../{l}/" hreflang="{l}" lang="{l}" aria-label="{LANG_NAMES[l]}"{cur if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    nav = "".join(f'<a href="#{i}">{e(l)}</a>' for i, l in zip(["parcours", "experiences", "projets", "formation", "contact"], t["nav"]))

    # trajet
    route_d = f"M{ROUTE[0]['x']} {ROUTE[0]['y']} " + " ".join(r["seg"] for r in ROUTE[1:])
    label_at = {"right": ('x="22" y="9" text-anchor="start"', 'x="22" y="-18" text-anchor="start"'),
                "left": ('x="-22" y="9" text-anchor="end"', 'x="-22" y="-18" text-anchor="end"'),
                "below": ('y="44" text-anchor="middle"', 'y="-24" text-anchor="middle"')}
    stops_svg = ""
    for i, r in enumerate(ROUTE):
        prefix = f"M{ROUTE[0]['x']} {ROUTE[0]['y']} " + " ".join(x["seg"] for x in ROUTE[1:i + 1])
        texts = ""
        if r["label"]:
            city_at, code_at = label_at[r["label"]]
            texts = f'<text class="stop-code" {code_at}>{r["code"]}</text><text class="stop-city" {city_at}>{e(r["city"])}</text>'
        stops_svg += (f'<g class="stop" data-stop="{i}" data-d="{prefix if i else ""}" transform="translate({r["x"]} {r["y"]})">'
                      f'<circle class="stop-halo" r="18"/><circle class="stop-dot" r="7"/>{texts}</g>')
    map_svg = "".join(f'<text class="map-land" x="{x}" y="{y}">{e(n)}</text>' for n, x, y in t["map"])
    panels = []
    for i, (r, (country, title, items, note)) in enumerate(zip(ROUTE, t["stops"])):
        lis = "".join(f'<li><span class="it-role">{e(a)}</span><span class="it-venue">{e(b)}</span>'
                      f'{f"<span class=it-year>{e(c)}</span>" if c else ""}</li>' for a, b, c in items)
        panels.append(f"""
          <article class="leg{' is-on' if i == 0 else ''}" data-leg="{i}">
            <div class="leg-head">
              <p class="leg-meta">{e(t['route_label'])} {i + 1:02d} · {e(country)} · {e(r['years'][lang])}</p>
              <h3 class="leg-city">{e(r['city'])}</h3>
              <p class="leg-title">{e(title)}</p>
            </div>
            <div class="leg-body"><ul>{lis}</ul><p class="leg-note">{e(note)}</p>
              {f'<a class="leg-more" href="#{ROUTE_TARGETS[i]}">{e(t["leg_more"])} {ARROW}</a>' if ROUTE_TARGETS[i] else ''}</div>
          </article>""")

    z = t["jum"]
    jum_roles = "".join(f'<li><strong>{e(a)}</strong><small>{e(b)}</small></li>' for a, b in z["roles"])
    months = "".join(f'<li style="--k:{i}">{e(m)}</li>' for i, m in enumerate(t["months"]))
    stars = "".join(f'<i style="--k:{i}">★</i>' for i in range(5))
    lw = t["loewe"]
    loewe_bullets = "".join(f"<li>{e(b)}</li>" for b in lw["bullets"])

    stats = "".join(f'<div class="stat" style="--k:{k}"><p class="big-n odo">{odometer(a)}</p><h3>{e(b)}</h3><p>{e(c)}</p></div>'
                    for k, (a, b, c) in enumerate(t["stats"]))
    flyers = "".join(f'<div class="flyer f{i} p{i}"><span class="flyer-k">{e(k)}</span><strong>{e(w)}</strong><span class="flyer-d">Clément L.</span></div>'
                     for i, (k, w) in enumerate(t["flyers"]))

    pj = t["pj"]
    fi, rd, bt, cs = pj["fichas"], pj["redo"], pj["bot"], pj["cesar"]
    fi_steps = "".join(f'<li><strong>{e(a)}</strong><span>{e(b)}</span></li>' for a, b in fi["steps"])
    bot_tags = "".join(f'<span class="tag">{e(x)}</span>' for x in bt["tags"])
    prompts = html.escape(json.dumps(t["prompts"], ensure_ascii=False))

    edu = "".join(f"""
        <li><details class="edu-row"{' open' if x.get('now') else ''}>
          <summary>
            <span class="edu-years">{e(x['years'][lang])}</span>
            <div><h3>{e(x['school'])}{f' <span class="tag tag-live">{e(t["edu_now"])}</span>' if x.get('now') else ''}</h3><p class="edu-prog">{e(x['prog'][lang])}</p></div>
            <span class="edu-plus" aria-hidden="true"></span>
          </summary>
          <div class="edu-more"><p>{e(x['desc'][lang])}</p><span class="tags">{''.join(f'<span class="tag">{e(g)}</span>' for g in x['tags'][lang])}</span></div>
        </details></li>""" for x in EDUCATION)
    skills = "".join(f'<span class="tag">{e(x)}</span>' for x in t["cv_skills"])
    hero_line = " <b>·</b> ".join(e(x) for x in HERO_LINE)
    langs_list = "".join(f'<li><strong>{e(a)}</strong><span>{e(b)}</span></li>' for a, b in t["langs"])

    off_stats = "".join(f'<li><strong>{e(a)}</strong><span>{e(b)}</span></li>' for a, b in t["off_stats"])
    cv_tabs = "".join(f'<button type="button" data-cv-lang="{l}" data-pdf="../cv/{pdf_name(l)}"{cur if l == lang else ""}>{l.upper()}</button>'
                      for l in LANGS)
    cv_langs = "".join(f'<a class="btn btn-quiet btn-sm" href="../cv/{pdf_name(l)}" download>{l.upper()}</a>' for l in LANGS)
    li_href = e(quote(LINKEDIN, safe=":/"))
    linkedin = f'<a class="btn btn-li" href="{li_href}" target="_blank" rel="noopener noreferrer">{LI_ICON} LinkedIn</a>' if LINKEDIN else ""
    li_float = f'<a class="li-btn" href="{li_href}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="LinkedIn">{LI_ICON}</a>' if LINKEDIN else ""
    user, domain = EMAIL.split("@")
    alt = t["alt"]
    alternates = head_links(lang, "")
    person = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": NAME, "url": f"{SITE_URL}{lang}/",
                         "jobTitle": t["cv_title"], "description": t["meta"], "knowsLanguage": LANGS,
                         "address": {"@type": "PostalAddress", "addressLocality": "Madrid", "addressCountry": "ES"},
                         "affiliation": {"@type": "EducationalOrganization", "name": "Vatel Madrid"},
                         "sameAs": [LINKEDIN] if LINKEDIN else []}, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['meta'])}">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['meta'])}">
{alternates}
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<script>try{{var s=localStorage.getItem('cl-theme');if(s)document.documentElement.dataset.theme=s;}}catch(_){{}}</script>
<link rel="stylesheet" href="../assets/fonts/fonts.css?v={ver('fonts/fonts.css')}">
<link rel="stylesheet" href="../assets/style.css?v={ver('style.css')}">
{NOSCRIPT}
<script type="application/ld+json">{person}</script>
</head>
<body>
<a class="skip" href="#main">{e(t['skip'])}</a>

<header class="nav-wrap">
  <nav class="nav-pill" aria-label="Navigation">
    <a class="nav-name" href="#top">{e(NAME)}</a>
    <span class="nav-links">{nav}</span>
    <button class="btn-cv" type="button" data-open-cv>CV</button>
    <span class="seg">{langs}</span>
    <button class="theme" type="button" aria-label="{e(t['theme'])}">{MOON}</button>
  </nav>
</header>

<main id="main">
<section class="hero" id="top">
  <div class="hero-light" aria-hidden="true"></div>
  <div class="hero-top">
    <p class="hero-label">{e(t['hero_role'])}<span class="hero-sub">{e(t['hero_role2'])}</span></p>
    <p class="hero-label">{e(t['hero_place'])}</p>
  </div>
  <div class="hero-mid">
    <h1 class="hero-name"><span class="sr-only">{e(NAME)}</span><span class="n1" aria-hidden="true">{letters(FIRST, 0)}</span><span class="n2" aria-hidden="true">{letters(LAST, len(FIRST))}</span></h1>
    <p class="hero-cities">{hero_line}</p>
    <p class="hero-bio">{e(t['hero_bio'])}</p>
  </div>
  <div class="hero-bottom">
    <div class="hero-ctas">
      <a class="btn btn-outline" href="#contact">{e(t['cta2'])}</a>
    </div>
  </div>
  <a class="scroll-cue" href="#parcours">{e(t['scroll'])}<svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 6l4 4 4-4"/></svg></a>
</section>

<section class="route-sec" id="parcours">
  <div class="route-pin">
    <div class="wrap">
      <div class="route-head">
        <div><p class="eyebrow">{e(t['route_eyebrow'])}</p><h2>{e(t['route_h'])}</h2></div>
        <p class="route-hint">{e(t['route_hint'])} <span>↓</span></p>
      </div>
      <div class="route-map">
        <svg viewBox="0 0 1000 300" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
          {map_svg}
          <path class="route-ghost" d="{route_d}"/>
          <path class="route-line" d="{route_d}"/>
          {stops_svg}
          <g class="plane"><path d="M-12 0 L10 -2 L14 0 L10 2 Z M-2 -1 L-6 -11 L-2 -11 L5 -1 Z M-2 1 L-6 11 L-2 11 L5 1 Z M-11 -1 L-14 -6 L-12 -6 L-8 -1 Z M-11 1 L-14 6 L-12 6 L-8 1 Z"/></g>
        </svg>
      </div>
      <div class="legs">{''.join(panels)}</div>
    </div>
  </div>
</section>

<section class="sec" id="experiences">
  <div class="wrap">
    <p class="eyebrow" data-reveal>{e(t['exp_eyebrow'])}</p>
    <h2 class="h2-lg" data-reveal>{e(t['exp_h'])}</h2>

    <div class="exp-grid">
      <article class="dark-card feat spot" id="jumeirah" data-reveal>
        <p class="chip-live"><i></i>{e(z['chip'])}</p>
        <h3>{e(z['h'])}</h3>
        <p>{e(z['p'])}</p>
        <ol class="months">{months}</ol>
        <ul class="duties">{jum_roles}</ul>
        <p class="feat-name">Jumeirah Mallorca <span>· {e(z['tag'])}</span><span class="stars" aria-hidden="true">{stars}</span></p>
      </article>

      <article class="card side-exp spot" id="loewe" data-reveal>
        <div class="side-visual" aria-hidden="true">
          <div class="bag">
            <span class="tissue"></span><span class="tissue t2"></span>
            <span class="bag-handle"></span>
            <span class="bag-body"><b>LOEWE</b><small>MADRID</small></span>
            <span class="bag-tag"><b>2022</b><small>{e(lw['card'])}</small></span>
          </div>
        </div>
        <div class="side-copy">
          <p class="eyebrow-sm">{e(lw['eyebrow'])} · Loewe Madrid</p>
          <h3>{e(lw['h'])}</h3>
          <p>{e(lw['p'])}</p>
          <ul class="bullets">{loewe_bullets}</ul>
        </div>
      </article>
    </div>

    <article class="card stats-card spot" id="chiffres" data-reveal>
      <div class="stats-copy">
        <p class="eyebrow-sm">{e(t['stats_eyebrow'])}</p>
        <div class="stats">{stats}</div>
      </div>
      <div class="flyers" aria-hidden="true">{flyers}</div>
    </article>

  </div>
</section>

<section class="sec" id="projets">
  <div class="wrap">
    <p class="eyebrow" data-reveal>{e(pj['eyebrow'])}</p>
    <h2 class="h2-lg" data-reveal>{e(pj['h'])}</h2>
    <div class="pj-intro" data-reveal>
      <p class="proj-p">{e(pj['p'])}</p>
      <div class="prompt" data-prompts="{prompts}"><span class="prompt-k">IA</span><p class="prompt-t">{e(t['prompts'][0])}</p><span class="prompt-send">{ARROW}</span></div>
    </div>

    <div class="pj-duo">
      <article class="dark-card pj-bot spot" data-reveal>
        <div class="bot-shots">
          <div class="bot-screen"><img src="../assets/projects/bot-chart.webp" alt="{e(alt['bot_chart'])}" width="1400" height="875" loading="lazy"><img class="alt" src="../assets/projects/bot-news.webp" alt="{e(alt['bot_news'])}" width="1400" height="875" loading="lazy"></div>
          <figure class="pj-phone ph-sm"><img src="../assets/projects/bot-mobile.webp" alt="{e(alt['bot_mobile'])}" width="520" height="1125" loading="lazy"></figure>
        </div>
        <p class="eyebrow-sm">{e(bt['tag'])}</p>
        <h3>{e(bt['h'])}</h3>
        <p>{e(bt['p'])}</p>
        <span class="tags">{bot_tags}</span>
      </article>

      <article class="card pj-cesar spot" data-reveal>
        <div class="cs-shots">
          <div class="cs-browser"><div class="ba-bar" aria-hidden="true"><i></i><i></i><i></i><span class="ba-url">cesarmateu.github.io</span></div>
            <div class="cs-view"><div class="cs-strip"><img src="../assets/projects/cesar-hero.webp" alt="{e(alt['cesar_hero'])}" width="1400" height="875" loading="lazy"><img src="../assets/projects/cesar-route.webp" alt="{e(alt['cesar_route'])}" width="1400" height="875" loading="lazy"></div></div></div>
          <figure class="pj-phone ph-sm"><img src="../assets/projects/cesar-mobile.webp" alt="{e(alt['cesar_mobile'])}" width="520" height="1125" loading="lazy"></figure>
        </div>
        <p class="eyebrow-sm">{e(cs['tag'])}</p>
        <h3>{e(cs['h'])}</h3>
        <p>{e(cs['p'])}</p>
        <a class="btn btn-quiet btn-sm" href="https://cesarmateu.github.io/{lang}/" target="_blank" rel="noopener">{e(cs['cta'])} {ARROW}</a>
      </article>
    </div>

    <article class="card pj pj-fichas spot" data-reveal>
      <div class="pj-copy">
        <p class="eyebrow-sm">{e(fi['tag'])}</p>
        <h3>{e(fi['h'])}</h3>
        <ol class="pj-steps">{fi_steps}</ol>
        <p class="pj-stat"><span class="big-n odo">{odometer(fi['stat'])}</span><b>h</b><span class="pj-stat-l">{e(fi['stat_l'])}</span></p>
      </div>
      <div class="pj-phones">
        <figure class="pj-phone ph-a"><img src="../assets/projects/fichas-1.webp" alt="{e(alt['fichas_1'])}" width="520" height="1125" loading="lazy"></figure>
        <figure class="pj-phone ph-b"><img src="../assets/projects/fichas-2.webp" alt="{e(alt['fichas_2'])}" width="520" height="1125" loading="lazy"></figure>
      </div>
    </article>

    <article class="card pj pj-redo spot" data-reveal>
      <div class="pj-copy">
        <p class="eyebrow-sm">{e(rd['tag'])}</p>
        <h3>{e(rd['h'])}</h3>
        <p>{e(rd['p'])}</p>
        <a class="btn btn-primary btn-sm" href="https://seo-agency-beta.vercel.app/#/" target="_blank" rel="noopener">{e(rd['cta'])} {ARROW}</a>
      </div>
      <div class="ba-wrap">
        <div class="ba" role="img" aria-label="DRM Fishing : {e(rd['before'])} / {e(rd['after'])}">
          <div class="ba-bar"><i></i><i></i><i></i><span class="ba-url"><span class="u-old">drmfishing.com</span><span class="u-new">DRM Fishing · {e(rd['new_url'])}</span></span></div>
          <div class="ba-view">
            <img class="ba-img" src="../assets/projects/drm-after.webp" alt="{e(alt['drm_after'])}" width="1000" height="4200" loading="lazy">
            <div class="ba-before"><img class="ba-img" src="../assets/projects/drm-before.webp" alt="{e(alt['drm_before'])}" width="1000" height="3417" loading="lazy"></div>
            <span class="ba-tag ba-tag-b">{e(rd['before'])}</span><span class="ba-tag ba-tag-a">{e(rd['after'])}</span>
            <span class="ba-handle"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 6l-4 4 4 4M12 6l4 4-4 4"/></svg></span>
          </div>
        </div>
        <p class="ba-hint">{e(rd['hint'])}</p>
      </div>
    </article>

  </div>
</section>

<section class="sec" id="formation">
  <div class="wrap">
    <p class="eyebrow" data-reveal>{e(t['edu_eyebrow'])}</p>
    <h2 class="h2-lg" data-reveal>{e(t['edu_h'])}</h2>
    <div class="edu-layout">
      <ul class="card edu-list" data-reveal>{edu}</ul>
      <div class="side">
        <article class="dark-card off-card spot" data-reveal>
          <p class="eyebrow-sm">{e(t['off_eyebrow'])}</p>
          <h3 class="off-h">{e(t['off_h'])} <span class="u">{e(t['off_h2'])}</span></h3>
          <p>{e(t['off_p'])}</p>
          <ul class="off-stats">{off_stats}</ul>
        </article>
        <article class="card side-card spot" data-reveal>
          <p class="eyebrow-sm">{e(t['cv_langs_h'])}</p>
          <ul class="langs-list">{langs_list}</ul>
        </article>
        <article class="card side-card spot" data-reveal>
          <p class="eyebrow-sm">{e(t['cv_skills_h'])}</p>
          <div class="tags skills">{skills}</div>
        </article>
      </div>
    </div>
  </div>
</section>

<section class="site-footer" id="contact">
  <div class="wrap">
    <div class="card contact-card spot" data-reveal>
      <div class="contact-copy">
        <p class="eyebrow">{e(t['contact_eyebrow'])}</p>
        <h2>{e(t['contact_h'])}</h2>
        <p class="footer-p">{e(t['contact_p'])} {e(t['cv_p'])}</p>
        <div class="row">
          <a class="btn btn-primary" href="{cv_href}" download>{DOWN} {e(t['cv_dl'])}</a>
          {mail_link(user, domain, "btn btn-quiet mail")}
          {linkedin}
        </div>
        <div class="row cv-langs"><span class="cv-langs-l">PDF</span>{cv_langs}<button class="btn btn-quiet btn-sm" type="button" data-open-cv>{e(t['cv_view'])}</button></div>
        <button class="qr-tile" type="button" data-open-qr>
          <img src="../assets/qr.svg?v={ver('qr.svg')}" alt="" width="72" height="72">
          <span><strong>{e(t['qr'])}</strong><small>{e(t['qr_p'])}</small></span>
        </button>
      </div>
      <button class="sheet" type="button" data-open-cv aria-label="{e(t['cv_view'])}">
        <img src="../cv/preview-{lang}.png" alt="CV — {e(NAME)}" width="794" height="1123" loading="lazy">
      </button>
    </div>
  </div>
</section>
</main>
{site_footer(lang, "../")}

<dialog class="cv-modal" aria-label="CV — {e(NAME)}">
  <div class="cv-modal-bar">
    <strong>CV — {e(NAME)}</strong>
    <span class="row"><span class="seg cv-seg">{cv_tabs}</span><a class="btn btn-primary btn-sm cv-pdf" href="{cv_href}" download>{DOWN} PDF</a>
    <button class="btn btn-quiet btn-sm" type="button" data-close>{e(t['close'])}</button></span>
  </div>
  <img class="cv-img" src="../cv/preview-{lang}.png" alt="CV — {e(NAME)}" width="794" height="1123">
</dialog>
<dialog class="qr-modal" aria-label="{e(t['qr'])}">
  <img src="../assets/qr.svg?v={ver('qr.svg')}" alt="{e(t['qr'])} — {e(SITE_URL)}" width="320" height="320">
  <p class="qr-name">{e(NAME)}</p>
  <p class="qr-url">{e(SITE_URL.replace('https://', '').rstrip('/'))}</p>
  <div class="row"><a class="btn btn-quiet btn-sm" href="../assets/qr.png?v={ver('qr.png')}" download="Clement-Lemaine-QR.png">{DOWN} PNG</a>
  <button class="btn btn-primary btn-sm" type="button" data-close>{e(t['close'])}</button></div>
</dialog>
{li_float}
<button class="route-cue" type="button" data-route-next data-n="{e(t['route_cue_n'])}">
  <span class="route-cue-arrow" aria-hidden="true"><svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 3v10M4 9l4 4 4-4"/></svg></span>
  <span class="route-cue-txt"><span>{e(t['route_cue'])}</span><small class="route-cue-n">{e(t['route_cue_n'].format(n=1, total=len(ROUTE)))}</small></span>
  <span class="route-cue-dots" aria-hidden="true">{"<i></i>" * len(ROUTE)}</span>
</button>
<button class="qr-btn" type="button" data-open-qr aria-label="{e(t['qr'])}" title="{e(t['qr'])}">{QR_ICON}<span>{e(t['qr'])}</span></button>
<button class="phone-btn" type="button" data-phone aria-label="{e(t['mobile_view'])}" title="{e(t['mobile_view'])}">{PHONE_ICON}<span>{e(t['mobile_view'])}</span></button>
<dialog class="phone-modal" aria-label="{e(t['mobile_view'])}">
  <button class="phone-close" type="button" data-phone-close aria-label="{e(t['close'])}">×</button>
  <div class="phone"><div class="phone-notch"></div><div class="phone-status"><span>9:41</span><span class="phone-icons"><i></i><i></i><i></i><b></b></span></div><iframe title="{e(t['mobile_view'])}" loading="lazy"></iframe></div>
</dialog>
<script src="../assets/main.js?v={ver('main.js')}"></script>
</body>
</html>
"""


def root_index():
    return """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Clément Lemaine</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>var l=(navigator.language||'fr').slice(0,2);location.replace((['fr','en','es'].indexOf(l)>-1?l:'en')+'/');</script>
<meta http-equiv="refresh" content="1;url=fr/"></head>
<body style="background:#0c1420"></body></html>
"""


# ---------------------------------------------------------------- CV

def cv(lang):
    t = T[lang]
    exps = "".join(f"""
      <div class="item">
        <div class="item-when">{e(x['year'][lang])}<small>{e(x['city'][lang])}</small></div>
        <div><h4>{e(x['role'][lang])}</h4><p class="where">{e(tr(x['venue'], lang))}{' · ' + e(x['group'][lang]) if x['group'] else ''}</p>
        <p>{e(x['desc'][lang])}</p></div>
      </div>""" for x in EXPERIENCES)
    edus = "".join(f"""
      <div class="item">
        <div class="item-when">{e(x['years'][lang])}</div>
        <div><h4>{e(x['school'])}</h4><p>{e(x['prog'][lang])}</p></div>
      </div>""" for x in EDUCATION)
    langs = "".join(f"<li><b>{e(a)}</b> — {e(b)}</li>" for a, b in t["langs"])
    ints = "".join(f"<li>{e(i)}</li>" for i in t["cv_int"])
    skills = "".join(f"<span>{e(s)}</span>" for s in t["cv_skills"])
    li = f'<li><a href="{e(quote(LINKEDIN, safe=":/"))}" style="color:inherit;text-decoration:none">{e(LINKEDIN.replace("https://", ""))}</a></li>' if LINKEDIN else ""
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><title>CV — {e(NAME)}</title>
<link rel="stylesheet" href="cv.css"></head>
<body><div class="page">
  <aside>
    <img class="photo" src="../assets/portrait.jpg" alt="{e(t['alt']['photo'])}">
    <h3>{e(t['cv_profile_h'])}</h3><p>{e(t['cv_profile'])}</p>
    <h3>{e(t['cv_contact_h'])}</h3>
    <ul><li>{e(EMAIL)}</li><li>{e(PHONE)}</li><li>{e(t['cv_city'])}</li>{li}<li>{e(t['nationality'])}</li></ul>
    <h3>{e(t['cv_langs_h'])}</h3><ul>{langs}</ul>
    <h3>{e(t['cv_int_h'])}</h3><ul>{ints}</ul>
    <div class="qr"><img src="../assets/qr.png" alt=""><p><b>{e(t['cv_qr'])}</b>{e(SITE_URL.replace('https://', '').rstrip('/')).replace('-', '&#8209;').replace('/', '<wbr>/')}</p></div>
  </aside>
  <section>
    <header><p class="kicker">{e(t['cv_title'])} · Vatel Madrid</p><h1>{e(NAME)}</h1></header>
    <h2>{e(t['cv_exp_h'])}</h2>{exps}
    <h2>{e(t['cv_edu_h'])}</h2>{edus}
    <h2>{e(t['cv_skills_h'])}</h2><div class="chips">{skills}</div>
  </section>
</div></body></html>
"""


def chrome(*args):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--virtual-time-budget=4000", *args], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    qr_code()
    for lang in LANGS:
        d = ROOT / lang
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page(lang), encoding="utf-8")
        for slug in SLUGS:
            (d / slug).mkdir(exist_ok=True)
            (d / slug / "index.html").write_text(legal_page(lang, slug), encoding="utf-8")
    (ROOT / "index.html").write_text(root_index(), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "llms.txt").write_text(llms_txt(), encoding="utf-8")
    print("site : fr/ en/ es/ + pages légales, sitemap.xml, llms.txt")

    if "--no-cv" in sys.argv:
        return
    cvdir = ROOT / "cv"
    for lang in LANGS:
        src = cvdir / f"cv-{lang}.html"
        src.write_text(cv(lang), encoding="utf-8")
        chrome("--no-pdf-header-footer", f"--print-to-pdf={cvdir / pdf_name(lang)}", src.as_uri())
        chrome("--window-size=794,1123", "--force-device-scale-factor=2",
               f"--screenshot={cvdir / f'preview-{lang}.png'}", src.as_uri())
        print(f"cv : {pdf_name(lang)} + preview-{lang}.png")


if __name__ == "__main__":
    main()
