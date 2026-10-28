# Website review — 2026-10-22/23 (prototype; not a launch approval)

Implementation self-check by the setup agents (Claude Code and Codex); a later independent reviewer and the director still decide on any launch.

## Automated (re-run with `python3 -m unittest discover -s tests -v` from this repository)

- One H1, a focusable `main` landmark, skip link, named navigation, unique IDs, working in-page fragments (Codex's `test_accessibility.py`).
- Only relative local assets; no script, iframe, form, web font or external request (`test_accessibility.py`, `test_site.py`).
- `index.html` exactly matches `content/site.json` rendered through `templates/index.template.html` (`tools/render_site.py --check`).
- Selected text/background and focus-outline pairs meet the 4.5:1 small-text target (W3C contrast minimum: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Before the fix, several muted labels measured 3.2–4.3:1.

## Browser checks (Claude, built-in browser, served on 127.0.0.1, 2026-10-23)

- No horizontal page overflow at 320, 375, 768 and 1024 px; at ≤710 px the navigation wraps and columns stack; at ≤420 px the person card stacks. The largest decorative orbit is clipped inside its own panel.
- First Tab press focuses a visible "Skip to content" link.
- Page loads with no external network requests.

## Not yet verified

1440 px and wider, 200–400% browser zoom, complete keyboard focus order, screen-reader announcements, high-contrast modes, and full WCAG conformance. Copy is still the starter kit's generic text and a visible draft notice; it does not yet describe the awarded SIGNAL theme.
