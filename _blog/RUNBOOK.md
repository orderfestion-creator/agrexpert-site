# AGREXPERT blog — runbook for each scheduled run

Site: https://agrexpert.ru — AGREXPERT, центр градостроительной экспертизы и согласований (ИП Романенко О. В.): разработка и согласование АГР в Москве (ДГП), АГО в Московской области, Санкт-Петербурге и регионах, 3D-модели НПМ/ВПМ и ЦИМ в IFC, аудит альбомов и снятие замечаний.
Readers: ГИПы, ГАПы, архитекторы, девелоперы и технические заказчики with a real object. Write for professionals: precise, no beginner filler.
Blog: https://agrexpert.ru/blog/ — Russian only. Two articles a week (Mon, Thu). Every second article is regional (see `_blog/KEYWORDS.md`).
The owner chose to publish immediately (no manual approval step). That makes the self-review in step 6 mandatory.

AGREXPERT is a separate brand. Never mention, link to or copy from itzbpla.ru, architeam.me, varimo.me, leustech.me.

## How publishing works
1. Article source: `_blog/posts/YYYY-MM-DD-<slug>.html`: META JSON header + HTML body. Copy the structure of the newest existing post (or the template at the end of this file).
2. `python3 _blog/build.py --check` builds `/blog/`, `/blog/<slug>/`, `/blog/rss.xml`, adds blog URLs to `sitemap.xml` and the «Блог» link on the home page. It must print `check OK`.
3. Commit everything and push to `main`. GitHub Actions (`.github/workflows/deploy.yml`) rebuilds, validates and uploads to Sprinthost over FTP.
4. `send.php` and `private/` (Telegram bot token, saved leads) exist only on the server. Never create, commit or upload them.
5. Do not edit generated `blog/` pages by hand. Do not change `index.html`, `privacy/`, `consent/` except what build.py does.

## Steps for a run
1. Read `_blog/KEYWORDS.md` and `_blog/LOG.md`. Even number of rows → first `todo` in section B; odd → first `todo` in section C. Never write about section A phrases.
2. Read `index.html` (services, process, FAQ, "что изменилось в 2026") so the article agrees with what the site says. If the site and an official source disagree, follow the official source in the article, and say so in the run report so the owner can fix the site.
3. Research with WebSearch / WebFetch:
   - **Official sources first**: mos.ru (ДГП), the text of the Moscow/regional resolution in its current wording (pravo.gov.ru, mos.ru/authority, docs of mosreg.ru, gov.spb.ru / kga.gov.spb.ru, consultant.ru or garant.ru for the current редакция), ГрК РФ ст. 40.1, ПП РФ № 857.
   - Then what professionals ask and what competitors answer, to find gaps. Never copy text.
4. Write the article following the SEO and article rules below.
5. Run `python3 _blog/build.py --check`. Fix every PROBLEM line.
6. **Self-review before publishing.** Re-read as a sceptical ГИП and as a reviewer of the commission:
   - Every regulatory statement (resolution number and date, which body reviews, composition of materials, review period, who may apply, exceptions, validity term): verified in an official source during THIS run, and that source is in META "sources" and/or linked in the text. Not verified → remove it or say «зависит от объекта и территории — проверяем для вашего случая». Never state fees, penalties or deadlines from memory.
   - Changes in law: if a rule changed recently (e.g. 284-ПП → 1423-ПП, Москомархитектура → ДГП), state which rule applies to which applications, as the official source says.
   - AGREXPERT's own terms, prices and deadlines: only exactly as on the site (`index.html`) and with a link to it. The site currently publishes no prices — do not invent any. If two places on the site disagree, quote neither.
   - No invented projects, clients, addresses, reviews, statistics, licences or people. The only real case material is in `_blog/PHOTOS.md`.
   - Same review for title, description, lead and FAQ answers (they appear in search and structured data).
   - Natural professional Russian, «вы», no keyword stuffing, no repeated phrases, no "в современном мире".
   - Does it answer the intent better than the current top results? Would the reader still need to search again? Fix gaps.
