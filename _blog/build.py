#!/usr/bin/env python3
"""AGREXPERT blog builder (Russian only, standard library only).

Sources:  _blog/posts/YYYY-MM-DD-<slug>.html
  <!--META
  { "slug": "...", "date": "YYYY-MM-DD", "title": "...", "h1": "...",
    "description": "...", "lead": "...", "keyword": "...",
    "region": "" | "Москва" | "Московская область" | "Санкт-Петербург" | "<другой регион>",
    "service": "/#services",            # main service target (page or home-page anchor)
    "faq": [{"q": "...", "a": "..."}],
    "sources": [{"title": "...", "url": "https://..."}] }   # official sources used for facts
  -->
  <h2>…</h2><p>…</p> …   (body HTML)

Output:   /blog/index.html, /blog/<slug>/index.html, /blog/rss.xml,
          blog URLs inside sitemap.xml (between <!--blog--> markers),
          "Блог" link in the home-page nav and footer.

Run:  python3 _blog/build.py [--check]
"""
import html
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_blog", "posts")
SVC = os.path.join(ROOT, "_blog", "services")
SITE = "https://agrexpert.ru"
REQUIRED = ["slug", "date", "title", "h1", "description", "lead", "keyword", "service"]
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
METRIKA = 113822254

CSS = """
:root{--paper:#E9ECE6;--sheet:#F6F7F3;--ink:#16202A;--muted:#56626C;--line:#C6CCC3;--grid:rgba(22,32,42,.055);
--accent:#2C6A5B;--accent-ink:#F6F7F3;--red:#B5432E;--ok-soft:rgba(44,106,91,.10);
--f-display:"Geologica","Golos Text",system-ui,sans-serif;--f-body:"Golos Text",system-ui,-apple-system,"Segoe UI",sans-serif;
--f-mono:"IBM Plex Mono",ui-monospace,"SFMono-Regular",Menlo,monospace;--wrap:1200px;--r:3px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#11161B;--sheet:#182027;--ink:#E4E9E3;--muted:#98A3AC;--line:#2C3741;--grid:rgba(228,233,227,.045);--accent:#6BB49F;--accent-ink:#0E1A16;--red:#E37A63;--ok-soft:rgba(107,180,159,.12);color-scheme:dark}}
:root[data-theme="dark"]{--paper:#11161B;--sheet:#182027;--ink:#E4E9E3;--muted:#98A3AC;--line:#2C3741;--grid:rgba(228,233,227,.045);--accent:#6BB49F;--accent-ink:#0E1A16;--red:#E37A63;--ok-soft:rgba(107,180,159,.12);color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 var(--f-body);-webkit-font-smoothing:antialiased}
a{color:inherit}
h1,h2,h3{font-family:var(--f-display);font-weight:600;line-height:1.15;letter-spacing:-.015em;text-wrap:balance;margin:0}
.wrap{max-width:var(--wrap);margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font:500 1rem/1 var(--f-body);padding:15px 22px;border-radius:var(--r);text-decoration:none;border:1.5px solid var(--ink);cursor:pointer}
.btn-primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn-ghost{background:transparent;color:var(--ink)}
.btn-ghost:hover{background:var(--ink);color:var(--paper)}
.btn svg{width:16px;height:16px}
.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:20px;height:64px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;font:700 1.0625rem/1 var(--f-display);letter-spacing:.06em}
.logo-mark{width:28px;height:28px}
.nav{display:flex;gap:26px;font-size:.9375rem}
.nav a{text-decoration:none;color:var(--muted)}
.nav a:hover,.nav a[aria-current]{color:var(--ink)}
.top .btn{padding:11px 16px;font-size:.9375rem}
@media (max-width:900px){.nav{display:none}}
@media (max-width:480px){.top .btn span{display:none}}
.crumbs{font:400 .8125rem/1.4 var(--f-mono);color:var(--muted);padding-top:20px}
.crumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0}
.crumbs li+li::before{content:"/";margin-right:6px}
.crumbs a{text-decoration:none}
.b-hero{padding:28px 0 36px;border-bottom:1px solid var(--line);background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:24px 24px}
.b-hero h1{font-size:clamp(1.875rem,4.4vw,3.125rem);font-weight:700;letter-spacing:-.025em;max-width:24ch;margin:10px 0 14px}
.eyebrow{font:500 .8125rem/1.3 var(--f-mono);text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}
.lead{color:var(--muted);font-size:1.1875rem;max-width:62ch;margin:0}
.b-meta{font:400 .8125rem/1.4 var(--f-mono);color:var(--muted);margin:16px 0 0}
.b-grid{display:grid;gap:36px;padding-block:40px 56px}
@media (min-width:980px){.b-grid{grid-template-columns:minmax(0,1fr) 320px;gap:56px}}
.b-body{min-width:0;max-width:72ch}
.b-body h2{font-size:clamp(1.5rem,2.6vw,1.875rem);margin:1.6em 0 .55em}
.b-body h2:first-child{margin-top:0}
.b-body h3{font-size:1.1875rem;margin:1.3em 0 .45em}
.b-body p{margin:0 0 1em}
.b-body ul,.b-body ol{padding-left:1.25em;margin:0 0 1.1em;display:grid;gap:6px}
.b-body li::marker{color:var(--accent)}
.b-body a{color:var(--accent)}
.table-wrap{overflow-x:auto;margin:6px 0 22px;border:1px solid var(--line);border-radius:var(--r);background:var(--sheet)}
.table-wrap table{border-collapse:collapse;width:100%;font-size:.9375rem}
.table-wrap th,.table-wrap td{padding:10px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
.table-wrap th{font-weight:600;background:var(--ok-soft)}
.table-wrap tr:last-child td{border-bottom:0}
.blog-note{border-left:3px solid var(--red);background:var(--sheet);padding:14px 18px;margin:6px 0 22px}
.blog-note p{margin:0}
.b-body figure{margin:8px 0 24px;border:1px solid var(--line);background:var(--sheet)}
.b-body figure img{display:block;width:100%;height:auto}
.b-body figcaption{font:400 .8125rem/1.4 var(--f-mono);color:var(--muted);padding:10px 14px}
.b-aside{display:grid;gap:16px;align-content:start}
@media (min-width:980px){.b-aside{position:sticky;top:88px}}
.card{background:var(--sheet);border:1px solid var(--line);border-radius:var(--r);padding:22px;display:grid;gap:12px}
.card h3{font-size:1.25rem}
.card p{margin:0;color:var(--muted);font-size:.9375rem}
.card .btn{width:100%}
.card dl{margin:0;display:grid;gap:6px;font-size:.9375rem}
.card dt{font:500 .71875rem/1.2 var(--f-mono);text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}
.card dd{margin:0 0 6px}
.card dd a{color:var(--accent)}
.sec{padding:8px 0 56px}
.sec h2{font-size:clamp(1.5rem,2.6vw,1.875rem);margin:0 0 20px}
.faq details{border-top:1px solid var(--line);padding:14px 0}
.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;font:600 1.0625rem/1.4 var(--f-display)}
.faq details p{margin:10px 0 0;max-width:72ch;color:var(--muted)}
.b-src{font-size:.875rem;color:var(--muted);border-top:1px solid var(--line);padding-top:16px;margin-top:28px}
.b-src ul{display:block;padding-left:1.1em;margin:6px 0 0}
.b-src a{color:var(--accent);overflow-wrap:anywhere}
.cards{display:grid;gap:18px}
@media (min-width:700px){.cards{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1050px){.cards{grid-template-columns:repeat(3,1fr)}}
.post{display:grid;gap:8px;align-content:start;text-decoration:none;background:var(--sheet);border:1px solid var(--line);border-radius:var(--r);padding:22px}
.post:hover{border-color:var(--accent)}
.post .d{font:400 .78rem/1.3 var(--f-mono);color:var(--muted)}
.post b{font:600 1.1875rem/1.25 var(--f-display)}
.post span{color:var(--muted);font-size:.9375rem}
.post em{font-style:normal;font-weight:500;color:var(--accent)}
.tag{display:inline-block;font:500 .72rem/1 var(--f-mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--line);padding:5px 8px;color:var(--muted);justify-self:start}
footer{background:var(--ink);color:color-mix(in srgb,var(--paper) 55%,transparent);padding-block:24px;font-size:.8125rem}
footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}
footer a{color:inherit}
footer .f-links{display:flex;flex-wrap:wrap;gap:8px 18px}
.cookie{position:fixed;z-index:30;left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));max-width:620px;margin-inline:auto;background:var(--sheet);color:var(--ink);border:1.5px solid var(--ink);padding:16px 18px;display:grid;gap:12px;font-size:.875rem;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.cookie a{color:var(--accent)}
.cookie-btns{display:flex;flex-wrap:wrap;gap:8px}
.cookie .btn{padding:10px 14px;font-size:.875rem}
.cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
.chips{display:flex;flex-wrap:wrap;gap:10px;list-style:none;padding:0;margin:0}
.chips a{display:inline-block;padding:9px 14px;border:1px solid var(--line);background:var(--sheet);text-decoration:none;font-size:.9375rem;border-radius:var(--r)}
.chips a:hover{border-color:var(--accent)}
.b-body ol.steps{counter-reset:st;list-style:none;padding:0;gap:14px}
.b-body ol.steps>li{counter-increment:st;position:relative;padding-left:46px}
.b-body ol.steps>li::before{content:counter(st,decimal-leading-zero);position:absolute;left:0;top:1px;font:500 .8125rem/1.6 var(--f-mono);color:var(--accent);border:1px solid var(--line);padding:0 6px;background:var(--sheet)}
"""

