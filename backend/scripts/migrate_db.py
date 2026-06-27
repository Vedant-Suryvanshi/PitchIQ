# backend/scripts/migrate_db.py
"""
Database migration runner script.
Run this to apply or rollback migrations.

Usage:
    python scripts/migrate_db.py upgrade
    python scripts/migrate_db.py downgrade
    python scripts/migrate_db.py history
    python scripts/migrate_db.py current
"""

import asyncio
import sys
import os
from pathlib import Path
import argparse

# Add parent directory to path so we can import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from alembic import command
from alembic.config import Config
import structlog

logger = structlog.get_logger(__name__)


def get_alembic_config() -> Config:
    """
    Get Alembic configuration.
    Tries to find alembic.ini in the current directory.
    """
    # Check if alembic.ini exists in current directory
    if os.path.exists("alembic.ini"):
        return Config("alembic.ini")
    
    # Check if alembic.ini exists in parent directory
    parent_dir = Path(__file__).parent.parent
    if os.path.exists(parent_dir / "alembic.ini"):
        return Config(str(parent_dir / "alembic.ini"))
    
    # Check for sync config
    if os.path.exists("alembic_sync.ini"):
        return Config("alembic_sync.ini")
    
    if os.path.exists(parent_dir / "alembic_sync.ini"):
        return Config(str(parent_dir / "alembic_sync.ini"))
    
    raise FileNotFoundError("No alembic.ini found. Run 'alembic init alembic' first.")


def run_migrations(target: str = "head") -> None:
    """
    Run migrations to target revision.
    """
    try:
        alembic_cfg = get_alembic_config()
        logger.info(f"Running upgrade to {target}...")
        command.upgrade(alembic_cfg, target)
        logger.info("✅ Migration completed successfully", target=target)
    except Exception as e:
        logger.error(f"❌ Migration failed: {str(e)}")
        raise


def rollback_migrations(revision: str = "-1") -> None:
    """
    Rollback migrations by one revision.
    """
    try:
        alembic_cfg = get_alembic_config()
        logger.info(f"Running downgrade to {revision}...")
        command.downgrade(alembic_cfg, revision)
        logger.info("✅ Rollback completed successfully", revision=revision)
    except Exception as e:
        logger.error(f"❌ Rollback failed: {str(e)}")
        raise


def show_history() -> None:
    """
    Show migration history.
    """
    try:
        alembic_cfg = get_alembic_config()
        command.history(alembic_cfg)
    except Exception as e:
        logger.error(f"❌ Failed to show history: {str(e)}")
        raise


def show_current() -> None:
    """
    Show current migration version.
    """
    try:
        alembic_cfg = get_alembic_config()
        command.current(alembic_cfg)
    except Exception as e:
        logger.error(f"❌ Failed to show current version: {str(e)}")
        raise


def stamp_head() -> None:
    """
    Stamp the database with the head revision.
    Useful when migrations are out of sync.
    """
    try:
        alembic_cfg = get_alembic_config()
        logger.info("Stamping database with head revision...")
        command.stamp(alembic_cfg, "head")
        logger.info("✅ Database stamped successfully")
    except Exception as e:
        logger.error(f"❌ Stamp failed: {str(e)}")
        raise


def create_migration(message: str = "Migration") -> None:
    """
    Create a new migration.
    """
    try:
        alembic_cfg = get_alembic_config()
        logger.info(f"Creating migration: {message}...")
        command.revision(alembic_cfg, autogenerate=True, message=message)
        logger.info("✅ Migration created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create migration: {str(e)}")
        raise


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Database migration tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/migrate_db.py upgrade
    python scripts/migrate_db.py downgrade
    python scripts/migrate_db.py create -m "Add new table"
    python scripts/migrate_db.py stamp
        """
    )
    
    # Main command
    parser.add_argument(
        "command",
        choices=["upgrade", "downgrade", "history", "current", "create", "stamp"],
        help="Command to run"
    )
    
    # Optional arguments
    parser.add_argument(
        "--revision", "-r",
        default="head",
        help="Target revision (default: head)"
    )
    parser.add_argument(
        "--message", "-m",
        default="Migration",
        help="Migration message (for create command)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Execute command
        if args.command == "upgrade":
            run_migrations(args.revision)
        elif args.command == "downgrade":
            rollback_migrations(args.revision)
        elif args.command == "history":
            show_history()
        elif args.command == "current":
            show_current()
        elif args.command == "create":
            create_migration(args.message)
        elif args.command == "stamp":
            stamp_head()
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()