#!/usr/bin/env python3
"""Builds the SVG assets used by the profile README.

    python3 scripts/build_assets.py

Everything is plain SVG with system fonts and CSS animation, so the images
render on GitHub without scripts or third-party requests. To add a technology
chip, add a line to CHIPS and run the script again.
"""

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

BG = "#0f1113"
PANEL = "#15181b"
LINE = "#24282c"
PAPER = "#f3f0eb"
TEXT = "#c9cbcc"
MUTED = "#8a9096"
AMBER = "#f28a2e"
SIGNAL = "#13b5d8"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# (file name, label, group) — group "used" = shipped in a project, "learning" = current study
CHIPS = [
    ("python", "Python", "used"),
    ("php", "PHP", "used"),
    ("javascript", "JavaScript", "used"),
    ("bash", "Bash", "used"),
    ("sql", "SQL", "used"),
    ("html-css", "HTML & CSS", "used"),
    ("laravel", "Laravel", "used"),
    ("filament", "Filament", "used"),
    ("tailwind-css", "Tailwind CSS", "used"),
    ("blade", "Blade", "used"),
    ("vanilla-js", "Vanilla JS", "used"),
    ("gsap", "GSAP", "used"),
    ("vite", "Vite", "used"),
    ("asyncio", "asyncio", "used"),
    ("telegram-bots", "Telegram bots", "used"),
    ("rest-apis", "REST APIs", "used"),
    ("mariadb", "MariaDB", "used"),
    ("linux", "Linux", "used"),
    ("docker", "Docker", "used"),
    ("systemd", "systemd", "used"),
    ("ufw", "UFW", "used"),
    ("apache-litespeed", "Apache / LiteSpeed", "used"),
    ("directadmin", "DirectAdmin", "used"),
    ("dns-tls", "DNS & TLS", "used"),
    ("xray-vless", "Xray / VLESS", "used"),
    ("git", "Git", "used"),
    ("github", "GitHub", "used"),
    ("playwright", "Playwright", "used"),
    ("pytest", "pytest", "used"),
    ("phpunit", "PHPUnit", "used"),
    ("paramiko", "paramiko", "used"),
    ("pillow", "Pillow", "used"),
    ("ffmpeg", "ffmpeg", "used"),
    ("composer-npm", "Composer & npm", "used"),
    ("devops-practices", "DevOps practices", "learning"),
    ("cybersecurity", "Cybersecurity", "learning"),
    ("ai-powered-solutions", "AI-powered solutions", "learning"),
]


def chip(label: str, group: str) -> str:
    size, char = 12.5, 7.55
    text_w = round(len(label) * char, 1)
    width = round(14 + 6 + 9 + text_w + 14)
    dot = (
        f'<circle cx="17" cy="14" r="3" fill="{AMBER}"/>'
        if group == "used"
        else f'<circle cx="17" cy="14" r="2.4" fill="none" stroke="{SIGNAL}" stroke-width="1.4"/>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28" role="img" aria-label="{escape(label)}">'
        f"<title>{escape(label)}</title>"
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="27" rx="6" fill="{PANEL}" stroke="{LINE}"/>'
        f"{dot}"
        f'<text x="29" y="18.3" font-family="{MONO}" font-size="{size}" fill="{PAPER}" textLength="{text_w}" lengthAdjust="spacingAndGlyphs">{escape(label)}</text>'
        "</svg>\n"
    )


def typed_lines(phrases, x, y, size, band_width, cycle=15.0):
    """Typewriter lines: an opaque cover slides right in steps and reveals the text."""
    char = size * 0.6
    window = 100 / len(phrases)
    css, body = [], []
    for i, phrase in enumerate(phrases):
        n, w = len(phrase), round(len(phrase) * char, 1)
        delay = 0 if i == 0 else -(cycle - i * cycle / len(phrases))
        css.append(
            f"@keyframes show{i}{{0%,{window - 0.02:.2f}%{{opacity:1}}{window:.2f}%,100%{{opacity:0}}}}"
            f"@keyframes type{i}{{0%{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"{window * 0.42:.2f}%,{window * 0.93:.2f}%{{transform:translateX({w}px);animation-timing-function:steps(1,end)}}"
            f"{window:.2f}%,100%{{transform:translateX(0)}}}}"
            f".p{i}{{animation:show{i} {cycle}s linear {delay}s infinite}}"
            f".c{i}{{animation:type{i} {cycle}s linear {delay}s infinite}}"
        )
        hidden = "" if i == 0 else ' opacity="0"'
        body.append(
            f'<g class="p{i}"{hidden}>'
            f'<text x="0" y="0" font-family="{MONO}" font-size="{size}" fill="{TEXT}" textLength="{w}" lengthAdjust="spacingAndGlyphs">{escape(phrase)}</text>'
            f'<g class="c{i} cover"><rect x="0" y="{-size * 1.05:.1f}" width="{band_width}" height="{size * 1.5:.1f}" fill="{BG}"/>'
            f'<rect class="cursor" x="3" y="{-size * 0.92:.1f}" width="{max(2, size * 0.12):.1f}" height="{size * 1.15:.1f}" fill="{AMBER}"/></g>'
            "</g>"
        )
    return "".join(css), f'<g transform="translate({x},{y})">{"".join(body)}</g>'


