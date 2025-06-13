"""
Database Migration Script

This script runs Alembic migrations to update the database schema.
"""

import os
import sys
from pathlib import Path
import argparse
import subprocess

# Add the parent directory to sys.path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))


def run_migration(args):
    """Run Alembic migrations with the specified command."""
    # Set current working directory to backend root
    os.chdir(parent_dir)

    alembic_cmd = [
        "alembic",
        "-c",
        "alembic.ini",
        args.command,
    ]

    if args.command == "upgrade" and args.revision:
        alembic_cmd.append(args.revision)
    elif args.command == "downgrade" and args.revision:
        alembic_cmd.append(args.revision)
    elif args.command == "revision" and args.message:
        alembic_cmd.extend(["--autogenerate", "-m", args.message])

    print(f"Running: {' '.join(alembic_cmd)}")
    subprocess.run(alembic_cmd, check=True)


def main():
    """Parse arguments and run the migration."""
    parser = argparse.ArgumentParser(description="Run database migrations.")
    parser.add_argument(
        "command",
        choices=["upgrade", "downgrade", "revision", "history", "current"],
        help="Migration command to run",
    )
    parser.add_argument(
        "--revision",
        help="Revision identifier (for upgrade/downgrade)",
        default="head",
    )
    parser.add_argument(
        "--message", help="Revision message (for new revision)", default=None
    )

    args = parser.parse_args()
    run_migration(args)


if __name__ == "__main__":
    main()