LOGO = ('<svg class="logo-mark" viewBox="0 0 28 28" aria-hidden="true"><rect x="1" y="1" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M6 21 L14 7 L22 21 M9.5 15.5 H18.5" fill="none" stroke="var(--accent)" stroke-width="2"/></svg>')
ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'

def header(current="blog"):
    cur = lambda k: ' aria-current="page"' if k == current else ""
    return (f'<header class="top"><div class="wrap"><a class="logo" href="/" aria-label="AGREXPERT — на главную">{LOGO}AGREXPERT</a>'
            f'<nav class="nav" aria-label="Разделы"><a href="/#services"{cur("services")}>Услуги</a><a href="/#objects">Объекты</a><a href="/#process">Как работаем</a>'
            f'<a href="/blog/"{cur("blog")}>Блог</a><a href="/#contacts">Контакты</a></nav>'
            f'<a class="btn btn-primary" href="/#audit">{ARROW}<span>Аудит альбома</span></a></div></header>')


FOOTER = ('<footer><div class="wrap"><span>© 2026 AGREXPERT · ИП Романенко О. В., ОГРНИП 326784700162354</span>'
          '<span class="f-links"><a href="/blog/">Блог</a><a href="/privacy/">Политика обработки персональных данных</a><a href="/consent/">Согласие на обработку данных</a></span></div></footer>'
          '<div class="cookie" id="cookie" hidden role="region" aria-label="Уведомление о cookies"><p>Мы используем cookies и сервис Яндекс Метрика, чтобы понимать, как работает сайт. '
          'Подробнее в <a href="/privacy/#cookies">Политике</a>.</p><div class="cookie-btns"><button class="btn btn-primary" type="button" id="ck-yes">Принять</button>'
          '<button class="btn btn-ghost" type="button" id="ck-no">Только необходимые</button></div></div>'
          '<script>(function(){var ID=' + str(METRIKA) + ';function load(){(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();'
          'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
          'ym(ID,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:false});}'
          'var ck=null;try{ck=localStorage.getItem("ck")}catch(e){}var bar=document.getElementById("cookie");'
          'if(ck==="yes")load();else if(ck!=="no")bar.hidden=false;'
          'function set(v){try{localStorage.setItem("ck",v)}catch(e){}bar.hidden=true;if(v==="yes")load();}'
          'document.getElementById("ck-yes").addEventListener("click",function(){set("yes")});'
          'document.getElementById("ck-no").addEventListener("click",function(){set("no")});'
          'document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[href^=\'/#audit\'],a[href^=\'mailto:\'],a[href^=\'https://t.me/\']");'
          'if(a&&window.ym)ym(ID,"reachGoal",location.pathname.indexOf("/services/")===0?"service_cta":"blog_cta");});})();</script>')

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "AGREXPERT", "url": SITE + "/", "email": "order@agrexpert.ru", "telephone": "+79006565574"}


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def human_date(d):
    y, m, dd = (int(x) for x in d.split("-"))
    return f"{dd} {MONTHS[m - 1]} {y}"


