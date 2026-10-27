# AGREXPERT keyword plan

Source: the owner's list (`_blog/keywords-raw.txt`, 2026-10-27), reworked into one search intent per article.
**One article per intent, never one article per phrase.** Search engines understand variants; near-duplicates compete with each other and look like scaled content.

## Rotation (decided by the owner)
Every SECOND article is regional. Count rows in `_blog/LOG.md`:
- even (0, 2, 4 …) → first `todo` topic in **section B (general)**;
- odd (1, 3, 5 …) → first `todo` topic in **section C (regional)**. Section C is already ordered so regions go round: Москва → Московская область → Санкт-Петербург → другие регионы.
If the needed section has no `todo` left, take the other section.
After publishing set the status to `done YYYY-MM-DD /blog/<slug>/`. If a topic turns out too close to a published one, set `merged into <slug>` and take the next.

## Outdated terms people still search
The owner's list uses «Москомархитектура», «МКА», «Постановление 284-ПП». The site says: since 03.12.2025 Москомархитектура is part of ДГП Москвы (свидетельства АГР issues ДГП), and since 30.09.2026 the procedure is 1423-ПП instead of 284-ПП (re-verify in an official source each time). These old words may be used as secondary phrases ("бывшая Москомархитектура", "ранее — 284-ПП") so searchers find the article, but the article must describe the CURRENT order and never present the old one as current.

## A. Commercial phrases → service pages, NOT blog topics
These are "buy" intents. They belong to service pages; in articles use them only as anchor text for links.
The service pages linked from the home page (`/services/agr-moscow/` etc.) do not exist yet. Until a page exists, link to the home-page anchor shown in brackets (the build fails on links to missing pages).

| Service target | Phrases |
|---|---|
| АГР Москва — `/services/agr-moscow/` (now `/#services`) | разработка агр москва цена; получение свидетельства агр стоимость; сопровождение агр под ключ; разработка альбома агр под ключ; согласование агр москва |
| АГО МО — `/services/ago-mo/` (now `/#services`) | заказать проект аго подмосковье; согласование аго в мособлархитектуре стоимость; согласование аго в московской области |
| АГО СПб — `/services/ago-spb/` (now `/#services`) | согласование архитектурно-градостроительного облика санкт-петербург |
| АГО регионы — `/services/ago-regions/` (now `/#services`) | согласование архитектурно градостроительного облика цена |
| Аудит и снятие замечаний — `/services/audit-and-fix/` (now `/#audit`) | аудит альбома аго на соответствие требованиям; устранение замечаний рабочей группы аго; доработка альбома после отказа |
| 3D-модели и ЦИМ — `/services/3d-ifc-models/` (now `/#services`) | выгрузка 3d модели для агр; разработка 3d модели ifc для агр |
| Бесплатный экспресс-аудит — `/#audit` | проверить альбом агр перед подачей |

