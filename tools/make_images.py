#!/usr/bin/env python3
"""Generates every marketing image (feature scenes, OG images, blog covers, template thumbnails).
Inputs: assets/img/templates/*.png and tools/source/phones/*.png (rendered with tool/site_render.dart in the Flutter repo)
        tools/source/{templates,edit-inv,create-inv,dashboard}.png (real app screenshots)
Run from the site root:  python3 tools/make_images.py
Needs: Pillow and Google Chrome (headless). Scenes are HTML files in _scenes/ rendered to JPG.
"""
import os, re, subprocess, tempfile, shutil, json, sys, http.server, threading, socketserver
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets/img")
SRC = os.path.join(ROOT, "tools/source")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 8121
os.makedirs(f"{ROOT}/_scenes", exist_ok=True)
os.makedirs(f"{IMG}/og", exist_ok=True)
os.makedirs(f"{IMG}/blog", exist_ok=True)


def slug(n):
    return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")


# ---------------------------------------------------------------- 1. template thumbnails png -> jpg
def convert_thumbs():
    for f in os.listdir(f"{IMG}/templates"):
        if f.endswith(".png"):
            im = Image.open(f"{IMG}/templates/{f}").convert("RGB")
            im.save(f"{IMG}/templates/{f[:-4]}.jpg", quality=86, optimize=True)
            os.remove(f"{IMG}/templates/{f}")


# ---------------------------------------------------------------- 2. real screenshots -> slots
def cover(im, w, h, anchor=(0.0, 0.0)):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
    x = int((im.width - w) * anchor[0]); y = int((im.height - h) * anchor[1])
    return im.crop((x, y, x + w, y + h))


def shots():
    t = Image.open(f"{SRC}/templates.png").convert("RGB")
    cover(t.crop((0, 0, 2092, 1200)), 900, 700, (0.5, 0)).save(f"{IMG}/how-step-2.jpg", quality=88)
    e = Image.open(f"{SRC}/edit-inv.png").convert("RGB")
    cover(e.crop((0, 60, 2088, 1322)), 900, 700, (0.5, 0)).save(f"{IMG}/how-step-3.jpg", quality=88)


# ---------------------------------------------------------------- 3. HTML scenes
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500&family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap">'
CSS = """
*{box-sizing:border-box;margin:0}
body{font-family:Inter,sans-serif;color:#4A4C5E;overflow:hidden;position:relative}
.bg{position:absolute;inset:0}
.phone{position:absolute;width:var(--w,300px);border:10px solid #1a1a1f;border-radius:46px;background:#fff;overflow:hidden}
.phone::before{content:"";position:absolute;top:9px;left:50%;transform:translateX(-50%);width:32%;height:20px;background:#1a1a1f;border-radius:14px;z-index:3}
.phone img{display:block;width:100%;aspect-ratio:600/1250;object-fit:cover;object-position:top}
.card{position:absolute;border-radius:14px;overflow:hidden;background:#fff;border:1px solid #EDE9E8}
.card img{display:block;width:100%;height:100%;object-fit:cover;object-position:top}
.chip{position:absolute;display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #EDE9E8;border-radius:16px;padding:12px 16px;font:600 15px Inter;color:#2B2D42;white-space:nowrap}
.chip small{display:block;font:400 12px Inter;color:#8A8C9B;margin-top:1px}
.chip i{width:34px;height:34px;border-radius:50%;background:#EAF6EE;display:flex;align-items:center;justify-content:center;flex:none}
.chip i svg{width:18px;height:18px;stroke:#43A567;fill:none;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.chip.pink i{background:#FDEDF0}.chip.pink i svg{stroke:#E94B6F}
.script{position:absolute;font:500 34px Caveat;color:#8A8C9B;transform:rotate(-6deg)}
h1{font:700 60px/1.06 'Playfair Display',serif;color:#2B2D42;letter-spacing:-.01em}
h1 em{font-style:normal;color:#E94B6F}
.eyebrow{font:600 15px Inter;letter-spacing:.1em;text-transform:uppercase;color:#E94B6F;margin-bottom:18px}
.logo{position:absolute;height:44px}
.qr{position:absolute;background:#fff;border-radius:14px;padding:12px;border:1px solid #EDE9E8}
.qr svg{width:100%;height:100%;display:block}
"""

