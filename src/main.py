import argparse
from pathlib import Path
from typing import Union, Dict, Any

from config_loader import load_config, ConfigError
from organizer import organize_files


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the Smart File Organizer Pro CLI.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments containing:
        - folder (str)
        - dry_run (bool)
    """
    parser = argparse.ArgumentParser(
        description="Smart File Organizer Pro - Professional Python Automation Tool"
    )

    parser.add_argument(
        "--folder",
        type=str,
        required=True,
        help="Path to the folder that should be organized."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without moving any files."
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the Smart File Organizer Pro CLI.

    Loads configuration, validates input, and triggers the file organization process.
    Provides clean error messages and prepares the structure for future extensions
    such as logging, reporting, and GUI integration.
    """
    args = parse_arguments()

    folder_path: Union[str, Path] = args.folder
    dry_run: bool = args.dry_run

    print("Smart File Organizer Pro v1.0.0")
    print("--------------------------------")

    # Load configuration
    try:
        config: Dict[str, Any] = load_config("config/config.json")
    except ConfigError as error:
        print(f"Configuration error: {error}")
        return

    # Run organizer
    try:
        stats = organize_files(folder_path, config, dry_run=dry_run)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return
    except Exception as error:
        print(f"Unexpected error: {error}")
        return

    # Display results
    print("\nOrganization completed.\n")
    print("File statistics:")
    for category, count in stats.items():
        print(f"- {category}: {count}")

    print("\nDone.")


if __name__ == "__main__":
    main()