Not topics at all: «подбор подрядчика на разработку буклета агр» (commercial, home page), «скан свидетельства агр пример заполнения» (would need a real document — never publish clients' documents; skip unless the owner provides an anonymised sample).

## B. General topics (even rows)

| # | Primary phrase (title/H1/slug) | Secondary phrases | Service target | Status |
|---|---|---|---|---|
| B1 | отличие АГО от АГР | чем отличается агр от аго; что такое агр; архитектурно-градостроительный облик что это; свидетельство агр и решение о согласовании аго | /#services | todo |
| B2 | причины отказа в согласовании АГР | причина отказа в выдаче свидетельства агр; отклонение альбома агр что делать; доработка альбома после отказа; повторная подача | /#audit | todo |
| B3 | состав альбома АГР и АГО | что входит в альбом агр; развертки фасадов; фотофиксация; ведомость отделки; колористика | /#services | todo |
| B4 | ТЭП в альбоме АГР | исправление тэп в альбоме агр; несоответствие тэп гпзу; предельные параметры; процент застройки | /#audit | todo |
| B5 | архитектурно-художественная подсветка в альбоме АГО | схема подсветки фасада; освещение в агр | /#services | todo |
| B6 | благоустройство и МАФ в альбоме АГО | раздел благоустройства аго; малые архитектурные формы; покрытия | /#services | todo |
| B7 | развертки фасадов для альбома АГР | развертка по улице; фотофиксация окружающей застройки; ракурсы | /#services | todo |
| B8 | АГО складского комплекса | согласование аго логистического парка; склад вдоль трассы; когда для склада нужен аго | /#services | todo |
| B9 | АГР многоквартирного дома | согласование агр мкд; альбом аго для жилого комплекса | /#services | todo |
| B10 | АГР торгового центра | проект агр трк; входные группы и витрины; вывески и агр | /#services | todo |
| B11 | АГО автомойки, СТО и АЗС | согласование аго автосервиса; придорожный сервис | /#services | todo |
| B12 | АГР гостиницы и апарт-отеля | разработка агр апарт отеля; аго гостиницы | /#services | todo |
| B13 | АГР производственного здания | агр цеха; аго опасного производственного объекта (only what is verified) | /#services | todo |
| B14 | схема транспортного обслуживания в альбоме АГО | транспортная схема; въезды и парковки | /#services | todo |
| B15 | АГО паркинга и гаражного комплекса | согласование аго паркинга; многоуровневый паркинг | /#services | todo |
| B16 | стоимость разработки альбома АГР | от чего зависит цена агр; цена за м2; что входит в цену; круги замечаний — NO numbers unless they are on the site | /#audit | todo |

## C. Regional topics (odd rows), in this order

| # | Region | Primary phrase | Secondary phrases | Service target | Status |
|---|---|---|---|---|---|
| C1 | Москва | получение свидетельства АГР в Москве | порядок согласования агр по 1423-пп; свидетельство об утверждении агр; архитектурная комиссия; дгп вместо москомархитектуры; изменения вместо 284-пп | /#services | todo |
| C2 | Московская область | согласование АГО в Московской области | получение свидетельства аго подмосковье; мособлархитектура; подача через рпгу; регламент согласования аго | /#services | todo |
| C3 | Санкт-Петербург | согласование АГО в Санкт-Петербурге | кга; требования к составу материалов; подача через gu.spb.ru | /#services | todo |
| C4 | Регионы | АГО по статье 40.1 ГрК РФ | пп рф 857; аго в регионах; где смотреть требования в пзз муниципалитета | /#services | todo |
| C5 | Москва | когда АГР в Москве не нужен | нужен ли агр для реконструкции здания; исключения; ижс и некапитальные объекты; магистральные улицы и зоны окн | /#services | todo |
| C6 | Московская область | когда не требуется АГО в Подмосковье | исключения из аго мо; когда не требуется получение свидетельства аго | /#services | todo |
| C7 | Санкт-Петербург | отказ КГА в согласовании облика | замечания кга; повторная подача спб | /#audit | todo |
| C8 | Регионы | АГО в Ленинградской области | (write only if the run finds the official regional procedure; otherwise mark `skipped: no official source` and take C9) | /#services | todo |
| C9 | Москва | 3D-модель для АГР в Москве | требования к 3d модели здания для дгп; нпм и впм; цим в ifc; выгрузка модели на mos.ru | /#services | todo |
| C10 | Московская область | состав альбома АГО для Мособлархитектуры | альбом аго для градостроительного совета мо; состав альбома аго 2026 | /#services | todo |
| C11 | Москва | внесение изменений в свидетельство АГР | корректировка агр; изменение фасадов в ходе стройки; срок действия свидетельства | /#services | todo |
| C12 | Московская область | рабочая группа по АГО в Московской области | рабочая группа аго красногорск; градостроительный совет мо; как проходит рассмотрение | /#audit | todo |

Cities of Moscow Oblast (Красногорск, Одинцово, Мытищи, Химки) are NOT separate articles — the procedure is regional, the same for all. Mention them only where it is naturally true.
When C runs out, ask the owner (in the run report) which regions to add next — never invent region clones.