def url_of(slug=None):
    return "/blog/" + (f"{slug}/" if slug else "")


# ---------------------------------------------------------------- posts

def load_posts():
    posts = []
    if os.path.isdir(SRC):
        for name in sorted(os.listdir(SRC)):
            if not name.endswith(".html"):
                continue
            raw = open(os.path.join(SRC, name), encoding="utf-8").read()
            m = re.match(r"\s*<!--META\s*(\{.*?\})\s*-->\s*(.*)\Z", raw, re.S)
            if not m:
                raise SystemExit(f"{name}: missing <!--META {{...}} --> header")
            meta = json.loads(m.group(1))
            missing = [k for k in REQUIRED if not meta.get(k)]
            if missing:
                raise SystemExit(f"{name}: missing meta fields {missing}")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["slug"]):
                raise SystemExit(f"{name}: bad slug {meta['slug']!r} (latin, digits, hyphens)")
            meta.update(body=m.group(2).strip(), file=name)
            meta.setdefault("updated", meta["date"])
            meta.setdefault("faq", [])
            meta.setdefault("sources", [])
            meta.setdefault("region", "")
            posts.append(meta)
    slugs = [p["slug"] for p in posts]
    dup = {s for s in slugs if slugs.count(s) > 1}
    if dup:
        raise SystemExit(f"duplicate slugs {sorted(dup)}")
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