def ports(x, y, count=5, w=40, h=32, gap=12):
    out = []
    for i in range(count):
        px = x + i * (w + gap)
        colour = SIGNAL if i == count - 1 else AMBER
        out.append(
            f'<rect x="{px}" y="{y}" width="{w}" height="{h}" rx="5" fill="{PANEL}" stroke="{LINE}"/>'
            f'<rect x="{px + 10}" y="{y + 11}" width="{w - 20}" height="{h - 17}" rx="2" fill="{BG}" stroke="{LINE}"/>'
            f'<circle class="blink b{i}" cx="{px + w / 2}" cy="{y - 12}" r="3" fill="{colour}"/>'
        )
    return "".join(out)


BASE_CSS = (
    "@keyframes led{0%,88%{opacity:1}90%,94%{opacity:.25}96%,100%{opacity:1}}"
    "@keyframes blink{0%,60%{opacity:1}70%,90%{opacity:.2}100%{opacity:1}}"
    "@keyframes cur{0%,49%{opacity:1}50%,100%{opacity:0}}"
    ".led{animation:led 5s steps(1,end) infinite}"
    ".blink{animation:blink 3.2s steps(1,end) infinite}"
    ".b1{animation-delay:-.6s}.b2{animation-delay:-1.9s}.b3{animation-delay:-1.1s}.b4{animation-delay:-2.6s}"
    ".cursor{animation:cur 1s steps(1,end) infinite}"
)
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}.cover{display:none}}"


def specs(items, x, y, col):
    out = []
    for i, (label, value) in enumerate(items):
        cx = x + i * col
        out.append(
            f'<text x="{cx}" y="{y}" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{AMBER}">{escape(label)}</text>'
            f'<text x="{cx}" y="{y + 28}" font-family="{SANS}" font-size="18" fill="{PAPER}">{escape(value)}</text>'
        )
    return "".join(out)


def header(mobile: bool) -> str:
    title = "Dovlet Halykov — software developer"
    desc = "Profile banner: websites, Linux automation and debugging. Based in Malaysia, open to junior roles and freelance work."
    if mobile:
        w, h = 640, 520
        css, typed = typed_lines(["Websites, end to end.", "Linux server automation.", "Debugging until it works."], 44, 272, 26, 640)
        body = (
            f'<circle class="led" cx="50" cy="60" r="5" fill="{AMBER}"/>'
            f'<text x="68" y="65" font-family="{MONO}" font-size="15" letter-spacing="2.4" fill="{MUTED}">SOFTWARE DEVELOPER</text>'
            f'<line x1="44" y1="98" x2="596" y2="98" stroke="{LINE}"/>'
            f'<text x="42" y="200" font-family="{SANS}" font-size="74" font-weight="700" letter-spacing="-2.4" fill="{PAPER}">Dovlet Halykov</text>'
            f"{typed}"
            f'<line x1="44" y1="330" x2="596" y2="330" stroke="{LINE}"/>'
            + specs([("FOCUS", "Web · Automation · Linux"), ("BASED IN", "Malaysia")], 44, 372, 330)
            + specs([("OPEN TO", "Junior roles · Freelance")], 44, 448, 330)
            + ports(374, 446, count=4)
        )
    else:
        w, h = 1200, 420
        css, typed = typed_lines(
            ["I build websites end to end: design, code, hosting.", "I automate Linux servers with Python and Bash.", "I debug things until they actually work."],
            74, 268, 24, 1200,
        )
        body = (
            f'<circle class="led" cx="80" cy="62" r="5" fill="{AMBER}"/>'
            f'<text x="98" y="67" font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="{MUTED}">SOFTWARE DEVELOPER</text>'
            f'<text x="1128" y="67" text-anchor="end" font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="{MUTED}">GITHUB.COM/DOVLET808</text>'
            f'<line x1="72" y1="96" x2="1128" y2="96" stroke="{LINE}"/>'
            f'<text x="69" y="206" font-family="{SANS}" font-size="88" font-weight="700" letter-spacing="-3" fill="{PAPER}">Dovlet Halykov</text>'
            f"{typed}"
            + ports(872, 170)
            + f'<line x1="72" y1="312" x2="1128" y2="312" stroke="{LINE}"/>'
            + specs([("FOCUS", "Web · Automation · Linux"), ("BASED IN", "Malaysia"), ("OPEN TO", "Junior roles · Freelance")], 72, 348, 352)
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
        f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>'
        f"<style>{BASE_CSS}{css}{REDUCED}</style>"
        f'<rect width="{w}" height="{h}" rx="22" fill="{BG}"/>'
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="21.5" fill="none" stroke="{LINE}"/>'
        f"{body}</svg>\n"
    )


