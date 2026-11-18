@echo off
REM Build AgriPulse for Windows 11.  Run from the project folder in a normal Command Prompt.
setlocal
where python >nul 2>nul || (echo Python 3.11+ is required. Install it from python.org and tick "Add to PATH". & exit /b 1)
if not exist .venv (python -m venv .venv || exit /b 1)
call .venv\Scripts\activate.bat || exit /b 1
python -m pip install --upgrade pip || exit /b 1
pip install -r requirements-dev.txt || exit /b 1
echo.
echo === Running automated tests ===
python -m pytest -q || (echo Tests failed - build stopped. & exit /b 1)
echo.
echo === Building executable ===
pyinstaller agripulse.spec --noconfirm --clean || exit /b 1
echo.
echo Done. Run dist\AgriPulse\AgriPulse.exe
echo Your data is stored in %%LOCALAPPDATA%%\AgriPulse (separate from the program).
endlocal
