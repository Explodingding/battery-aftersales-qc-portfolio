# Eight Gates Before Release: Quality Control for Repaired Lithium-Ion Battery Packs

*Lessons from battery manufacturing and Brainport production — applied to aftersales*

---

## The problem nobody talks about in aftersales

New battery packs leave the factory with a documented chain of evidence: incoming materials, process parameters, final test, release authorization.

**Repaired packs often don't.**

A module swap, harness repair, or BMS re-flash can restore function — or introduce a latent fault that returns in 72 hours at a customer's ESS site or bus depot. In aftersales, you are the last line before the product meets Durapower's **100% safety track record** standard again.

After seven years in battery and high-tech environments — including **Northvolt Poland** and **Prodrive Technologies in Eindhoven** — I believe repair quality needs the same discipline as production, not a lighter checklist.

---

## NMC and LFP fail differently — treat them differently

Integrators like **Durapower** work across both chemistries:

| | **NMC** | **LFP** |
|---|---------|---------|
| **Typical use** | EV, bus, high energy mobility | ESS, UPS, datacenter backup |
| **Common returns** | Cell drift, thermal stress, HV connector wear | BMS/CAN timeout, config mismatch, seal ingress |
| **QC focus** | Tight IR tolerance, thermal verification | Firmware golden images, connector integrity, balance over cycle life |

One inspection checklist for all chemistries is how repeat repairs happen.

---

## My 8-step repair QC gate

Every returned pack — Helmond service center or field return — passes the same verified states:

1. **Incoming & ESD** — serial match, visual, quarantine if safety-critical  
2. **HV isolation (IR)** — safety gate before any energization  
3. **Cell / module balance** — ΔV limits (stricter on NMC)  
4. **BMS / CAN diagnostics** — separate comms layer from cell layer faults  
5. **Thermal system** — leak check, pump/fan function  
6. **Repair execution** — per work instruction: torque, traceability, ESD log  
7. **Post-repair functional test** — charge/discharge, pre-charge profile  
8. **Final release** — pack voltage in SPC control, documentation complete  

Failures stop the line. No "we'll check it at the customer."

---

## Case study: BMS timeout on an LFP ESS pack (not a board swap)

**Symptom:** CAN timeout / BMS no response on a 280 kWh LFP container at an energy storage site.

**First instinct:** Replace the BMS board.  
**Actual root cause (dual layer):**

- **Physical:** moisture ingress on connector XJ12 after an external cable swap in the field — pin 4–7 open circuit.  
- **Logical:** firmware profile still set to a **bus depot** config, not the **ESS site controller v4.2** — wrong CAN map after unauthorized re-flash.

**Repair:** Harness section replacement per WI + re-flash from site golden image + 4-hour CAN soak test.  
**Scale:** Three similar returns same month → incoming connector photo mandatory for all ESS returns; config backup required before any BMS software action.

**Result:** First-time-right release in 1.2 days; FC-02 (BMS timeout) down ~38% over the following quarter after WI update.

The lesson: **high-volume aftersales scales through standard work**, not skipped tests.

---

## Top faults — quick playbook for production volume

From Pareto analysis on repair data, roughly **80% of volume** sits in eight codes:

| Fault | Fast contain | Scale countermeasure |
|-------|--------------|----------------------|
| BMS / CAN timeout | No re-flash without config backup | Golden firmware library per site profile |
| Cell imbalance | Stop charge; log max cell ID | SPC on incoming ΔV; module serial poka-yoke |
| IR below limit | HV lockout | Monthly torque calibration + MSA on IR tester |
| Pre-charge / contactor | Disable remote close | Pre-kitted contactor bays |
| Thermal / coolant leak | Drain; ventilate | Seal photo on outdoor ESS returns |
| Firmware mismatch | Snapshot config on intake | Automated hash compare in repair log |

**Target KPI:** FTTR ≥ 92%. Any repeat within 30 days → automatic 8D.

---

## Five rules for high-volume repair lines

1. **One defect → one permanent gate change** within 48 hours  
2. **Pre-kit bays** for top Pareto faults — cycle time matters, safety gates don't bend  
3. **Golden images & torque logs** — every HV job traceable to calibrated tool ID  
4. **Daily 15-min defect huddle** — aftersales, production, development  
5. **Linking pin role** — field patterns feed back to engineering; I learned this escalating repeat faults to Quality & R&D at Prodrive  

---

## What I built (and why I'm sharing it)

Because a job application only had room for a CV, I packaged this into an **interactive HTML portfolio**:

- KPI dashboard: FTTR trend, SPC on post-repair voltage, Pareto fault modes  
- Full repair playbook with the LFP ESS BMS case study  
- NMC vs LFP repair focus guide  

If you're in battery aftersales, quality engineering, or ESS service — I hope it's useful. **Comment or message me** and I'll share the link.

---

## About the author

**Łukasz Klimowski** — M.Sc. Electronics & Telecommunications. Production support and maintenance in battery manufacturing (Northvolt), high-tech production (Prodrive, Brainport), and current industrial environment in Belgium/Netherlands. IPC-A-610 / IPC-7711 rework standards. Fluent English (C1). Focused on moving from production equipment care to **owning quality of repaired battery products**.

---

*What's the #1 repeat fault you see on returned packs — and did you fix the process or only the part?*

#QualityEngineering #BatteryAftersales #LithiumIon #EMobility #ESS #RootCauseAnalysis #SPC #Brainport
