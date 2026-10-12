#!/usr/bin/env python3
"""Builds the Art Keeper website's pages from _src/ (standard library only).

    python3 build.py

Wraps each page in the shared header and footer and writes plain HTML files
that GitHub Pages serves as they are. The built pages are committed, so the
site works without running this; run it after changing anything in _src/.

The Privacy Policy and Terms of Use are taken word for word from
_src/legal/privacy.html and _src/legal/terms.html (the approved text). To
publish new wording, replace those two files and rebuild. The only change made
to them is wrapping the permissions table so it scrolls on narrow phones.
"""

from html import escape
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "_src"

NAV = [("/support/", "Support"), ("/privacy/", "Privacy"), ("/terms/", "Terms")]


def layout(*, title: str, description: str, path: str, body: str, home: bool = False) -> str:
    page_title = "Art Keeper" if home else f"{title} · Art Keeper"
    canonical = f"https://artkeeper.app{path}"

    def current(href: str) -> str:
        return ' aria-current="page"' if href == path else ""

    nav_links = "".join(f'<a href="{href}"{current(href)}>{label}</a>' for href, label in NAV)
    footer_links = "".join(f'<li><a href="{href}"{current(href)}>{label}</a></li>' for href, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(page_title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#F4EFE6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121A2A" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/Figtree-400Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Figtree-700Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="wrap">
    <a class="wordmark" href="/"{' aria-current="page"' if home else ''}><img src="/assets/icon-192.png" alt="" width="32" height="32">Art Keeper</a>
    <nav class="topnav" aria-label="Main">{nav_links}</nav>
  </div>
</header>
<main id="main">
{body.strip()}
</main>
<footer class="footer">
  <div class="wrap">
    <nav aria-label="Footer"><ul><li><a href="/"{' aria-current="page"' if home else ''}>Home</a></li>{footer_links}</ul></nav>
    <p><a href="mailto:support@artkeeper.app">support@artkeeper.app</a></p>
  </div>
</footer>
</body>
</html>
"""


def legal_body(name: str) -> str:
    raw = (SRC / "legal" / f"{name}.html").read_text(encoding="utf-8")
    m = re.search(r"<body[^>]*>(.*)</body>", raw, re.S)
    if not m:
        raise SystemExit(f"_src/legal/{name}.html has no <body>")
    inner = m.group(1).strip()
    inner = inner.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
    return f'<div class="wrap wrap--text">\n<article class="prose">\n{inner}\n</article>\n</div>'


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{path.relative_to(ROOT)} isn't a PNG")
    return struct.unpack(">II", head[16:24])


def screens(body: str) -> str:
    """Fills the home page's screenshots carousel from images/screens/.

    Keeps each <li> whose image exists (adding its width and height), and drops
    the whole block between the screens:start and screens:end comments when
    none do, so the section stays hidden until the screenshots arrive.
    """
    m = re.search(r"\s*<!-- screens:start.*?-->(.*?)<!-- screens:end -->\n?", body, re.S)
    if not m:
        return body
    section = m.group(1)
    kept = 0

    def keep(li: re.Match) -> str:
        nonlocal kept
        src = re.search(r'src="/(images/screens/[^"]+)"', li.group(0)).group(1)
        path = ROOT / src
        if not path.exists():
            return ""
        alt = re.search(r'alt="([^"]*)"', li.group(0)).group(1)
        if not alt.strip() or "TODO" in alt:
            raise SystemExit(f"{src}: write its alt text in _src/home.html before building")
        w, h = png_size(path)
        kept += 1
        return li.group(0).replace("<img ", f'<img width="{w}" height="{h}" ', 1)

    section = re.sub(r"[ \t]*<li class=\"screen\">.*?</li>\n", keep, section, flags=re.S)
    return body[: m.start()] + ("\n" + section.rstrip() + "\n" if kept else "\n") + body[m.end():]


PAGES = [
    dict(out="index.html", path="/", home=True, title="Art Keeper",
         description="Scan and keep your child's art and schoolwork, organized by child and school year, with their story in their own voice. No account needed.",
         body=lambda: screens((SRC / "home.html").read_text(encoding="utf-8"))),
    dict(out="support/index.html", path="/support/", title="Support",
         description="Get help with Art Keeper: contact support@artkeeper.app and answers to common questions.",
         body=lambda: (SRC / "support.html").read_text(encoding="utf-8")),
    dict(out="privacy/index.html", path="/privacy/", title="Privacy Policy",
         description="Art Keeper's privacy policy.", body=lambda: legal_body("privacy")),
    dict(out="terms/index.html", path="/terms/", title="Terms of Use",
         description="Art Keeper's terms of use.", body=lambda: legal_body("terms")),
    dict(out="404.html", path="/404.html", title="Page not found",
         description="This page doesn't exist.", body=lambda: (SRC / "404.html").read_text(encoding="utf-8")),
]


def main() -> None:
    for p in PAGES:
        out = ROOT / p["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            layout(title=p["title"], description=p["description"], path=p["path"], body=p["body"](), home=p.get("home", False)),
            encoding="utf-8",
        )
        print("wrote", p["out"])


if __name__ == "__main__":
    main()
