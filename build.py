"""Build the static Reachloop landing pages (GitHub Pages serves the output as-is).

Run: python3 build.py  → writes index.html, apps/, local/, shops/.
No external requests on any page: fonts are self-hosted, no analytics, no cookies.
The waitlist form (Tally) is embedded once its form id is set in WAITLIST_FORM_ID.
"""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WAITLIST_FORM_ID = ""  # set when the Tally form exists; empty = "opening soon"

SEGMENTS = {
    "apps": {
        "top": "#0b1026",
        "bottom": "#3b2fd9",
        "accent": "#b9b4ff",
        "label": "App & SaaS founders",
        "title": "An AI that runs your app's TikTok and Instagram",
        "h1": "Your app gets a growth team that never stops testing.",
        "sub": "Reachloop writes, designs and publishes a slideshow every day, measures what "
        "each one did, and does more of what brings installs. You keep building.",
        "you": "app",
        "examples": "launch playbooks, onboarding tips, App Store page fixes",
    },
    "local": {
        "top": "#1a0f0a",
        "bottom": "#d9622b",
        "accent": "#ffd2b8",
        "label": "Salons, cafés, gyms & studios",
        "title": "An AI that posts for your business every day",
        "h1": "Your business posts every day. You don't have to.",
        "sub": "Reachloop writes, designs and publishes posts for your salon, café, gym or "
        "studio, learns which ones bring bookings, and does more of those.",
        "you": "business",
        "examples": "quiet-day offers, review requests, behind-the-scenes posts",
    },
    "shops": {
        "top": "#04140f",
        "bottom": "#0f9d6b",
        "accent": "#b6f5dc",
        "label": "Shopify, Etsy & TikTok Shop sellers",
        "title": "An AI that runs your shop's TikTok and Instagram",
        "h1": "Your products, posted every day, by an AI that learns what sells.",
        "sub": "Reachloop turns your catalogue into daily slideshow posts, measures which ones "
        "bring orders, and shifts toward what works.",
        "you": "shop",
        "examples": "product moments, packing videos, before/after descriptions",
    },
}

CSS = """
@font-face { font-family: "Poppins"; font-weight: 800; font-display: swap;
  src: url("/assets/fonts/Poppins-ExtraBold.ttf") format("truetype"); }
:root { --top: #0b1026; --bottom: #3b2fd9; --accent: #b9b4ff; --ink: #ffffff;
  --muted: rgba(255,255,255,.78); --card: rgba(255,255,255,.08); --line: rgba(255,255,255,.16); }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; min-height: 100vh; color: var(--ink);
  font: 17px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: linear-gradient(180deg, var(--top) 0%, var(--bottom) 100%) fixed; }
.wrap { max-width: 760px; margin: 0 auto; padding: 28px 18px 56px; }
header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.brand { display: flex; align-items: center; gap: 10px; color: var(--ink); text-decoration: none;
  font-family: Poppins, sans-serif; font-weight: 800; font-size: 20px; }
.brand span.r { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 10px;
  background: rgba(255,255,255,.14); }
.tag { font-size: 13px; color: var(--muted); border: 1px solid var(--line); border-radius: 999px;
  padding: 4px 10px; white-space: nowrap; }
h1 { font-family: Poppins, sans-serif; font-weight: 800; line-height: 1.12; letter-spacing: -.01em;
  font-size: clamp(32px, 7vw, 52px); margin: 48px 0 16px; }
h2 { font-family: Poppins, sans-serif; font-weight: 800; font-size: 24px; margin: 44px 0 14px; }
h1, h2, p, li { overflow-wrap: break-word; }
p.sub { font-size: 19px; color: var(--muted); margin: 0 0 22px; max-width: 40em; }
.note { display: inline-block; background: var(--card); border: 1px solid var(--line);
  border-left: 4px solid var(--accent); border-radius: 12px; padding: 12px 14px; font-size: 15px; }
.cta { display: inline-block; margin-top: 22px; background: var(--accent); color: #111;
  font-weight: 700; text-decoration: none; padding: 14px 22px; border-radius: 14px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr));
  gap: 12px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 16px; }
.card b { display: block; font-size: 16px; margin-bottom: 4px; }
.card p { margin: 0; color: var(--muted); font-size: 15px; }
.step { font-family: Poppins, sans-serif; color: var(--accent); font-size: 14px; }
ul.honest { padding-left: 20px; color: var(--muted); }
ul.honest li { margin: 6px 0; }
.waitlist { background: rgba(0,0,0,.22); border: 1px solid var(--line); border-radius: 18px;
  padding: 20px; margin-top: 12px; }
.waitlist iframe { width: 100%; min-height: 420px; border: 0; }
a.seg { color: var(--ink); text-decoration: none; display: block; }
a.seg:hover .card { border-color: var(--accent); }
footer { margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--line); color: var(--muted);
  font-size: 13px; }
footer a { color: var(--muted); }
"""