# ---------------------------------------------------------------- rendering

def page(title, desc, canonical, ld, crumbs, main_html, og_type="article", robots="index,follow,max-image-preview:large", image="/img/agr-v1-white.webp", current="blog"):
    cr = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for u, n in crumbs[:-1]) + f'<li><span aria-current="page">{esc(crumbs[-1][1])}</span></li>'
    ld_all = [{"@context": "https://schema.org", "@graph": [ORG] + ld}]
    ldj = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in ld_all)
    return ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">'
            f'<link rel="canonical" href="{SITE}{canonical}"><meta name="robots" content="{robots}">'
            f'<link rel="alternate" type="application/rss+xml" title="Блог AGREXPERT" href="{SITE}/blog/rss.xml">'
            f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="AGREXPERT"><meta property="og:locale" content="ru_RU">'
            f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
            f'<meta property="og:url" content="{SITE}{canonical}"><meta property="og:image" content="{SITE}{image}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geologica:wght@400;500;600;700&family=Golos+Text:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'
            f'<style>{CSS}</style>{ldj}</head><body>{header(current)}'
            f'<nav class="crumbs wrap" aria-label="Навигация"><ol>{cr}</ol></nav><main id="top">{main_html}</main>{FOOTER}</body></html>\n')


def aside():
    return ('<aside class="b-aside"><div class="card"><h3>Бесплатный аудит альбома за 24 часа</h3>'
            '<p>Пришлите альбом АГР или АГО до подачи или вместе с замечаниями — вернём список рисков и что с ними делать.</p>'
            f'<a class="btn btn-primary" href="/#audit">{ARROW}<span>Отправить на аудит</span></a></div>'
            '<div class="card"><h3>Написать эксперту</h3><dl><dt>E-mail</dt><dd><a href="mailto:order@agrexpert.ru">order@agrexpert.ru</a></dd>'
            '<dt>Telegram</dt><dd><a href="https://t.me/archirider">@archirider</a></dd></dl>'
            '<p>Просим обращаться письменно: письмо с материалами точно дойдёт до эксперта.</p></div></aside>')


def card(p):
    tag = f'<span class="tag">{esc(p["region"])}</span>' if p["region"] else ""
    return (f'<a class="post" href="{url_of(p["slug"])}">{tag}<span class="d">{human_date(p["date"])}</span>'
            f'<b>{esc(strip_tags(p["h1"]))}</b><span>{esc(p["description"])}</span><em>Читать →</em></a>')


