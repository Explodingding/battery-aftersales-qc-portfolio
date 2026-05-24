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
    .map((r) => {
      const yr = r.year ? ` (${r.year})` : "";
      return `<li><a href="${r.url}" target="_blank" rel="noopener">${r.title}</a>${yr} — ${r.use}</li>`;
    })
    .join("");
  document.getElementById("disclaimer").textContent = analyticsData.disclaimer;
  document.getElementById("key-messages").innerHTML = analyticsData.key_messages
    .map((m) => `<div class="key-msg">${m}</div>`)
    .join("");
}

function renderDatasetTable() {
  const tbody = document.querySelector("#dataset-table tbody");
  if (!tbody || !analyticsData.open_datasets) return;
  tbody.innerHTML = analyticsData.open_datasets.datasets
    .map(
      (d) => `<tr>
        <td>${d.name}</td>
        <td>${d.year}</td>
        <td>${d.cells}</td>
        <td>${d.chemistry}</td>
        <td>${d.eis ? "Yes" : "—"}</td>
        <td>${d.log_data ? "Yes" : "—"}</td>
        <td>${d.focus}</td>
      </tr>`
    )
    .join("");
  const note = document.getElementById("dataset-note");
  if (note) note.textContent = analyticsData.open_datasets.note;
}

function buildGenerationChart() {
  const g = analyticsData.generation_bol;
  const labels = g.generations.map((x) => x.label);
  new Chart(document.getElementById("chart-generation"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Capacity CV @ BOL (%)",
          data: g.generations.map((x) => x.capacity_cv_pct),
          backgroundColor: "rgba(13,92,99,0.75)",
        },
        {
          label: "Resistance CV @ BOL (%)",
          data: g.generations.map((x) => x.resistance_cv_pct),
          backgroundColor: "rgba(220,38,38,0.65)",
        },
        {
          label: "OCV spread @ BOL (%)",
          data: g.generations.map((x) => x.ocv_spread_pct),
          backgroundColor: "rgba(124,58,237,0.65)",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Beginning-of-life uniformity — legacy 18650 vs modern HG2 / 21700",
        },
        legend: { position: "bottom" },
      },
      scales: { y: { beginAtZero: true, title: { display: true, text: "CV or spread (%)" } } },
    },
  });

  const list = document.getElementById("generation-notes");
  if (list) {
    list.innerHTML = g.generations
      .map(
        (x) =>
          `<li><strong>${x.label}</strong> (${x.era}) — ${x.notes} <em>[${x.source}]</em></li>`
      )
      .join("");
  }
  const trend = document.getElementById("generation-trend");
  if (trend) trend.textContent = g.trend_summary;
}

function buildLiteratureScatter() {
  const pts = analyticsData.literature_points;
  const m = analyticsData.impedance_mismatch;
  new Chart(document.getElementById("chart-literature-points"), {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Published anchor points",
          data: pts.map((p) => ({ x: p.spread_pct, y: p.impact_y })),
          backgroundColor: "#dc2626",
          pointRadius: 8,
          pointHoverRadius: 10,
        },
        {
          label: "Modeled cycle life (%)",
          data: m.spread_pct.map((x, i) => ({ x, y: m.relative_cycle_life_pct[i] })),
          type: "line",
          borderColor: "#0d5c63",
          backgroundColor: "transparent",
          pointRadius: 0,
          showLine: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      parsing: false,
      plugins: {
        title: { display: true, text: "Spread vs impact — literature anchors on modeled curve" },
        tooltip: {
          callbacks: {
            label(ctx) {
              const p = pts[ctx.dataIndex];
              if (ctx.datasetIndex === 0 && p) {
                return `${p.source}: ${p.spread_pct}% — ${p.metric} (${p.impact})`;
              }
              return `Modeled life: ${ctx.parsed.y}% @ ${ctx.parsed.x}% spread`;
            },
          },
        },
      },
      scales: {
        x: { title: { display: true, text: "Resistance / spread (%)" } },
        y: { title: { display: true, text: "Relative impact / cycle life (%)" } },
      },
    },
  });

  const ul = document.getElementById("literature-points-list");
  if (ul) {
    ul.innerHTML = pts
      .map((p) => `<li><strong>${p.spread_pct}%</strong> — ${p.impact} (${p.source})</li>`)
      .join("");
  }
}

