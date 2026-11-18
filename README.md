# 🌾 AgriPulse — Smarter Livestock Management

> Offline-first, multi-species livestock and farm management desktop software.  
> Built with **Python · Flask · SQLAlchemy · SQLite · Waitress · pywebview**.

---

## Overview

AgriPulse is a fully offline desktop application designed for small-to-medium livestock farms in East Africa and beyond. It runs as a local web server (Waitress) and opens in a native desktop window (pywebview) or any browser — no internet, no cloud, no subscriptions.

### Supported Species
Cattle · Dairy Goats · Meat Goats · Sheep · Pigs · Poultry · Rabbits

### Core Modules
| Module | Features |
|---|---|
| **Dashboard** | Live KPIs, farm alerts, species population chart, milk trend, expense chart |
| **Animals** | Registration, profiles, archiving, hard-delete with Danger Zone, breed tracking |
| **Breeding** | Service records, gestation calculator, pregnancy status, delivery tracking |
| **Health** | Veterinary records, vaccination scheduler, disease/treatment logs |
| **Nutrition** | Feed inventory, feeding allocation, nutritional analysis (DM, CP, ME), low-stock alerts |
| **Growth & Weight** | Weight tracking, ADG calculation, FCR (Feed Conversion Ratio), growth chart |
| **Production** | Milk, egg, and meat yield records with daily/monthly summaries |
| **Finance** | Income & expense tracking, enterprise-level P&L, net balance |
| **Tasks** | Routine management scheduling with priority and status tracking |
| **Calendar** | Visual monthly event calendar with farm activities |
| **Notifications** | Smart alerts: due births, overdue vaccines, low feed, upcoming tasks |
| **Reports** | 9 report types — CSV and PDF export |
| **Settings** | Farm profile, currency, weight/milk units, alert horizon, species parameters |
| **Backup & Restore** | One-click SQLite backup with 3-second countdown restore |

---

## Project Structure

```
AgriPulse/
├── app/
│   ├── __init__.py              # App factory (create_app), seed data
│   ├── models.py                # All SQLAlchemy models (13 tables)
│   ├── calculations/
│   │   └── engine.py            # FCR, ADG, nutrition, finance calculations
│   ├── routes/
│   │   ├── api_routes.py        # REST API blueprint  (/api/*)
│   │   └── main_routes.py       # Page views + report export blueprint
│   ├── services/
│   │   ├── backup_service.py    # SQLite backup / restore
│   │   ├── export_service.py    # CSV + PDF report generation
│   │   └── notification_service.py  # Alert generation engine
│   ├── static/
│   │   ├── css/style.css        # All styles — responsive (480/768/1024px)
│   │   └── js/app.js            # Single-page frontend (vanilla JS)
│   └── templates/
│       ├── base.html            # Shell: sidebar, topbar, modals, toast container
│       ├── index.html           # All view sections (13 modules)
│       └── report_print.html    # PDF-ready report layout
├── tests/
│   └── test_agripulse.py        # pytest suite (5 tests)
├── documentation/               # Comprehensive user & technical manuals, defence Q&A
│   ├── 01_TECHNICAL_DOCUMENTATION.md
│   ├── 02_INSTALLATION.md
│   ├── 03_USER_MANUAL.md
│   ├── 04_DEFENCE_QUESTIONS.md
│   ├── AgriPulse_Documentation.docx
│   ├── AgriPulse_Documentation.pdf
│   └── diagrams/                # Architecture diagrams (SVG & PNG)
├── tools/                       # Utilities (docs builder, diagram generator)
├── build_windows.bat            # Windows 11 automated build script
├── installer.iss                # Inno Setup Windows installer definition
├── config.py                    # Config class, paths (dev + PyInstaller frozen)
├── run.py                       # Dev/LAN server (Waitress, auto-opens browser)
├── desktop.py                   # pywebview desktop launcher
├── agripulse.spec               # PyInstaller build spec (Windows EXE)
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Dev & build dependencies
├── Procfile                     # Gunicorn entry (web hosting fallback)
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
└── README.md                    # This file
```

---

## Quick Start

### Prerequisites
- Python 3.12+
- Windows 10/11 (for desktop mode); any OS for browser mode

### 1. Clone & set up