def render_post(p, posts):
    url = url_of(p["slug"])
    h1 = strip_tags(p["h1"])
    ld = [{"@type": "BlogPosting", "headline": h1, "description": p["description"], "datePublished": p["date"], "dateModified": p["updated"],
           "inLanguage": "ru", "mainEntityOfPage": SITE + url, "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}},
          {"@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Блог", "item": SITE + "/blog/"},
              {"@type": "ListItem", "position": 3, "name": h1, "item": SITE + url}]}]
    if p["region"]:
        ld[0]["spatialCoverage"] = p["region"]
    faq = ""
    if p["faq"]:
        ld.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip_tags(f["q"]),
                   "acceptedAnswer": {"@type": "Answer", "text": strip_tags(f["a"])}} for f in p["faq"]]})
        items = "".join(f"<details><summary>{esc(strip_tags(f['q']))}</summary><p>{f['a']}</p></details>" for f in p["faq"])
        faq = f'<section class="sec"><div class="wrap"><h2>Частые вопросы</h2><div class="faq">{items}</div></div></section>'
    src = ""
    if p["sources"]:
        src = '<div class="b-src">Официальные источники:<ul>' + "".join(
            f'<li><a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["title"])}</a></li>' for s in p["sources"]) + "</ul></div>"
    others = [o for o in posts if o["slug"] != p["slug"]][:3]
    rel = f'<section class="sec"><div class="wrap"><h2>Читайте также</h2><div class="cards">{"".join(card(o) for o in others)}</div></div></section>' if others else ""
    kicker = "Блог AGREXPERT" + (f" · {esc(p['region'])}" if p["region"] else "")
    main = (f'<section class="b-hero"><div class="wrap"><p class="eyebrow">{kicker}</p><h1>{p["h1"]}</h1><p class="lead">{p["lead"]}</p>'
            f'<p class="b-meta"><time datetime="{p["date"]}">{human_date(p["date"])}</time> · AGREXPERT, центр градостроительной экспертизы и согласований</p></div></section>'
            f'<div class="wrap b-grid"><article class="b-body">{p["body"]}{src}</article>{aside()}</div>{faq}{rel}')
    title = p["title"] if "AGREXPERT" in p["title"] else f'{p["title"]} | AGREXPERT'
    img = re.search(r'<img[^>]+src="(/img/[^"]+)"', p["body"])
    return page(title, p["description"], url, ld, [("/", "Главная"), ("/blog/", "Блог"), (url, h1)], main,
                image=img.group(1) if img else "/img/agr-v1-white.webp")


def render_index(posts):
    cards = "".join(card(p) for p in posts) or '<p class="lead">Первые статьи скоро.</p>'
    ld = [{"@type": "Blog", "name": "Блог AGREXPERT", "url": SITE + "/blog/", "inLanguage": "ru", "publisher": {"@id": SITE + "/#org"},
           "blogPost": [{"@type": "BlogPosting", "headline": strip_tags(p["h1"]), "url": SITE + url_of(p["slug"]), "datePublished": p["date"]} for p in posts[:30]]}]
    main = ('<section class="b-hero"><div class="wrap"><p class="eyebrow">Блог · АГР и АГО</p><h1>АГР и АГО на практике</h1>'
            '<p class="lead">Как устроены согласования архитектурно-градостроительного решения в Москве и облика в Московской области, '
            'Петербурге и регионах: состав альбома, 3D-модели, причины отказов и что с ними делать.</p></div></section>'
            f'<section class="sec" style="padding-top:40px"><div class="wrap"><h2>Все статьи</h2><div class="cards">{cards}</div></div></section>')
    robots = "index,follow" if posts else "noindex,follow"
    return page("Блог об АГР и АГО: согласование облика зданий | AGREXPERT",
                "Статьи о разработке и согласовании АГР в Москве и АГО в Московской области, Санкт-Петербурге и регионах: порядок, состав альбома, 3D-модели, причины отказов.",
                "/blog/", ld, [("/", "Главная"), ("/blog/", "Блог")], main, og_type="website", robots=robots)


def render_rss(posts):
    items = "".join(f"<item><title>{esc(strip_tags(p['h1']))}</title><link>{SITE}{url_of(p['slug'])}</link><guid>{SITE}{url_of(p['slug'])}</guid>"
                    f"<pubDate>{date.fromisoformat(p['date']).strftime('%a, %d %b %Y')} 07:00:00 +0300</pubDate><description>{esc(p['description'])}</description></item>"
                    for p in posts[:30])
    return ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Блог AGREXPERT</title>'
            f'<link>{SITE}/blog/</link><description>АГР и АГО: разработка и согласование облика зданий</description><language>ru</language>{items}</channel></rss>\n')