function buildFadeChart() {
  const f = analyticsData.fade_trajectories;
  new Chart(document.getElementById("chart-fade"), {
    type: "line",
    data: {
      labels: f.cycles,
      datasets: [
        { label: "NASA accelerated (2008–2014 baseline)", data: f.nasa_accelerated_pct, borderColor: "#64748b", borderDash: [6, 3] },
        { label: "KIT mild cycling (2024 dataset style)", data: f.kit_mild_cycling_pct, borderColor: "#059669" },
        { label: "KIT fast-charge / stress", data: f.kit_fast_charge_pct, borderColor: "#d97706" },
        { label: "Weak cell in string (3% offset)", data: f.weak_cell_in_string_pct, borderColor: "#dc2626" },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { title: { display: true, text: "Normalized capacity retention vs cycles — era & condition comparison" } },
      scales: {
        x: { title: { display: true, text: "Equivalent cycle index" } },
        y: { min: 30, max: 100, title: { display: true, text: "Relative capacity (%)" } },
      },
    },
  });
  const note = document.getElementById("fade-note");
  if (note) note.textContent = f.note;
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

function renderFormFactorCards() {
  const ff = analyticsData.form_factors;
  const el = document.getElementById("form-factor-cards");
  if (!el || !ff) return;
  el.innerHTML = ff.form_factors
    .map(
      (f) => `<article class="ff-card">
        <h3>${f.label}</h3>
        <p class="ff-examples">${f.examples}</p>
        <dl>
          <dt>Construction</dt><dd>${f.construction}</dd>
          <dt>Electrode layout</dt><dd>${f.electrode_layout}</dd>
          <dt>Casing</dt><dd>${f.casing}</dd>
          <dt>Typical chemistry</dt><dd>${f.typical_chemistry}</dd>
          <dt>Aftersales context</dt><dd>${f.durapower_context}</dd>
        </dl>
      </article>`
    )
    .join("");
  const summary = document.getElementById("form-factor-summary");
  if (summary) summary.textContent = ff.summary;
}

function buildFormFactorRadar() {
  const s = analyticsData.form_factors.aftersales_scores;
  const labels = s.labels;
  new Chart(document.getElementById("chart-form-factor"), {
    type: "radar",
    data: {
      labels,
      datasets: [
        {
          label: "Cylindrical",
          data: s.cylindrical,
          borderColor: "#0d5c63",
          backgroundColor: "rgba(13,92,99,0.15)",
        },
        {
          label: "Prismatic",
          data: s.prismatic,
          borderColor: "#d97706",
          backgroundColor: "rgba(217,119,6,0.12)",
        },
        {
          label: "Pouch",
          data: s.pouch,
          borderColor: "#dc2626",
          backgroundColor: "rgba(220,38,38,0.1)",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 5,
          ticks: { stepSize: 1 },
        },
      },
      plugins: {
        title: {
          display: true,
          text: "Aftersales-relevant scores by form factor (1=weak · 5=strong)",
        },
        subtitle: {
          display: true,
          text: analyticsData.form_factors.score_note,
        },
      },
    },
  });
}

function renderInternalStructure() {
  const st = analyticsData.internal_structure;
  const stack = document.getElementById("shared-stack");
  if (stack && st) {
    stack.innerHTML = `<strong>Common Li-ion stack (all formats):</strong><ul>${st.shared_stack
      .map((x) => `<li>${x}</li>`)
      .join("")}</ul>`;
  }
  const diff = document.getElementById("structure-diff");
  if (diff && st) {
    diff.innerHTML = st.differences
      .map(
        (d) => `<div class="struct-row">
          <h4>${d.topic}</h4>
          <div class="struct-cols">
            <div class="col-head">Cylindrical</div><div class="col-head">Prismatic</div><div class="col-head">Pouch</div>
            <div>${d.cylindrical}</div><div>${d.prismatic}</div><div>${d.pouch}</div>
          </div>
        </div>`
      )
      .join("");
  }
}

function buildSwellingChart() {
  const sb = analyticsData.situation_behavior.swelling_vs_cycles;
  new Chart(document.getElementById("chart-swelling"), {
    type: "line",
    data: {
      labels: sb.cycles,
      datasets: [
        { label: "Cylindrical (minimal)", data: sb.cylindrical_pct, borderColor: "#0d5c63" },
        { label: "Prismatic", data: sb.prismatic_pct, borderColor: "#d97706" },
        { label: "Pouch", data: sb.pouch_pct, borderColor: "#dc2626" },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { title: { display: true, text: "Illustrative swelling / thickness growth index (%)" } },
      scales: {
        x: { title: { display: true, text: "Cycle index" } },
        y: { beginAtZero: true, title: { display: true, text: "Swelling index (%)" } },
      },
    },
  });
  const note = document.getElementById("swelling-note");
  if (note) note.textContent = sb.note;
}

function renderScenarioTable() {
  const sb = analyticsData.situation_behavior;
  const el = document.getElementById("scenario-table");
  if (!el || !sb) return;
  el.innerHTML = sb.scenarios
    .map(
      (s) => `<article class="scenario-card">
        <h4>${s.situation}</h4>
        <p><strong>Cylindrical:</strong> ${s.cylindrical}</p>
        <p><strong>Prismatic:</strong> ${s.prismatic}</p>
        <p><strong>Pouch:</strong> ${s.pouch}</p>
        <p class="qc-line"><strong>Aftersales QC:</strong> ${s.aftersales_qc}</p>
      </article>`
    )
    .join("");
  const chem = document.getElementById("chemistry-note");
  if (chem) chem.textContent = sb.chemistry_note;
}

async function init() {
  await loadAnalytics();
  renderReferences();
  renderFormFactorCards();
  buildFormFactorRadar();
  renderInternalStructure();
  buildSwellingChart();
  renderScenarioTable();
  renderDatasetTable();
  buildGenerationChart();
  buildLiteratureScatter();
  buildFadeChart();
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
