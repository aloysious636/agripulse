"""Smoke test run INSIDE a PyInstaller bundle: proves templates, static files, SQLite and PDF export work frozen.
Build/run instructions are in documentation/INSTALLATION.md (section "Verifying a build")."""
import os
import sys
import tempfile

from app import create_app

app = create_app(data_dir=os.environ.get("AGRIPULSE_DATA_DIR") or tempfile.mkdtemp(),
                 config_overrides={"WTF_CSRF_ENABLED": False})
c = app.test_client()
c.post("/animals/new", data={"tag_number": "FROZEN-1", "species_id": 1, "sex": "Female"})
checks = {"/": "Dashboard", "/animals/": "FROZEN-1", "/static/css/app.css": "--forest", "/static/js/charts.js": "AgriCharts",
          "/reports/animal-inventory": "FROZEN-1", "/settings/?tab=backup": "Backup", "/calendar/": "Farm calendar"}
bad = 0
for url, needle in checks.items():
    r = c.get(url)
    ok = r.status_code == 200 and needle in r.get_data(as_text=True)
    bad += not ok
    print(("OK   " if ok else "FAIL ") + url, r.status_code)
pdf = c.get("/reports/animal-inventory.pdf")
ok = pdf.status_code == 200 and pdf.data.startswith(b"%PDF")
bad += not ok
print(("OK   " if ok else "FAIL ") + "PDF export", len(pdf.data), "bytes")
print("frozen =", getattr(sys, "frozen", False), "| bundle dir =", getattr(sys, "_MEIPASS", "-"))
sys.exit(1 if bad else 0)
