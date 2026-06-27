# backend/scripts/backup_db.py
"""
Database backup script for PostgreSQL
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import structlog

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


def create_backup():
    """Create a database backup."""
    # Create backup directory if it doesn't exist
    backup_dir = Path(__file__).parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"pitchiq_backup_{timestamp}.sql"
    
    # Extract database connection details
    db_url = settings.database_url
    if "postgresql" in db_url:
        # Parse connection string
        # postgresql+asyncpg://user:password@host:port/database
        parts = db_url.replace("postgresql+asyncpg://", "").split("@")
        user_pass = parts[0].split(":")
        host_port_db = parts[1].split("/")
        host_port = host_port_db[0].split(":")
        
        user = user_pass[0]
        password = user_pass[1] if len(user_pass) > 1 else ""
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else "5432"
        database = host_port_db[1] if len(host_port_db) > 1 else "pitchiq"
        
        # Build pg_dump command
        cmd = [
            "pg_dump",
            "--host", host,
            "--port", port,
            "--username", user,
            "--dbname", database,
            "--format", "custom",
            "--file", str(backup_file),
            "--verbose"
        ]
        
        # Set password environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        logger.info("backup.starting", file=str(backup_file))
        
        try:
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("backup.success", file=str(backup_file), size=backup_file.stat().st_size)
                return str(backup_file)
            else:
                logger.error("backup.failed", error=result.stderr)
                return None
        except Exception as e:
            logger.error("backup.exception", error=str(e))
            return None
    else:
        logger.warning("backup.skip", reason="Not using PostgreSQL")
        return None


def list_backups():
    """List all available backups."""
    backup_dir = Path(__file__).parent.parent / "backups"
    if not backup_dir.exists():
        return []
    
    backups = []
    for file in backup_dir.glob("pitchiq_backup_*.sql"):
        backups.append({
            "file": str(file),
            "size": file.stat().st_size,
            "created": datetime.fromtimestamp(file.stat().st_ctime)
        })
    
    return sorted(backups, key=lambda x: x["created"], reverse=True)


def restore_backup(backup_file: str):
    """Restore a database backup."""
    # Extract database connection details
    db_url = settings.database_url
    if "postgresql" in db_url:
        parts = db_url.replace("postgresql+asyncpg://", "").split("@")
        user_pass = parts[0].split(":")
        host_port_db = parts[1].split("/")
        host_port = host_port_db[0].split(":")
        
        user = user_pass[0]
        password = user_pass[1] if len(user_pass) > 1 else ""
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else "5432"
        database = host_port_db[1] if len(host_port_db) > 1 else "pitchiq"
        
        # Build pg_restore command
        cmd = [
            "pg_restore",
            "--host", host,
            "--port", port,
            "--username", user,
            "--dbname", database,
            "--verbose",
            "--clean",
            "--if-exists",
            str(backup_file)
        ]
        
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        logger.info("restore.starting", file=backup_file)
        
        try:
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("restore.success", file=backup_file)
                return True
            else:
                logger.error("restore.failed", error=result.stderr)
                return False
        except Exception as e:
            logger.error("restore.exception", error=str(e))
            return False
    else:
        logger.warning("restore.skip", reason="Not using PostgreSQL")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Database backup tool")
    parser.add_argument("action", choices=["backup", "list", "restore"],
                       help="Action to perform")
    parser.add_argument("--file", help="Backup file to restore")
    
    args = parser.parse_args()
    
    if args.action == "backup":
        result = create_backup()
        if result:
            print(f"✅ Backup created: {result}")
        else:
            print("❌ Backup failed")
            sys.exit(1)
    
    elif args.action == "list":
        backups = list_backups()
        if backups:
            print("📋 Available backups:")
            for b in backups:
                size_mb = b["size"] / (1024 * 1024)
                print(f"  {b['file']} ({size_mb:.2f} MB) - {b['created']}")
        else:
            print("No backups found")
    
    elif args.action == "restore":
        if not args.file:
            print("❌ Please specify --file")
            sys.exit(1)
        
        if not Path(args.file).exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        
        confirm = input(f"⚠️  Restore {args.file}? This will overwrite current data! (yes/no): ")
        if confirm.lower() == "yes":
            if restore_backup(args.file):
                print(f"✅ Database restored from: {args.file}")
            else:
                print("❌ Restore failed")
                sys.exit(1)


if __name__ == "__main__":
    main()