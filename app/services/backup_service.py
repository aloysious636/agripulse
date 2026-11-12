import shutil
from datetime import datetime
from pathlib import Path
from flask import current_app
from app.models import db

class BackupService:
    @staticmethod
    def create_backup() -> dict:
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        if not db_uri.startswith('sqlite:///') or ':memory:' in db_uri:
            raise ValueError("Cannot perform file backup on an in-memory database.")

        db_path = Path(db_uri.replace('sqlite:///', ''))
        backup_dir = Path(current_app.config['BACKUP_FOLDER'])
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"agripulse_backup_{timestamp}.db"
        dest_path = backup_dir / backup_filename

        db.session.commit()
        shutil.copy2(db_path, dest_path)

        return {
            'filename': backup_filename,
            'path': str(dest_path),
            'size_kb': round(dest_path.stat().st_size / 1024, 2),
            'timestamp': timestamp
        }

    @staticmethod
    def list_backups() -> list:
        backup_dir = Path(current_app.config['BACKUP_FOLDER'])
        if not backup_dir.exists():
            return []
        files = sorted(backup_dir.glob('agripulse_backup_*.db'), key=lambda p: p.stat().st_mtime, reverse=True)
        return [{
            'filename': f.name,
            'size_kb': round(f.stat().st_size / 1024, 2),
            'created_at': datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        } for f in files]

    @staticmethod
    def restore_backup(source_path: Path) -> bool:
        if not source_path.exists():
            raise FileNotFoundError("Backup file does not exist.")
        with open(source_path, 'rb') as f:
            header = f.read(16)
        if not header.startswith(b'SQLite format 3'):
            raise ValueError("Uploaded file is not a valid SQLite database.")

        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        db_path = Path(db_uri.replace('sqlite:///', ''))

        db.session.remove()
        db.engine.dispose()
        shutil.copy2(source_path, db_path)
        return True