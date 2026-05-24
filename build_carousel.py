"""Generate 5 LinkedIn carousel slides (1080x1080 PNG)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "linkedin" / "carousel"
W, H = 1080, 1080

COLORS = {
    "bg_dark": (13, 92, 99),
    "bg_mid": (15, 118, 110),
    "white": (255, 255, 255),
    "muted": (203, 213, 225),
    "accent": (8, 145, 178),
    "lfp": (5, 150, 105),
    "nmc": (124, 58, 237),
    "warn": (217, 119, 6),
    "card": (240, 253, 250),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def gradient_bg() -> Image.Image:
    img = Image.new("RGB", (W, H), COLORS["bg_dark"])
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(COLORS["bg_dark"][0] * (1 - t) + COLORS["bg_mid"][0] * t)
        g = int(COLORS["bg_dark"][1] * (1 - t) + COLORS["bg_mid"][1] * t)
        b = int(COLORS["bg_dark"][2] * (1 - t) + COLORS["bg_mid"][2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img


def draw_header(draw: ImageDraw.ImageDraw, title: str, subtitle: str = "") -> int:
    draw.rectangle([(0, 0), (W, 8)], fill=COLORS["accent"])
    draw.text((60, 48), title, font=font(52, True), fill=COLORS["white"])
    y = 115
    if subtitle:
        draw.text((60, y), subtitle, font=font(28), fill=COLORS["muted"])
        y += 45
    draw.line([(60, y), (W - 60, y)], fill=(255, 255, 255, 80), width=2)
    return y + 30


def text_width(text: str, fnt: ImageFont.FreeTypeFont) -> float:
    try:
        return fnt.getlength(text)
    except AttributeError:
        return fnt.getsize(text)[0]


def wrap_text(text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if text_width(test, fnt) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def slide1_cover() -> Image.Image:
    img = gradient_bg()
    draw = ImageDraw.Draw(img)
    draw.text((60, 320), "8 GATES", font=font(88, True), fill=COLORS["white"])
    draw.text((60, 420), "BEFORE RELEASE", font=font(88, True), fill=COLORS["white"])
    draw.text((60, 540), "Quality control for repaired", font=font(36), fill=COLORS["muted"])
    draw.text((60, 590), "lithium-ion battery packs", font=font(36), fill=COLORS["muted"])
    draw.rounded_rectangle([(60, 680), (520, 740)], radius=12, fill=COLORS["accent"])
    draw.text((80, 695), "NMC · LFP · ESS · EV Aftersales", font=font(26, True), fill=COLORS["white"])
    draw.text((60, 800), "Łukasz Klimowski", font=font(32, True), fill=COLORS["white"])
    draw.text((60, 850), "Northvolt · Prodrive · Brainport", font=font(26), fill=COLORS["muted"])
    draw.text((60, 980), "1 / 6", font=font(24), fill=COLORS["muted"])
    return img


def slide2_gate() -> Image.Image:
    img = gradient_bg()
    draw = ImageDraw.Draw(img)
    y0 = draw_header(draw, "8-Step Repair QC Gate", "Every returned pack — same verified states")
    steps = [
        "Incoming & ESD check",
        "HV isolation (IR test)",
        "Cell / module balance",
        "BMS / CAN diagnostics",
        "Thermal system check",
        "Repair to work instruction",
        "Post-repair functional test",
        "Final release + SPC",
    ]
    y = y0
    for i, step in enumerate(steps, 1):
        draw.ellipse([(60, y), (100, y + 40)], fill=COLORS["accent"])
        draw.text((72, y + 6), str(i), font=font(22, True), fill=COLORS["white"])
        draw.text((120, y + 6), step, font=font(30), fill=COLORS["white"])
        y += 58
    draw.text((60, 980), "2 / 6  ·  Failures stop the line", font=font(24), fill=COLORS["muted"])
    return img


def slide3_chemistry() -> Image.Image:
    img = gradient_bg()
    draw = ImageDraw.Draw(img)
    y0 = draw_header(draw, "NMC vs LFP", "Different chemistry → different repair focus")
    # NMC card
    draw.rounded_rectangle([(60, y0), (510, y0 + 340)], radius=16, fill=COLORS["nmc"])
    draw.text((80, y0 + 20), "NMC", font=font(40, True), fill=COLORS["white"])
    for i, line in enumerate(["EV · Bus · Mobility", "Cell drift · Thermal", "HV connector wear", "Tight IR tolerance"]):
        draw.text((80, y0 + 80 + i * 55), "• " + line, font=font(28), fill=COLORS["white"])
    # LFP card
    y2 = y0
    draw.rounded_rectangle([(550, y2), (1020, y2 + 340)], radius=16, fill=COLORS["lfp"])
    draw.text((570, y2 + 20), "LFP", font=font(40, True), fill=COLORS["white"])
    for i, line in enumerate(["ESS · UPS · Datacenter", "BMS / CAN timeout", "Config mismatch", "Seal ingress"]):
        draw.text((570, y2 + 80 + i * 55), "• " + line, font=font(28), fill=COLORS["white"])
    draw.text((60, 720), "One checklist for all chemistries", font=font(34, True), fill=COLORS["warn"])
    draw.text((60, 775), "= how repeat repairs happen", font=font(34, True), fill=COLORS["white"])
    draw.text((60, 980), "3 / 6", font=font(24), fill=COLORS["muted"])
    return img


def slide4_case() -> Image.Image:
    img = gradient_bg()
    draw = ImageDraw.Draw(img)
    y0 = draw_header(draw, "Case: BMS Timeout", "LFP ESS pack — not a board swap")
    draw.rounded_rectangle([(60, y0), (200, y0 + 44)], radius=8, fill=COLORS["lfp"])
    draw.text((75, y0 + 8), "FC-02", font=font(24, True), fill=COLORS["white"])
    draw.text((220, y0 + 8), "CAN timeout at energy storage site", font=font(28), fill=COLORS["muted"])
    items = [
        ("Symptom", "BMS no response — board swap didn't fix it"),
        ("Root cause 1", "Connector moisture — pin 4-7 open circuit"),
        ("Root cause 2", "Wrong firmware profile (bus vs ESS site)"),
        ("Fix", "Harness section + golden image re-flash"),
        ("Result", "FTTR Yes · 1.2 days · FC-02 down 38%"),
    ]
    y = y0 + 70
    for label, text in items:
        draw.text((60, y), label.upper(), font=font(22, True), fill=COLORS["accent"])
        for line in wrap_text(text, font(30), W - 120):
            draw.text((60, y + 28), line, font=font(30), fill=COLORS["white"])
            y += 38
        y += 22
    draw.text((60, 980), "4 / 6  ·  Dual-layer RCA", font=font(24), fill=COLORS["muted"])
    return img


def slide5_form_factor() -> Image.Image:
    img = gradient_bg()
    draw = ImageDraw.Draw(img)
    y0 = draw_header(draw, "Cell format vs QC gate", "Cylindrical · Prismatic · Pouch — same Li-ion, different tests")

    cards = [
        ("Cylindrical", COLORS["accent"], [
            "Jelly-roll · steel case",
            "QC: per-cell IR spread",
            "String match + BMS relearn",
            "Best mechanical robustness",
        ]),
        ("Prismatic", COLORS["warn"], [
            "Stacked · hard Al/steel case",
            "QC: weld/busbar IR",
            "Compression frame + shims",
            "Common for LFP ESS modules",
        ]),
        ("Pouch", (220, 38, 38), [
            "Laminated foil · no rigid shell",
            "QC: laminate + bulge check",
            "Stack pressure / frame torque",
            "Swelling breaks thermal contact",
        ]),
    ]
    col_w = 300
    gap = 30
    x0 = 60
    card_h = 520
    for i, (title, color, lines) in enumerate(cards):
        x = x0 + i * (col_w + gap)
        draw.rounded_rectangle([(x, y0), (x + col_w, y0 + card_h)], radius=14, fill=color)
        draw.text((x + 16, y0 + 16), title, font=font(32, True), fill=COLORS["white"])
        y = y0 + 70
        for line in lines:
            for wrapped in wrap_text(line, font(24), col_w - 32):
                draw.text((x + 16, y), "• " + wrapped, font=font(24), fill=COLORS["white"])
                y += 34
            y += 8

    draw.text((60, y0 + card_h + 24), "Aftersales: match the gate to construction — not chemistry alone.", font=font(28, True), fill=COLORS["white"])
    draw.text((60, y0 + card_h + 68), "Analytics: …/battery-analytics.html", font=font(22), fill=COLORS["muted"])
    draw.text((60, 980), "5 / 6  ·  Form factor drives failure mode", font=font(24), fill=COLORS["muted"])
    return img


def slide6_cta() -> Image.Image:
    img = gradient_bg()
    draw = ImageDraw.Draw(img)
    draw.text((60, 200), "High-volume", font=font(64, True), fill=COLORS["white"])
    draw.text((60, 280), "aftersales?", font=font(64, True), fill=COLORS["white"])
    draw.text((60, 400), "Target FTTR ≥ 92%", font=font(38), fill=COLORS["muted"])
    draw.text((60, 460), "Scale fixes via WI updates,", font=font(32), fill=COLORS["muted"])
    draw.text((60, 505), "golden firmware, torque logs", font=font(32), fill=COLORS["muted"])
    draw.rounded_rectangle([(60, 580), (1020, 720)], radius=16, fill=COLORS["accent"])
    draw.text((90, 610), "Full interactive portfolio", font=font(36, True), fill=COLORS["white"])
    draw.text((90, 665), "Link in comments ↓", font=font(32), fill=COLORS["white"])
    draw.text((60, 780), "Dashboard · SPC · Pareto · Repair Playbook", font=font(28), fill=COLORS["muted"])
    draw.text((60, 830), "#BatteryQuality #Aftersales #QualityEngineering", font=font(24), fill=COLORS["muted"])
    draw.text((60, 900), "What's your #1 repeat fault on returned packs?", font=font(30, True), fill=COLORS["white"])
    draw.text((60, 980), "6 / 6", font=font(24), fill=COLORS["muted"])
    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    slides = [
        ("01-cover.png", slide1_cover),
        ("02-eight-gate.png", slide2_gate),
        ("03-nmc-lfp.png", slide3_chemistry),
        ("04-case-bms.png", slide4_case),
        ("05-form-factor-qc.png", slide5_form_factor),
        ("06-cta-link.png", slide6_cta),
    ]
    for name, fn in slides:
        path = OUT / name
        fn().save(path, "PNG", optimize=True)
        print(f"PNG: {path}")
    print(f"\nLinkedIn: Create post -> Add document -> upload 01-06 PNGs from {OUT}")


if __name__ == "__main__":
    main()
