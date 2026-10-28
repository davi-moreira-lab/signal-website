# Website launch checklist (approval gate)

**Launched 2026-10-27** at https://davi-moreira-lab.github.io/signal-website/ with Davi's approval ("Publish SIGNAL site first"; hosting "Public signal-website"; JMHC wording "Publish now"). Status of each item at launch:

- [x] The lab director approves website copy, program brand, attribution and current affiliation. (Davi, 2026-10-27; record in `programs/signal/communications/2026-10-27_signal-website-copy-draft.md`.)
- [x] No project/paper/student/collaborator is listed without confirmed public-release rights and consent as appropriate. (Only Davi is named; affiliates and students are not listed.)
- [x] Institutional identities/logos comply with university policy; site does not imply official endorsement. (No Purdue or JMHC logos; footer disclaimer kept.)
- [x] Confirm GitHub repository owner, visibility and source rights before any push or Pages configuration. (Owner `davi-moreira-lab`, public, chosen by Davi 2026-10-27; source scanned by `preflight.py` and for personal data.)
- [x] Inspect generated `index.html`, `styles.css`, scripts and source JSON for secrets, restricted data or drafts. (Prototype banner and footer note removed; no scripts.)
- [x] Verify on mobile and desktop; inspect accessibility, links, titles and contact policy.
- [x] Decide where to host (GitHub Pages as one option), review plan restrictions and public access. (GitHub Pages on the Free plan, which requires a public repository.)
- [x] Only then approve public deployment; domain and DNS decisions are separate. (No custom domain.)
- [ ] Align copy with the awarded SIGNAL theme and confirm JMHC/Purdue naming rules (SIGNAL is a JMHC Interdisciplinary Research Generator); approve or replace the proposed methodological themes. **Copy aligned and approved; JMHC has not confirmed the naming.** Davi chose to publish before that confirmation (2026-10-27); adjust if JMHC asks.
- [ ] Finish browser QA: 1440 px, 200–400% zoom, full keyboard order and screen-reader output (320/375/768/1024 px reflow and skip-link focus were checked on 2026-10-23; see `STATIC_REVIEW.md`). **Done 2026-10-27:** 1440 px, 720 px and 360 px widths (200% and 400% zoom equivalents) with no sideways scrolling, and the keyboard order of links (skip link, home, five menu items, hero buttons). **Not done:** a pass with a real screen reader.
- [x] Deploy only an allowlisted artifact (`index.html`, `styles.css`, `assets/davi-moreira.jpg` and `.nojekyll`); keep `AGENTS.md`, `CLAUDE.md`, docs, tests and tools out of the published site. (`.github/workflows/pages.yml`; verified live: the three public files return 200, `README.md`, `AGENTS.md` and `content/site.json` return 404.)
- [x] Record the actual GitHub plan and the separately approved site access mode; source-repository privacy is not access control for a Pages site. (Plan: GitHub Free. Access: public site from a public repository.)

Later changes publish on every push to `main`, after the workflow re-runs the render check and site tests.