def esc(text: str) -> str:
    """HTML-escape a text node."""
    return html.escape(text, quote=True)


def head(title: str, description: str, icon: str, colors: dict[str, str] | None) -> str:
    """The document head with segment colours as CSS variables."""
    style_vars = ""
    if colors:
        style_vars = (
            f":root {{ --top: {colors['top']}; --bottom: {colors['bottom']}; "
            f"--accent: {colors['accent']}; }}"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="icon" type="image/png" href="/assets/{icon}">
<link rel="stylesheet" href="/assets/style.css">
<style>{style_vars}</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="brand" href="/"><span class="r">R</span>Reachloop</a>
  <span class="tag">AI-run, openly</span>
</header>
"""


def waitlist(segment: str) -> str:
    """The waitlist block: the Tally embed when configured, else 'opening soon'."""
    if WAITLIST_FORM_ID:
        src = (
            f"https://tally.so/embed/{WAITLIST_FORM_ID}?alignLeft=1&hideTitle=1"
            f"&transparentBackground=1&segment={segment}"
        )
        body = f'<iframe src="{esc(src)}" title="Reachloop waitlist" loading="lazy"></iframe>'
    else:
        body = (
            "<p><b>The waitlist opens in a few days.</b> The first 20 founding members get "
            "50% off for life and are onboarded personally.</p>"
        )
    return f'<h2 id="waitlist">Join the founding list</h2>\n<div class="waitlist">{body}</div>\n'


FOOTER = """<footer>
  <p>Reachloop is an AI growth engine. Every post on our accounts is written, designed and
  published by AI, and labelled as AI-generated. No fake engagement: it never likes, follows,
  comments or messages on anyone's behalf.</p>
  <p><a href="/apps/">For app founders</a> · <a href="/local/">For local businesses</a> ·
  <a href="/shops/">For online shops</a></p>
</footer>
</div>
</body>
</html>
"""


def segment_page(name: str, s: dict[str, str]) -> str:
    """One segment's landing page."""
    return (
        head(f"Reachloop — {s['title']}", s["sub"], f"favicon-{name}.png", s)
        + f"""
<h1>{esc(s['h1'])}</h1>
<p class="sub">{esc(s['sub'])}</p>
<p class="note">The account that sent you here is run by Reachloop, start to finish:
every post, every caption, every posting time.</p>
<br><a class="cta" href="#waitlist">Join the founding list</a>

<h2>How it works</h2>
<div class="grid">
  <div class="card"><span class="step">1</span><b>Tell it about your {esc(s['you'])}</b>
    <p>Five minutes: what you sell, who buys it, how you sound.</p></div>
  <div class="card"><span class="step">2</span><b>It posts every day</b>
    <p>Slideshows for TikTok and Instagram: {esc(s['examples'])}.</p></div>
  <div class="card"><span class="step">3</span><b>It learns what works</b>
    <p>Every post is a small experiment. What brings results gets more, the rest gets
    dropped. You get a short weekly report.</p></div>
</div>

<h2>Honest by design</h2>
<ul class="honest">
  <li>Posts are labelled as AI-generated. No fake people, no invented reviews or numbers.</li>
  <li>No engagement tricks: it never auto-likes, follows, comments or DMs, so your account
    stays safe.</li>
  <li>It publishes through the platforms' official posting access. Your passwords never
    leave you.</li>
</ul>

{waitlist(name)}"""
        + FOOTER
    )


def index_page() -> str:
    """The root page: what Reachloop is, and a door per segment."""
    cards = "\n".join(
        f'  <a class="seg" href="/{name}/"><div class="card"><b>{esc(s["label"])}</b>'
        f"<p>{esc(s['title'])}.</p></div></a>"
        for name, s in SEGMENTS.items()
    )
    return (
        head(
            "Reachloop — an AI that runs your TikTok and Instagram",
            "Reachloop writes, designs and publishes posts every day and learns what works.",
            "favicon.png",
            None,
        )
        + f"""
<h1>An AI that runs your TikTok and Instagram, and learns what grows you.</h1>
<p class="sub">Reachloop writes, designs and publishes a post every day, measures what each
one did, and does more of what works. Our own accounts are run by it, openly.</p>

<h2>Who it's for</h2>
<div class="grid">
{cards}
</div>
"""
        + FOOTER
    )


def main() -> None:
    """Write every page and the stylesheet."""
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(index_page(), encoding="utf-8")
    for name, s in SEGMENTS.items():
        (ROOT / name).mkdir(exist_ok=True)
        (ROOT / name / "index.html").write_text(segment_page(name, s), encoding="utf-8")
    print("built:", ", ".join(["index.html"] + [f"{n}/index.html" for n in SEGMENTS]))


if __name__ == "__main__":
    main()
