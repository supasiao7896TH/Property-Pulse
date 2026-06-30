# AGENTS.md

Instructions for AI coding agents (Claude Code, Copilot, Codex, etc.)
working in this repository. See `context.md` for a fuller architectural
write-up — read that first if you need background before changing code.

## Project in one line

A zero-build, single-file Thai-language PWA (`index.html`) for tracking a
small personal rental property portfolio, persisted entirely client-side in
IndexedDB. No backend, no package manager, no bundler.

## Where things live

- `index.html` — the entire app: markup, styles, and JS. Almost every
  change happens here.
- `manifest.json` — PWA metadata. Edit only for branding/icon changes.
- `sw.js` — service worker / offline cache. Keep `APP_SHELL` in sync with
  any renamed/added top-level files; bump the `CACHE` constant when you do.
- `icons/` — generated PNG/SVG icons. Regenerate via `make_icons.py`
  (`python3 make_icons.py`, requires Pillow) rather than hand-editing PNGs.

## Setup

Nothing to install. There is no `package.json`. To preview the app:

```bash
python3 -m http.server 8000   # from the repo root
```

then open `http://localhost:8000/`. Opening `index.html` directly via
`file://` works for most UI but the service worker won't register without a
real HTTP origin.

## Verifying changes

There is no test suite, linter, or CI. Verification is manual:
1. Serve the directory locally (see above) and open it in a browser.
2. Exercise the specific view/feature you changed (Dashboard, Rooms,
   Transactions, Settings).
3. Check the browser console for JS errors — there's no build step to
   catch syntax mistakes ahead of time.
4. If you touched IndexedDB schema or persistence logic, test Export DB →
   Import DB in Settings to make sure round-tripping still works, and test
   on a fresh IndexedDB (clear site data) to make sure `onupgradeneeded`
   still creates a working DB from scratch.

## Editing guidelines

- Keep the **single-file, zero-build** architecture. Do not add a bundler,
  npm dependencies, or split the app into modules/files unless the user
  explicitly asks for that — it's a deliberate constraint, not an oversight.
- Match existing code style: vanilla JS, IIFE module pattern (`DBManager`,
  `App`), `const`-first, template-string-built DOM via `innerHTML`.
- All user-facing text is Thai. New strings should match existing tone and
  terminology (e.g. "ยูนิต" for unit, "ยอดเงิน" for amount).
- Always escape interpolated user data with the existing `escHtml` helper
  when building `innerHTML` strings.
- Use `formatMoney`/`formatMoneyShort` for currency display — don't
  hand-roll number formatting.
- Call `lucide.createIcons()` (scoped to the new root when possible) after
  injecting any markup with `data-lucide` attributes.
- If you change what's stored in IndexedDB, bump `CONFIG.DB_VERSION` in
  `index.html` and add the needed store/index creation in
  `DBManager.init`'s `onupgradeneeded` handler.
- The CSP `<meta>` tag in `<head>` still allow-lists
  `https://generativelanguage.googleapis.com` even though Gemini AI
  integration was removed (see git history: "remove: Gemini AI Engine").
  Don't reintroduce AI/network calls without explicit product direction;
  tighten rather than loosen the CSP when in doubt.
- Don't reintroduce Chart.js usage casually — it's currently loaded but
  unused (the cash-flow chart was deliberately removed). If you add a
  chart back, make sure it's an intentional feature, not leftover scaffolding.

## Commit conventions

This repo's history uses short, conventional-style prefixes: `feat:`,
`fix:`, `refactor:`, `remove:`, followed by an imperative summary. Follow
that style for new commits.
