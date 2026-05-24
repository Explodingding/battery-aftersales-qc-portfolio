# Battery Aftersales Quality — HTML Portfolio

**Candidate:** Łukasz Klimowski  
**Target:** Quality Engineer (Aftersales) — Durapower Technology Group, Helmond

---

## Start here

**New to batteries?** Open **`html/start-here.html`** — 3 paths: hiring manager, aftersales engineer, or 5-min course.

| Page | Content |
|------|---------|
| **`start-here.html`** | Hub · before/after story · pack diagram |
| **`learn.html`** | 5-minute intro course + quiz |
| **`decision-tree.html`** | Interactive symptom → QC guide |
| **`glossary.html`** | Plain-language terms |
| **`cheat-sheet.html`** | Printable 8-gate reference |
| **`index.html`** | QC dashboard (FTTR, SPC, Pareto) |
| **`repair-playbook.html`** | BMS case + prismatic swell case + fault table |
| **`battery-analytics.html`** | Form factors · literature data · models |

> Charts load from `html/data/portfolio.json`. If empty, run:
> ```bash
> python export_portfolio_json.py
> ```
> For live reload with fetch API, use a local server:
> ```bash
> python -m http.server 8080 --directory html
> ```
> Then open http://localhost:8080

---

## What's inside (HTML visualizations)

| Section | Content |
|---------|---------|
| **Durapower context** | NMC/LFP, EV/ESS/UPS applications, EVAAP, Helmond aftersales mission |
| **Pack anatomy** | What we repair: enclosure, modules, BMS, thermal |
| **KPI cards** | FTTR, pass rate, repeat repair, turnaround |
| **`html/repair-playbook.html`** | Case study BMS timeout (LFP ESS) + top faults quick-fix table for high volume |
| **8-step QC gate** | Full battery repair workflow (IR, balance, BMS, thermal, release) |
| **NMC vs LFP** | Different fault patterns & QC focus per chemistry |
| **8D example** | Repeat IR failure after module swap |
| **Experience map** | Northvolt + Prodrive → Durapower aftersales |

---

## Files

```
battery-aftersales-quality/
├── html/
│   ├── index.html              ← main dashboard
│   ├── assets/
│   │   ├── portfolio.css
│   │   └── portfolio.js
│   └── data/
│       └── portfolio.json      ← generated from CSV
├── export_portfolio_json.py
├── build_quality_portfolio.py  ← optional Excel (legacy)
└── data/                       ← source CSVs
```

---

## Durapower alignment

Portfolio reflects public company profile:
- Singapore HQ, global integrator (201–500 employees)
- **NMC** and **LFP** chemistries
- EV, HEV, specialty vehicles, ESS, UPS, datacenter, telecom
- **EVAAP** member since 2014
- Helmond: European aftersales & repair quality

Repair data is **illustrative**; methodology and case studies reflect **real Northvolt/Prodrive experience**.

---

## With application

1. Link or PDF-print the HTML dashboard (`Ctrl+P` → Save as PDF)
2. Attach CV + cover letter from `../html/` and `../pdf/`
3. Mention in cover letter: *"Interactive HTML portfolio shows my repair QC approach for NMC/LFP systems"*
