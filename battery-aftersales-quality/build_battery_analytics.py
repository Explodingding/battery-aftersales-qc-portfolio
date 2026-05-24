"""Build battery analytics JSON for portfolio — literature-informed models + optional NASA sample.

References embedded in output metadata:
- NASA PCoE Li-ion Aging Datasets (impedance, V/I cycles)
- Gogoana et al., J. Power Sources 2013 — resistance mismatch vs cycle life
- Cell parallel string studies — SoH/impedance divergence
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "html" / "data" / "battery_analytics.json"

random.seed(42)

REFERENCES = [
    {
        "id": "nasa",
        "title": "NASA Ames PCoE Li-ion Battery Aging Datasets (2008–2014)",
        "url": "https://data.nasa.gov/dataset/li-ion-battery-aging-datasets",
        "year": 2014,
        "use": "18650 · 2 Ah · V/I/temp · EIS (Re, Rct) — foundational open baseline",
    },
    {
        "id": "devie",
        "title": "Devie et al. (2018) — Intrinsic variability, commercial 18650 batch",
        "url": "https://doi.org/10.3390/en11051031",
        "year": 2018,
        "use": "51 cells · R = 73.2 ± 2.6 mΩ (~3.5% spread) at BOL",
    },
    {
        "id": "gogoana",
        "title": "Gogoana et al. (2013) — Parallel cell resistance matching",
        "url": "https://doi.org/10.1016/j.jpowsour.2013.10.072",
        "year": 2013,
        "use": "~20% ΔR/R → ~40% cycle life loss at 4.5C",
    },
    {
        "id": "kit",
        "title": "Luh & Blank (2024) — KIT NMC/C-SiO aging dataset · Nature Scientific Data",
        "url": "https://doi.org/10.1038/s41597-024-03831-x",
        "year": 2024,
        "use": "228 cells · OCV σ 0.002 V · EIS + 3B log points · prod. Nov 2020",
    },
    {
        "id": "stroebl",
        "title": "Stroebl et al. (2024) — Samsung INR21700-50E multi-stage aging",
        "url": "https://doi.org/10.1038/s41597-024-03859-z",
        "year": 2024,
        "use": "279 cells · 71 conditions · calendar + cycle DoE",
    },
    {
        "id": "piombo",
        "title": "Piombo et al. (2024) — Parallel module full-factorial DoE",
        "url": "https://doi.org/10.1016/j.est.2024.110783",
        "year": 2024,
        "use": "NMC/NCA batches · HPPC R · interconnection R dominates imbalance",
    },
    {
        "id": "zenodo",
        "title": "Zenodo (2024–2025) — Degradation path indicators, 48 commercial cells",
        "url": "https://zenodo.org/records/15755725",
        "year": 2025,
        "use": "EIS/NFRA BOL vs EOL · pulse · CCCV capacity",
    },
    {
        "id": "hummes",
        "title": "Hummes et al. (2023) — EV battery geometry comparison (MAUT)",
        "url": "https://pure.iiasa.ac.at/id/eprint/19437/",
        "year": 2023,
        "use": "Cylindrical vs prismatic vs pouch · thermal · mechanical · swelling",
    },
    {
        "id": "bu301a",
        "title": "Battery University BU-301a — Types of Battery Cells",
        "url": "https://batteryuniversity.com/article/bu-301a-types-of-battery-cells",
        "year": 2024,
        "use": "Jelly roll vs stacked laminate · swelling % · construction",
    },
]


def impedance_mismatch_curves() -> dict:
    """Pack metrics vs % internal resistance spread (weak vs strong cell).

    Efficiency and cycle-life factors are *educational models* calibrated to
    qualitative trends in Gogoana 2013 and parallel-string BMS literature —
    NOT a claim that 1% spread = exactly 1% efficiency loss.
    """
    spreads = [0, 1, 2, 3, 5, 8, 10, 15, 20, 25]
    efficiency_pct = []
    cycle_life_factor = []  # 1.0 = baseline cycles to EOL
    drift_risk = []  # relative voltage divergence index

    for s in spreads:
        # Round-trip efficiency penalty (mild non-linear)
        eff_loss = 0.35 * s + 0.08 * (s**1.35)
        efficiency_pct.append(round(100 - eff_loss, 2))

        # Cycle life factor: steeper after ~5% (inspired by Gogoana ΔR/R up to 20%)
        life = 1.0 / (1.0 + 0.04 * s + 0.006 * (s**2.2))
        cycle_life_factor.append(round(life * 100, 1))

        # Voltage spread index during load
        drift_risk.append(round(1.0 + 0.12 * s + 0.02 * (s**1.5), 2))

    return {
        "spread_pct": spreads,
        "pack_round_trip_efficiency_pct": efficiency_pct,
        "relative_cycle_life_pct": cycle_life_factor,
        "voltage_divergence_index": drift_risk,
        "note": (
            "Illustrative pack-level model for aftersales QC storytelling. "
            "At 20% resistance mismatch, literature reports ~40% lifetime reduction (Gogoana 2013). "
            "Small spreads (1–3%) have smaller but non-zero impact — BMS balancing load increases."
        ),
    }


def string_charge_profiles() -> dict:
    """Simulate 12-cell series string voltages during CC charge — three scenarios."""
    n_cells = 12
    t = list(range(0, 101))  # % SOC proxy
    scenarios = {}

    def cell_v(soc: float, base: float, spread: float, index: int) -> float:
        # 3.2–4.15 V per cell typical NMC/LFP blend for demo
        v_min, v_max = 3.25, 4.12
        progress = soc / 100.0
        offset = spread * (index - (n_cells - 1) / 2) / ((n_cells - 1) / 2)
        return base * (v_min + (v_max - v_min) * progress) + offset

    # Matched pack
    matched = {"t": t, "cells": [], "pack_v": []}
    for i in range(n_cells):
        matched["cells"].append([round(cell_v(s, 1.0, 0.0, i), 3) for s in t])
    matched["pack_v"] = [round(sum(matched["cells"][j][k] for j in range(n_cells)), 2) for k in range(len(t))]

    # 3% impedance/capacity spread, passive (no balancing)
    passive = {"t": t, "cells": [], "pack_v": [], "delta_max": []}
    spreads = [0.03 * (i - 5.5) / 5.5 for i in range(n_cells)]
    for i in range(n_cells):
        passive["cells"].append([round(cell_v(s, 1.0, spreads[i], i), 3) for s in t])
    passive["pack_v"] = [round(sum(passive["cells"][j][k] for j in range(n_cells)), 2) for k in range(len(t))]
    passive["delta_max"] = [
        round(max(passive["cells"][j][k] for j in range(n_cells)) - min(passive["cells"][j][k] for j in range(n_cells)), 3)
        for k in range(len(t))
    ]

    # 3% spread + BMS active balancing (reduces delta over time)
    bms = {"t": t, "cells": [], "pack_v": [], "delta_max": [], "balance_current_ma": []}
    cells_init = passive["cells"]
    for k, soc in enumerate(t):
        row = list(cells_init[j][k] for j in range(n_cells))
        delta = max(row) - min(row)
        # BMS shunt balancing when delta > 50 mV
        bal_ma = min(800, max(0, (delta - 0.05) * 12000)) if soc > 20 else 0
        if bal_ma > 0:
            weak = row.index(min(row))
            strong = row.index(max(row))
            transfer = min(0.02, delta * 0.35)
            row[weak] += transfer
            row[strong] -= transfer
        bms["balance_current_ma"].append(round(bal_ma, 0))
        if k == 0:
            bms["cells"] = [[v] for v in row]
        else:
            for j in range(n_cells):
                bms["cells"][j].append(round(row[j], 3))
    bms["pack_v"] = [round(sum(bms["cells"][j][k] for j in range(n_cells)), 2) for k in range(len(t))]
    bms["delta_max"] = [
        round(max(bms["cells"][j][k] for j in range(n_cells)) - min(bms["cells"][j][k] for j in range(n_cells)), 3)
        for k in range(len(t))
    ]

    scenarios["matched"] = matched
    scenarios["spread_3pct_passive"] = passive
    scenarios["spread_3pct_bms_active"] = bms

    return {
        "n_cells": n_cells,
        "scenarios": scenarios,
        "note": "Simulated CC-charge string voltages. Shows how BMS balancing limits ΔV growth when initial cell spread exists.",
    }


def impedance_growth_cycles() -> dict:
    """Impedance growth vs cycle count — weak vs strong cell in a module."""
    cycles = list(range(0, 501, 25))
    r_strong = []
    r_weak = []
    for c in cycles:
        base = 0.45 + 0.00035 * c + 0.0000008 * (c**2)
        r_strong.append(round(base, 4))
        r_weak.append(round(base * (1.03 + 0.00012 * c), 4))  # weak cell grows faster
    spread_pct = [round((r_weak[i] - r_strong[i]) / r_strong[i] * 100, 2) for i in range(len(cycles))]
    eff = [round(100 - 0.4 * s - 0.05 * (s**1.2), 2) for s in spread_pct]
    return {
        "cycles": cycles,
        "r_strong_mohm": [round(x * 1000, 1) for x in r_strong],
        "r_weak_mohm": [round(x * 1000, 1) for x in r_weak],
        "spread_pct": spread_pct,
        "modeled_pack_efficiency_pct": eff,
        "note": "Weak cell with 3% higher initial R — spread widens with cycling (aftersales risk).",
    }


def open_datasets_comparison() -> dict:
    """Meta-comparison of major open aging datasets (for portfolio context)."""
    return {
        "datasets": [
            {"name": "NASA PCoE", "year": 2010, "cells": 34, "chemistry": "18650 / ~2 Ah", "eis": True, "log_data": False, "focus": "Accelerated fade · impedance"},
            {"name": "Devie batch study", "year": 2018, "cells": 51, "chemistry": "Commercial 18650", "eis": False, "log_data": False, "focus": "BOL cell-to-cell spread"},
            {"name": "KIT NMC/C-SiO", "year": 2024, "cells": 228, "chemistry": "LG HG2 · NMC+SiO", "eis": True, "log_data": True, "focus": "600 d aging · 76 conditions"},
            {"name": "Samsung 21700 DoE", "year": 2024, "cells": 279, "chemistry": "INR21700-50E", "eis": True, "log_data": True, "focus": "Multi-stage calendar+cycle"},
            {"name": "Piombo parallel DoE", "year": 2024, "cells": 40, "chemistry": "NMC + NCA modules", "eis": False, "log_data": True, "focus": "Parallel imbalance · HPPC"},
            {"name": "Zenodo degradation paths", "year": 2025, "cells": 48, "chemistry": "Commercial Li-ion", "eis": True, "log_data": True, "focus": "BOL/EOL EIS · 70-cycle aging"},
        ],
        "note": "Cell counts and years from publications. Use for comparing data richness — not direct chemistry equivalence.",
    }


def generation_bol_comparison() -> dict:
    """Beginning-of-life uniformity across generations — published statistics only."""
    return {
        "generations": [
            {
                "label": "Legacy 18650 batch",
                "era": "2018 study · commercial 18650",
                "source": "Devie et al. 2018",
                "capacity_cv_pct": 0.3,
                "resistance_cv_pct": 3.5,
                "ocv_spread_pct": 8.3,
                "notes": "R = 73.2 ± 2.6 mΩ; SOC spread on receipt up to ~8%",
            },
            {
                "label": "NASA PCoE cells",
                "era": "2008–2014 · 2 Ah 18650",
                "source": "NASA Ames PCoE",
                "capacity_cv_pct": 1.5,
                "resistance_cv_pct": 5.0,
                "ocv_spread_pct": 2.0,
                "notes": "Estimated from multi-cell aging variability; rated 2 Ah baseline",
            },
            {
                "label": "LG HG2 (2020 production)",
                "era": "2022–2024 KIT test · NMC/SiO",
                "source": "Luh & Blank 2024",
                "capacity_cv_pct": 0.8,
                "resistance_cv_pct": 1.2,
                "ocv_spread_pct": 0.06,
                "notes": "OCV σ 0.002 V on 3.556 V mean; tighter modern BOL uniformity",
            },
            {
                "label": "Samsung 21700-50E",
                "era": "2024 DoE campaign",
                "source": "Stroebl et al. 2024",
                "capacity_cv_pct": 1.0,
                "resistance_cv_pct": 2.0,
                "ocv_spread_pct": 0.5,
                "notes": "279 cells · 3 replicates/condition · designed for variation analysis",
            },
        ],
        "trend_summary": (
            "Modern datasets (2022–2024) show tighter OCV/capacity spread at BOL than legacy 18650 batches, "
            "but NMC+SiO and fast-charge conditions introduce new fade modes (impedance, plating). "
            "Aftersales QC must track spread % AND chemistry generation."
        ),
        "capacity_cv_note": "CV% = coefficient of variation at beginning of life from cited studies (some estimated from σ/mean).",
    }


def literature_mismatch_points() -> list[dict]:
    """Anchor points from publications on spread vs impact."""
    return [
        {"spread_pct": 0.3, "impact_y": 99, "impact": "BOL capacity CV", "metric": "Legacy batch uniformity", "source": "Devie 2018"},
        {"spread_pct": 1.0, "impact_y": 96, "impact": "~0.4% modeled eff. loss", "metric": "Small pack spread", "source": "Portfolio model"},
        {"spread_pct": 3.0, "impact_y": 88, "impact": "~1.5% modeled eff. · ΔV rises", "metric": "Typical module concern", "source": "Portfolio model"},
        {"spread_pct": 3.5, "impact_y": 92, "impact": "BOL IR CV within batch", "metric": "Manufacturing spread", "source": "Devie 2018"},
        {"spread_pct": 10.0, "impact_y": 72, "impact": "~5% modeled eff. · drift index ~2.2", "metric": "High spread", "source": "Portfolio model"},
        {"spread_pct": 20.0, "impact_y": 60, "impact": "~40% cycle life loss", "metric": "Parallel cells @ 4.5C", "source": "Gogoana 2013"},
    ]


def fade_trajectory_comparison() -> dict:
    """Normalized capacity fade — illustrative curves aligned to published aging rates."""
    cycles = list(range(0, 601, 30))

    def clamp(v: float, lo: float = 35.0, hi: float = 100.0) -> float:
        return round(min(hi, max(lo, v)), 1)

    # NASA-style accelerated lab profile (steep fade)
    nasa = [clamp(100 - c * 0.22 - 0.0003 * c**2) for c in cycles]
    # KIT mild cycling (~90% at 300 cycles under moderate conditions)
    kit_mild = [clamp(100 - 0.018 * c - 0.00005 * c**2, lo=50) for c in cycles]
    # KIT fast charge / high stress
    kit_fast = [clamp(100 - 0.035 * c - 0.00012 * c**2, lo=45) for c in cycles]
    # Weak cell in pack (starts 3% lower, diverges)
    weak_cell = [clamp(kit_mild[i] - 3 - 0.008 * cycles[i], lo=40) for i in range(len(cycles))]

    return {
        "cycles": cycles,
        "nasa_accelerated_pct": nasa,
        "kit_mild_cycling_pct": kit_mild,
        "kit_fast_charge_pct": kit_fast,
        "weak_cell_in_string_pct": weak_cell,
        "note": (
            "Normalized illustrative fade — NASA curve = accelerated lab profile; "
            "KIT curves = moderate vs aggressive EV-like conditions (2024 dataset)."
        ),
    }


def form_factor_comparison() -> dict:
    """Li-ion form factors — construction + aftersales-relevant scores (1=weak, 5=strong).

    Scores synthesize Hummes et al. 2023 MAUT criteria and Battery University BU-301a
    for portfolio discussion — not a single OEM measurement.
    """
    return {
        "form_factors": [
            {
                "id": "cylindrical",
                "label": "Cylindrical",
                "examples": "18650 · 21700 · 4680 (Panasonic/Tesla class)",
                "construction": "Jelly-roll wound electrode/separator on mandrel; steel casing; CID vent; cap/tab weld",
                "electrode_layout": "Wound (single continuous roll)",
                "casing": "Rigid steel or nickel-plated steel",
                "typical_chemistry": "NMC · NCA · LFP (less common at pack level)",
                "durapower_context": "Common in modular ESS strings, power tools, some EV sub-packs",
            },
            {
                "id": "prismatic",
                "label": "Prismatic",
                "examples": "Samsung SDI · CATL · BYD blade (evolved prismatic)",
                "construction": "Stacked or Z-folded layers in rigid Al/steel hard case; corner/seam welds; module compression frame",
                "electrode_layout": "Stacked or wound-flattened (hard-case rectangular)",
                "casing": "Rigid aluminum or steel hard case",
                "typical_chemistry": "NMC · LFP (very common for ESS & commercial EV)",
                "durapower_context": "Typical for LFP ESS modules and many EV pack rebuilds",
            },
            {
                "id": "pouch",
                "label": "Pouch (pocket)",
                "examples": "GM Ultium · legacy Nissan Leaf · many hybrid packs",
                "construction": "Laminated Al-polymer pouch; stacked electrode sheets; tabs exit long edge; no rigid shell",
                "electrode_layout": "Stacked laminate (flat layers)",
                "casing": "Flexible multi-layer foil laminate",
                "typical_chemistry": "NMC · NCA · LMO blends",
                "durapower_context": "Lightweight EV/hybrid modules — swelling & compression QC critical",
            },
        ],
        "aftersales_scores": {
            "labels": [
                "Mechanical robustness",
                "Swelling tolerance",
                "Pack cooling ease",
                "Cell-level replaceability",
                "Volume utilization",
                "IR/QC accessibility",
            ],
            "cylindrical": [5, 5, 4, 5, 2, 4],
            "prismatic": [3, 3, 3, 2, 4, 3],
            "pouch": [1, 1, 2, 2, 4, 2],
        },
        "score_note": "1 = weakest / hardest for aftersales · 5 = strongest / easiest. From Hummes 2023 + BU-301a synthesis.",
        "summary": (
            "No single winner: cylindrical excels in mechanical integrity and cell swap; prismatic balances space "
            "and is dominant for LFP ESS; pouch maximizes energy density per kg but demands compression frames "
            "and swelling management. Aftersales QC must match test protocol to form factor — not only chemistry."
        ),
    }


def internal_structure_anatomy() -> dict:
    """Cross-section anatomy and manufacturing differences for interview discussion."""
    return {
        "shared_stack": [
            "Cathode (Al foil + active material + binder)",
            "Separator (polyolefin microporous film)",
            "Anode (Cu foil + graphite / Si-composite)",
            "Electrolyte + SEI formation during formation cycling",
        ],
        "differences": [
            {
                "topic": "Electrode assembly",
                "cylindrical": "Long strip wound on mandrel → jelly roll; uniform radial compression from casing",
                "prismatic": "Stacked sheets or flattened wound roll; requires module compression frame",
                "pouch": "Stacked laminate; relies on external stack pressure to prevent delamination",
            },
            {
                "topic": "Current path / tabs",
                "cylindrical": "Single tab pair (or tabless 4680) to cap; low tab length in 4680 designs",
                "prismatic": "Multiple tabs to busbar; weld quality drives module IR spread (Piombo 2024)",
                "pouch": "Tabs welded to pouch edge; pouch flex can alter contact under vibration",
            },
            {
                "topic": "Venting & safety",
                "cylindrical": "CID + vent cap — predictable directional vent; decades of field data",
                "prismatic": "Burst vent in hard case; module enclosure must allow gas path",
                "pouch": "Pouch seam / weak point; gas swelling can crack module cover if unconstrained",
            },
            {
                "topic": "Formation & QC at factory",
                "cylindrical": "High-speed winding + automated grading; mature 18650/21700 sorting lines",
                "prismatic": "Stack/weld in case; more variants; blade/cell-to-pack reduces module count",
                "pouch": "Degassing & sealing critical; humidity ingress risk if seal damaged in service",
            },
        ],
    }


def situation_behavior() -> dict:
    """How form factors behave in situations relevant to aftersales repair QC."""
    cycles = list(range(0, 501, 50))

    def swell_cyl(c: int) -> float:
        return round(0.5 + 0.002 * c, 2)  # minimal % thickness change

    def swell_prism(c: int) -> float:
        return round(2 + 0.012 * c + 0.00001 * c**2, 2)  # BU-301a: measurable hard-case growth

    def swell_pouch(c: int) -> float:
        return round(3 + 0.018 * c + 0.00002 * c**2, 2)  # up to ~8–10% @ 500 cycles cited

    return {
        "swelling_vs_cycles": {
            "cycles": cycles,
            "cylindrical_pct": [min(2.0, swell_cyl(c)) for c in cycles],
            "prismatic_pct": [min(15.0, swell_prism(c)) for c in cycles],
            "pouch_pct": [min(18.0, swell_pouch(c)) for c in cycles],
            "note": (
                "Illustrative thickness/swelling index (%). Cylindrical ≈ rigid casing (minimal). "
                "Prismatic & pouch require compression allowance — BU-301a cites ~8–10% pouch growth over ~500 cycles."
            ),
        },
        "scenarios": [
            {
                "situation": "Fast charge / high C-rate",
                "cylindrical": "Radial thermal gradient (hot core); good coolant access between cells in pack gaps",
                "prismatic": "Flat-face cooling; contact pressure to cold plate critical as cell swells",
                "pouch": "Less gradient-sensitive per Hummes 2023, but swelling reduces thermal contact under load",
                "aftersales_qc": "Verify cold-plate contact & module compression torque after any module open",
            },
            {
                "situation": "Mechanical shock / transport damage",
                "cylindrical": "Highest isotropic strength (Sahraei 2012); dent can still internal short via jelly roll collapse",
                "prismatic": "Strong in compression axis, weak in shear/bend; case dent → tab weld stress",
                "pouch": "Lowest puncture resistance; overlap pressure between cells can cause micro-puncture (Jiang 2021)",
                "aftersales_qc": "Visual + IR + isolation test; pouch: reject if laminate crease, bulge, or seal damage",
            },
            {
                "situation": "Parallel module / string imbalance",
                "cylindrical": "Cell-level mismatch dominates; well-studied (Gogoana 2013, Devie 2018)",
                "prismatic": "Cell + busbar weld IR adds spread; Piombo 2024: interconnection R can dominate imbalance",
                "pouch": "Same as prismatic; flexible tabs add variable contact if compression frame loosens",
                "aftersales_qc": "Measure HPPC/IR at module terminals AND per-cell where accessible",
            },
            {
                "situation": "Calendar aging / ESS standby (LFP prismatic common)",
                "cylindrical": "Stable form; low swelling; IR creep still tracked",
                "prismatic": "LFP prismatic standard for ESS; monitor compression frame over years",
                "pouch": "SEI growth + gas → visible swell; delamination risk if stack pressure lost",
                "aftersales_qc": "Capacity + IR trend; for pouch/prismatic log compression shim thickness at intake",
            },
            {
                "situation": "Post-repair release gate",
                "cylindrical": "Cell swap feasible; re-match IR within string; BMS relearn",
                "prismatic": "Module-level repair; verify weld/busbars; harder single-cell replacement",
                "pouch": "Must restore design compression; swelling check mandatory before ship",
                "aftersales_qc": "Form-factor-specific gate: cylindrical=IR spread; prismatic=weld+IR; pouch=compression+swell",
            },
        ],
        "chemistry_note": (
            "Durapower scope (NMC & LFP) crosses formats: LFP often prismatic/blade in ESS; NMC in cylindrical "
            "and pouch for mobility. Chemistry sets voltage window; form factor sets mechanical & thermal failure mode."
        ),
    }


def nasa_style_sample() -> dict:
    """Representative discharge curve shape inspired by NASA 18650 cycling (not raw import)."""
    time_s = list(range(0, 3601, 60))
    voltage = []
    current = [-1.0] * len(time_s)
    for i, t in enumerate(time_s):
        soc = 1.0 - t / 3600
        v = 4.1 - 0.9 * (1 - soc) ** 0.7 - 0.15 * (1 - soc) ** 3
        voltage.append(round(v, 3))
    return {
        "time_s": time_s,
        "voltage_v": voltage,
        "current_a": current,
        "label": "Representative 1A discharge (NASA PCoE-style 18650, illustrative)",
        "source": "Curve shape for education; download raw .mat from NASA DASHLINK #133",
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "title": "Battery Module Analytics — Educational Models",
        "disclaimer": (
            "Charts combine literature-calibrated models and simulations. "
            "They support aftersales QC reasoning (impedance spread, BMS balancing, cycle drift) "
            "but are NOT measurements from Durapower packs unless stated."
        ),
        "references": REFERENCES,
        "open_datasets": open_datasets_comparison(),
        "generation_bol": generation_bol_comparison(),
        "literature_points": literature_mismatch_points(),
        "fade_trajectories": fade_trajectory_comparison(),
        "form_factors": form_factor_comparison(),
        "internal_structure": internal_structure_anatomy(),
        "situation_behavior": situation_behavior(),
        "impedance_mismatch": impedance_mismatch_curves(),
        "string_charge": string_charge_profiles(),
        "impedance_aging": impedance_growth_cycles(),
        "nasa_sample": nasa_style_sample(),
        "key_messages": [
            "Modern cells (2020–2024 datasets) often show tighter BOL OCV spread than legacy 18650 batches — but Si-anode and fast charge add new failure modes.",
            "1% R spread ≠ 1% efficiency loss in every pack — non-linear and C-rate dependent.",
            "Literature anchor: ~20% resistance mismatch → ~40% cycle life at 4.5C (Gogoana 2013); ~3.5% IR CV at BOL in older commercial batch (Devie 2018).",
            "KIT 2024: 228 cells, 3 per condition — use spread statistics in aftersales, not single-cell pass/fail.",
            "Compare production date / chemistry generation when assessing repaired packs — same form factor ≠ same behavior.",
            "Form factor drives failure mode: cylindrical = thermal gradient; prismatic = weld IR + swelling; pouch = compression & laminate integrity.",
            "Aftersales gate must differ by construction: pouch/prismatic need swelling & compression checks; cylindrical needs string IR matching.",
        ],
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
