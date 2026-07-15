#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Static site generator for BH Door Solutions Metro Detroit.
Consumes scripts/_copy.json (produced by the copywriting workflow) + metadata below,
and emits a fully SEO-optimized static site (clean directory URLs, JSON-LD, sitemap,
robots, manifest, Matomo). Run:  python scripts/build.py
"""
import json, os, html, datetime, re, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY = json.load(open(os.path.join(ROOT, "scripts", "_copy.json"), encoding="utf-8"))
TODAY = datetime.date.today().isoformat()

def _asset_ver():
    """Content hash of CSS/JS so browsers refetch only when they actually change."""
    h = hashlib.md5()
    for f in ("assets/css/styles.css", "assets/css/fonts.css", "assets/js/main.js"):
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            h.update(open(p, "rb").read())
    return h.hexdigest()[:8]
ASSET_VER = _asset_ver()

# --------------------------------------------------------------------------- #
#  BUSINESS
# --------------------------------------------------------------------------- #
BIZ = dict(
    name="BH Door Solutions Metro Detroit",
    short="BH Door Solutions",
    phone="(313) 236-4558",
    tel="+13132364558",
    telplain="3132364558",
    email="info@bhdoorsolutionsmetrodetroit.com",
    domain="bhdoorsolutionsmetrodetroit.com",
    base="https://bhdoorsolutionsmetrodetroit.com",
    area_line="Serving Metro Detroit & suburbs within 35 miles",
    counties=["Wayne County", "Oakland County", "Macomb County"],
    hours_short="Sun–Thu 9am–5pm · Fri 9am–12pm",
    hours_full="Sun–Thu 9am–5pm · Fri 9am–12pm · Sat closed",
    lat=42.45, lng=-83.15, radius=56327,
    facebook="", instagram="", google="",   # placeholders — set real profile URLs
    license_no="",                            # placeholder — client to confirm
)

# --------------------------------------------------------------------------- #
#  INLINE SVG ICONS  (stroke uses currentColor)
# --------------------------------------------------------------------------- #
def _svg(p, fill=False, vb="0 0 24 24"):
    a = ('fill="currentColor" stroke="none"' if fill else
         'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"')
    return f'<svg viewBox="{vb}" {a} aria-hidden="true">{p}</svg>'

ICONS = {
 "phone": _svg('<path d="M6.5 3.5h3l1.5 4-2 1.5a12 12 0 0 0 5 5l1.5-2 4 1.5v3a2 2 0 0 1-2 2A16.5 16.5 0 0 1 4.5 5.5a2 2 0 0 1 2-2Z"/>'),
 "arrow": _svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
 "check": _svg('<path d="M20 6 9 17l-5-5"/>'),
 "star": _svg('<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 17l-5.2 2.7 1-5.8L3.5 9.7l5.9-.9z"/>', fill=True),
 "clock": _svg('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>'),
 "shield": _svg('<path d="M12 3l7 3v5c0 4.5-3 7.8-7 9-4-1.2-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>'),
 "wrench": _svg('<path d="M14.5 6a3.8 3.8 0 0 0 4.9 4.9l-8 8a2.6 2.6 0 0 1-3.7-3.7z"/><path d="M14.5 6l-2.2-2.2M6.5 14.5 4.3 12.3"/>'),
 "door": _svg('<path d="M6 20V5a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v15"/><path d="M4 20h16"/><circle cx="14.5" cy="12" r="1" fill="currentColor" stroke="none"/>'),
 "mappin": _svg('<path d="M12 21s6.5-5.6 6.5-10.5A6.5 6.5 0 0 0 5.5 10.5C5.5 15.4 12 21 12 21Z"/><circle cx="12" cy="10.5" r="2.3"/>'),
 "mail": _svg('<rect x="3.5" y="5" width="17" height="14" rx="2"/><path d="m4 6.5 8 6 8-6"/>'),
 "chevron": _svg('<path d="m6 9 6 6 6-6"/>'),
 "bolt": _svg('<path d="M13 2 4.5 13.5H11l-1 8.5L19.5 10H13z"/>', fill=True),
 "building": _svg('<rect x="5" y="3.5" width="14" height="17" rx="1"/><path d="M9 8h2M13 8h2M9 12h2M13 12h2M9 16h2M13 16h2"/>'),
 "lock": _svg('<rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>'),
 "wind": _svg('<path d="M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h9a2.5 2.5 0 1 1-2.5 2.5"/>'),
 "panels": _svg('<rect x="4" y="3.5" width="7" height="17" rx="1"/><rect x="13" y="3.5" width="7" height="17" rx="1"/>'),
 "slide": _svg('<rect x="3.5" y="4" width="17" height="16" rx="1"/><path d="M12 4v16"/><path d="M15 10v4"/>'),
 "frame": _svg('<rect x="4.5" y="3.5" width="15" height="17" rx="1"/><rect x="8" y="7" width="8" height="13"/>'),
 "dollar": _svg('<path d="M12 3v18"/><path d="M16 7.5a3.5 3 0 0 0-4-2.5c-2 0-3.5 1-3.5 3s1.6 2.6 3.5 3 3.8 1 3.8 3.2S14 20 12 20a3.6 3 0 0 1-4-2.5"/>'),
 "truck": _svg('<path d="M3 6.5h11v9H3zM14 9.5h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17.5" cy="17.5" r="1.8"/>'),
 "badge": _svg('<circle cx="12" cy="10" r="6.5"/><path d="M8.5 15 7 21l5-2 5 2-1.5-6"/><path d="m9.5 10 1.7 1.7 3.3-3.3"/>'),
 "users": _svg('<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><path d="M16 5.2a3.2 3.2 0 0 1 0 6.1M17 20a5.5 5.5 0 0 0-2-4.3"/>'),
 "calendar": _svg('<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 9h16M8 3v4M16 3v4"/>'),
 "spark": _svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>'),
 "home": _svg('<path d="M4 11 12 4l8 7"/><path d="M6 10v10h12V10"/><path d="M10 20v-6h4v6"/>'),
 "leaf": _svg('<path d="M5 19c0-8 6-14 14-14 0 8-6 14-14 14Z"/><path d="M5 19c3-3 6-5 9-6"/>'),
 "hand": _svg('<path d="M9 11V5.5a1.5 1.5 0 0 1 3 0V11m0-1V4.5a1.5 1.5 0 0 1 3 0V11m0-.5a1.5 1.5 0 0 1 3 0V15a6 6 0 0 1-6 6h-1a6 6 0 0 1-5.2-3L4 13.5a1.6 1.6 0 0 1 2.7-1.7L8 13.5"/><path d="M6 8V5.5a1.5 1.5 0 0 1 3 0V11"/>'),
 "facebook": _svg('<path d="M14 8.5V6.8c0-.8.4-1.3 1.4-1.3H17V2.6h-2.4c-2.4 0-3.6 1.4-3.6 3.7v2.2H9v3h2v8h3v-8h2.2l.5-3z"/>', fill=True),
 "instagram": _svg('<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1.1" fill="currentColor" stroke="none"/>'),
 "google": _svg('<path d="M21 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.1a4.4 4.4 0 0 1-1.9 2.9v2.4h3.1c1.8-1.7 2.7-4.1 2.7-7.1z"/><path d="M12 21c2.4 0 4.5-.8 6-2.2l-3.1-2.4c-.8.6-1.9 1-2.9 1a5 5 0 0 1-4.7-3.5H4.1v2.4A9 9 0 0 0 12 21z"/><path d="M7.3 13.9a5.4 5.4 0 0 1 0-3.4V8.1H4.1a9 9 0 0 0 0 8.1z"/><path d="M12 6.6c1.3 0 2.5.5 3.4 1.4l2.6-2.6A9 9 0 0 0 4.1 8.1l3.2 2.4A5 5 0 0 1 12 6.6z"/>', fill=True),
}
def ico(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<span{c}>{ICONS.get(name, ICONS["check"])}</span>' if cls else ICONS.get(name, ICONS["check"])

# --------------------------------------------------------------------------- #
#  SERVICE + CITY METADATA  (merged with copy at build time)
# --------------------------------------------------------------------------- #
SVC_META = [
 ("entry-door-installation", "Entry & Front Doors", "door", "svc-entry", "Installation"),
 ("patio-door-installation", "Patio & Sliding Doors", "slide", "svc-patio", "Installation"),
 ("storm-door-installation", "Storm & Screen Doors", "wind", "svc-storm", "Installation"),
 ("interior-door-installation", "Interior Doors", "panels", "svc-interior", "Installation"),
 ("door-repair", "Door Repair", "wrench", "svc-repair", "Repair"),
 ("sliding-door-repair", "Sliding Door Repair", "slide", "svc-sliding-repair", "Repair"),
 ("door-frame-repair", "Door Frame & Jamb Repair", "frame", "svc-frame", "Repair"),
 ("lock-hardware-installation", "Locks & Hardware", "lock", "svc-lock", "Repair"),
 ("commercial-door-repair", "Commercial Doors", "building", "svc-commercial", "Commercial"),
 ("door-installation-cost", "Cost Guide", "dollar", "svc-cost", "Planning"),
]
SVC_ORDER = [s[0] for s in SVC_META]
SVC_INFO = {s[0]: dict(nav=s[1], icon=s[2], img=s[3], group=s[4]) for s in SVC_META}

RELATED = {
 "entry-door-installation": ["storm-door-installation","door-frame-repair","lock-hardware-installation","door-installation-cost"],
 "patio-door-installation": ["sliding-door-repair","entry-door-installation","interior-door-installation","door-installation-cost"],
 "storm-door-installation": ["entry-door-installation","door-frame-repair","door-repair","door-installation-cost"],
 "interior-door-installation": ["entry-door-installation","patio-door-installation","door-repair","lock-hardware-installation"],
 "door-repair": ["door-frame-repair","sliding-door-repair","lock-hardware-installation","entry-door-installation"],
 "sliding-door-repair": ["patio-door-installation","door-repair","door-frame-repair","storm-door-installation"],
 "door-frame-repair": ["door-repair","lock-hardware-installation","entry-door-installation","storm-door-installation"],
 "lock-hardware-installation": ["door-repair","door-frame-repair","entry-door-installation","interior-door-installation"],
 "commercial-door-repair": ["door-frame-repair","lock-hardware-installation","door-repair","door-installation-cost"],
 "door-installation-cost": ["entry-door-installation","patio-door-installation","storm-door-installation","door-repair"],
}

CITY_META = {
 "warren": ("Macomb", ["sterling-heights","clinton-township","royal-oak"], ["entry-door-installation","storm-door-installation","door-repair","door-frame-repair"]),
 "sterling-heights": ("Macomb", ["warren","clinton-township","shelby-township"], ["entry-door-installation","patio-door-installation","storm-door-installation","door-repair"]),
 "dearborn": ("Wayne", ["livonia","southfield","canton"], ["entry-door-installation","storm-door-installation","door-repair","door-frame-repair"]),
 "troy": ("Oakland", ["birmingham","rochester-hills","royal-oak"], ["entry-door-installation","patio-door-installation","interior-door-installation","lock-hardware-installation"]),
 "livonia": ("Wayne", ["canton","farmington-hills","northville"], ["entry-door-installation","patio-door-installation","door-repair","storm-door-installation"]),
 "canton": ("Wayne", ["livonia","northville","farmington-hills"], ["entry-door-installation","patio-door-installation","interior-door-installation","door-installation-cost"]),
 "farmington-hills": ("Oakland", ["novi","southfield","livonia"], ["entry-door-installation","patio-door-installation","interior-door-installation","lock-hardware-installation"]),
 "rochester-hills": ("Oakland", ["troy","shelby-township","birmingham"], ["entry-door-installation","patio-door-installation","lock-hardware-installation","interior-door-installation"]),
 "novi": ("Oakland", ["farmington-hills","northville","troy"], ["entry-door-installation","patio-door-installation","interior-door-installation","door-installation-cost"]),
 "southfield": ("Oakland", ["farmington-hills","royal-oak","ferndale"], ["entry-door-installation","door-repair","storm-door-installation","commercial-door-repair"]),
 "royal-oak": ("Oakland", ["ferndale","birmingham","troy"], ["entry-door-installation","patio-door-installation","interior-door-installation","door-repair"]),
 "st-clair-shores": ("Macomb", ["clinton-township","warren","grosse-pointe-woods"], ["patio-door-installation","entry-door-installation","storm-door-installation","door-frame-repair"]),
 "shelby-township": ("Macomb", ["sterling-heights","rochester-hills","clinton-township"], ["entry-door-installation","patio-door-installation","interior-door-installation","door-installation-cost"]),
 "clinton-township": ("Macomb", ["sterling-heights","warren","shelby-township"], ["door-repair","entry-door-installation","storm-door-installation","door-frame-repair"]),
 "birmingham": ("Oakland", ["royal-oak","troy","ferndale"], ["entry-door-installation","patio-door-installation","interior-door-installation","lock-hardware-installation"]),
 "ferndale": ("Oakland", ["royal-oak","southfield","birmingham"], ["entry-door-installation","patio-door-installation","door-repair","interior-door-installation"]),
 "grosse-pointe-woods": ("Wayne", ["st-clair-shores","warren","clinton-township"], ["entry-door-installation","patio-door-installation","lock-hardware-installation","interior-door-installation"]),
 "northville": ("Wayne", ["novi","canton","livonia"], ["entry-door-installation","patio-door-installation","interior-door-installation","door-installation-cost"]),
}
CITY_ORDER = [c["slug"] for c in COPY["cities"]] if COPY.get("cities") else list(CITY_META.keys())

# lookup dicts from copy
SVC_COPY = {s["slug"]: s for s in COPY["services"]}
CITY_COPY = {c["slug"]: c for c in COPY["cities"]}
CORE = COPY["core"]

# --------------------------------------------------------------------------- #
#  SHARED COPY
# --------------------------------------------------------------------------- #
VALUE_PROPS = [
 ("clock","Fast, Same-Day Service","Need it handled today? We move quickly across metro Detroit and get to your door the same day whenever our schedule allows — no waiting weeks for a fix."),
 ("mappin","Local Metro Detroit Specialists","We know Michigan homes and Michigan weather. From Wayne to Oakland to Macomb County, we're right around the corner."),
 ("door","The Only Door Company You'll Need","Entry, patio, storm, interior, and commercial doors — installation and repair, residential and commercial, all under one call."),
 ("hand","Honest, Upfront Pricing","Clear flat-rate quotes and free, no-obligation estimates. No surprises, no pressure, no hard sell — ever."),
 ("truck","One-Visit Fix","Our trucks come fully stocked so most jobs are finished the first time we're out — no waiting on a second trip."),
 ("spark","Curb-Appeal Upgrade","A new door doesn't just work better — it transforms your entryway and boosts your home's value and efficiency."),
]
PROCESS = [
 ("Call or Book Online","Tell us what's going on — a drafty front door, a slider off its track, a break-in. We'll answer your questions and schedule a visit that works for you."),
 ("Free On-Site Estimate","We measure, assess, and give you a clear, flat-rate quote in plain English — with honest options at every price point. No obligation."),
 ("Expert Installation or Repair","Our fully-stocked trucks mean most jobs are done in one visit. We install and repair clean, level, weather-tight, and to code."),
 ("Backed by Our Guarantee","We stand behind our workmanship and clean up before we leave. Your doors open smooth, seal tight, and lock secure — guaranteed."),
]
TRUST_ITEMS = [
 ("shield","Licensed & Insured"),
 ("clock","Same-Day Service Available"),
 ("dollar","Free, No-Obligation Estimates"),
 ("badge","Workmanship Guarantee"),
 ("mappin","Local Metro Detroit Team"),
 ("hand","Financing Available"),
]
HERO_CHIPS = [("shield","Licensed & Insured"),("clock","Same-Day Service"),("dollar","Free Estimates"),("badge","Workmanship Guarantee")]
BRANDS = ["Therma-Tru","ProVia","Pella","Andersen","Masonite","LARSON"]

# --------------------------------------------------------------------------- #
#  HELPERS
# --------------------------------------------------------------------------- #
def esc(s): return html.escape(str(s), quote=True)
def U(path): return path if path.startswith("http") else BIZ["base"] + path

def svc_url(slug): return f"/services/{slug}/"
def city_url(slug): return f"/service-areas/{slug}/"
def city_name(slug): return CITY_COPY[slug]["city"]

def paras(lst): return "".join(f"<p>{esc_inline(p)}</p>" for p in lst)
def esc_inline(s):
    # allow simple emphasis by escaping then leaving text; keep it plain-safe
    return esc(s)

TOP_CITIES = ["warren","sterling-heights","troy","livonia","royal-oak","dearborn","canton","novi"]

# --------------------------------------------------------------------------- #
#  MATOMO  (exact snippet supplied by client)
# --------------------------------------------------------------------------- #
MATOMO = """<!-- Matomo -->
<script>
  var _paq = window._paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(["setDocumentTitle", document.domain + "/" + document.title]);
  _paq.push(["setCookieDomain", "*.bhdoorsolutionsmetrodetroit.com"]);
  _paq.push(["setDomains", ["*.bhdoorsolutionsmetrodetroit.com"]]);
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://matomo.alphalockandsafe.com/matomo/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '21']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img referrerpolicy="no-referrer-when-downgrade" src="https://matomo.alphalockandsafe.com/matomo/matomo.php?idsite=21&amp;rec=1" style="border:0;" alt="" /></p></noscript>
<!-- End Matomo Code -->"""

# --------------------------------------------------------------------------- #
#  JSON-LD
# --------------------------------------------------------------------------- #
def business_node():
    area = [{"@type":"City","name":city_name(s)+", MI"} for s in CITY_ORDER]
    area += [{"@type":"AdministrativeArea","name":c} for c in BIZ["counties"]]
    area += [{"@type":"AdministrativeArea","name":"Metropolitan Detroit"}]
    node = {
        "@type": ["HomeAndConstructionBusiness","GeneralContractor","LocalBusiness"],
        "@id": BIZ["base"] + "/#business",
        "name": BIZ["name"],
        "alternateName": BIZ["short"],
        "url": BIZ["base"] + "/",
        "telephone": BIZ["tel"],
        "email": BIZ["email"],
        "image": U("/assets/img/hero-home.jpg"),
        "logo": U("/assets/img/icon-512.png"),
        "description": "Residential and commercial door installation and repair serving metro Detroit and suburbs within 35 miles — entry, patio, storm, interior, and commercial doors, plus fast same-day repairs.",
        "priceRange": "$$",
        "areaServed": area,
        "address": {"@type":"PostalAddress","addressLocality":"Detroit","addressRegion":"MI","addressCountry":"US"},
        "serviceArea": {"@type":"GeoCircle",
            "geoMidpoint":{"@type":"GeoCoordinates","latitude":BIZ["lat"],"longitude":BIZ["lng"]},
            "geoRadius": BIZ["radius"]},
        "openingHoursSpecification": [
            {"@type":"OpeningHoursSpecification","dayOfWeek":["Sunday","Monday","Tuesday","Wednesday","Thursday"],"opens":"09:00","closes":"17:00"},
            {"@type":"OpeningHoursSpecification","dayOfWeek":["Friday"],"opens":"09:00","closes":"12:00"}],
        "knowsAbout":["Door installation","Door repair","Entry doors","Patio doors","Storm doors","Interior doors","Commercial doors","Door frame repair"],
    }
    same = [x for x in [BIZ["facebook"],BIZ["instagram"],BIZ["google"]] if x]
    if same: node["sameAs"] = same
    return node

def website_node():
    return {"@type":"WebSite","@id":BIZ["base"]+"/#website","url":BIZ["base"]+"/",
            "name":BIZ["name"],"publisher":{"@id":BIZ["base"]+"/#business"}}

def breadcrumb_node(items):
    return {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":U(u)} for i,(n,u) in enumerate(items)]}

def faq_node(faqs):
    return {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def service_node(name, slug, desc, areas=None):
    node = {"@type":"Service","name":name,"serviceType":name,
            "provider":{"@id":BIZ["base"]+"/#business"},
            "url":U(svc_url(slug)),"description":desc,
            "areaServed":[{"@type":"City","name":city_name(s)+", MI"} for s in (areas or TOP_CITIES)]}
    return node

def jsonld(graph):
    return ('<script type="application/ld+json">' +
            json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, separators=(",",":")) +
            "</script>")

# --------------------------------------------------------------------------- #
#  LAYOUT COMPONENTS
# --------------------------------------------------------------------------- #
def header(active=""):
    def dd_service(slug):
        i = SVC_INFO[slug]; c = SVC_COPY[slug]
        return (f'<a class="dd-item" href="{svc_url(slug)}"><span class="di-ic">{ICONS[i["icon"]]}</span>'
                f'<span><b>{esc(i["nav"])}</b><span>{esc(c["hero_tagline"][:64])}</span></span></a>')
    svc_items = "".join(dd_service(s) for s in SVC_ORDER)
    city_items = "".join(
        f'<a class="dd-item" href="{city_url(s)}"><span class="di-ic">{ICONS["mappin"]}</span>'
        f'<span><b>{esc(city_name(s))}</b><span>{esc(CITY_META[s][0])} County</span></span></a>'
        for s in CITY_ORDER[:12])
    return f'''<div class="topbar"><div class="container">
    <div class="topbar-left">
      <span class="ico">{ICONS["mappin"]} {esc(BIZ["area_line"])}</span>
      <span class="ico">{ICONS["clock"]} {esc(BIZ["hours_short"])}</span>
    </div>
    <div class="topbar-right">
      <span class="badge-24"><span class="dot ok"></span>Same-Day Service Available</span>
      <a href="mailto:{BIZ["email"]}">{ICONS["mail"]} {esc(BIZ["email"])}</a>
    </div></div></div>
  <header class="site-header" id="siteHeader">
    <div class="container"><nav class="nav" aria-label="Primary">
      <a class="brand" href="/" aria-label="{esc(BIZ["name"])} home">
        <img src="/assets/img/logo-mark.svg" width="48" height="48" alt="{esc(BIZ["short"])} logo">
        <span class="wm"><span class="name">BH Door Solutions</span><span class="tag">Metro Detroit</span></span>
      </a>
      <ul class="nav-menu">
        <li><a href="/"{' aria-current="page"' if active=="home" else ''}>Home</a></li>
        <li class="has-dd"><button aria-expanded="false" aria-haspopup="true" aria-controls="dd-services">Services <span class="caret">{ICONS["chevron"]}</span></button>
          <div class="dropdown" id="dd-services"><div class="dd-grid three">{svc_items}</div>
            <div class="dd-foot"><span>Residential &amp; commercial — installation &amp; repair.</span>
            <a class="sc-link" href="/services/">All services {ICONS["arrow"]}</a></div></div></li>
        <li class="has-dd"><button aria-expanded="false" aria-haspopup="true" aria-controls="dd-areas">Service Areas <span class="caret">{ICONS["chevron"]}</span></button>
          <div class="dropdown areas" id="dd-areas"><div class="dd-grid three">{city_items}</div>
            <div class="dd-foot"><span>18+ metro Detroit cities across 3 counties.</span>
            <a class="sc-link" href="/service-areas/">All areas {ICONS["arrow"]}</a></div></div></li>
        <li><a href="/services/door-installation-cost/"{' aria-current="page"' if active=="cost" else ''}>Pricing</a></li>
        <li><a href="/about/"{' aria-current="page"' if active=="about" else ''}>About</a></li>
        <li><a href="/reviews/"{' aria-current="page"' if active=="reviews" else ''}>Reviews</a></li>
        <li><a href="/contact/"{' aria-current="page"' if active=="contact" else ''}>Contact</a></li>
      </ul>
      <div class="nav-actions">
        <a class="nav-call" href="tel:{BIZ["tel"]}"><span class="ring">{ICONS["phone"]}</span>
          <span><small>Call for a free estimate</small><span class="ph">{esc(BIZ["phone"])}</span></span></a>
        <a class="btn btn-primary" href="/contact/">Free Estimate</a>
        <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
    </nav></div>
  </header>'''

def mobile_cta():
    return (f'<div class="mobile-cta"><a class="btn btn-navy" href="tel:{BIZ["tel"]}">{ICONS["phone"]} Call Now</a>'
            f'<a class="btn btn-primary" href="/contact/">Free Estimate</a></div>')

def footer():
    svc_links = "".join(f'<li><a href="{svc_url(s)}">{esc(SVC_INFO[s]["nav"])}</a></li>' for s in SVC_ORDER[:8])
    city_links = "".join(f'<li><a href="{city_url(s)}">{esc(city_name(s))}</a></li>' for s in TOP_CITIES)
    social = ""
    for key,url in [("google",BIZ["google"]),("facebook",BIZ["facebook"]),("instagram",BIZ["instagram"])]:
        href = url or "#"
        social += f'<a href="{href}" aria-label="{key.title()}"{" rel=nofollow" if not url else ""}>{ICONS[key]}</a>'
    lic = f' · License #{esc(BIZ["license_no"])}' if BIZ["license_no"] else ""
    return f'''<footer class="site-footer">
    <div class="container"><div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/"><img src="/assets/img/logo-mark.svg" width="46" height="46" alt="">
          <span class="wm"><span class="name">BH Door Solutions</span><span class="tag">Metro Detroit</span></span></a>
        <p>Residential &amp; commercial door installation and repair across metro Detroit — entry, patio, storm, interior, and commercial doors, plus fast same-day repairs. Licensed &amp; insured, honest pricing, free estimates.</p>
        <div class="social">{social}</div>
      </div>
      <div class="footer-col"><h4>Services</h4><ul>{svc_links}
        <li><a href="/services/">All services →</a></li></ul></div>
      <div class="footer-col"><h4>Service Areas</h4><ul>{city_links}
        <li><a href="/service-areas/">All areas →</a></li></ul></div>
      <div class="footer-col"><h4>Get in Touch</h4>
        <ul class="footer-contact">
          <li>{ICONS["phone"]}<span><a href="tel:{BIZ["tel"]}">{esc(BIZ["phone"])}</a><br><small>Same-day service available</small></span></li>
          <li>{ICONS["mail"]}<a href="mailto:{BIZ["email"]}">{esc(BIZ["email"])}</a></li>
          <li>{ICONS["mappin"]}<span>{esc(BIZ["area_line"])}</span></li>
          <li>{ICONS["clock"]}<span>{esc(BIZ["hours_full"])}</span></li>
        </ul>
        <a class="btn btn-primary btn-block" href="/contact/">Request Free Estimate</a>
      </div>
    </div></div>
    <div class="footer-bottom"><div class="container">
      <span>© {datetime.date.today().year} {esc(BIZ["name"])}. All rights reserved.{lic}</span>
      <span><a href="/service-areas/">Service Areas</a> · <a href="/services/">Services</a> · <a href="/contact/">Contact</a> · <a href="/sitemap.xml">Sitemap</a></span>
    </div></div>
  </footer>'''

def breadcrumb(items):
    lis = ""
    for i,(n,u) in enumerate(items):
        last = i == len(items)-1
        if last: lis += f'<li><span aria-current="page">{esc(n)}</span></li>'
        else: lis += f'<li><a href="{u}">{esc(n)}</a></li>'
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><ol>{lis}</ol></div></nav>'

def cta_band(title="Ready for doors that work — and wow?", text="Get a free, no-obligation estimate today. Fast, same-day service across metro Detroit whenever our schedule allows."):
    return f'''<section class="section"><div class="container"><div class="cta-band"><div class="inner">
      <div><h2>{esc(title)}</h2><p>{esc(text)}</p></div>
      <div class="cta-actions">
        <a class="btn btn-primary btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a>
        <a class="btn btn-white btn-lg" href="/contact/">Free Estimate</a>
      </div></div></div></div></section>'''

def faq_section(faqs, heading="Frequently Asked Questions", sub=None):
    items = ""
    for q,a in faqs:
        items += f'<details><summary>{esc(q)}</summary><div class="faq-a"><p>{esc(a)}</p></div></details>'
    subhtml = f'<p>{esc(sub)}</p>' if sub else ''
    return f'''<section class="section bg-cloud"><div class="container">
      <div class="section-head center"><span class="eyebrow">Answers</span><h2>{esc(heading)}</h2>{subhtml}</div>
      <div class="faq">{items}</div></div></section>'''

def trust_strip():
    items = "".join(f'<div class="trust-item">{ICONS[i]} {esc(t)}</div>' for i,t in TRUST_ITEMS)
    return f'<div class="truststrip"><div class="container">{items}</div></div>'

def brands_block():
    b = "".join(f'<span>{esc(x)}</span>' for x in BRANDS)
    return f'''<section class="section-sm"><div class="container">
      <p class="text-center" style="color:var(--steel);font-weight:600;margin-bottom:18px">Trusted brands we install &amp; service</p>
      <div class="brands">{b}</div></div></section>'''

def value_props_block(intro=None):
    cards = ""
    for i,t,d in VALUE_PROPS:
        cards += f'<div class="why-card"><div class="f-ic">{ICONS[i]}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
    sub = f'<p>{esc(intro)}</p>' if intro else ''
    return f'''<section class="section bg-navy"><div class="container">
      <div class="section-head center"><span class="eyebrow">Why BH Door Solutions</span>
        <h2>Metro Detroit homeowners &amp; businesses trust us</h2>{sub}</div>
      <div class="grid grid-3">{cards}</div></div></section>'''

def process_block():
    steps = ""
    for t,d in PROCESS:
        steps += f'<div class="step"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
    return f'''<section class="section"><div class="container">
      <div class="section-head center"><span class="eyebrow">How it works</span>
        <h2>Simple, honest, and done right the first time</h2>
        <p>From your first call to the final walkthrough, we keep it clear and easy.</p></div>
      <div class="grid grid-4 steps">{steps}</div></div></section>'''

def reviews_invite():
    """Honest review section — invites Google reviews instead of fabricating testimonials."""
    g = BIZ["google"] or "#"
    return f'''<section class="section"><div class="container">
      <div class="split">
        <div><span class="eyebrow">Reviews</span>
          <h2>Building a reputation, one door at a time</h2>
          <p class="lead">We'd rather earn your trust than borrow someone else's words. Every job is done to the standard we'd want in our own home — clean, on time, and guaranteed.</p>
          <p>Worked with us? We'd love your feedback. Checking us out? Read verified reviews from metro Detroit homeowners on Google.</p>
          <div class="hero-cta">
            <a class="btn btn-primary" href="{g}"{' rel="nofollow"' if not BIZ["google"] else ''} target="_blank" rel="noopener">{ICONS["google"]} Read Google Reviews</a>
            <a class="btn btn-ghost" href="/reviews/">More about our promise {ICONS["arrow"]}</a>
          </div>
        </div>
        <div class="grid" style="gap:16px">
          <div class="feature"><div class="f-ic">{ICONS["badge"]}</div><h3>Workmanship guarantee</h3><p>We stand behind every install and repair. If it isn't right, we make it right.</p></div>
          <div class="feature"><div class="f-ic">{ICONS["clock"]}</div><h3>On-time, tidy service</h3><p>We show up when we say, protect your floors, and clean up before we go.</p></div>
        </div>
      </div></div></section>'''

# --------------------------------------------------------------------------- #
#  PAGE SHELL
# --------------------------------------------------------------------------- #
def render(path, title, description, body, graph, active="", og_image="/assets/img/og-image.jpg", extra_head=""):
    canonical = U(path)
    g = [business_node()] + graph
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0d2035">
<meta name="msvalidate.01" content="534011101779A9CCE428FCB92474BE37">
<meta name="format-detection" content="telephone=yes">
<meta name="geo.region" content="US-MI"><meta name="geo.placename" content="Detroit, Michigan">
<link rel="preload" href="/assets/fonts/manrope-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/styles.css?v={ASSET_VER}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/assets/img/logo-mark.svg">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(BIZ["name"])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{U(og_image)}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{U(og_image)}">
{extra_head}
{jsonld(g)}
</head>
<body>
<a href="#main" class="skip-link btn btn-primary">Skip to main content</a>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
{mobile_cta()}
<script src="/assets/js/main.js?v={ASSET_VER}" defer></script>
{MATOMO}
</body>
</html>'''
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    return path

# --------------------------------------------------------------------------- #
#  PAGES
# --------------------------------------------------------------------------- #
def build_home():
    h = CORE["home"]
    h1 = esc(h["hero_h1"])
    hl = h.get("hero_hl","")
    if hl and hl in h["hero_h1"]:
        h1 = esc(h["hero_h1"]).replace(esc(hl), f'<span class="hl">{esc(hl)}</span>')
    chips = "".join(f'<span class="ht">{ICONS[i]} {esc(t)}</span>' for i,t in HERO_CHIPS)
    # service cards
    cards = ""
    for s in SVC_ORDER:
        i = SVC_INFO[s]; c = SVC_COPY[s]
        cards += f'''<a class="card svc-card" href="{svc_url(s)}">
          <div class="sc-media"><img src="/assets/img/{i["img"]}.webp" width="1200" height="800" loading="lazy" alt="{esc(c["h1"])} in metro Detroit"><span class="sc-tag">{esc(i["group"])}</span></div>
          <div class="sc-body"><h3>{esc(i["nav"])}</h3><p>{esc(c["hero_tagline"])}</p>
          <span class="sc-link">Learn more {ICONS["arrow"]}</span></div></a>'''
    # city chips
    chips_city = "".join(
        f'<a class="city-chip" href="{city_url(s)}">{esc(city_name(s))} {ICONS["arrow"]}<span>{CITY_META[s][0]} Co.</span></a>'
        for s in CITY_ORDER)
    intro_body = paras(h["intro_body"])
    faqs = [(f["q"],f["a"]) for f in h["faqs"]]
    graph = [website_node(), breadcrumb_node([("Home","/")]), faq_node(faqs),
             service_node("Door Installation and Repair","door-repair",h["meta_description"])]
    body = f'''<section class="hero"><div class="container"><div class="hero-grid">
      <div class="hero-copy">
        <span class="eyebrow">Door Installation &amp; Repair · Metro Detroit</span>
        <h1>{h1}</h1>
        <p class="lead">{esc(h["hero_sub"])}</p>
        <div class="hero-cta">
          <a class="btn btn-primary btn-lg" href="/contact/">{ICONS["calendar"]} Get My Free Estimate</a>
          <a class="btn btn-ghost btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a>
        </div>
        <div class="hero-trust">{chips}</div>
      </div>
      <div class="hero-media">
        <img src="/assets/img/hero-home.webp" width="1600" height="1000" fetchpriority="high" alt="Newly installed fiberglass front entry door on a metro Detroit home">
        <div class="hero-badge"><span class="hb-ic">{ICONS["clock"]}</span><span><b>Same-Day</b><span>service available across metro Detroit</span></span></div>
      </div>
    </div></div></section>
    {trust_strip()}
    <section class="section"><div class="container">
      <div class="split">
        <div><span class="eyebrow">Metro Detroit's door specialists</span>
          <h2>{esc(h["intro_h2"])}</h2>{intro_body}
          <div class="hero-cta"><a class="btn btn-navy" href="/services/">Explore our services {ICONS["arrow"]}</a>
          <a class="btn btn-ghost" href="/service-areas/">Areas we serve</a></div>
        </div>
        <div class="page-hero-media"><img src="/assets/img/process-install.webp" width="1200" height="800" loading="lazy" alt="BH Door Solutions installers fitting a new exterior door in metro Detroit" style="border-radius:var(--r-xl);box-shadow:var(--sh-3)"></div>
      </div></div></section>
    <section class="section bg-cloud"><div class="container">
      <div class="section-head center"><span class="eyebrow">Our Services</span>
        <h2>Every door, one trusted local team</h2><p>{esc(h["services_intro"])}</p></div>
      <div class="grid grid-3">{cards}</div>
    </div></section>
    {value_props_block(h.get("why_intro"))}
    {process_block()}
    <section class="section bg-cloud"><div class="container">
      <div class="section-head center"><span class="eyebrow">Service Areas</span>
        <h2>Proudly serving metro Detroit &amp; 18+ suburbs</h2><p>{esc(h["areas_intro"])}</p></div>
      <div class="city-grid">{chips_city}</div>
      <p class="text-center mt-2"><a class="btn btn-navy" href="/service-areas/">See all service areas {ICONS["arrow"]}</a></p>
    </div></section>
    {reviews_invite()}
    {brands_block()}
    {faq_section(faqs, "Door installation & repair FAQs", "Quick answers for metro Detroit homeowners and businesses.")}
    {cta_band()}'''
    render("/", h["meta_title"], h["meta_description"], body, graph, active="home")

def build_services_hub():
    groups = {}
    for s in SVC_ORDER:
        groups.setdefault(SVC_INFO[s]["group"], []).append(s)
    sections = ""
    for grp in ["Installation","Repair","Commercial","Planning"]:
        cards = ""
        for s in groups.get(grp,[]):
            i=SVC_INFO[s]; c=SVC_COPY[s]
            cards += f'''<a class="card svc-card" href="{svc_url(s)}">
              <div class="sc-media"><img src="/assets/img/{i["img"]}.webp" width="1200" height="800" loading="lazy" alt="{esc(c["h1"])}"><span class="sc-tag">{esc(grp)}</span></div>
              <div class="sc-body"><h3>{esc(c["h1"])}</h3><p>{esc(c["hero_tagline"])}</p><span class="sc-link">View service {ICONS["arrow"]}</span></div></a>'''
        sections += f'<div class="section-head" style="margin-top:12px"><h2>{esc(grp)}</h2></div><div class="grid grid-3">{cards}</div>'
    graph = [breadcrumb_node([("Home","/"),("Services","/services/")]),
             service_node("Door Services","door-repair","Full-service residential and commercial door installation and repair across metro Detroit.")]
    body = f'''<section class="page-hero"><div class="container"><div class="page-hero-grid">
      <div><span class="eyebrow">Our Services</span><h1>Door Services in Metro Detroit</h1>
      <p>From a brand-new fiberglass front door to a slider that's jumped its track, BH Door Solutions installs and repairs every kind of residential and commercial door across Wayne, Oakland, and Macomb counties — with fast, same-day service.</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/contact/">Get a Free Estimate</a>
      <a class="btn btn-ghost btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a></div></div>
      <div class="page-hero-media"><img src="/assets/img/svc-entry.webp" width="1200" height="800" alt="Door services in metro Detroit"></div>
    </div></div></section>
    {breadcrumb([("Home","/"),("Services","/services/")])}
    {trust_strip()}
    <section class="section"><div class="container">{sections}</div></section>
    {value_props_block()}
    {cta_band()}'''
    render("/services/", "Door Services Metro Detroit | BH Door Solutions",
           "Residential & commercial door installation and repair in metro Detroit — entry, patio, storm, interior & commercial doors, plus fast same-day repairs. Free estimates.",
           body, graph)

def build_service(slug):
    c = SVC_COPY[slug]; i = SVC_INFO[slug]
    secs = ""
    for s in c["sections"]:
        b = paras(s["body"])
        bl = ""
        if s.get("bullets"):
            bl = "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in s["bullets"]) + "</ul>"
        secs += f'<h2>{esc(s["h2"])}</h2>{b}{bl}'
    incl = "".join(f"<li>{esc(x)}</li>" for x in c["whats_included"])
    why = ""
    for w in c["why_us"]:
        why += f'<div class="feature"><div class="f-ic">{ICONS[i["icon"]]}</div><h3>{esc(w["title"])}</h3><p>{esc(w["text"])}</p></div>'
    faqs = [(f["q"],f["a"]) for f in c["faqs"]]
    # related services
    rel = ""
    for r in RELATED[slug]:
        ri=SVC_INFO[r]; rc=SVC_COPY[r]
        rel += f'''<a class="card svc-card" href="{svc_url(r)}">
          <div class="sc-media"><img src="/assets/img/{ri["img"]}.webp" width="1200" height="800" loading="lazy" alt="{esc(rc["h1"])}"></div>
          <div class="sc-body"><h3>{esc(ri["nav"])}</h3><p>{esc(rc["hero_tagline"])}</p><span class="sc-link">Learn more {ICONS["arrow"]}</span></div></a>'''
    city_links = " · ".join(f'<a href="{city_url(s)}">{esc(city_name(s))}</a>' for s in TOP_CITIES)
    graph = [breadcrumb_node([("Home","/"),("Services","/services/"),(c["h1"],svc_url(slug))]),
             service_node(c["h1"], slug, c["meta_description"]), faq_node(faqs)]
    active = "cost" if slug=="door-installation-cost" else ""
    emergency_badge = f'<span class="pill">{esc(i["group"])}</span>'
    body = f'''<section class="page-hero"><div class="container"><div class="page-hero-grid">
      <div>{emergency_badge}<h1 style="margin-top:.5em">{esc(c["h1"])}</h1>
      <p>{esc(c["hero_tagline"])}</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/contact/">Get a Free Estimate</a>
      <a class="btn btn-ghost btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a></div></div>
      <div class="page-hero-media"><img src="/assets/img/{i["img"]}.webp" width="1200" height="800" fetchpriority="high" alt="{esc(c["h1"])} in metro Detroit by BH Door Solutions"></div>
    </div></div></section>
    {breadcrumb([("Home","/"),("Services","/services/"),(SVC_INFO[slug]["nav"],svc_url(slug))])}
    {trust_strip()}
    <section class="section"><div class="container"><div class="split" style="align-items:flex-start">
      <div class="prose">
        <p class="lead">{esc(c["intro_lead"])}</p>
        {secs}
        <h2>What's included</h2>
        <ul>{incl}</ul>
      </div>
      <aside class="sidebar-card">
        <h3>Request this service</h3>
        <p style="color:var(--slate);font-size:.95rem">Free, no-obligation estimate — usually same or next day across metro Detroit.</p>
        <a class="btn btn-primary btn-block" href="/contact/">Get My Free Estimate</a>
        <p class="text-center" style="margin:.8em 0 .2em;color:var(--steel);font-size:.9rem">or call</p>
        <a class="btn btn-navy btn-block" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a>
        <h3 style="margin-top:1.4em">Why choose BH</h3>
        <ul class="chk">
          <li>Licensed &amp; insured local team</li>
          <li>Fast, same-day service available</li>
          <li>Upfront, flat-rate pricing</li>
          <li>Workmanship guarantee</li>
          <li>Fully-stocked trucks — one-visit fix</li>
        </ul>
      </aside>
    </div></div></section>
    <section class="section bg-cloud"><div class="container">
      <div class="section-head center"><span class="eyebrow">Why homeowners choose us</span><h2>The BH Door Solutions difference</h2></div>
      <div class="grid grid-3">{why}</div></div></section>
    {faq_section(faqs, esc(SVC_INFO[slug]["nav"]) + " — FAQs")}
    <section class="section"><div class="container">
      <div class="section-head"><span class="eyebrow">Serving metro Detroit</span><h2>Available across every suburb we serve</h2>
      <p>Including {city_links} and <a href="/service-areas/">18+ more cities</a>.</p></div>
      <div class="section-head" style="margin-top:8px"><h2 style="font-size:1.5rem">Related services</h2></div>
      <div class="grid grid-4">{rel}</div></div></section>
    {cta_band()}'''
    render(svc_url(slug), c["meta_title"], c["meta_description"], body, graph, active=active,
           og_image="/assets/img/og-image.jpg")

def build_areas_hub():
    by_county = {"Wayne":[],"Oakland":[],"Macomb":[]}
    for s in CITY_ORDER:
        by_county[CITY_META[s][0]].append(s)
    cols = ""
    for county in ["Wayne","Oakland","Macomb"]:
        chips = "".join(f'<a class="city-chip" href="{city_url(s)}">{esc(city_name(s))} {ICONS["arrow"]}</a>' for s in by_county[county])
        cols += f'<div><div class="section-head" style="margin-bottom:14px"><h2 style="font-size:1.4rem">{esc(county)} County</h2></div><div class="grid" style="gap:10px">{chips}</div></div>'
    graph = [breadcrumb_node([("Home","/"),("Service Areas","/service-areas/")])]
    body = f'''<section class="page-hero"><div class="container"><div class="page-hero-grid">
      <div><span class="eyebrow">Service Areas</span><h1>Door Installation &amp; Repair Across Metro Detroit</h1>
      <p>No storefront, no markup for a fancy showroom — just a local crew that comes to you. We serve metro Detroit and every suburb within 35 miles across Wayne, Oakland, and Macomb counties.</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/contact/">Get a Free Estimate</a>
      <a class="btn btn-ghost btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a></div></div>
      <div class="page-hero-media"><img src="/assets/img/area-neighborhood.webp" width="1600" height="900" alt="Metro Detroit suburban neighborhood served by BH Door Solutions"></div>
    </div></div></section>
    {breadcrumb([("Home","/"),("Service Areas","/service-areas/")])}
    {trust_strip()}
    <section class="section"><div class="container">
      <div class="section-head"><h2>Cities we serve</h2><p>Tap your city for local door installation and repair details. Don't see yours? We likely still cover it — just <a href="/contact/">ask</a>.</p></div>
      <div class="grid grid-3">{cols}</div></div></section>
    {value_props_block()}
    {cta_band()}'''
    render("/service-areas/", "Service Areas — Door Installation & Repair Metro Detroit | BH Door Solutions",
           "See the metro Detroit cities BH Door Solutions serves for door installation & repair — 18+ suburbs across Wayne, Oakland & Macomb counties. Same-day service, free estimates.",
           body, graph)

def build_city(slug):
    c = CITY_COPY[slug]; county, neighbors, top = CITY_META[slug]
    ctx = paras(c["local_context"])
    why = "".join(f"<li>{esc(x)}</li>" for x in c["why_local"])
    faqs = [(f["q"],f["a"]) for f in c["faqs"]]
    top_cards = ""
    for s in top:
        si=SVC_INFO[s]; sc=SVC_COPY[s]
        top_cards += f'''<a class="card svc-card" href="{svc_url(s)}">
          <div class="sc-media"><img src="/assets/img/{si["img"]}.webp" width="1200" height="800" loading="lazy" alt="{esc(si["nav"])} in {esc(c["city"])}, MI"></div>
          <div class="sc-body"><h3>{esc(si["nav"])}</h3><p>{esc(sc["hero_tagline"])}</p><span class="sc-link">Learn more {ICONS["arrow"]}</span></div></a>'''
    neigh = "".join(f'<a class="city-chip" href="{city_url(n)}">{esc(city_name(n))} {ICONS["arrow"]}<span>{CITY_META[n][0]} Co.</span></a>' for n in neighbors)
    graph = [breadcrumb_node([("Home","/"),("Service Areas","/service-areas/"),(c["city"],city_url(slug))]),
             service_node(f"Door Installation and Repair in {c['city']}, MI", "door-repair", c["meta_description"], areas=[slug]),
             faq_node(faqs)]
    img = "area-neighborhood.webp" if CITY_ORDER.index(slug)%2==0 else "area-neighborhood2.webp"
    body = f'''<section class="page-hero"><div class="container"><div class="page-hero-grid">
      <div><span class="eyebrow">{esc(county)} County · Metro Detroit</span><h1>{esc(c["h1"])}</h1>
      <p>{esc(c["hero_tagline"])}</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/contact/">Free Estimate in {esc(c["city"])}</a>
      <a class="btn btn-ghost btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a></div></div>
      <div class="page-hero-media"><img src="/assets/img/{img}" width="1600" height="900" fetchpriority="high" alt="Door installation and repair in {esc(c["city"])}, Michigan"></div>
    </div></div></section>
    {breadcrumb([("Home","/"),("Service Areas","/service-areas/"),(c["city"],city_url(slug))])}
    {trust_strip()}
    <section class="section"><div class="container"><div class="split" style="align-items:flex-start">
      <div class="prose">
        <p class="lead">{esc(c["intro_lead"])}</p>
        <h2>Door installation &amp; repair {esc(c["city"])} homeowners rely on</h2>
        {ctx}
        <h2>The doors {esc(c["city"])} homes need most</h2>
        <p>{esc(c["service_emphasis"])}</p>
      </div>
      <aside class="sidebar-card">
        <h3>Free estimate in {esc(c["city"])}</h3>
        <p style="color:var(--slate);font-size:.95rem">Local, licensed &amp; insured. Same-day service available across {esc(county)} County.</p>
        <a class="btn btn-primary btn-block" href="/contact/">Get My Free Estimate</a>
        <p class="text-center" style="margin:.8em 0 .2em;color:var(--steel);font-size:.9rem">or call</p>
        <a class="btn btn-navy btn-block" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a>
        <h3 style="margin-top:1.4em">Why {esc(c["city"])} calls BH</h3>
        <ul class="chk">{why}</ul>
      </aside>
    </div></div></section>
    <section class="section bg-cloud"><div class="container">
      <div class="section-head center"><span class="eyebrow">Popular in {esc(c["city"])}</span><h2>Our most-requested {esc(c["city"])} door services</h2></div>
      <div class="grid grid-4">{top_cards}</div></div></section>
    {faq_section(faqs, f"Door service in {esc(c['city'])} — FAQs")}
    <section class="section"><div class="container">
      <div class="section-head"><span class="eyebrow">Nearby</span><h2>We also serve neighboring communities</h2></div>
      <div class="city-grid">{neigh}</div></div></section>
    {cta_band(f"Need a door installed or repaired in {c['city']}?", "Get a free, no-obligation estimate today. Fast, same-day service across " + county + " County whenever our schedule allows.")}'''
    render(city_url(slug), c["meta_title"], c["meta_description"], body, graph)

def build_about():
    a = CORE["about"]
    secs = ""
    imgs = ["about-team.webp","process-install.webp","area-neighborhood.webp"]
    for idx,s in enumerate(a["body"]):
        secs += f'<h2>{esc(s["h2"])}</h2>{paras(s["paras"])}'
    vals = ""
    ics = ["shield","clock","hand","badge","truck","spark"]
    for idx,v in enumerate(a["values"]):
        vals += f'<div class="feature"><div class="f-ic">{ICONS[ics[idx%len(ics)]]}</div><h3>{esc(v["title"])}</h3><p>{esc(v["text"])}</p></div>'
    graph = [breadcrumb_node([("Home","/"),("About","/about/")])]
    body = f'''<section class="page-hero"><div class="container"><div class="page-hero-grid">
      <div><span class="eyebrow">About Us</span><h1>{esc(a["h1"])}</h1><p>{esc(a["lead"])}</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/contact/">Work With Us</a>
      <a class="btn btn-ghost btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a></div></div>
      <div class="page-hero-media"><img src="/assets/img/about-team.webp" width="1200" height="900" alt="BH Door Solutions — metro Detroit door installation and repair team"></div>
    </div></div></section>
    {breadcrumb([("Home","/"),("About","/about/")])}
    {trust_strip()}
    <section class="section"><div class="container"><div class="prose wide" style="margin-inline:auto">{secs}</div></div></section>
    <section class="section bg-cloud"><div class="container">
      <div class="section-head center"><span class="eyebrow">What we stand for</span><h2>Values behind every door</h2></div>
      <div class="grid grid-3">{vals}</div></div></section>
    {process_block()}
    {cta_band()}'''
    render("/about/", a["meta_title"], a["meta_description"], body, graph, active="about")

def build_financing():
    f = CORE["financing"]
    pts = "".join(f"<li>{esc(x)}</li>" for x in f["points"])
    graph = [breadcrumb_node([("Home","/"),("Financing","/financing/")])]
    body = f'''<section class="page-hero"><div class="container"><div class="page-hero-grid">
      <div><span class="eyebrow">Financing</span><h1>{esc(f["h1"])}</h1><p>{esc(f["lead"])}</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="/contact/">Ask About Financing</a>
      <a class="btn btn-ghost btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} {esc(BIZ["phone"])}</a></div></div>
      <div class="page-hero-media"><img src="/assets/img/svc-cost.webp" width="1200" height="800" alt="Door installation financing options in metro Detroit"></div>
    </div></div></section>
    {breadcrumb([("Home","/"),("Financing","/financing/")])}
    <section class="section"><div class="container"><div class="prose wide" style="margin-inline:auto">
      {paras(f["body"])}
      <h2>Flexible ways to pay</h2><ul>{pts}</ul>
      <div class="note">Ask your BH Door Solutions estimator about current financing options and promotions when you book your free estimate. Terms are provided by third-party lenders on approved credit.</div>
    </div></div></section>
    {cta_band()}'''
    render("/financing/", f["meta_title"], f["meta_description"], body, graph)

def build_reviews():
    graph = [breadcrumb_node([("Home","/"),("Reviews","/reviews/")])]
    g = BIZ["google"] or "#"
    body = f'''<section class="page-hero"><div class="container"><div class="page-hero-grid">
      <div><span class="eyebrow">Reviews</span><h1>What Metro Detroit Says About Us</h1>
      <p>{esc(CORE["reviews_lead"])}</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg" href="{g}"{' rel="nofollow"' if not BIZ["google"] else ''} target="_blank" rel="noopener">{ICONS["google"]} Read Google Reviews</a>
      <a class="btn btn-ghost btn-lg" href="/contact/">Get a Free Estimate</a></div></div>
      <div class="page-hero-media"><img src="/assets/img/svc-entry.webp" width="1200" height="800" alt="Happy metro Detroit homeowners and their new doors"></div>
    </div></div></section>
    {breadcrumb([("Home","/"),("Reviews","/reviews/")])}
    {trust_strip()}
    <section class="section"><div class="container"><div class="prose wide" style="margin-inline:auto">
      <h2>Our promise to every customer</h2>
      <p>Reviews are earned, not written. As we complete jobs across metro Detroit, verified customer reviews will appear here and on our Google Business Profile. In the meantime, here's exactly what you can expect when you call BH Door Solutions:</p>
      <ul>
        <li><strong>On-time arrival</strong> in the window we promise — with a heads-up when we're on the way.</li>
        <li><strong>A clear, upfront quote</strong> before any work starts. No surprises, no pressure.</li>
        <li><strong>Clean, careful work</strong> that protects your home, followed by a full cleanup.</li>
        <li><strong>A workmanship guarantee</strong> — if something isn't right, we come back and make it right.</li>
      </ul>
      <div class="note">Already worked with us? We'd be grateful for your feedback — it helps your neighbors find a door company they can trust. Call {esc(BIZ["phone"])} and we'll send you a review link.</div>
    </div></div></section>
    {reviews_invite()}
    {cta_band()}'''
    render("/reviews/", "Reviews — BH Door Solutions Metro Detroit",
           "See what to expect from BH Door Solutions — metro Detroit's local door installation & repair team. Licensed, insured, guaranteed, same-day service.",
           body, graph, active="reviews")

def build_contact():
    graph = [breadcrumb_node([("Home","/"),("Contact","/contact/")])]
    svc_opts = "".join(f'<option value="{esc(SVC_INFO[s]["nav"])}">{esc(SVC_INFO[s]["nav"])}</option>' for s in SVC_ORDER)
    body = f'''<section class="page-hero"><div class="container"><div class="page-hero-grid">
      <div><span class="eyebrow">Contact</span><h1>Get Your Free Door Estimate</h1>
      <p>{esc(CORE["contact_lead"])}</p>
      <ul class="chk" style="margin-top:1.2em;max-width:420px">
        <li>Free, no-obligation estimates</li>
        <li>Fast, same-day service available</li>
        <li>Licensed, insured &amp; local to metro Detroit</li>
      </ul>
      <div style="margin-top:1.4em"><a class="btn btn-primary btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} Call {esc(BIZ["phone"])}</a></div>
      </div>
      <div class="form-card">
        <h2 style="font-size:1.5rem;margin-bottom:.2em">Request a callback</h2>
        <p style="color:var(--steel);font-size:.92rem;margin-bottom:1em">We'll get back to you fast — usually the same day.</p>
        <div id="formErr" class="note" role="alert" style="display:none;border-color:var(--danger);background:var(--danger-050);margin-bottom:16px">Sorry — something went wrong sending your request. Please call us at <a href="tel:{BIZ["tel"]}">{esc(BIZ["phone"])}</a> and we'll help right away.</div>
        <form action="https://bh-door-form.oren-siyonov.workers.dev" method="POST">
          <div class="form-row">
            <div class="field"><label for="name">Name <span class="req">*</span></label><input id="name" name="name" required autocomplete="name"></div>
            <div class="field"><label for="phone">Phone <span class="req">*</span></label><input id="phone" name="phone" type="tel" required autocomplete="tel"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="city">City / ZIP</label><input id="city" name="city" autocomplete="address-level2" placeholder="e.g. Royal Oak"></div>
            <div class="field"><label for="service">Service needed</label><select id="service" name="service"><option value="">Choose…</option>{svc_opts}<option>Not sure / other</option></select></div>
          </div>
          <div class="field"><label for="message">How can we help?</label><textarea id="message" name="message" placeholder="Tell us about your door…"></textarea></div>
          <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
          <button class="btn btn-primary btn-lg btn-block" type="submit">{ICONS["calendar"]} Request My Free Estimate</button>
          <p class="form-note">By submitting you agree to be contacted about your request. We never share your information.</p>
        </form>
      </div>
    </div></div></section>
    {breadcrumb([("Home","/"),("Contact","/contact/")])}
    <section class="section bg-cloud"><div class="container"><div class="grid grid-3">
      <div class="feature"><div class="f-ic">{ICONS["phone"]}</div><h3>Call or email</h3><p><a href="tel:{BIZ["tel"]}">{esc(BIZ["phone"])}</a><br><a href="mailto:{BIZ["email"]}">{esc(BIZ["email"])}</a></p></div>
      <div class="feature"><div class="f-ic">{ICONS["clock"]}</div><h3>Hours</h3><p>{esc(BIZ["hours_full"])}</p></div>
      <div class="feature"><div class="f-ic">{ICONS["mappin"]}</div><h3>Service area</h3><p>{esc(BIZ["area_line"])} across Wayne, Oakland &amp; Macomb counties.</p></div>
    </div></div></section>
    {cta_band("Let's get your door sorted", "Tell us what's going on and we'll take care of it. Free estimates and fast, same-day service across metro Detroit whenever our schedule allows.")}'''
    render("/contact/", "Contact — Free Door Estimate | BH Door Solutions Metro Detroit",
           "Contact BH Door Solutions for a free door installation or repair estimate in metro Detroit. Call (313) 236-4558 — fast, same-day service available.",
           body, graph, active="contact")

def build_gallery():
    graph = [breadcrumb_node([("Home","/"),("Gallery","/gallery/")])]
    shots = [("svc-entry","Fiberglass entry door with sidelights"),("svc-patio","Sliding glass patio door install"),
             ("svc-storm","Full-view storm door"),("svc-interior","Interior & barn doors"),
             ("svc-frame","Door frame & jamb repair"),("svc-lock","Smart lock & hardware"),
             ("svc-commercial","Commercial storefront doors"),("process-install","Professional installation"),
             ("cta-door","Craftsman front entry")]
    cards = "".join(
        f'<figure class="card"><div class="sc-media" style="aspect-ratio:3/2"><img src="/assets/img/{s}.webp" width="1200" height="800" loading="lazy" alt="{esc(t)} — BH Door Solutions metro Detroit"></div>'
        f'<figcaption class="sc-body"><h3 style="font-size:1.05rem">{esc(t)}</h3></figcaption></figure>'
        for s,t in shots)
    body = f'''<section class="page-hero"><div class="container">
      <div style="max-width:760px"><span class="eyebrow">Gallery</span><h1>Our Door Work Across Metro Detroit</h1>
      <p>A look at the kind of installations and repairs we do every week for homeowners and businesses around Wayne, Oakland, and Macomb counties.</p></div>
    </div></section>
    {breadcrumb([("Home","/"),("Gallery","/gallery/")])}
    <section class="section"><div class="container"><div class="grid grid-3">{cards}</div>
      <div class="note mt-3">Photos shown are representative of our work and product styles. Ask us for recent project examples in your neighborhood when you book a free estimate.</div>
    </div></section>
    {cta_band()}'''
    render("/gallery/", "Gallery — Door Installation & Repair | BH Door Solutions Metro Detroit",
           "See examples of door installation and repair work by BH Door Solutions across metro Detroit — entry, patio, storm, interior & commercial doors.",
           body, graph)

def build_faq_hub():
    all_faqs = [(f["q"],f["a"]) for f in CORE["home"]["faqs"]]
    seen = set(q for q,_ in all_faqs)
    for s in SVC_ORDER:
        for f in SVC_COPY[s]["faqs"]:
            if f["q"] not in seen:
                all_faqs.append((f["q"],f["a"])); seen.add(f["q"])
    graph = [breadcrumb_node([("Home","/"),("FAQ","/faq/")]), faq_node(all_faqs)]
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="faq-a"><p>{esc(a)}</p></div></details>' for q,a in all_faqs)
    body = f'''<section class="page-hero"><div class="container">
      <div style="max-width:760px"><span class="eyebrow">Answers</span><h1>Door Installation &amp; Repair FAQs</h1>
      <p>Everything metro Detroit homeowners and businesses ask us about doors — costs, timelines, warranties, emergencies, and more.</p></div>
    </div></section>
    {breadcrumb([("Home","/"),("FAQ","/faq/")])}
    <section class="section"><div class="container"><div class="faq">{items}</div></div></section>
    {cta_band()}'''
    render("/faq/", "Door Installation & Repair FAQs | BH Door Solutions Metro Detroit",
           "Answers to common questions about door installation & repair in metro Detroit — cost, timelines, warranties, same-day service, and more.",
           body, graph)

def build_thanks():
    graph = [breadcrumb_node([("Home","/"),("Thank You","/thank-you/")])]
    body = f'''<section class="section" style="min-height:52vh;display:grid;place-items:center;text-align:center"><div class="container" style="max-width:640px">
      <div class="f-ic" style="margin:0 auto 18px;width:70px;height:70px;background:var(--success-050);color:var(--success);border-radius:18px;display:grid;place-items:center">{ICONS["check"]}</div>
      <h1>Thanks — we've got your request!</h1>
      <p class="lead">A member of the BH Door Solutions team will reach out shortly, usually the same day. Need us sooner?</p>
      <div class="hero-cta" style="justify-content:center"><a class="btn btn-primary btn-lg" href="tel:{BIZ["tel"]}">{ICONS["phone"]} Call {esc(BIZ["phone"])}</a>
      <a class="btn btn-ghost btn-lg" href="/">Back to home</a></div>
    </div></section>'''
    render("/thank-you/", "Thank You | BH Door Solutions Metro Detroit",
           "Thanks for contacting BH Door Solutions. We'll be in touch shortly.", body, graph,
           extra_head='<meta name="robots" content="noindex,follow">')

def build_404():
    body = f'''<section class="section" style="min-height:56vh;display:grid;place-items:center;text-align:center"><div class="container" style="max-width:640px">
      <span class="eyebrow" style="justify-content:center">Error 404</span>
      <h1>This door won't open</h1>
      <p class="lead">The page you're looking for isn't here — but we can still help with yours. Try one of these:</p>
      <div class="hero-cta" style="justify-content:center"><a class="btn btn-primary btn-lg" href="/">Home</a>
      <a class="btn btn-ghost btn-lg" href="/services/">Services</a>
      <a class="btn btn-ghost btn-lg" href="/contact/">Free Estimate</a></div>
    </div></section>'''
    # 404 must be at root
    doc = page_wrap("/404.html","Page Not Found | BH Door Solutions","Page not found.",body,[],robots="noindex,follow")
    open(os.path.join(ROOT,"404.html"),"w",encoding="utf-8").write(doc)

def page_wrap(path,title,desc,body,graph,robots="index,follow,max-image-preview:large"):
    # minimal wrapper reusing render's doc for 404 (canonical omitted)
    g=[business_node()]+graph
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}"><meta name="robots" content="{robots}">
<meta name="theme-color" content="#0d2035">
<link rel="stylesheet" href="/assets/css/styles.css?v={ASSET_VER}"><link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/assets/img/logo-mark.svg"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
{jsonld(g)}</head><body>{header()}<main id="main">{body}</main>{footer()}{mobile_cta()}
<script src="/assets/js/main.js?v={ASSET_VER}" defer></script>
{MATOMO}</body></html>'''

# --------------------------------------------------------------------------- #
#  SITEMAP / ROBOTS / MANIFEST / CNAME
# --------------------------------------------------------------------------- #
def build_meta_files():
    urls = ["/","/services/","/service-areas/","/about/","/reviews/","/financing/","/gallery/","/faq/","/contact/"]
    urls += [svc_url(s) for s in SVC_ORDER]
    urls += [city_url(s) for s in CITY_ORDER]
    entries = ""
    for u in urls:
        pr = "1.0" if u=="/" else ("0.9" if u in ("/services/","/service-areas/") else "0.8")
        cf = "weekly" if u in ("/","/services/","/service-areas/") else "monthly"
        entries += f'  <url><loc>{U(u)}</loc><lastmod>{TODAY}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n'
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n'
    open(os.path.join(ROOT,"sitemap.xml"),"w",encoding="utf-8").write(sitemap)

    robots = f"""User-agent: *