CHECK = '<svg viewBox="0 0 24 24"><path d="m5 12 5 5L20 7"/></svg>'
EYE = '<svg viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>'
QRSVG = '<svg viewBox="0 0 64 64"><rect width="64" height="64" fill="#fff"/><g fill="#2B2D42"><rect x="4" y="4" width="18" height="18"/><rect x="42" y="4" width="18" height="18"/><rect x="4" y="42" width="18" height="18"/><rect x="8" y="8" width="10" height="10" fill="#fff"/><rect x="46" y="8" width="10" height="10" fill="#fff"/><rect x="8" y="46" width="10" height="10" fill="#fff"/><rect x="11" y="11" width="4" height="4"/><rect x="49" y="11" width="4" height="4"/><rect x="11" y="49" width="4" height="4"/><rect x="28" y="6" width="6" height="6"/><rect x="28" y="20" width="10" height="6"/><rect x="6" y="28" width="8" height="6"/><rect x="20" y="30" width="8" height="8"/><rect x="34" y="30" width="6" height="10"/><rect x="46" y="28" width="12" height="6"/><rect x="28" y="44" width="8" height="8"/><rect x="42" y="42" width="6" height="6"/><rect x="52" y="44" width="8" height="10"/><rect x="40" y="54" width="10" height="6"/></g></svg>'

TINTS = {"pink": ("#FDEDF0", "#FFF6F0"), "blue": ("#EAF1FF", "#F4EEFB"), "green": ("#E9F6EE", "#EAF7FB"), "gold": ("#FFF5DD", "#FDEDF0"), "violet": ("#F1EAFB", "#FDEDF0"), "night": ("#E7E9F7", "#F1EAFB")}


def page(w, h, body, tint="pink"):
    a, b = TINTS[tint]
    return f'<!doctype html><meta charset="utf-8">{FONTS}<style>{CSS}</style><body style="width:{w}px;height:{h}px"><div class="bg" style="background:linear-gradient(135deg,{a},{b})"></div>{body}</body>'


def phone(slug_, x, y, w=300, rot=0, z=2):
    return f'<div class="phone" style="left:{x}px;top:{y}px;--w:{w}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}"><img src="/tools/source/phones/{slug_}.png"></div>'


def card(slug_, x, y, w, h, rot=0, z=1):
    return f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}"><img src="/assets/img/templates/{slug_}.jpg"></div>'


def chip(txt, sub, x, y, kind="", icon=CHECK, z=5):
    return f'<div class="chip {kind}" style="left:{x}px;top:{y}px;z-index:{z}"><i>{icon}</i><span>{txt}<small>{sub}</small></span></div>'


def feature(main, back, chips, tint, script=None):
    """900x700 scene: a phone with the template, a rotated card behind it and floating status chips."""
    b = card(back[0], 470, 70, 300, 375, rot=8, z=1) + card(back[1], 90, 130, 260, 325, rot=-9, z=1)
    b += phone(main, 300, 60, 290, 0, 2)
    for c in chips:
        b += c
    if script:
        b += f'<div class="script" style="left:{script[1]}px;top:{script[2]}px">{script[0]}</div>'
    return page(900, 700, b, tint)


SCENES = {}  # (relative output path, w, h) -> html

