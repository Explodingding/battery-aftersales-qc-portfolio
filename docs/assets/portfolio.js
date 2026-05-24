const DURAPOWER = {
  name: "Durapower Technology Group",
  hq: "Singapore",
  chemistries: ["NMC (Nickel Manganese Cobalt)", "LFP (Lithium Iron Phosphate)"],
  applications: [
    "Full-electric & hybrid vehicles",
    "Specialty electric vehicles",
    "Stationary ESS / micro-grid",
    "UPS & datacenter backup",
  ],
  memberSince: "EVAAP member since 2014",
};

const INSPECTION_GATE = [
  { step: 1, name: "Incoming & ESD", test: "Visual, serial match, ESD handling", limit: "No damage / leak / loose HV" },
  { step: 2, name: "HV isolation (IR)", test: "Insulation resistance @ 500 V DC", limit: ">= 500 MOhm" },
  { step: 3, name: "Cell / module balance", test: "Voltage delta across groups", limit: "dV <= 50 mV (NMC) / 80 mV (LFP)" },
  { step: 4, name: "BMS diagnostics", test: "CAN readout, fault codes, contactors", limit: "No active safety DTCs" },
  { step: 5, name: "Thermal system", test: "Leak check, pump/fan function", limit: "No coolant loss" },
  { step: 6, name: "Repair execution", test: "Per work instruction WI-AS-xx", limit: "Traceable parts, torque log" },
  { step: 7, name: "Post-repair functional", test: "Charge/discharge, pre-charge", limit: "Profiles within spec" },
  { step: 8, name: "Final release", test: "Pack voltage, labeling", limit: "SPC in-control, docs complete" },
];

const REPAIR_BY_CHEMISTRY = [
  {
    chemistry: "NMC",
    typical: "EV bus modules, high energy density packs",
    faults: ["Cell voltage drift", "Thermal events", "BMS balancing errors", "HV connector wear"],
    checks: "Strict thermal monitoring; IR tolerance tight; module traceability critical",
  },
  {
    chemistry: "LFP",
    typical: "ESS containers, port logistics, UPS storage",
    faults: ["Capacity fade mismatch", "Contactor/pre-charge", "CAN timeouts", "Seal ingress"],
    checks: "Balance over cycle life; firmware match to site controller",
  },
];

const EIGHT_D = {
  title: "Repeat IR failure after NMC module replacement",
  steps: {
    D1: "Team: QE, production engineer, aftersales lead",
    D2: "IR 450 vs 500 MOhm min — 2nd event in 3 weeks (EV bus pack)",
    D3: "Quarantine 4 packs; stop release to Eindhoven Bus Depot",
    D4: "Root cause: busbar torque 18 Nm vs 25 Nm WI — wrench out of calibration",
    D5: "Recalibrate tools; torque verification in checklist; retrain",
    D6: "30 consecutive packs pass IR + functional test",
    D7: "Monthly torque calibration; MSA on IR tester; update CP-AS-014",
    D8: "Closed; shared at aftersales-production linking meeting",
  },
};

async function loadData() {
  const res = await fetch("data/portfolio.json");
  if (!res.ok) throw new Error("Run: python export_portfolio_json.py");
  return res.json();
}

function kpiCard(label, value) {
  return `<div class="kpi-card"><div class="value">${value}</div><div class="label">${label}</div></div>`;
}

function renderKPIs(data) {
  const k = data.kpis;
  const html = [
    kpiCard("First-Time-Right", k.fttr_pct + "%"),
    kpiCard("Inspection pass rate", k.inspection_pass_pct + "%"),
    kpiCard("Repeat repair rate", k.repeat_repair_pct + "%"),
    kpiCard("Avg turnaround", k.avg_turnaround_days + "d"),
    kpiCard("Repairs (last month)", String(k.repairs_last_month)),
    kpiCard("NCR (month)", String(k.ncr_count)),
  ].join("");
  document.getElementById("kpi-grid").innerHTML = html.replaceAll("<div", "<div").replaceAll("</div>", "</div>");
}

function renderDurapowerContext() {
  const tags = DURAPOWER.chemistries
    .map((c) => `<span class="tag ${c.includes("NMC") ? "nmc" : "lfp"}">${c}</span>`)
    .concat(DURAPOWER.applications.map((a) => `<span class="tag">${a}</span>`))
    .join("");
  document.getElementById("durapower-context").innerHTML =
    `<p><strong>${DURAPOWER.name}</strong> (Singapore) designs, manufactures and integrates lithium systems for automotive and ESS — <strong>NMC</strong> and <strong>LFP</strong>. Applications: EV/HEV, specialty vehicles, renewable ESS, UPS, datacenter, telecom. 25+ countries. Helmond aftersales must uphold the <strong>100% safety track record</strong>. ${DURAPOWER.memberSince}.</p><div class="tag-row">${tags}</div>`;
}

function renderWorkflow() {
  document.getElementById("workflow").innerHTML = INSPECTION_GATE.map(
    (s) => `<div class="wf-step"><div class="num">${s.step}</div><strong>${s.name}</strong><span>${s.test}</span></div>`
  ).join("").replaceAll("<div", "<div").replaceAll("</div>", "</div>");
}

