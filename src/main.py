import argparse
from pathlib import Path
from typing import Union, Dict, Any

from config_loader import load_config, ConfigError
from organizer import organize_files
from utils.logger import get_logger


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the Smart File Organizer Pro CLI.
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
    """
    logger = get_logger("Main")
    logger.info("Application started")

    args = parse_arguments()

    folder_path: Union[str, Path] = args.folder
    dry_run: bool = args.dry_run

    logger.info(f"Received folder argument: {folder_path}")
    logger.info(f"Dry-run mode: {dry_run}")

    print("Smart File Organizer Pro v1.0.1")
    print("--------------------------------")

    # Load configuration
    try:
        config: Dict[str, Any] = load_config("config/config.json")
        logger.info("Configuration loaded successfully")
    except ConfigError as error:
        logger.error(f"Configuration error: {error}")
        print(f"Configuration error: {error}")
        return

    # Run organizer
    try:
        logger.info("Starting file organization process")
        stats = organize_files(folder_path, config, dry_run=dry_run)
        logger.info("File organization completed successfully")
    except FileNotFoundError as error:
        logger.error(f"Source folder not found: {error}")
        print(f"Error: {error}")
        return
    except Exception as error:
        logger.error(f"Unexpected error: {error}")
        print(f"Unexpected error: {error}")
        return

    # Display results
    print("\nOrganization completed.\n")
    print("File statistics:")
    for category, count in stats.items():
        print(f"- {category}: {count}")

    logger.info(f"Statistics: {stats}")
    logger.info("Application finished")


if __name__ == "__main__":
    main()