FEATS = {
    "wedding": ("garden-romance", ("golden-arch-x", "cherry-blossom"), "pink", ("Emma & Jack", "RSVP: yes, 2 guests")),
    "birthday": ("balloon-bash", ("confetti-night", "rose-polaroids"), "gold", ("Sofia is 8!", "RSVP: yes, 4 guests")),
    "baby": ("little-star", ("bento-kids", "peach-polaroids"), "blue", ("Baby Emma", "RSVP: yes, 2 guests")),
    "quince": ("royal-frame", ("lavender-dream", "cherry-blossom"), "violet", ("Valentina", "RSVP: yes, 6 guests")),
    "corporate": ("modern-hero", ("year-in-review", "poster-noir"), "night", ("Annual Summit", "42 of 60 confirmed")),
    "graduation": ("photo-grid-party", ("poster-bold", "grid-gold"), "gold", ("Class of 2026", "RSVP: yes, 3 guests")),
    "anniversary": ("cherry-blossom", ("garden-romance", "ivory-frame"), "pink", ("Anna & Tom", "RSVP: yes, 2 guests")),
    "gender": ("starry-night", ("little-star", "twin-moons"), "night", ("Boy or girl?", "RSVP: yes, 5 guests")),
    "holiday": ("confetti-night", ("year-in-review", "moonlight-dinner"), "night", ("Holiday party", "RSVP: yes, 2 guests")),
    "savedate": ("quiet-edit", ("twin-moons", "sand-minimal"), "pink", ("Save the date", "Opened 2 min ago")),
    "text": ("boho-arch", ("balloon-bash", "modern-hero"), "pink", ("New message", "Tap the link to RSVP")),
    "maker": ("bento-bloom", ("balloon-bash", "garden-romance"), "gold", ("Drag & drop", "Photos, shapes, text")),
    "qr": ("garden-romance", ("boho-arch", "sage-circles"), "pink", ("Scan to RSVP", "Opens in any browser")),
    "rsvp": ("golden-arch", ("garden-romance", "boho-arch"), "green", ("12 replies today", "9 yes · 2 maybe · 1 no")),
}


def scenes():
    for k, (main, back, tint, chipt) in FEATS.items():
        b = (back[0].replace("-x", ""), back[1])
        html = feature(main, b, [chip(chipt[0], chipt[1], 60, 520, "" if k != "text" else "pink"),
                                 chip("Opened just now", "Guest viewed the invitation", 590, 130, "pink", EYE)], tint)
        SCENES[(f"{k}-feature.jpg", 900, 700)] = html
    # how step 4: the "Your invitation is live" moment (rebuilt so it shows no test data)
    import random
    rnd = random.Random(7)
    conf = "".join(f'<i style="position:absolute;left:{rnd.randint(20,880)}px;top:{rnd.randint(10,680)}px;width:{rnd.randint(8,16)}px;height:{rnd.randint(5,10)}px;background:{rnd.choice(["#E94B6F","#F2A93B","#43A567","#6C5CE7","#3AA0FF"])};transform:rotate({rnd.randint(0,180)}deg);border-radius:2px;z-index:1"></i>' for _ in range(46))
    m = f'''<div style="position:absolute;left:150px;top:70px;width:600px;height:560px;background:#fff;border-radius:26px;border:1px solid #EDE9E8;z-index:3;text-align:center;padding-top:40px">
<div style="font:700 44px/1.1 'Playfair Display',serif;color:#2B2D42;margin-top:12px">Your invitation is live!</div>
<p style="font:400 18px/1.5 Inter;margin:12px 60px 0">&ldquo;Sofia&rsquo;s Birthday&rdquo; is ready to share. Send the link or let guests scan the code.</p>
<div class="qr" style="position:relative;width:150px;height:150px;margin:22px auto 0">{QRSVG}</div>
<div style="margin:22px 40px 0;height:48px;border:1px solid #EDE9E8;border-radius:12px;display:flex;align-items:center;justify-content:space-between;padding:0 8px 0 16px;font:500 15px Inter;color:#2B2D42;background:#FAF8F7"><span>myinviteqr.com/?i=4f9a2c...</span><span style="background:#fff;border:1px solid #EDE9E8;border-radius:8px;padding:6px 14px;font-weight:600">Copy</span></div>
<div style="margin:16px 40px 0;height:52px;border-radius:12px;background:#E94B6F;color:#fff;font:600 16px/52px Inter">Go to my event &rarr;</div></div>'''
    SCENES[("how-step-4.jpg", 900, 700)] = page(900, 700, conf + m)
    # home QR scene: printed card + phone
    b = card("garden-romance", 70, 90, 340, 425, rot=-7, z=1)
    b += f'<div class="qr" style="left:250px;top:390px;width:150px;height:150px;transform:rotate(-7deg);z-index:3">{QRSVG}</div>'
    b += phone("garden-romance", 480, 50, 290, 5, 2)
    b += '<div class="script" style="left:110px;top:560px">Scan to RSVP</div>'
    SCENES[("qr-code-invitation.jpg", 900, 700)] = page(900, 700, b)
    # dashboard in a browser frame + phone
    d = f'<div class="card" style="left:40px;top:70px;width:800px;height:540px;border-radius:18px;z-index:1"><div style="height:34px;background:#F6F4F3;border-bottom:1px solid #EDE9E8;display:flex;align-items:center;gap:7px;padding:0 14px"><i style="width:11px;height:11px;border-radius:50%;background:#FF6B6B"></i><i style="width:11px;height:11px;border-radius:50%;background:#F2C94C"></i><i style="width:11px;height:11px;border-radius:50%;background:#43A567"></i></div><img src="/tools/source/dashboard.png" style="height:calc(100% - 34px);object-fit:cover;object-position:top left"></div>'
    d += chip("Sifas birthday", "1 confirmed", 560, 590, "", CHECK, 5)
    SCENES[("rsvp-dashboard.jpg", 900, 700)] = page(900, 700, d, "green")
    # how step 1: wizard screenshot
    w1 = Image.open(f"{SRC}/wizard-step1.png").convert("RGB")
    cover(w1.crop((30, 235, 1030, 935)), 900, 700, (0.0, 0.0)).save(f"{IMG}/how-step-1.jpg", quality=88)