# ---------------------------------------------------------------- service pages

SVC_REQUIRED = ["slug", "title", "h1", "description", "lead", "eyebrow", "service_type", "area", "updated"]


def load_services():
    out = []
    if not os.path.isdir(SVC):
        return out
    for name in sorted(os.listdir(SVC)):
        if not name.endswith(".html"):
            continue
        raw = open(os.path.join(SVC, name), encoding="utf-8").read()
        m = re.match(r"\s*<!--META\s*(\{.*?\})\s*-->\s*(.*)\Z", raw, re.S)
        if not m:
            raise SystemExit(f"services/{name}: missing META header")
        meta = json.loads(m.group(1))
        missing = [k for k in SVC_REQUIRED if not meta.get(k)]
        if missing:
            raise SystemExit(f"services/{name}: missing meta fields {missing}")
        meta.update(body=m.group(2).strip(), file="services/" + name)
        meta.setdefault("faq", [])
        meta.setdefault("sources", [])
        meta.setdefault("related", [])
        meta.setdefault("order", 99)
        out.append(meta)
    out.sort(key=lambda x: x["order"])
    return out


def render_service(sv, services, posts):
    url = f"/services/{sv['slug']}/"
    by = {x["slug"]: x for x in services}
    ld = [{"@type": "Service", "name": strip_tags(sv["h1"]), "serviceType": sv["service_type"], "description": sv["description"],
           "areaServed": sv["area"], "provider": {"@id": SITE + "/#org"}, "url": SITE + url},
          {"@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Услуги", "item": SITE + "/#services"},
              {"@type": "ListItem", "position": 3, "name": strip_tags(sv["h1"]), "item": SITE + url}]}]
    faq = ""
    if sv["faq"]:
        ld.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip_tags(f["q"]),
                   "acceptedAnswer": {"@type": "Answer", "text": strip_tags(f["a"])}} for f in sv["faq"]]})
        items = "".join(f"<details><summary>{esc(strip_tags(f['q']))}</summary><p>{f['a']}</p></details>" for f in sv["faq"])
        faq = f'<section class="sec"><div class="wrap"><h2>Частые вопросы</h2><div class="faq">{items}</div></div></section>'
    src = ""
    if sv["sources"]:
        src = '<div class="b-src">Нормативная база и официальные источники:<ul>' + "".join(
            f'<li><a href="{esc(x["url"])}" rel="noopener" target="_blank">{esc(x["title"])}</a></li>' for x in sv["sources"]) + "</ul></div>"
    rel = [by[r] for r in sv["related"] if r in by]
    chips = "".join(f'<li><a href="/services/{r["slug"]}/">{esc(strip_tags(r["h1"]))}</a></li>' for r in rel)
    rel_html = f'<section class="sec"><div class="wrap"><h2>Другие услуги</h2><ul class="chips">{chips}</ul></div></section>' if chips else ""
    linked = [p for p in posts if p.get("service") == url][:3]
    blog_html = f'<section class="sec"><div class="wrap"><h2>Статьи по теме</h2><div class="cards">{"".join(card(p) for p in linked)}</div></div></section>' if linked else ""
    main = (f'<section class="b-hero"><div class="wrap"><p class="eyebrow">{esc(sv["eyebrow"])}</p><h1>{sv["h1"]}</h1><p class="lead">{sv["lead"]}</p>'
            f'<div class="cta-row"><a class="btn btn-primary" href="/#audit">{ARROW}<span>Бесплатный аудит за 24 часа</span></a>'
            '<a class="btn btn-ghost" href="mailto:order@agrexpert.ru">Написать на order@agrexpert.ru</a></div></div></section>'
            f'<div class="wrap b-grid"><article class="b-body">{sv["body"]}{src}</article>{aside()}</div>{faq}{blog_html}{rel_html}')
    title = sv["title"] if "AGREXPERT" in sv["title"] else f'{sv["title"]} | AGREXPERT'
    img = re.search(r'<img[^>]+src="(/img/[^"]+)"', sv["body"])
    return page(title, sv["description"], url, ld, [("/", "Главная"), ("/#services", "Услуги"), (url, strip_tags(sv["h1"]))], main,
                og_type="website", image=img.group(1) if img else "/img/agr-v1-white.webp", current="services")


