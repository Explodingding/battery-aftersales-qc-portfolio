# Changelog — Battery Aftersales QC Portfolio

## v2.0 — Audience layer (May 2026)

### New pages
- **start-here.html** — hub with 3 audience paths (hiring / aftersales / curious)
- **learn.html** — 5-minute plain-language course + quiz
- **decision-tree.html** — interactive symptom → QC check guide
- **glossary.html** — FTTR, IR, BMS, CAN, etc. explained simply
- **cheat-sheet.html** — printable 8-gate reference
- **changelog.html** — this history on the site

### Visual & UX
- Shared site navigation across all pages
- Pack anatomy SVG + before/after repair story on Start Here
- Data tier badges: Published · Literature model · Illustrative QC · Method/WI
- OG preview image for LinkedIn link cards (`assets/og-preview.png`)
- Hub banner on dashboard linking to course & decision tree

### Content & methodology
- Gate method cards (time box, pass/fail, plain-language why)
- Second case study: prismatic LFP module swelling after swap
- Form-factor analytics (cylindrical · prismatic · pouch) — prior release extended
- Glossary tooltips via `data-glossary` attributes

### Build
- `build_portfolio_site.py` — generates pages + OG image
- `data/glossary.json`, `decision_tree.json`, `gate_methods.json`

---

## v1.0 — Core portfolio (May 2026)

- QC dashboard (`index.html`) — KPI, FTTR, Pareto, SPC, 8D
- Repair playbook — BMS timeout LFP ESS case + fault quick-fix table
- Module analytics — literature datasets, generation BOL, impedance models
- GitHub Pages deploy via `docs/`
- LinkedIn 6-slide carousel

---

## Live site

https://explodingding.github.io/battery-aftersales-qc-portfolio/

**Recommended entry for newcomers:** [start-here.html](https://explodingding.github.io/battery-aftersales-qc-portfolio/start-here.html)