```powershell
git clone <repo-url>
cd AgriPulse
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 2. Run (browser/LAN mode)

```powershell
python run.py
# Opens http://127.0.0.1:5000 automatically
# Also available on local network: http://<your-ip>:5000
```

### 3. Run (desktop app mode)

```powershell
python desktop.py
# Opens as a native window via pywebview
```

### 4. Build Windows EXE

```powershell
pyinstaller agripulse.spec --clean
# Output: dist/AgriPulse.exe (standalone, no Python needed)
```

---

## Running Tests

```powershell
venv\Scripts\python -m pytest tests/ -v
```

**Test suite (5 tests):**
- `test_database_and_species_initialization`
- `test_animal_registration_and_duplicate_tag_prevention`
- `test_species_specific_breeding_calculations`
- `test_weight_adg_and_nutrition_stock_deduction`
- `test_reports_csv_and_pdf_exports`

---

## Configuration

All configuration lives in `config.py`.

| Setting | Dev value | Frozen (EXE) value |
|---|---|---|
| Database | `instance/agripulse.db` | `%LOCALAPPDATA%\AgriPulse\agripulse.db` |
| Backups | `instance/backups/` | `%LOCALAPPDATA%\AgriPulse\backups/` |
| Uploads | `instance/uploads/` | `%LOCALAPPDATA%\AgriPulse\uploads/` |
| Secret key | env `AGRIPULSE_SECRET` | env `AGRIPULSE_SECRET` |

### Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `AGRIPULSE_SECRET` | `agripulse-offline-secure-key-2026` | Flask session secret |

---

## API Reference

All REST endpoints are under `/api/`. They return JSON.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/settings` | Fetch farm settings |
| PUT | `/api/settings` | Update farm settings (name, currency, units, alert days) |
| GET | `/api/species` | List all species |
| PUT | `/api/species/<id>` | Update species biological parameters |
| GET | `/api/animals` | List animals (filter: `search`, `species_id`, `status`) |
| POST | `/api/animals` | Register new animal |
| GET | `/api/animals/<id>` | Full animal profile (breeding, health, weights, FCR) |
| DELETE | `/api/animals/<id>` | Archive (`?mode=archive`) or hard-delete (`?mode=hard`) |
| GET | `/api/breeding` | List breeding records |
| POST | `/api/breeding` | Create breeding record (females only) |
| PUT | `/api/breeding/<id>` | Update pregnancy status |
| GET | `/api/health` | List health records |
| POST | `/api/health` | Add veterinary/health record |
| GET | `/api/feeds` | List feed inventory |
| POST | `/api/feeds` | Add feed stock |
| GET | `/api/feeding-records` | List feeding allocations |
| POST | `/api/feeding-records` | Record feeding allocation |
| GET | `/api/weights` | List weight records (filter: `animal_id`) |
| POST | `/api/weights` | Record weight measurement (auto-calculates ADG) |
| GET | `/api/production` | List production records |
| POST | `/api/production` | Add production record |
| GET | `/api/tasks` | List routine tasks |
| POST | `/api/tasks` | Schedule routine task |
| PUT | `/api/tasks/<id>` | Update task status |
| GET | `/api/finance` | Financial summary + transactions |
| POST | `/api/finance` | Record income/expense transaction |
| GET | `/api/notifications` | Fetch alerts (`?include_resolved=true`) |
| POST | `/api/notifications/resolve` | Mark alert as resolved |
| GET | `/api/dashboard` | KPIs, top alerts, recent health, charts data |
| GET | `/api/calendar` | Monthly calendar events |
| GET | `/api/backup` | List backups |
| POST | `/api/backup` | Create new backup |
| POST | `/api/backup/restore` | Restore from backup file |
| GET | `/api/backup/download/<filename>` | Download backup file |

**Report exports** (blueprint: `main_bp`):

| Method | Endpoint | Description |
|---|---|---|
| GET | `/reports/export` | Export report (`?type=&format=csv\|pdf&start_date=&end_date=`) |

**Report types:** `animals`, `breeding`, `health`, `weights`, `production`, `nutrition`, `finance`, `tasks`, `notifications`

---

## Responsive Design

| Breakpoint | Behaviour |
|---|---|
| ≥ 1025px (desktop) | Full sidebar + content, 4-col forms, 5-col KPI grid |
| 769–1024px (tablet) | 200px sidebar, 3-col KPIs, 2-col forms |
| ≤ 768px (mobile) | Hamburger drawer sidebar, 2-col KPIs, stacked forms, full-width modals |
| ≤ 480px (small mobile) | Compact KPIs, smaller buttons, 2-col KPI grid |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | Flask 3.0 |
| ORM | SQLAlchemy 2.0 + Flask-SQLAlchemy |
| Database | SQLite (single file, offline) |
| WSGI server | Waitress 3.0 (dev + production) |
| Desktop shell | pywebview 5.1 |
| Frontend | Vanilla JS (no framework), HTML5, CSS3 |
| PDF export | Jinja2 HTML → browser print |
| Packaging | PyInstaller 6.6 (Windows EXE) |
| Testing | pytest 9.2 |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, branch strategy, and PR guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## License

Proprietary — AgriPulse Livestock Enterprise © 2026. All rights reserved.
