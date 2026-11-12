# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None
project_root = Path(os.path.abspath(SPECPATH))

hidden_imports = [
    'waitress',
    'webview',
    'sqlalchemy.sql.default_comparator',
    'sqlite3',
] + collect_submodules('flask') + collect_submodules('sqlalchemy')

datas = [
    (str(project_root / 'app' / 'templates'), os.path.join('app', 'templates')),
    (str(project_root / 'app' / 'static'), os.path.join('app', 'static')),
] + collect_data_files('webview')

a = Analysis(
    ['desktop.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy', 'numpy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AgriPulse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)