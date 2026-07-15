# BH Door Solutions Metro Detroit — Website

Static, SEO-first marketing site for **BH Door Solutions Metro Detroit** — residential & commercial door
installation and repair serving metro Detroit and suburbs within 35 miles (Wayne, Oakland & Macomb counties).

- **Phone:** (313) 236-4558 · **Email:** info@bhdoorsolutionsmetrodetroit.com
- **Hours:** Sun–Thu 9am–5pm · Fri 9am–12pm · Sat closed
- **Domain:** https://bhdoorsolutionsmetrodetroit.com
- **Host:** GitHub Pages (custom domain via `CNAME`)
- **Analytics:** Matomo (site ID 21)

## Structure

```
/                       Homepage
/services/              Services hub  → 10 service pages
/service-areas/         Areas hub     → 18 city pages
/about/  /contact/  /reviews/  /financing/  /gallery/  /faq/  /thank-you/
/assets/  css · js · fonts (self-hosted) · img (WebP + logo/favicons)
sitemap.xml · robots.txt · site.webmanifest · CNAME · 404.html
```

## Build

The HTML is generated from data + templates (no framework, no build tools beyond Python):

```bash
python scripts/build.py            # regenerate all pages from scripts/_copy.json
python scripts/generate_images.py  # (re)generate imagery via the Gemini API
```

- **Content** lives in `scripts/_copy.json` (page copy) and `scripts/build.py` (business data, metadata, templates,
  JSON-LD, shared copy).
- Edit copy/metadata, then rerun `build.py`. Output HTML is committed so GitHub Pages can serve it directly.

## SEO features

Unique title/description/canonical per page · JSON-LD (`HomeAndConstructionBusiness`, `Service`, `FAQPage`,
`BreadcrumbList`, `GeoCircle` service radius, **no street address** — service-area business) · Open Graph + Twitter
cards · XML sitemap + robots · clean directory URLs · internal hub-and-spoke linking · mobile-first + tap-to-call ·
self-hosted fonts + WebP for Core Web Vitals · accessible semantics.

See **CONTENT-TODO.md** for the handful of client-supplied values to fill in before/after launch.