function renderInspectionTable() {
  document.querySelector("#inspection-table tbody").innerHTML = INSPECTION_GATE.map(
    (r) => `<tr><td>${r.step}</td><td>${r.name}</td><td>${r.test}</td><td>${r.limit}</td></tr>`
  ).join("");
}

function renderChemistry() {
  document.getElementById("chemistry-repair").innerHTML = REPAIR_BY_CHEMISTRY.map(
    (c) => `<div class="section" style="margin:0;padding:1rem;">
      <h3><span class="tag ${c.chemistry === "NMC" ? "nmc" : "lfp"}">${c.chemistry}</span> ${c.typical}</h3>
      <p><strong>Typical faults:</strong> ${c.faults.join(" · ")}</p>
      <p class="repair-focus"><strong>QC focus:</strong> ${c.checks}</p></div>`
  ).join("").replaceAll("<div", "<div").replaceAll("</div>", "</div>");
}

function renderEightD() {
  const dl = Object.entries(EIGHT_D.steps).map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("");
  document.getElementById("eight-d").innerHTML = `<p><strong>${EIGHT_D.title}</strong></p><dl class="eight-d">${dl}</dl>`;
}

function renderRecentRepairs(rows) {
  document.querySelector("#recent-repairs tbody").innerHTML = rows.map(
    (r) => `<tr><td>${r.repair_id}</td><td>${r.product_type}</td><td>${r.fault_description}</td>
    <td class="${r.first_time_right === "Yes" ? "pass" : "fail"}">${r.first_time_right}</td><td>${r.repair_hours}h</td></tr>`
  ).join("");
}

function renderExperience() {
  document.getElementById("experience-map").innerHTML = `
    <div class="grid-2">
      <div><h3>Northvolt (battery plant)</h3><ul><li>HV systems on battery line</li><li>RCA, repair logs, EN docs</li><li>Safety-critical diagnostics</li></ul></div>
      <div><h3>Prodrive Eindhoven</h3><ul><li>Escalation to Quality &amp; R&amp;D</li><li>Shop-floor repair + reporting</li><li>25 min from Helmond campus</li></ul></div>
    </div>
    <p class="experience-callout"><strong>My method on repaired Durapower packs:</strong> intake, IR/balance/BMS tests, repair to WI, SPC on release voltage, 8D on repeats, feedback to production &amp; R&amp;D.</p>`;
}

async function init() {
  const data = await loadData();
  document.getElementById("totals-note").textContent =
    `${data.totals.repairs} repairs · ${data.totals.inspections} inspections · ${data.totals.spc_samples} SPC samples (illustrative model)`;
  renderKPIs(data);
  renderDurapowerContext();
  renderWorkflow();
  renderInspectionTable();
  renderChemistry();
  renderEightD();
  renderRecentRepairs(data.recent_repairs);
  renderExperience();

  Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
  new Chart(document.getElementById("chart-fttr"), {
    type: "line",
    data: {
      labels: data.kpi_trend.months,
      datasets: [
        { label: "FTTR %", data: data.kpi_trend.fttr, borderColor: "#0d5c63", fill: true, backgroundColor: "rgba(13,92,99,0.1)", tension: 0.3 },
        { label: "Pass %", data: data.kpi_trend.pass_rate, borderColor: "#0891b2", borderDash: [4, 4], tension: 0.3 },
      ],
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 70, max: 100 } } },
  });
  new Chart(document.getElementById("chart-pareto"), {
    type: "bar",
    data: {
      labels: data.fault_pareto.map((x) => x.label.split(" / ")[0]),
      datasets: [{ data: data.fault_pareto.map((x) => x.count), backgroundColor: "#0d5c63" }],
    },
    options: { indexAxis: "y", responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } },
  });
  const s = data.spc;
  new Chart(document.getElementById("chart-spc"), {
    type: "line",
    data: {
      labels: s.labels.map((d) => d.slice(5)),
      datasets: [
        { label: "Voltage V", data: s.voltage, borderColor: "#0d5c63", pointRadius: 3 },
        { label: "UCL", data: s.labels.map(() => s.ucl), borderColor: "#dc2626", borderDash: [6, 3], pointRadius: 0 },
        { label: "LCL", data: s.labels.map(() => s.lcl), borderColor: "#dc2626", borderDash: [6, 3], pointRadius: 0 },
      ],
    },
    options: { responsive: true, maintainAspectRatio: false },
  });
  new Chart(document.getElementById("chart-category"), {
    type: "doughnut",
    data: {
      labels: data.fault_categories.map((x) => x.label),
      datasets: [{ data: data.fault_categories.map((x) => x.count), backgroundColor: ["#0d5c63", "#0891b2", "#d97706", "#7c3aed"] }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  });
  new Chart(document.getElementById("chart-chemistry"), {
    type: "pie",
    data: {
      labels: data.chemistry_mix.map((x) => x.label),
      datasets: [{ data: data.chemistry_mix.map((x) => x.count), backgroundColor: ["#7c3aed", "#059669", "#0891b2"] }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  });
}

document.addEventListener("DOMContentLoaded", () => init().catch((e) => {
  const err = document.getElementById("load-error");
  err.hidden = false;
  err.textContent = e.message;
}));
