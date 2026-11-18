# 23. Installation Instructions

AgriPulse can be used in three ways: (A) run the finished program, (B) run from source on Windows 11, (C) build the Windows executable yourself. Your records are stored in a separate folder, so installing or updating the program never overwrites them.

## 23.1 Where your data lives

| Item | Location (Windows) |
|---|---|
| Database | `%LOCALAPPDATA%\AgriPulse\db\agripulse.db` |
| Animal photographs | `%LOCALAPPDATA%\AgriPulse\uploads\` |
| Backups (default) | `%LOCALAPPDATA%\AgriPulse\backups\` (can be changed in Settings) |
| Log file | `%LOCALAPPDATA%\AgriPulse\logs\agripulse.log` |

`%LOCALAPPDATA%` normally expands to `C:\Users\<you>\AppData\Local`. Set the environment variable `AGRIPULSE_DATA_DIR` to use a different folder (for example for testing).

## 23.2 Option A — run the packaged program

1. Copy the whole `dist\AgriPulse` folder to the computer (for example `C:\AgriPulse`). Do not copy only the `.exe`; the folder contains the files it needs.
2. Double-click `AgriPulse.exe`. A window titled *AgriPulse — Smarter Livestock Management.* opens. No browser and no internet connection are needed.
3. Open **Settings ▸ Farm & formats** and enter the farm name, location, date format and currency (default KES).
4. Optionally right-click `AgriPulse.exe` ▸ *Send to* ▸ *Desktop (create shortcut)*.

The program needs the **Microsoft Edge WebView2 Runtime**. It is already installed on Windows 11. On Windows 10, install the "Evergreen Standalone Installer" from Microsoft once; this is the only item that may require a one-time download.

## 23.3 Option B — run from source (development)

Requirements: Windows 11, Python 3.11 or newer (tick *Add Python to PATH* in the installer), Visual Studio Code (optional).

```bat
cd path\to\AgriPulse
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python desktop.py          :: opens the desktop window
```

or simply double-click `run_dev.bat`. To work in a normal web browser while developing, run `python run.py` and open `http://127.0.0.1:5000`.

In VS Code: *Ctrl+Shift+P ▸ Python: Select Interpreter ▸ .venv*, open a terminal and run the commands above.

## 23.4 Option C — build the Windows executable

1. Complete Option B steps 1–2 (create and activate `.venv`).
2. Run `build_windows.bat`. It installs the build tools (`requirements-dev.txt`), **runs the automated tests (the build stops if any fail)**, then runs PyInstaller with `AgriPulse.spec`.
3. The result is `dist\AgriPulse\AgriPulse.exe` (a folder-based build, which starts faster and is more reliable with antivirus programs than a single-file build).

Manual equivalent:

```bat
pip install -r requirements-dev.txt
python -m pytest -q
pyinstaller AgriPulse.spec --noconfirm --clean
```

**Optional installer.** `installer.iss` is an Inno Setup script that wraps `dist\AgriPulse` in a normal Windows installer with Start-menu and desktop shortcuts. Install Inno Setup, open `installer.iss`, press *Compile*. (This script was written for convenience and has not been compiled in the development environment.)

## 23.5 Running the automated tests

```bat
python -m pytest -q
```

Expected: `169 passed`. Optional front-end checks (needs Node.js):

```bat
python tests\frontend\dump_pages.py pages
cd tests\frontend && npm install && set PAGES_DIR=..\..\pages && node run.js
```

## 23.6 Windows 11 verification checklist

The development environment could not open a Windows window, so please perform this checklist once after each build. Each item is a few seconds.

| # | Check | Expected |
|---|---|---|
| 1 | Double-click `AgriPulse.exe` | Window opens within a few seconds showing the dashboard; no console window appears |
| 2 | Disconnect from Wi-Fi / unplug cable, restart the program | Everything still works |
| 3 | Start the program a second time | Message "AgriPulse is already running"; no second window |
| 4 | Register an animal with a photograph | Saved; photograph appears on the profile |
| 5 | Close the program and open it again | The animal is still there |
| 6 | Reports ▸ any report ▸ **PDF** | A save dialog (or download) appears; the PDF opens and is readable |
| 7 | Reports ▸ any report ▸ **CSV** | Opens in Excel with correct accents; columns separated |
| 8 | Reports ▸ **Print** | The print dialog shows the report without the sidebar |
| 9 | Settings ▸ Backup & restore ▸ *Create backup now* | A `.zip` appears in the backup folder |
| 10 | Add an animal, then restore the backup | The animal added after the backup disappears; a `…beforerestore…zip` safety copy exists |
| 11 | Delete something (e.g. a feeding record) | A confirmation dialog appears; Cancel keeps it, Confirm deletes it |
| 12 | Close the window | The program exits; (with the default setting) a `…autoexit…zip` backup appears |
| 13 | Check `%LOCALAPPDATA%\AgriPulse\logs\agripulse.log` | No `ERROR` lines after normal use |

If item 6 shows no save dialog, update to the newest pywebview (the launcher enables `ALLOW_DOWNLOADS`) or use **Settings ▸ Backup & restore ▸ Download** for backups and the CSV links for data.

## 23.7 Troubleshooting

| Problem | Cause / fix |
|---|---|
| "AgriPulse could not start its local service" | Another program is blocking local ports or antivirus quarantined a file. Read the log file; add the AgriPulse folder to the antivirus exclusions. |
| White window / blank page | WebView2 Runtime missing (Windows 10). Install it. |
| "pywebview is not installed" | Run `pip install -r requirements.txt` in the active `.venv`. |
| Dates show a different format | *Settings ▸ Farm & formats ▸ Date format*. |
| Backup folder error | The chosen folder is not writable; choose another folder in *Backup & restore*. |
| Restore refused | The file is not an AgriPulse backup, is damaged, or was made by a newer AgriPulse; your current data is **not** changed. |
| Need to start fresh | Close the program and rename `%LOCALAPPDATA%\AgriPulse` (keep it as a copy). A new empty database is created on next start. |
