/** 5-minute intro course */

const CHAPTERS = [
  {
    title: "What is this about?",
    body: `<p>A <strong>repaired battery pack</strong> goes back into a bus, truck, or energy storage container.
      If we skip checks, the next failure can be a <strong>safety event</strong> — not just an unhappy customer.</p>
      <p>This portfolio shows an <strong>8-step gate</strong> I would run on every returned pack before release.
      Think of it like an aircraft pre-flight checklist — boring until it saves you.</p>`,
  },
  {
    title: "What's inside a battery pack?",
    body: `<p>A pack is not one big battery. It contains:</p>
      <ul>
        <li><strong>Modules</strong> — groups of cells wired together</li>
        <li><strong>BMS</strong> — brain that monitors voltage, temperature, and talks to the vehicle/site</li>
        <li><strong>Thermal system</strong> — coolant or air to keep cells in range</li>
        <li><strong>HV contactors</strong> — big switches that connect/disconnect power safely</li>
      </ul>
      <p>Cells come in <strong>cylindrical</strong> (like a AA), <strong>prismatic</strong> (hard box), or <strong>pouch</strong> (soft laminated pocket). Same chemistry — different repair checks.</p>`,
  },
  {
    title: "The 8 gates in plain language",
    body: `<ol>
        <li><strong>Incoming</strong> — right serial, no visible damage</li>
        <li><strong>Insulation (IR)</strong> — safe to touch electrically?</li>
        <li><strong>Balance</strong> — cells agree on voltage?</li>
        <li><strong>BMS / CAN</strong> — brain online and talking?</li>
        <li><strong>Thermal</strong> — cooling OK?</li>
        <li><strong>Repair</strong> — fix per work instruction</li>
        <li><strong>Functional test</strong> — prove it works under load</li>
        <li><strong>Release</strong> — paperwork + SPC sign-off</li>
      </ol>
      <p><strong>FTTR</strong> = all eight pass the first time after repair.</p>`,
  },
  {
    title: "Why \"BMS timeout\" is often not the board",
    body: `<p>Field teams often swap the BMS when communication fails. In the LFP ESS case in this portfolio, root cause was:</p>
      <ul>
        <li>Corroded connector pins (physical layer)</li>
        <li>Wrong firmware profile for the site controller (software layer)</li>
      </ul>
      <p>Gate 4 catches this <em>before</em> an expensive module swap.</p>
      <p><a href="repair-playbook.html#case-study">Read the full case study →</a></p>`,
  },
  {
    title: "Quick check — did it stick?",
    body: `<div class="learn-quiz" id="learn-quiz">
      <p><strong>1.</strong> What should you do before energizing a returned pack?</p>
      <label><input type="radio" name="q1" value="a"> Run the insulation (IR) test</label>
      <label><input type="radio" name="q1" value="b"> Swap the BMS immediately</label>
      <p style="margin-top:1rem"><strong>2.</strong> FTTR means:</p>
      <label><input type="radio" name="q2" value="a"> First-Time-Right — passes all gates first attempt</label>
      <label><input type="radio" name="q2" value="b"> Fast test then release</label>
      <button type="button" class="btn-primary" id="quiz-submit" style="margin-top:1rem;padding:0.55rem 1rem;border:none;border-radius:8px;background:#0d5c63;color:white;font-weight:600;cursor:pointer">Check answers</button>
      <p id="quiz-result" style="margin-top:0.75rem;font-weight:600"></p>
    </div>`,
  },
];

let chapterIndex = 0;

function renderChapter() {
  document.querySelectorAll(".learn-chapter").forEach((el, i) => {
    el.classList.toggle("active", i === chapterIndex);
  });
  document.querySelectorAll(".learn-dot").forEach((el, i) => {
    el.classList.toggle("active", i === chapterIndex);
    el.classList.toggle("done", i < chapterIndex);
  });
  document.getElementById("learn-prev").disabled = chapterIndex === 0;
  document.getElementById("learn-next").textContent =
    chapterIndex === CHAPTERS.length - 1 ? "Finish" : "Next →";
}

function initLearn() {
  const main = document.getElementById("learn-chapters");
  main.innerHTML = CHAPTERS.map(
    (c, i) => `<article class="learn-chapter ${i === 0 ? "active" : ""}" data-i="${i}">
      <h2>Chapter ${i + 1}: ${c.title}</h2>${c.body}</article>`
  ).join("");

  const dots = document.getElementById("learn-progress");
  dots.innerHTML = CHAPTERS.map(
    (_, i) => `<button type="button" class="learn-dot ${i === 0 ? "active" : ""}" data-i="${i}">${i + 1}</button>`
  ).join("");
  dots.querySelectorAll(".learn-dot").forEach((btn) => {
    btn.addEventListener("click", () => {
      chapterIndex = parseInt(btn.dataset.i, 10);
      renderChapter();
    });
  });

  document.getElementById("learn-prev").addEventListener("click", () => {
    if (chapterIndex > 0) {
      chapterIndex--;
      renderChapter();
    }
  });
  document.getElementById("learn-next").addEventListener("click", () => {
    if (chapterIndex < CHAPTERS.length - 1) {
      chapterIndex++;
      renderChapter();
    } else {
      document.getElementById("learn-complete").hidden = false;
      main.hidden = true;
      document.querySelector(".learn-nav").hidden = true;
      localStorage.setItem("learn-complete", "1");
    }
  });

  document.getElementById("quiz-submit")?.addEventListener("click", () => {
    const q1 = document.querySelector('input[name="q1"]:checked')?.value;
    const q2 = document.querySelector('input[name="q2"]:checked')?.value;
    const ok = q1 === "a" && q2 === "a";
    const el = document.getElementById("quiz-result");
    el.textContent = ok
      ? "Correct — you know the basics. Explore the dashboard or decision tree next."
      : "Review chapter 3: IR before HV, and FTTR = first-time-right through all gates.";
    el.style.color = ok ? "#059669" : "#dc2626";
  });

  if (localStorage.getItem("learn-complete")) {
    document.getElementById("learn-complete").hidden = false;
    main.hidden = true;
    document.querySelector(".learn-nav").hidden = true;
  }
}

document.addEventListener("DOMContentLoaded", initLearn);
