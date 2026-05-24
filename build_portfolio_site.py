"""Generate HTML pages and OG preview image."""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "battery-aftersales-quality" / "html"
ASSETS = HTML / "assets"
OG = "https://explodingding.github.io/battery-aftersales-qc-portfolio/assets/og-preview.png"
SITE = "https://explodingding.github.io/battery-aftersales-qc-portfolio"

NAV = """  <nav class="toolbar no-print">
    <motion id="site-nav" class="site-nav"></div>
    <button type="button" onclick="window.print()">Print / PDF</button>
  </nav>"""

FOOT = '  <p class="footer-note">Portfolio · Łukasz Klimowski · <a href="changelog.html">Changelog</a></p>'


def shell(title: str, desc: str, path: str, body: str, scripts: str = "") -> str:
    nav = NAV.replace("motion", "motion").replace("motion", "div")
    nav = nav.replace("<motion ", "<div ").replace("</motion>", "</motion>")
    nav = NAV.replace("<motion ", "<div ").replace("</motion>", "</div>")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{SITE}/{path}">
  <meta property="og:image" content="{OG}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="assets/portfolio.css">
  <link rel="stylesheet" href="assets/site.css">
</head>
<body>
{nav}
{body}
{FOOT}
  <script src="assets/site.js"></script>
{scripts}
</body>
</html>"""


def build_learn() -> None:
    body = """
  <header class="hero"><div class="hero-inner">
    <span class="hero-badge">5 chapters · ~5 minutes</span>
    <h1>Battery aftersales in 5 minutes</h1>
    <p>Plain language intro — what a pack is, why 8 gates exist, quick quiz.</p>
  </div></header>
  <main class="container"><section class="section">
    <div id="learn-progress" class="learn-progress"></div>
    <motion id="learn-chapters"></div>
    <div class="learn-nav no-print">
      <button type="button" class="btn-secondary" id="learn-prev">← Back</button>
      <button type="button" class="btn-primary" id="learn-next">Next →</button>
    </div>
    <div id="learn-complete" class="learn-complete" hidden>
      <h2>You know the basics</h2>
      <p><a href="decision-tree.html">Decision tree</a> · <a href="index.html">Dashboard</a> · <a href="repair-playbook.html">Playbook</a></p>
    </div>
  </section></main>"""
    body = body.replace("<motion ", "<div ").replace("</motion>", "</div>")
    (HTML / "learn.html").write_text(
        shell("5-Minute Course — Battery Aftersales QC", "Plain-language intro to repair QC gates.", "learn.html", body,
              '  <script src="assets/learn.js"></script>'),
        encoding="utf-8",
    )


def build_decision_tree() -> None:
    body = """
  <header class="hero"><div class="hero-inner">
    <span class="hero-badge">Interactive intake guide</span>
    <h1>Returned pack — what do you check first?</h1>
    <p>Symptom → recommended gates. Not a substitute for work instructions.</p>
  </div></header>
  <main class="container"><section class="section">
    <div id="tier-legend" class="tier-legend"></div>
    <div id="dt-root"></div>
  </section></main>"""
    (HTML / "decision-tree.html").write_text(
        shell("Decision Tree — Battery Aftersales Intake", "Interactive EV vs ESS symptom guide.", "decision-tree.html", body,
              '  <script src="assets/decision-tree.js"></script>\n  <script>renderTierLegend();</script>'),
        encoding="utf-8",
    )


def build_glossary() -> None:
    body = """
  <header class="hero"><motion class="hero-inner"><h1>Glossary</h1>
    <p>Plain-language definitions. Hover terms on other pages for quick tips.</p>
  </div></header>
  <main class="container"><section class="section glossary-page"><dl id="glossary-list"></dl></section></main>"""
    body = body.replace("<motion ", "<div ")
    (HTML / "glossary.html").write_text(
        shell("Glossary — Battery Aftersales Terms", "FTTR, IR, BMS, CAN explained simply.", "glossary.html", body,
              '  <script>document.addEventListener("DOMContentLoaded", () => renderGlossaryPage());</script>'),
        encoding="utf-8",
    )


def build_cheat_sheet() -> None:
    body = """
  <header class="hero"><div class="hero-inner"><h1>8-Gate QC Cheat Sheet</h1>
    <p>Print (Ctrl+P) for workshop use.</p></motion></header>
  <main class="container"><section class="section">
    <div id="cheat-grid" class="cheat-grid"></div>
    <p style="font-size:0.8rem;color:var(--muted);margin-top:1rem;">Add-on by format: cylindrical → IR spread · prismatic → compression · pouch → swell check.</p>
  </section></main>"""
    body = body.replace("</motion>", "</div>")
    scripts = """  <script>
fetch("data/gate_methods.json").then(r=>r.json()).then(d=>{
  document.getElementById("cheat-grid").innerHTML = d.gates.map(g=>
    '<div class="cheat-cell"><strong>Gate '+g.step+': '+g.name+'</strong>Pass: '+g.pass+'<br>Fail: '+g.fail_action+'<br><em>'+g.plain_why+'</em></div>'
  ).join("");
});
</script>"""
    (HTML / "cheat-sheet.html").write_text(
        shell("QC Cheat Sheet — 8 Gates", "Printable repair QC reference.", "cheat-sheet.html", body, scripts),
        encoding="utf-8",
    )


def build_changelog() -> None:
    body = """
  <header class="hero"><div class="hero-inner"><h1>Changelog</h1></div></header>
  <main class="container"><section class="section changelog-list">
    <h3>May 2026 — v2.0 Audience layer</h3>
    <ul>
      <li>Start-here hub · 5-min course · decision tree · glossary · cheat sheet</li>
      <li>Form-factor analytics · second case study (prismatic swelling)</li>
      <li>Gate method cards · data tier badges · OG preview image</li>
    </ul>
    <h3>May 2026 — v1.0 Core portfolio</h3>
    <ul>
      <li>QC dashboard · repair playbook · module analytics · LinkedIn carousel</li>
    </ul>
  </section></main>"""
    (HTML / "changelog.html").write_text(
        shell("Changelog", "Portfolio update history.", "changelog.html", body), encoding="utf-8"
    )


def build_og() -> None:
    if not Image:
        return
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), (13, 92, 99))
    draw = ImageDraw.Draw(img)
    try:
        f1 = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 52)
        f2 = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 28)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    draw.text((60, 180), "8 GATES BEFORE RELEASE", font=f1, fill=(255, 255, 255))
    draw.text((60, 260), "Battery aftersales quality portfolio", font=f2, fill=(203, 213, 225))
    draw.text((60, 320), "Interactive guides · NMC · LFP · EV · ESS", font=f2, fill=(203, 213, 225))
    draw.text((60, 520), "Łukasz Klimowski", font=f2, fill=(125, 211, 252))
    img.save(ASSETS / "og-preview.png", "PNG", optimize=True)


def main() -> None:
    build_learn()
    build_decision_tree()
    build_glossary()
    build_cheat_sheet()
    build_changelog()
    build_og()
    print("Site pages OK")


if __name__ == "__main__":
    main()
