#!/usr/bin/env python
"""Generate photorealistic site imagery for BH Door Solutions Metro Detroit via the
Gemini image API, then crop/resize/compress to web-optimized WebP.
Idempotent: skips images that already exist in assets/img/. Run again to fill gaps.
"""
import base64, json, os, sys, time, urllib.request, urllib.error, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "img")
RAW_DIR = os.path.join(ROOT, "scripts", "_raw")
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

# API key: from GEMINI_API_KEY env var, or a file pointed to by GEMINI_KEY_FILE.
# Only required for actual generation — `python generate_images.py variants` works without it.
KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not KEY:
    kf = os.environ.get("GEMINI_KEY_FILE", "")
    if kf and os.path.exists(kf):
        KEY = open(kf, encoding="utf-8").read().strip()
MODEL = "gemini-2.5-flash-image"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"

STYLE = (" Professional editorial real-estate photography, natural daylight, clean and crisp, "
         "sharp focus, high detail, photorealistic, inviting. No text, no words, no watermark, "
         "no brand logos, no readable signage, no people's faces in closeups unless specified.")

# name: (prompt, aspect 'wide'|'card'|'portrait', (w,h))
IMAGES = {
 "hero-home": ("A beautiful upscale suburban Michigan home at golden hour with a freshly installed modern "
    "dark charcoal fiberglass front entry door with glass sidelights and a transom window, warm interior "
    "glow, manicured landscaping, wide welcoming exterior composition, cinematic warm light." , "wide", (1600,1000)),
 "svc-entry": ("An elegant newly installed fiberglass front entry door with decorative glass sidelights and a "
    "transom on a brick colonial home in Michigan, rich painted finish, brushed nickel handleset, curb appeal.", "card", (1200,800)),
 "svc-patio": ("A bright modern sliding glass patio door viewed from inside a tastefully furnished living room "
    "looking out onto a green backyard and wood deck, lots of natural light, clean contemporary interior.", "card", (1200,800)),
 "svc-storm": ("A full-view glass storm door installed over a front entry on a brick Michigan home, springtime, "
    "clean aluminum frame, reflections, tidy porch.", "card", (1200,800)),
 "svc-interior": ("A bright modern hallway interior with stylish white shaker panel interior doors and one sliding "
    "barn door on a black rail, light oak floors, minimalist decor.", "card", (1200,800)),
 "svc-repair": ("Close up of a professional handyman's hands using a screwdriver to adjust a brass door hinge on a "
    "white interior door, tool belt visible, shallow depth of field, skilled craftsmanship.", "card", (1200,800)),
 "svc-sliding-repair": ("Extreme close up of a technician's hands replacing a worn roller wheel on the bottom track "
    "of a sliding glass patio door, tools on the floor, detailed mechanical repair.", "card", (1200,800)),
 "svc-frame": ("A carpenter repairing and reinforcing a wooden exterior door frame and jamb with a drill and wood "
    "shims, fresh lumber, secure sturdy repair, workshop-quality craftsmanship.", "card", (1200,800)),
 "svc-lock": ("Close up of a professional installing a modern brushed-nickel keypad smart lock and handleset on a "
    "charcoal front door, precise hands, clean modern hardware.", "card", (1200,800)),
 "svc-commercial": ("A modern aluminum and glass commercial storefront double door entrance of a small business on "
    "a clean city street, daytime, professional, reflective glass, no readable signage.", "card", (1200,800)),
 "svc-emergency": ("A door service technician making an emergency repair to a home's front entry at dusk, a service "
    "van with soft amber warning lights in the driveway, focused urgent professional work, secure and reassuring.", "card", (1200,800)),
 "svc-cost": ("A clean neat flat lay lineup of different door material samples on a table: fiberglass, steel, solid "
    "wood, and glass-panel door swatches with a tape measure and notepad, bright studio light, top-down.", "card", (1200,800)),
 "area-neighborhood": ("A leafy tree-lined street in an attractive metro Detroit Michigan suburb with well-kept "
    "colonial and ranch homes, green lawns, summer afternoon, wide establishing shot.", "wide", (1600,900)),
 "area-neighborhood2": ("A charming autumn street of brick colonial and mid-century ranch homes in a Michigan suburb, "
    "orange and gold trees, warm afternoon light, welcoming residential scene.", "wide", (1600,900)),
 "process-install": ("Two professional door installers in plain navy work uniforms carefully fitting a new exterior "
    "entry door into a home's doorway, teamwork, tools and level visible, bright daylight, no readable branding.", "card", (1200,800)),
 "about-team": ("A friendly confident professional door installer in a plain navy uniform standing with arms crossed "
    "beside a clean white work van in a Michigan driveway, approachable, trustworthy, bright morning light, no readable branding.", "card", (1200,900)),
 "cta-door": ("A stunning modern craftsman-style fiberglass front door with sidelights on a welcoming home porch at "
    "warm dusk with a glowing porch light, rich inviting tones.", "wide", (1600,760)),
}