def project_card(eyebrow: str, name: str, lines: list[str]) -> str:
    """Typographic preview for projects that have no user interface to screenshot."""
    w, h = 1440, 900
    rows = "".join(
        f'<line x1="120" y1="{520 + i * 86}" x2="1320" y2="{520 + i * 86}" stroke="{LINE}"/>'
        f'<text x="120" y="{574 + i * 86}" font-family="{MONO}" font-size="20" letter-spacing="2" fill="{AMBER}">{i + 1:02d}</text>'
        f'<text x="200" y="{575 + i * 86}" font-family="{SANS}" font-size="34" fill="{TEXT}">{escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(name)}">'
        f"<title>{escape(name)}</title><style>{BASE_CSS}{REDUCED}</style>"
        f'<rect width="{w}" height="{h}" fill="{BG}"/>'
        f'<circle class="led" cx="128" cy="150" r="8" fill="{AMBER}"/>'
        f'<text x="156" y="158" font-family="{MONO}" font-size="22" letter-spacing="3.6" fill="{MUTED}">{escape(eyebrow)}</text>'
        f'<text x="114" y="356" font-family="{MONO}" font-size="104" font-weight="700" letter-spacing="-3" fill="{PAPER}">{escape(name)}</text>'
        + ports(1000, 126, count=5, w=52, h=42, gap=14)
        + rows
        + "</svg>\n"
    )


def divider() -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="12" viewBox="0 0 1200 12" role="presentation" aria-hidden="true">'
        "<style>@keyframes run{0%{transform:translateX(-140px)}100%{transform:translateX(1200px)}}"
        ".run{animation:run 7s linear infinite}@media (prefers-reduced-motion:reduce){.run{animation:none;display:none}}</style>"
        f'<rect y="5.5" width="1200" height="1" fill="{LINE}"/>'
        f'<rect class="run" y="5" width="140" height="2" rx="1" fill="{AMBER}"/>'
        f'<circle cx="6" cy="6" r="3" fill="{AMBER}"/><circle cx="1194" cy="6" r="3" fill="{SIGNAL}"/>'
        "</svg>\n"
    )


def main() -> None:
    (ASSETS / "chips").mkdir(parents=True, exist_ok=True)
    (ASSETS / "projects").mkdir(parents=True, exist_ok=True)
    (ASSETS / "header.svg").write_text(header(mobile=False), encoding="utf-8")
    (ASSETS / "header-mobile.svg").write_text(header(mobile=True), encoding="utf-8")
    (ASSETS / "divider.svg").write_text(divider(), encoding="utf-8")
    for name, label, group in CHIPS:
        (ASSETS / "chips" / f"{name}.svg").write_text(chip(label, group), encoding="utf-8")
    (ASSETS / "projects" / "hostinger-vps-bot.svg").write_text(
        project_card(
            "PYTHON · TELEGRAM BOT",
            "hostinger-vps-bot",
            ["Full VPS lifecycle from a Telegram chat", "asyncio · paramiko · Playwright", "95 unit tests · 100 % parser coverage"],
        ),
        encoding="utf-8",
    )
    print(f"wrote header, mobile header, divider, {len(CHIPS)} chips and 1 project card to {ASSETS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