def check_services(services):
    problems = []
    pages, anchors = known_targets()
    for sv in services:
        f = sv["file"]
        blob = sv["body"] + json.dumps(sv["faq"], ensure_ascii=False)
        for href in re.findall(r'href="(/[^"?]*)"', blob):
            if not link_ok(href, pages, anchors):
                problems.append(f"{f}: internal link {href} does not exist")
        for src in re.findall(r'src="(/[^"]+)"', sv["body"]):
            if not os.path.exists(os.path.join(ROOT, src.lstrip("/"))):
                problems.append(f"{f}: image {src} not found")
        for img in re.findall(r"<img\b[^>]*>", sv["body"]):
            if 'alt="' not in img or 'alt=""' in img:
                problems.append(f"{f}: image without alt text")
        if re.search(r"<h1\b", sv["body"]):
            problems.append(f"{f}: body must not contain <h1>")
        if not 110 <= len(sv["description"]) <= 170:
            problems.append(f"{f}: description is {len(sv['description'])} chars (aim 120-160)")
        if len(strip_tags(sv["title"])) > 70:
            problems.append(f"{f}: title too long")
        for r in sv["related"]:
            if r not in {x["slug"] for x in services}:
                problems.append(f"{f}: related service {r} missing")
    return problems


# ---------------------------------------------------------------- site wiring (idempotent)

def wire_home():
    path = os.path.join(ROOT, "index.html")
    s = open(path, encoding="utf-8").read()
    o = s
    i = s.find('<nav class="nav"')
    j = s.find("</nav>", i)
    if i >= 0 and '<a href="/blog/">' not in s[i:j]:
        s = s[:i] + s[i:j].replace('<a href="#contacts">', '<a href="/blog/">Блог</a>\n      <a href="#contacts">', 1) + s[j:]
    k = s.find('<span class="f-links">')
    if k >= 0 and '<a href="/blog/">Блог</a><a href="/privacy/">' not in s:
        s = s.replace('<span class="f-links"><a href="/privacy/">', '<span class="f-links"><a href="/blog/">Блог</a><a href="/privacy/">', 1)
    if s != o:
        open(path, "w", encoding="utf-8").write(s)
        return True
    return False


def write_sitemap(posts, services=()):
    path = os.path.join(ROOT, "sitemap.xml")
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"\s*<!--blog-->.*?<!--/blog-->", "", s, flags=re.S)
    s = re.sub(r"\s*<!--services-->.*?<!--/services-->", "", s, flags=re.S)
    sv = "".join(f"\n  <url><loc>{SITE}/services/{x['slug']}/</loc><lastmod>{x['updated']}</lastmod></url>" for x in services)
    s = s.replace("\n</urlset>", "\n  <!--services-->" + sv + "\n  <!--/services-->\n</urlset>", 1)
    urls = []
    if posts:
        urls.append(f"  <url><loc>{SITE}/blog/</loc><lastmod>{posts[0]['date']}</lastmod></url>")
        urls += [f"  <url><loc>{SITE}{url_of(p['slug'])}</loc><lastmod>{p['updated']}</lastmod></url>" for p in posts]
    block = "\n  <!--blog-->\n" + "\n".join(urls) + ("\n" if urls else "") + "  <!--/blog-->"
    s = s.replace("\n</urlset>", block + "\n</urlset>", 1)
    open(path, "w", encoding="utf-8").write(s)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)


# ---------------------------------------------------------------- checks

def stems(t):
    return {w[:5] for w in re.findall(r"\w+", strip_tags(t).lower()) if len(w) > 3}


def known_targets():
    pages = set()
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
        if "index.html" in files:
            rel = os.path.relpath(dirpath, ROOT)
            pages.add("/" if rel == "." else f"/{rel}/")
    anchors = set(re.findall(r'\bid="([\w-]+)"', open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()))
    return pages, anchors


def link_ok(href, pages, anchors):
    path, _, frag = href.partition("#")
    if path not in pages:
        return False
    return not frag or path != "/" or frag in anchors