Allow: /

Sitemap: {BIZ['base']}/sitemap.xml
"""
    open(os.path.join(ROOT,"robots.txt"),"w",encoding="utf-8").write(robots)

    manifest = {
        "name": BIZ["name"], "short_name": BIZ["short"],
        "description": "Door installation & repair in metro Detroit.",
        "start_url": "/", "display": "standalone",
        "background_color": "#0d2035", "theme_color": "#0d2035",
        "icons": [
            {"src":"/assets/img/icon-192.png","sizes":"192x192","type":"image/png"},
            {"src":"/assets/img/icon-512.png","sizes":"512x512","type":"image/png"},
            {"src":"/assets/img/apple-touch-icon.png","sizes":"512x512","type":"image/png","purpose":"any maskable"},
        ],
    }
    open(os.path.join(ROOT,"site.webmanifest"),"w",encoding="utf-8").write(json.dumps(manifest,indent=2))
    open(os.path.join(ROOT,"CNAME"),"w",encoding="utf-8").write(BIZ["domain"]+"\n")
    open(os.path.join(ROOT,".nojekyll"),"w",encoding="utf-8").write("")
    # Bing Webmaster Tools site verification (public by design)
    open(os.path.join(ROOT,"BingSiteAuth.xml"),"w",encoding="utf-8").write(
        '<?xml version="1.0"?>\n<users>\n  <user>534011101779A9CCE428FCB92474BE37</user>\n</users>\n')

# --------------------------------------------------------------------------- #
def main():
    build_home()
    build_services_hub()
    for s in SVC_ORDER: build_service(s)
    build_areas_hub()
    for c in CITY_ORDER: build_city(c)
    build_about()
    build_financing()
    build_reviews()
    build_contact()
    build_gallery()
    build_faq_hub()
    build_thanks()
    build_404()
    build_meta_files()
    n = 9 + len(SVC_ORDER) + len(CITY_ORDER)
    print(f"Built {n} pages + sitemap/robots/manifest/CNAME.")

if __name__ == "__main__":
    main()
