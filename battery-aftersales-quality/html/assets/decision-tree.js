/** Interactive decision tree from data/decision_tree.json */

let treeData = null;
const breadcrumb = [];

async function loadTree() {
  const res = await fetch("data/decision_tree.json");
  if (!res.ok) throw new Error("Missing decision_tree.json");
  treeData = await res.json();
}

function renderNode(nodeId) {
  const root = document.getElementById("dt-root");
  const node = treeData.nodes[nodeId];
  if (!node) {
    root.innerHTML = "<p>Unknown step.</p>";
    return;
  }

  if (node.result) {
    const checks = node.checks.map((c) => `<li>${c}</li>`).join("");
    const link = node.link
      ? `<p><a href="${node.link}">${node.link_label || "Learn more"} →</a></p>`
      : "";
    const tier = typeof tierBadge === "function" ? tierBadge(node.tier) : "";
    root.innerHTML = `<div class="dt-result"><div class="dt-breadcrumb">${breadcrumb.join(" → ")}</div>${tier}<h3>${node.title}</h3><p><strong>Check first:</strong></p><ul>${checks}</ul>${link}<button type="button" class="btn-secondary" id="dt-restart" style="margin-top:1rem;padding:0.5rem 1rem;border:1px solid #e2e8f0;border-radius:8px;cursor:pointer">Start over</button></div>`;
    root.innerHTML = root.innerHTML.replace("<div class=\"dt-result\">", "<div class=\"dt-result\">");
    document.getElementById("dt-restart").addEventListener("click", () => {
      breadcrumb.length = 0;
      renderNode(treeData.start);
    });
    return;
  }

  const opts = node.options
    .map(
      (o) =>
        `<button type="button" data-next="${o.next}" data-label="${o.label.replace(/"/g, "&quot;")}">${o.label}</button>`
    )
    .join("");

  root.innerHTML = `<div class="dt-card"><div class="dt-breadcrumb">${breadcrumb.join(" → ") || "Start"}</div><p class="dt-question">${node.question}</p><div class="dt-options">${opts}</div></div>`;
  root.innerHTML = root.innerHTML.replace('<div class="dt-breadcrumb">', '<div class="dt-breadcrumb">');

  root.querySelectorAll(".dt-options button").forEach((btn) => {
    btn.addEventListener("click", () => {
      breadcrumb.push(btn.dataset.label);
      renderNode(btn.dataset.next);
    });
  });
}

async function initDecisionTree() {
  await loadTree();
  renderNode(treeData.start);
}

document.addEventListener("DOMContentLoaded", () =>
  initDecisionTree().catch((e) => {
    document.getElementById("dt-root").innerHTML = `<p style="color:#dc2626">${e.message}</p>`;
  })
);
