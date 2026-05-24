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
        "title": "NASA Ames PCoE Li-ion Battery Aging Datasets",
        "url": "https://data.nasa.gov/dataset/li-ion-battery-aging-datasets",
        "use": "Cell-level V, I, temperature, EIS (Re, Rct) over cycle life",
    },
    {
        "id": "gogoana",
        "title": "Gogoana et al. (2013) — Internal resistance matching, parallel cells",
        "url": "https://doi.org/10.1016/j.jpowsour.2013.10.072",
        "use": "~20% resistance mismatch → ~40% cycle life reduction at 4.5C",
    },
    {
        "id": "kit",
        "title": "KIT NMC/C-SiO comprehensive aging dataset",
        "url": "https://radar.kit.edu/radar/en/dataset/kww7jv8ajuvchcah",
        "use": "Large-scale impedance & capacity fade (NMC, >200 cells)",
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
        "impedance_mismatch": impedance_mismatch_curves(),
        "string_charge": string_charge_profiles(),
        "impedance_aging": impedance_growth_cycles(),
        "nasa_sample": nasa_style_sample(),
        "key_messages": [
            "1% R spread ≠ 1% efficiency loss in every pack — relationship is non-linear and C-rate dependent.",
            "Literature: ~20% resistance mismatch can cut cycle life ~40% at high C-rate (Gogoana 2013).",
            "BMS active balancing reduces voltage divergence but adds heat/complexity — QC must verify it works.",
            "Aftersales: measure IR per module, log spread %, trend over cycles — catch weak strings before release.",
        ],
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