def check(posts):
    problems = []
    pages, anchors = known_targets()
    keywords = {}
    for p in posts:
        f = p["file"]
        blob = p["body"] + json.dumps(p["faq"], ensure_ascii=False)
        for href in re.findall(r'href="(/[^"?]*)"', blob):
            if not link_ok(href, pages, anchors):
                problems.append(f"{f}: internal link {href} does not exist")
        for src in re.findall(r'src="(/[^"]+)"', p["body"]) + [x.split()[0] for ss in re.findall(r'srcset="([^"]+)"', p["body"]) for x in ss.split(",")]:
            if not os.path.exists(os.path.join(ROOT, src.strip().lstrip("/"))):
                problems.append(f"{f}: image {src.strip()} not found")
        for img in re.findall(r"<img\b[^>]*>", p["body"]):
            if 'alt="' not in img or 'alt=""' in img:
                problems.append(f"{f}: image without alt text")
        if re.search(r"&lt;\w", p["body"]):
            problems.append(f"{f}: escaped HTML in body")
        if re.search(r"<h1\b", p["body"]):
            problems.append(f"{f}: body must not contain <h1> (it comes from META)")
        if not 110 <= len(p["description"]) <= 170:
            problems.append(f"{f}: description is {len(p['description'])} chars (aim 120-160)")
        if len(strip_tags(p["title"])) > 70:
            problems.append(f"{f}: title is {len(p['title'])} chars (keep <= 65)")
        need = stems(p["keyword"])
        for field in ("title", "h1"):
            lacking = need - stems(p[field])
            if lacking:
                problems.append(f"{f}: {field} does not contain the keyword '{p['keyword']}' (missing {sorted(lacking)})")
        if not need <= stems(p["body"][:1200]):
            problems.append(f"{f}: keyword '{p['keyword']}' is not in the first paragraph")
        n = len(re.findall(r'href="/', p["body"]))
        if n < 3:
            problems.append(f"{f}: only {n} internal links in body (need 3+)")
        if f'href="{p["service"]}"' not in p["body"]:
            problems.append(f"{f}: body has no link to its service target {p['service']}")
        if not link_ok(p["service"], pages, anchors):
            problems.append(f"{f}: service target {p['service']} does not exist")
        if len(p["faq"]) and not 3 <= len(p["faq"]) <= 6:
            problems.append(f"{f}: FAQ should have 3-6 questions")
        for s in p["sources"]:
            if not s.get("url", "").startswith("https://") or not s.get("title"):
                problems.append(f"{f}: bad source entry {s}")
        for bad in ("+7 900", "+79006565574", "656-55-74"):
            if bad in p["body"]:
                problems.append(f"{f}: phone number in body (contacts are in the template)")
        chars = len(strip_tags(p["body"]))
        if chars < 3000:
            problems.append(f"{f}: body is only {chars} characters — too thin")
        k = p["keyword"].lower().strip()
        if k in keywords:
            problems.append(f"{f}: keyword '{k}' already used by {keywords[k]} (one article per intent)")
        keywords[k] = f
    return problems


def main():
    wired = wire_home()
    posts = load_posts()
    services = load_services()
    for sv in services:
        write(os.path.join(ROOT, "services", sv["slug"], "index.html"), render_service(sv, services, posts))
    base = os.path.join(ROOT, "blog")
    live = {p["slug"] for p in posts}
    if os.path.isdir(base):  # remove pages of deleted/renamed posts
        for d in os.listdir(base):
            if os.path.isdir(os.path.join(base, d)) and d not in live:
                for f in os.listdir(os.path.join(base, d)):
                    os.remove(os.path.join(base, d, f))
                os.rmdir(os.path.join(base, d))
    for p in posts:
        write(os.path.join(base, p["slug"], "index.html"), render_post(p, posts))
    write(os.path.join(base, "index.html"), render_index(posts))
    write(os.path.join(base, "rss.xml"), render_rss(posts))
    write_sitemap(posts, services)
    print(f"built: {len(posts)} post(s), {len(services)} service page(s)" + ("; Блог link added to home page" if wired else ""))
    if "--check" in sys.argv:
        problems = check(posts) + check_services(services)
        for pr in problems:
            print("PROBLEM:", pr)
        if problems:
            sys.exit(1)
        print("check OK")


if __name__ == "__main__":
    main()