# OG images (1200x630) and blog covers: headline on the left, phone on the right
OGS = {
    "home": ("Design <em>free</em> digital invitations with a QR code", "Free to design. Pay once only to publish.", "garden-romance", "pink"),
    "how": ("Free digital invitation maker: <em>how it works</em>", "Four steps from idea to shared invitation.", "balloon-bash", "gold"),
    "pricing": ("Design free. <em>Pay once</em> to publish.", "Essential $9.99 · Premium $19.99 · no subscription.", "golden-arch", "pink"),
    "templates": ("50 free digital invitation <em>templates</em>", "Weddings, birthdays, baby showers and more.", "bento-bloom", "gold"),
    "faq": ("Digital invitations <em>FAQ</em>", "QR codes, RSVPs, guests and pricing explained.", "modern-hero", "night"),
    "contact": ("We are here <em>to help</em>", "Support for your invitation, order or event.", "boho-arch", "pink"),
    "privacy": ("Privacy <em>Policy</em>", "How we handle your information.", "quiet-edit", "pink"),
    "terms": ("Terms of <em>Service</em>", "The rules for using MyInviteQR.", "quiet-edit", "pink"),
    "blog": ("Free invitation ideas, wording <em>and guides</em>", "The MyInviteQR blog.", "twin-moons", "pink"),
    "wedding": ("Free digital <em>wedding</em> invitations", "QR code, online RSVP, one link for every guest.", "garden-romance", "pink"),
    "birthday": ("Free digital <em>birthday</em> invitations", "Colorful designs. Text one link to everyone.", "balloon-bash", "gold"),
    "baby": ("Free digital <em>baby shower</em> invitations", "Sweet designs and easy replies.", "little-star", "blue"),
    "quince": ("Free digital <em>quinceañera</em> invitations", "Elegant designs for up to 1,000 guests.", "royal-frame", "violet"),
    "corporate": ("Free <em>corporate event</em> invitations", "Professional, branded, trackable.", "modern-hero", "night"),
    "qr": ("Free <em>QR code</em> invitations", "Guests scan and RSVP in seconds.", "garden-romance", "pink"),
    "rsvp": ("Free <em>online RSVP</em> for events", "See who is coming in real time.", "golden-arch", "green"),
    "graduation": ("Free digital <em>graduation</em> invitations", "Celebrate the big day online.", "photo-grid-party", "gold"),
    "anniversary": ("Free digital <em>anniversary</em> invitations", "Milestone celebrations, beautifully shared.", "cherry-blossom", "pink"),
    "gender": ("Free digital <em>gender reveal</em> invitations", "Boy or girl? Invite everyone.", "starry-night", "night"),
    "holiday": ("Free digital <em>holiday party</em> invitations", "Festive designs for family and office.", "confetti-night", "night"),
    "maker": ("Free online <em>invitation maker</em>", "Drag, drop and share with a QR code.", "bento-bloom", "gold"),
    "savedate": ("Free digital <em>save the date</em>", "One link from announcement to invitation.", "quiet-edit", "pink"),
    "text": ("Send invitations <em>by text</em>", "One link. Opens on any phone.", "boho-arch", "pink"),
    "blog-how-to-write-wedding-invitation-wording": ("Wedding invitation <em>wording</em> examples", "Traditional and modern, free to copy.", "garden-romance", "pink"),
    "blog-digital-vs-paper-invitations": ("Digital vs <em>paper</em> invitations", "Cost, speed, RSVPs and etiquette.", "golden-arch", "gold"),
    "blog-how-to-make-a-qr-code-invitation": ("How to make a <em>QR code</em> invitation", "Five easy steps.", "boho-arch", "pink"),
    "blog-baby-shower-invitation-wording": ("Baby shower invitation <em>wording</em>", "20 free ideas and examples.", "little-star", "blue"),
    "blog-birthday-invitation-wording": ("Birthday invitation <em>wording</em>", "25 free ideas for kids and adults.", "balloon-bash", "gold"),
    "blog-how-to-track-rsvps-for-your-event": ("How to track <em>RSVPs</em>", "A simple free guide.", "modern-hero", "night"),
    "blog-quinceanera-invitation-ideas": ("Quinceañera invitation <em>ideas</em>", "Wording, themes and tips.", "royal-frame", "violet"),
}


