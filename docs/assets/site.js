/** Shared navigation, glossary tooltips, data-tier helpers */

const SITE_PAGES = [
  { id: "start-here", href: "start-here.html", label: "Start here" },
  { id: "learn", href: "learn.html", label: "5-min course" },
  { id: "decision-tree", href: "decision-tree.html", label: "Decision tree" },
  { id: "index", href: "index.html", label: "Dashboard" },
  { id: "playbook", href: "repair-playbook.html", label: "Playbook" },
  { id: "analytics", href: "battery-analytics.html", label: "Analytics" },
  { id: "cheat-sheet", href: "cheat-sheet.html", label: "Cheat sheet" },
  { id: "glossary", href: "glossary.html", label: "Glossary" },
  { id: "changelog", href: "changelog.html", label: "Changelog" },
];

let glossaryData = null;

function currentPageId() {
  const path = window.location.pathname.split("/").pop() || "index.html";
  const map = {
    "index.html": "index",
    "start-here.html": "start-here",
    "learn.html": "learn",
    "decision-tree.html": "decision-tree",
    "repair-playbook.html": "playbook",
    "battery-analytics.html": "analytics",
    "cheat-sheet.html": "cheat-sheet",
    "glossary.html": "glossary",
    "changelog.html": "changelog",
  };
  return map[path] || "index";
}

function injectSiteNav(containerSelector = "#site-nav") {
  const el = document.querySelector(containerSelector);
  if (!el) return;
  const active = currentPageId();
  el.innerHTML = SITE_PAGES.map(
    (p) => `<a href="${p.href}" class="${p.id === active ? "active" : ""}">${p.label}</a>`
  ).join("");
}

function tierBadge(tier) {
  const labels = {
    published: "Published data",
    modeled: "Literature model",
    illustrative: "Illustrative QC",
    method: "Method / WI",
  };
  return `<span class="tier-badge tier-${tier}">${labels[tier] || tier}</span>`;
}

function renderTierLegend(containerId = "tier-legend") {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = ["published", "modeled", "illustrative", "method"].map(tierBadge).join(" ");
}

async function loadGlossary() {
  if (glossaryData) return glossaryData;
  const res = await fetch("data/glossary.json");
  glossaryData = res.ok ? await res.json() : { terms: [] };
  return glossaryData;
}

function glossaryTipEl() {
  let tip = document.getElementById("glossary-tip");
  if (!tip) {
    tip = document.createElement("div");
    tip.id = "glossary-tip";
    tip.className = "glossary-tip";
    document.body.appendChild(tip);
  }
  return tip;
}

function showGlossaryTip(term, x, y) {
  const tip = glossaryTipEl();
  if (!tip) return;
  const gate = term.gate ? ` · Gate ${term.gate}` : "";
  tip.innerHTML = `<strong>${term.term}</strong>${gate}<br>${term.plain}`;
  tip.classList.add("visible");
  tip.style.left = `${x + 12}px`;
  tip.style.top = `${y + 12}px`;
}

function hideGlossaryTip() {
  document.getElementById("glossary-tip")?.classList.remove("visible");
}

async function initGlossaryTooltips(root = document.body) {
  const data = await loadGlossary();
  const byId = Object.fromEntries(data.terms.map((t) => [t.id, t]));
  root.querySelectorAll("[data-glossary]").forEach((el) => {
    const term = byId[el.getAttribute("data-glossary")];
    if (!term) return;
    el.classList.add("glossary-term");
    const show = (e) => showGlossaryTip(term, e.clientX || 0, e.clientY || 0);
    el.addEventListener("mouseenter", show);
    el.addEventListener("mouseleave", hideGlossaryTip);
  });
}

async function renderGlossaryPage() {
  const data = await loadGlossary();
  const dl = document.getElementById("glossary-list");
  if (!dl) return;
  dl.innerHTML = data.terms
    .map(
      (t) =>
        `<dt>${t.term}${t.gate ? ` <span class="tier-badge tier-method">Gate ${t.gate}</span>` : ""}</dt><dd>${t.plain}</dd>`
    )
    .join("");
}

function packDiagramHtml() {
  return `<svg viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg" aria-label="Pack to cell anatomy">
    <rect x="20" y="40" width="600" height="140" rx="8" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>
    <text x="320" y="30" text-anchor="middle" font-size="14" font-weight="600" fill="#0f172a">Battery pack (enclosure + BMS + thermal)</text>
    <rect x="40" y="60" width="120" height="100" rx="4" fill="#0d5c63" opacity="0.85"/>
    <rect x="170" y="60" width="120" height="100" rx="4" fill="#0d5c63" opacity="0.85"/>
    <rect x="300" y="60" width="120" height="100" rx="4" fill="#0d5c63" opacity="0.85"/>
    <rect x="430" y="60" width="120" height="100" rx="4" fill="#0891b2" opacity="0.9"/>
    <text x="100" y="115" text-anchor="middle" fill="white" font-size="11">Module</text>
    <text x="230" y="115" text-anchor="middle" fill="white" font-size="11">Module</text>
    <text x="360" y="115" text-anchor="middle" fill="white" font-size="11">Module</text>
    <text x="490" y="115" text-anchor="middle" fill="white" font-size="11">BMS</text>
    <circle cx="100" cy="200" r="14" fill="#0891b2"/><text x="100" y="204" text-anchor="middle" fill="white" font-size="8">18650</text>
    <rect x="218" y="188" width="24" height="24" rx="2" fill="#d97706"/>
    <rect x="348" y="190" width="28" height="20" rx="2" fill="#dc2626" opacity="0.9"/>
    <text x="320" y="175" text-anchor="middle" font-size="10" fill="#64748b">Cell formats: cylindrical · prismatic · pouch</text>
  </svg>
  <div class="cell-links">
    <a href="battery-analytics.html">Form factor comparison</a>
    <a href="decision-tree.html">Which test first?</a>
  </div>`;
}

function injectPackDiagram(containerId = "pack-diagram") {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = packDiagramHtml();
}

document.addEventListener("DOMContentLoaded", () => {
  injectSiteNav();
  initGlossaryTooltips().catch(() => {});
});
