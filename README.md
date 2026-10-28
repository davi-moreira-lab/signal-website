# SIGNAL Website — a program of Davi Moreira Research Lab

The static website for SIGNAL, **live since 2026-10-27 at https://davi-moreira-lab.github.io/signal-website/** (public repository `davi-moreira-lab/signal-website`, published with Davi's approval). No custom domain has been purchased, registered or verified. SIGNAL is the program brand and Dr. Davi Moreira's Research Lab is the durable umbrella. Current affiliation: Purdue University (update when affiliation changes).

## Preview locally

```bash
# from the workspace root (davi-moreira-lab/)
cd programs/signal/website
python3 tools/render_site.py
python3 tools/render_site.py --check   # confirms index.html matches site.json + template
python3 -m http.server 8000 --bind 127.0.0.1
```

Visit http://localhost:8000. Ctrl+C stops the preview. `--bind 127.0.0.1` keeps the preview on this computer; without it Python serves the folder to the whole local network. No external scripts, fonts, images or paid hosting are needed.

## Editing

Edit `content/site.json` for approved text and current affiliation; run `python3 tools/render_site.py` to regenerate `index.html` from `templates/index.template.html`. Edit `styles.css` for visual design. Commit both `content/site.json` and `index.html` when ready. Do not add unverified publications, students, credentials, logos or institutional endorsements.

## Publication

Every push to `main` runs `.github/workflows/pages.yml`: it re-checks that `index.html` is freshly rendered, runs the site tests, and deploys to GitHub Pages only an isolated artifact containing `index.html`, `styles.css`, `assets/davi-moreira.jpg` and `.nojekyll`. Pushing to `main` therefore publishes; push only approved copy. The repository is public because GitHub Free serves Pages only from public repositories (Davi's decision, 2026-10-27); its source holds nothing sensitive and must stay that way. Never select the source repository's `main` branch root as the publishing source: that can expose instructions, source JSON, tools, tests and internal publication documents. Follow `publication/RELEASE_CHECKLIST.md`; review the actual artifact before deployment. Source-repository privacy does not make a Pages site private. Custom domains and DNS need separate approval.