def ogs():
    for k, (t, sub, tpl, tint) in OGS.items():
        b = f'<img class="logo" src="/assets/img/logo-wordmark.png" style="left:64px;top:56px;height:46px">'
        b += f'<div style="position:absolute;left:64px;top:170px;width:640px"><div class="eyebrow">Digital invitations with QR code</div><h1 style="font-size:58px">{t}</h1><p style="font:400 26px/1.4 Inter;margin-top:22px;color:#4A4C5E">{sub}</p></div>'
        b += phone(tpl, 800, 60, 270, 4, 2) + card("garden-romance" if tpl != "garden-romance" else "boho-arch", 730, 300, 190, 238, -10, 1)
        SCENES[(f"og/{k}.jpg", 1200, 630)] = page(1200, 630, b, tint)
        if k.startswith("blog-"):
            SCENES[(f"blog/{k[5:]}.jpg", 1200, 630)] = page(1200, 630, b, tint)


# ---------------------------------------------------------------- render
def shot(item):
    (out, w, h), html = item
    name = re.sub(r"[^a-z0-9]+", "_", out)
    fp = f"{ROOT}/_scenes/{name}.html"
    open(fp, "w").write(html)
    png = f"{ROOT}/_scenes/{name}.png"
    ud = tempfile.mkdtemp()
    if os.path.exists(png):
        os.remove(png)
    try:
      subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", f"--user-data-dir={ud}", f"--window-size={w},{h}",
                    "--force-device-scale-factor=1", "--virtual-time-budget=5000", f"--screenshot={png}", f"http://localhost:{PORT}/_scenes/{name}.html"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
    except subprocess.TimeoutExpired:
      pass  # Chrome sometimes hangs on exit after writing the screenshot
    im = Image.open(png).convert("RGB").crop((0, 0, w, h))
    im.save(f"{IMG}/{out}", quality=88, optimize=True)
    shutil.rmtree(ud, ignore_errors=True)
    return out


def main():
    only = sys.argv[1:]  # optional filters
    convert_thumbs()
    shots()
    scenes()
    ogs()
    Handler = http.server.SimpleHTTPRequestHandler
    os.chdir(ROOT)
    srv = socketserver.ThreadingTCPServer(("", PORT), type("H", (Handler,), {"log_message": lambda *a: None}))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    items = [(k, v) for k, v in SCENES.items() if not only or any(o in k[0] for o in only)]
    with ThreadPoolExecutor(3) as ex:
        for i, o in enumerate(ex.map(shot, items)):
            print(i + 1, len(items), o, flush=True)
    srv.shutdown()
    shutil.rmtree(f"{ROOT}/_scenes", ignore_errors=True)


if __name__ == "__main__":
    main()
