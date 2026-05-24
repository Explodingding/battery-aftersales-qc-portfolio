# LinkedIn — publikacja z materiałów aplikacyjnych

**Cel:** Pokazać kompetencje Quality / battery aftersales, skoro aplikacja przyjęła tylko CV.  
**Język:** angielski (Brainport / Durapower / międzynarodowa widoczność)  
**Ton:** thought leadership, nie „proszę o pracę” — zaproszenie do rozmowy / komentarzy.

---

## Strategia (3 kroki)

| Krok | Co | Kiedy |
|------|-----|-------|
| **1** | Post główny (krótki) | Dzień 1 — maksymalny zasięg |
| **2** | Artykuł LinkedIn | Dzień 3–5 — link w komentarzu pod postem |
| **3** | Komentarz + DM do Pawła | Po publikacji posta — osobno, krótko |

---

## Krok 1 — POST (wklej w „Rozpocznij post”)

```
After 7+ years in battery and high-tech manufacturing (Northvolt · Prodrive · Brainport),
I built something I wish I had earlier in my career:

a practical repair QC playbook for lithium-ion aftersales.

Not theory — an 8-step gate I would run on every returned pack:
incoming → IR → cell balance → BMS/CAN → thermal → repair to WI → functional test → SPC release.

Why it matters:
→ NMC packs (EV/bus) and LFP systems (ESS/UPS) fail differently
→ "BMS timeout" is often NOT a BMS board — it's connector + config (I document a full LFP ESS case)
→ High-volume aftersales needs FTTR ≥92% without skipping safety gates

I mapped top fault codes (CAN timeout, cell drift, IR fail, pre-charge, thermal)
to contain → diagnose in 15 min → fix → verify → scale (WI update, golden firmware, torque logs).

Built as an interactive HTML portfolio — charts, SPC, Pareto, 8D example.
Happy to share the link in comments if useful for QE / aftersales / battery service teams.

What's the #1 repeat fault you see on returned packs? 👇

#BatteryQuality #Aftersales #QualityEngineering #EMobility #ESS #Brainport #RCA #SPC
```

**Załącznik:** 1 obraz — screenshot dashboardu (`Battery_Aftersales_Quality_Portfolio` lub `repair-playbook.html` w przeglądarce). LinkedIn preferuje wizual.

**Pierwszy komentarz (od Ciebie, zaraz po publikacji):**
```
Link to the portfolio (HTML dashboard + repair playbook with LFP ESS BMS case study):
[WKLEJ LINK — GitHub Pages / Netlify / OneDrive publiczny / lub PDF w dokumentach LinkedIn]

Background: M.Sc. Electronics, IPC rework standards, Northvolt production support,
Prodrive Eindhoven (Quality/R&D escalation). Open to quality-focused roles in battery aftersales — Helmond / Brainport region.
```

---

## Krok 2 — ARTYKUŁ LinkedIn

W LinkedIn: **Napisz artykuł** → tytuł i treść z pliku `article-battery-aftersales-quality.md`  
(albo otwórz `article-battery-aftersales-quality.html` → skopiuj sekcje).

**Tytuł proponowany:**
`Eight Gates Before Release: Quality Control for Repaired Lithium-Ion Battery Packs`

**Podtytuł (opcjonalnie):**
`Lessons from battery manufacturing and Brainport production — applied to aftersales`

---

## Krok 3 — wiadomość do Pawła (osobno, nie w poście)

```
Hi Pawel,

I published a short piece on battery aftersales QC (8-step gate + LFP ESS case study)
— built from the same work I prepared for the Helmond application.
Only had room for CV in the form, so I wanted the methodology visible somewhere useful.

[link]

No pressure — if it’s relevant for the team, happy to discuss.
Łukasz
```

---

## Hashtags — rotacja (nie wszystkie naraz)

**Core:** #QualityEngineering #BatteryAftersales #LithiumIon #RCA  
**Industry:** #EMobility #EnergyStorage #ESS #Automotive  
**Regional:** #Brainport #Helmond #Netherlands  
**Methods:** #SPC #8D #RootCauseAnalysis #FirstTimeRight  

Max 3–5 hashtagów w poście + reszta w komentarzu = mniej „spamowo”.

---

## Hosting linku (wybierz jedno)

| Opcja | Jak |
|-------|-----|
| **GitHub Pages** | Repo publiczny → Settings → Pages → folder `html` |
| **Netlify Drop** | Przeciągnij folder `battery-aftersales-quality/html` |
| **LinkedIn Documents** | PDF z `repair-playbook.html` (Ctrl+P) — bez klikalnego linku, ale działa od razu |
| **Featured na profilu** | Link do artykułu LinkedIn + PDF portfolio |

---

## Checklist przed publikacją

- [ ] Screenshot dashboardu (1200×627 lub 1080×1080)
- [ ] Post opublikowany wtorek–czwartek, 8:00–10:00 CET
- [ ] Komentarz z linkiem w ciągu 2 min
- [ ] Featured section na profilu zaktualizowany
- [ ] Headline LinkedIn: *Quality Engineer · Battery Aftersales · RCA · Brainport*
- [ ] Odpowiedzi na komentarze w ciągu 24 h (algorytm)

---

## Pliki w tym folderze

| Plik | Użycie |
|------|--------|
| `post-main.txt` | Gotowy post do wklejenia |
| `post-comment-link.txt` | Pierwszy komentarz z linkiem |
| `article-battery-aftersales-quality.md` | Treść artykułu LinkedIn |
| `article-battery-aftersales-quality.html` | Podgląd / druk PDF artykułu |
| `dm-pawel.txt` | Szablon wiadomości |