def crop_resize(im, w, h):
    im = im.convert("RGB")
    tw, th = w, h
    sw, sh = im.size
    scale = max(tw/sw, th/sh)
    nw, nh = int(sw*scale+0.5), int(sh*scale+0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    left = (nw-tw)//2; top = (nh-th)//2
    return im.crop((left, top, left+tw, top+th))

def gen(name, prompt, tries=3):
    raw_path = os.path.join(RAW_DIR, name+".png")
    if os.path.exists(raw_path):
        return raw_path
    if not KEY:
        raise SystemExit("Set GEMINI_API_KEY (or GEMINI_KEY_FILE) to run image generation.")
    body = {"contents":[{"parts":[{"text": prompt + STYLE}]}]}
    for t in range(tries):
        try:
            req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                headers={"Content-Type":"application/json"})
            r = urllib.request.urlopen(req, timeout=180)
            d = json.load(r)
            for p in d["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    open(raw_path,"wb").write(base64.b64decode(p["inlineData"]["data"]))
                    return raw_path
            print(f"  [{name}] no image part, retry"); time.sleep(3)
        except urllib.error.HTTPError as e:
            print(f"  [{name}] HTTP {e.code}: {e.read().decode()[:200]}"); time.sleep(5+t*5)
        except Exception as e:
            print(f"  [{name}] err {e}"); time.sleep(5)
    return None

def make_og(hero_raw):
    """Compose a branded 1200x630 Open Graph image from the hero."""
    out = os.path.join(IMG_DIR, "og-image.jpg")
    im = crop_resize(Image.open(hero_raw), 1200, 630)
    # darken bottom-left gradient for text legibility
    overlay = Image.new("RGBA", im.size, (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    for y in range(im.size[1]):
        a = int(150 * (y/im.size[1])**1.3)
        od.line([(0,y),(im.size[0],y)], fill=(9,20,40,a))
    od.rectangle([0,0,im.size[0],im.size[1]], fill=(9,20,40,70))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(im)
    def font(sz, bold=True):
        for fp in ([r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"] if bold
                   else [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"]):
            if os.path.exists(fp):
                return ImageFont.truetype(fp, sz)
        return ImageFont.load_default()
    # accent bar
    d.rectangle([70,300,86,470], fill=(232,161,27))
    d.text((110,300), "BH Door Solutions", font=font(74), fill=(255,255,255))
    d.text((112,392), "METRO DETROIT", font=font(30), fill=(248,190,76))
    d.text((110,452), "Door Installation & Repair  •  Same-Day Service", font=font(30, False), fill=(230,238,246))
    d.text((110,500), "(313) 236-4558", font=font(40), fill=(255,255,255))
    im.save(out, quality=88)
    print("  og-image.jpg written")

def make_variants():
    """Responsive srcset variants (-480/-800/-1200.webp) for every template image.
    Sourced from _raw PNGs when available (best quality), else downscaled from the
    full-size webp. Idempotent — skips variants that already exist."""
    widths = (480, 800, 1200)
    for name, (_prompt, _aspect, (w, h)) in IMAGES.items():
        if name == "svc-emergency":
            continue  # service removed from the business
        src_raw = os.path.join(RAW_DIR, name + ".png")
        src_webp = os.path.join(IMG_DIR, name + ".webp")
        src = src_raw if os.path.exists(src_raw) else src_webp
        if not os.path.exists(src):
            print(f"  !! no source for {name}, skipping"); continue
        im0 = Image.open(src)
        for vw in widths:
            if vw >= w:
                continue
            out = os.path.join(IMG_DIR, f"{name}-{vw}.webp")
            if os.path.exists(out):
                continue
            vh = int(round(vw * h / w))
            crop_resize(im0.copy(), vw, vh).save(out, "WEBP", quality=80, method=6)
            print(f"  {name}-{vw}.webp ({vw}x{vh})")
    # the two 1600px area shots are the LCP on 18 city pages — recompress the full size
    for name in ("area-neighborhood", "area-neighborhood2"):
        raw = os.path.join(RAW_DIR, name + ".png")
        full = os.path.join(IMG_DIR, name + ".webp")
        if os.path.exists(raw) and os.path.exists(full) and os.path.getsize(full) > 280_000:
            w, h = IMAGES[name][2]
            crop_resize(Image.open(raw), w, h).save(full, "WEBP", quality=74, method=6)
            print(f"  recompressed {name}.webp -> {os.path.getsize(full)//1024}KB")
    print("variants DONE")

def main():
    hero_raw = None
    for name,(prompt,aspect,(w,h)) in IMAGES.items():
        webp = os.path.join(IMG_DIR, name+".webp")
        if os.path.exists(webp):
            print(f"skip {name} (exists)")
            if name=="hero-home": hero_raw = os.path.join(RAW_DIR,"hero-home.png")
            continue
        print(f"generating {name} ...")
        raw = gen(name, prompt)
        if not raw:
            print(f"  FAILED {name}"); continue
        if name=="hero-home": hero_raw = raw
        im = crop_resize(Image.open(raw), w, h)
        im.save(webp, "WEBP", quality=82, method=6)
        # also a jpg fallback for hero
        if aspect=="wide":
            im.save(os.path.join(IMG_DIR, name+".jpg"), quality=84)
        print(f"  -> {name}.webp ({w}x{h})")
    if hero_raw and os.path.exists(hero_raw):
        make_og(hero_raw)
    print("DONE")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "variants":
        make_variants()
    else:
        main()
        make_variants()