7. Update `_blog/KEYWORDS.md` (status → `done YYYY-MM-DD /blog/<slug>/`) and add a row to `_blog/LOG.md` with status "not live".
8. `git add -A && git commit -m "Blog: <title>" && git push origin main` (do `git fetch origin main` and rebase first if needed).
9. Wait for the deploy: `gh run list --repo orderfestion-creator/agrexpert-site --limit 1` every ~20 s until completed. On success set the LOG row to "live" (small extra commit + push). On failure `gh run view <id> --log-failed` and report.
10. Report to the owner in Russian, short: title, link, primary keyword, region (if any), one line about the content, plus any site/official-source mismatch found in step 2.

## If something is broken
- `git push` fails or the repo is unreachable: do NOT write a second article. Tell the owner what failed and that GitHub access needs fixing (claude.ai → Settings → Connectors → GitHub, access to agrexpert-site). Put the article text in the message.
- Deploy fails on the FTP step: report the error line (most likely the FTP_PASSWORD secret was changed/removed, or the server folder differs). Retry at most once.
- A previous LOG row is "not live": fix/publish it first, no second article in the same run.
- Queues empty: report and stop. Do not invent topics.

## SEO rules (Google Search Central and Yandex guidance, October 2026)
- People-first: written for a ГИП/developer who must get the object through the commission. Leave them able to plan the work, avoid a refusal and send a good enquiry.
- Show first-hand practice: what we check first (ГПЗУ, ТЭП, окружение, ОКН, магистрали), what goes into the album and models, where albums get returned and why, how to answer remarks. Concrete — nothing that could be on any website.
- YMYL-adjacent (legal procedure, money, deadlines): accuracy first; when it depends on the object or territory, say so plainly.
- Yandex: original text, no keyword stuffing, clear structure; the Яндекс Метрика counter is in the template (loaded after cookie consent).
- One search intent per article; never two articles for the same intent (build fails on a repeated keyword).
- Regional articles: only what really differs in that region (body, legal basis, portal, composition, exceptions, review). No doorway clones with a swapped city name. Moscow Oblast cities are not separate articles.
- Usually 5,000–10,000 characters of body text; never pad.
- On-page: primary phrase in title (≤ 65 chars, near the start), H1, slug, first paragraph, META keyword, and naturally in one H2. Description 120–160 chars, includes the primary phrase. Secondary phrases in H2/H3/body where they fit, once or twice each.
- Structure: direct answer in the first paragraph; H2 sections matching real questions; a table where it helps decide (e.g. Москва / МО / СПб, или «нужно / не нужно»); numbered "типичные ошибки"; "что прислать на аудит" list.
- Internal links: 3+ in the body. One to the topic's service target from KEYWORDS.md, using a section-A phrase as anchor text; `/#audit` (бесплатный аудит за 24 часа) where natural; 1–2 earlier blog posts when genuinely related (optionally add a link back from an older related post by editing its source). The build fails on links to pages/anchors that do not exist. When the `/services/...` pages appear on the site, switch to them and update section A.
- External links: only to official sources (rel="noopener" target="_blank" is fine). List them in META "sources" too.
- FAQ in META: 4–6 real questions, short accurate answers.
- Authorship: AGREXPERT (organization). Never invent people or credentials.

## Article rules
- Body HTML allowed: h2, h3, p, strong, em, a, ul, ol, li, `<div class="table-wrap"><table>…</table></div>`, `<div class="blog-note"><p>…</p></div>` (warning, e.g. typical reason for refusal), figure (see `_blog/PHOTOS.md`). No h1 in the body.
- Terms: АГР — архитектурно-градостроительное решение (Москва); АГО — архитектурно-градостроительный облик (МО, СПб, регионы); ДГП, ГПЗУ, ТЭП, НПМ/ВПМ, ЦИМ, ОКН — expand each on first use.
- Contacts are in the template; don't paste phone numbers into the body.
- META "region": "" for general topics; "Москва", "Московская область", "Санкт-Петербург" or the region name for section C.

## Template
```
<!--META
{
  "slug": "otlichie-ago-ot-agr",
  "date": "2026-11-02",
  "title": "…",
  "h1": "…",
  "description": "…",
  "lead": "…",
  "keyword": "отличие АГО от АГР",
  "region": "",
  "service": "/#services",
  "faq": [{"q": "…", "a": "…"}],
  "sources": [{"title": "Градостроительный кодекс РФ, ст. 40.1", "url": "https://…"}]
}
-->
<p>Direct answer with the primary phrase…</p>
<h2>…</h2>
```
