import os
import sys
from pathlib import Path

def get_app_data_dir() -> Path:
    """Resolve persistent writable application directory across dev and frozen PyInstaller modes."""
    if getattr(sys, 'frozen', False):
        base_dir = Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'AgriPulse'
    else:
        base_dir = Path(__file__).resolve().parent / 'instance'
    
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / 'uploads').mkdir(parents=True, exist_ok=True)
    (base_dir / 'backups').mkdir(parents=True, exist_ok=True)
    return base_dir

def get_resource_dir() -> Path:
    """Resolve static and template directory when bundled with PyInstaller."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / 'app'
    return Path(__file__).resolve().parent / 'app'

APP_DATA_DIR = get_app_data_dir()
RESOURCE_DIR = get_resource_dir()

class Config:
    SECRET_KEY = os.environ.get('AGRIPULSE_SECRET', 'agripulse-offline-secure-key-2026')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{APP_DATA_DIR / 'agripulse.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = str(APP_DATA_DIR / 'uploads')
    BACKUP_FOLDER = str(APP_DATA_DIR / 'backups')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max photo upload

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"