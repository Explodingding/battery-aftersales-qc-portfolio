let analyticsData = null;
let stringChart = null;
let activeScenario = "spread_3pct_bms_active";

async function loadAnalytics() {
  const res = await fetch("data/battery_analytics.json");
  if (!res.ok) throw new Error("Run: python build_battery_analytics.py");
  analyticsData = await res.json();
}

function renderReferences() {
  const ul = document.getElementById("references");
  ul.innerHTML = analyticsData.references
    .map((r) => `<li><a href="${r.url}" target="_blank" rel="noopener">${r.title}</a> — ${r.use}</li>`)
    .join("");
  document.getElementById("disclaimer").textContent = analyticsData.disclaimer;
  document.getElementById("key-messages").innerHTML = analyticsData.key_messages
    .map((m) => `<div class="key-msg">${m}</div>`)
    .join("")
    .replaceAll("<div", "<div")
    .replaceAll("</div>", "</div>")
    .replaceAll("</div>", "</div>");
}

function buildMismatchCharts() {
  const m = analyticsData.impedance_mismatch;
  new Chart(document.getElementById("chart-efficiency"), {
    type: "line",
    data: {
      labels: m.spread_pct.map((x) => x + "%"),
      datasets: [{
        label: "Modeled pack round-trip efficiency (%)",
        data: m.pack_round_trip_efficiency_pct,
        borderColor: "#0d5c63",
        fill: true,
        backgroundColor: "rgba(13,92,99,0.1)",
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { title: { display: true, text: "Efficiency vs internal R spread (weak vs strong cell)" } },
    },
  });

  new Chart(document.getElementById("chart-cycle-life"), {
    type: "line",
    data: {
      labels: m.spread_pct.map((x) => x + "%"),
      datasets: [
        {
          label: "Relative cycle life to EOL (%)",
          data: m.relative_cycle_life_pct,
          borderColor: "#dc2626",
        },
        {
          label: "Voltage divergence index",
          data: m.voltage_divergence_index,
          borderColor: "#7c3aed",
          borderDash: [4, 4],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: { display: true, text: "Cycle life & voltage divergence vs R spread" },
        annotation: { note: m.note },
      },
    },
  });
}

function buildAgingChart() {
  const a = analyticsData.impedance_aging;
  new Chart(document.getElementById("chart-aging"), {
    type: "line",
    data: {
      labels: a.cycles,
      datasets: [
        { label: "Strong cell R (mΩ)", data: a.r_strong_mohm, borderColor: "#059669" },
        { label: "Weak cell R (mΩ)", data: a.r_weak_mohm, borderColor: "#dc2626" },
        {
          label: "Spread (%)",
          data: a.spread_pct,
          borderColor: "#7c3aed",
          yAxisID: "y1",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { title: { display: true, text: "mΩ" } },
        y1: { position: "right", title: { display: true, text: "Spread %" }, grid: { drawOnChartArea: false } },
      },
    },
  });

  new Chart(document.getElementById("chart-eff-vs-cycles"), {
    type: "line",
    data: {
      labels: a.cycles,
      datasets: [{
        label: "Modeled pack efficiency (%)",
        data: a.modeled_pack_efficiency_pct,
        borderColor: "#0891b2",
        fill: true,
        backgroundColor: "rgba(8,145,178,0.1)",
      }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  });
}

function buildNasaSample() {
  const n = analyticsData.nasa_sample;
  new Chart(document.getElementById("chart-nasa"), {
    type: "line",
    data: {
      labels: n.time_s.map((t) => Math.round(t / 60)),
      datasets: [{ label: "Voltage (V)", data: n.voltage_v, borderColor: "#0d5c63", pointRadius: 0 }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { x: { title: { display: true, text: "Time (min)" } } },
      plugins: { title: { display: true, text: n.label } },
    },
  });
}

function renderStringChart(scenarioKey) {
  activeScenario = scenarioKey;
  document.querySelectorAll(".scenario-tabs button").forEach((b) => {
    b.classList.toggle("active", b.dataset.scenario === scenarioKey);
  });

  const sc = analyticsData.string_charge.scenarios[scenarioKey];
  const n = analyticsData.string_charge.n_cells;
  const colors = ["#0d5c63", "#0891b2", "#059669", "#d97706", "#7c3aed", "#dc2626", "#64748b", "#0ea5e9", "#84cc16", "#f43f5e", "#a855f7", "#14b8a6"];

  const datasets = [];
  for (let c = 0; c < n; c++) {
    datasets.push({
      label: `Cell ${c + 1}`,
      data: sc.cells[c],
      borderColor: colors[c % colors.length],
      borderWidth: c === 0 || c === n - 1 ? 2 : 1,
      pointRadius: 0,
      hidden: c !== 0 && c !== n - 1 && scenarioKey === "matched",
    });
  }
  datasets.push({
    label: "Pack total V",
    data: sc.pack_v,
    borderColor: "#000",
    borderWidth: 2,
    borderDash: [6, 3],
    pointRadius: 0,
  });
  if (sc.delta_max) {
    datasets.push({
      label: "Max ΔV string (V)",
      data: sc.delta_max,
      borderColor: "#dc2626",
      borderWidth: 2,
      yAxisID: "y1",
      pointRadius: 0,
    });
  }

  if (stringChart) stringChart.destroy();
  stringChart = new Chart(document.getElementById("chart-string"), {
    type: "line",
    data: { labels: sc.t.map((x) => x + "% SOC"), datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { title: { display: true, text: "Cell / pack voltage (V)" } },
        y1: { position: "right", title: { display: true, text: "ΔV" }, grid: { drawOnChartArea: false } },
      },
    },
  });
}

function setupScenarioTabs() {
  const tabs = document.getElementById("scenario-tabs");
  const labels = {
    matched: "Matched cells",
    spread_3pct_passive: "3% spread — no balancing",
    spread_3pct_bms_active: "3% spread — BMS active balance",
  };
  tabs.innerHTML = Object.keys(labels)
    .map(
      (k) => `<button type="button" data-scenario="${k}" class="${k === activeScenario ? "active" : ""}">${labels[k]}</button>`
    )
    .join("");
  tabs.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => renderStringChart(btn.dataset.scenario));
  });
}

async function init() {
  await loadAnalytics();
  renderReferences();
  buildMismatchCharts();
  buildAgingChart();
  buildNasaSample();
  setupScenarioTabs();
  renderStringChart(activeScenario);
}

document.addEventListener("DOMContentLoaded", () => init().catch((e) => {
  document.getElementById("load-error").hidden = false;
  document.getElementById("load-error").textContent = e.message;
}));
