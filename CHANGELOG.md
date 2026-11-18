# Changelog

All notable changes to AgriPulse are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] — 2026-11-18 — Production-Ready Release

### Fixed
- **[P0] `app.js` not loaded** — `base.html` was missing the `<script>` tag; entire frontend was non-functional. Added with `defer` before `</body>`.
- **[P1] `species_id` validation** — `POST /api/animals` now returns HTTP 400 with a clear error if `species_id` is missing or non-integer.
- **[P1] Sex validation on breeding** — `POST /api/breeding` now rejects male animals with HTTP 400 (`"Only female animals can have breeding records"`).
- **[P1] Settings unit persistence** — `PUT /api/settings` now saves `weight_unit`, `milk_unit`, and `date_format` correctly.
- **[P2] Backup restore page reload** — After restore, the app now shows a 3-second countdown toast then calls `location.reload()` instead of silently re-fetching stale data.
- **[P2] `TriggerBackup` case mismatch** — Template called `AgriPulse.TriggerBackup()` but JS defined `triggerBackup()`. Both renamed to `triggerBackup`.
- **[P2] Weight form not resetting** — `submitWeight()` now calls `e.target.reset()` and `setDefaultDates()` after save.
- **[P2] CSS duplicate `@media` blocks** — Removed two conflicting `@media (max-width: 768px)` blocks that used `left` offset approach, conflicting with the transform-based drawer.
- **[P2] CSS `.sidebar.collapsed`** — Was `display:none !important` (causes layout flash). Replaced with smooth `width:0` collapse with CSS transition.
- **[P2] Double `/* /*` comment** — Typo in `style.css` fixed.
- **[P3] FCR calculation** — `GET /api/animals/<id>` now returns a computed `fcr` field (kg feed per kg weight gain) based on feeding records and weight history.

### Added
- **Animal profile → FCR section** — Feed Conversion Ratio displayed per-animal in the profile modal.
- **Animal profile → Danger Zone** — Collapsible section with double-confirm hard-delete (`DELETE /api/animals/<id>?mode=hard`).
- **`hardDeleteAnimal()` JS method** — Two-step confirm dialog before permanent deletion.
- **Weight/milk unit settings** — New `weight_unit` (kg/lb) and `milk_unit` (Liters/Gallons) selects in farm Settings. All labels throughout the app dynamically reflect the saved unit.
- **`api()` error boundary** — `fetch()` `TypeError` (network down) now shows a user-friendly "Network error — check your connection." toast.
- **Loading state in animals table** — Shows "Loading…" row while fetching, preventing blank-table flash.
- **CSS `.d-md-none` utility** — Properly hides the hamburger toggler on desktop (≥769px) and shows it on mobile.
- **Tablet breakpoint (769–1024px)** — 3-column KPIs, 200px sidebar, 2-column forms.
- **Small mobile breakpoint (≤480px)** — Compact KPI cards and buttons.
- **`{% block scripts %}` in `base.html`** — Child templates can inject page-specific scripts.
- **Meta tags** — `theme-color`, `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style` added to `<head>`.

### Changed
- `README.md` — Fully rewritten with project structure, API reference, responsive design table, tech stack, and quick-start guide.
- `CHANGELOG.md` — Added (this file).
- `CONTRIBUTING.md` — Added coding standards and PR guidelines.
- `.gitignore` — Expanded to cover common Python, IDE, and OS artefacts.

---

## [1.0.0] — 2026-11-01 — Initial Release

### Added
- Multi-species livestock management (Cattle, Goats, Sheep, Pigs, Poultry, Rabbits).
- Animal registration with tag number, breed, DOB, sex, production category.
- Breeding records with gestation calculator and pregnancy status tracking.
- Veterinary / health records with disease, medication, and outcome logging.
- Vaccination schedule reference per species (scientifically established protocols).
- Feed inventory management with low-stock alerts.
- Feeding allocation with per-animal nutritional analysis (DM, CP, ME).
- Weight tracking with automatic ADG (Average Daily Gain) calculation.
- Milk, egg, and meat production records.
- Financial transaction ledger (income/expense) with enterprise P&L summary.
- Routine task scheduling with priority and completion tracking.
- Monthly calendar view of all farm events.
- Smart notification engine: breeding due dates, vaccination reminders, low feed, overdue tasks.
- 9-type report system with CSV and PDF export.
- One-click SQLite backup and restore.
- Farm settings: name, location, owner, currency, alert horizon, species parameters.
- Offline-first architecture — no internet required after install.
- Waitress WSGI server for LAN access (phone/tablet on same Wi-Fi).
- pywebview desktop shell for native window experience.
- PyInstaller build spec for standalone Windows EXE packaging.
- pytest suite covering core workflows.
