# Content & Setup TODO — before / soon after launch

The site is fully built and SEO-ready. A few values are **intentionally left as placeholders** so we never publish
fabricated business data. Fill these in (edit `scripts/build.py`, then run `python scripts/build.py` to rebuild),
or ask and we'll do it.

## 🔴 Do before / right after launch

1. **Contact form** — ✅ **working.** Submissions post to a Cloudflare Worker (`bh-door-form`,
   `https://bh-door-form.oren-siyonov.workers.dev`) that emails the lead to **info@bhdoorsolutionsmetrodetroit.com**
   via Resend (from `leads@gothamsitestudio.com`), then redirects to `/thank-you/`.
   - Worker source: `../bh-door-form-worker/` (deploy with `npx wrangler deploy`; the Resend key is a Worker
     secret, not in code).
   - **To change who receives leads:** edit `TO` in `bh-door-form-worker/src/index.js` and redeploy.
   - Confirm `info@bhdoorsolutionsmetrodetroit.com` forwards to a real inbox (Namecheap email forwarding).

2. **Google Business Profile (GBP)** — set up GBP as a **service-area business** (hide address, list the service-area
   cities). This is the #1 local-ranking lever for an address-less business. Then set `BIZ["google"]` (and
   `facebook` / `instagram`) in `build.py` so the footer, reviews page, and schema `sameAs` link to real profiles.

3. **License number** — set `BIZ["license_no"]` in `build.py` (shows in the footer). **Confirm the "Licensed &
   Insured" claim is accurate.** If the business is not yet licensed/insured, remove those trust badges
   (`TRUST_ITEMS`, `HERO_CHIPS`, sidebar lists) — do not claim it otherwise.

4. **Submit sitemap** — after DNS is live and HTTPS works, submit `https://bhdoorsolutionsmetrodetroit.com/sitemap.xml`
   to **Google Search Console** and **Bing Webmaster Tools** (both are already connected via MCP if you want us to).

## 🟡 Verify / customize

5. **Reviews** — the site does **not** publish any fabricated reviews or star ratings (per Google's guidelines).
   Once you collect real Google reviews, we can add them plus `AggregateRating` schema for star rich-results.
6. **Brands installed** — `BRANDS` list is Therma-Tru, ProVia, Pella, Andersen, Masonite, LARSON. Adjust to the
   brands you actually install/service.
7. **Financing** — `/financing/` is written generically ("options on approved credit"). Confirm your real lender/terms.
8. **Business hours** — set to **Sun–Thu 9am–5pm · Fri 9am–12pm · Sat closed** (top bar, footer, contact page, and
   schema `openingHoursSpecification`). The site makes **no 24/7 or after-hours claims**. Confirm the hours are right.
9. **Cost guide** — `/services/door-installation-cost/` uses *typical* market price ranges for education, always
   pointing to a free exact estimate. Confirm the ranges are in line with your pricing.
10. **Gallery** — `/gallery/` uses representative imagery. Swap in real, geo-tagged project photos when available
    (great for local SEO).

## ✅ Already done
- Matomo analytics installed on every page (site ID **21**, `matomo.alphalockandsafe.com`).
- 37 pages: home, 10 services, services hub, 18 city pages, areas hub, about, contact, reviews, financing, gallery, FAQ.
- Full technical SEO: unique titles/descriptions, canonicals, JSON-LD (HomeAndConstructionBusiness + Service + FAQPage
  + BreadcrumbList, no street address, GeoCircle service radius), Open Graph + Twitter cards, sitemap.xml, robots.txt,
  clean directory URLs, self-hosted fonts, WebP images, mobile tap-to-call, accessibility.

## How to rebuild after edits
```
cd "bh door solutions metro detroit"
python scripts/build.py        # regenerates all HTML from _copy.json + build.py
```
To regenerate images: `python scripts/generate_images.py` (needs the Gemini API key file).
