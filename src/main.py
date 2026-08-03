import argparse
from pathlib import Path
from typing import Union, Dict, Any

from config_loader import load_config, ConfigError
from organizer import organize_files
from utils.logger import get_logger
from utils.report import ReportData, ReportFormatter, ReportWriter


# Project root detection
PROJECT_ROOT = Path(__file__).resolve().parent.parent


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

    print("Smart File Organizer Pro v1.1.1")
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

        stats = organize_files(
            folder_path,
            config,
            dry_run=dry_run
        )

        logger.info("File organization completed successfully")

    except FileNotFoundError as error:
        logger.error(f"Source folder not found: {error}")
        print(f"Error: {error}")
        return

    except Exception as error:
        logger.error(f"Unexpected error: {error}")
        print(f"Unexpected error: {error}")
        return

    # Print statistics
    print("\nOrganization completed.\n")
    print("File statistics:")

    for category, count in stats.items():
        print(f"- {category}: {count}")

    logger.info(f"Statistics: {stats}")

    # Generate report
    try:
        logger.info("Generating report")

        report = ReportData(
            str(folder_path),
            stats
        )

        text_report = ReportFormatter.to_text(report)

        writer = ReportWriter(
            output_dir=PROJECT_ROOT / "reports"
        )

        saved_path = writer.save_text_report(text_report)

        logger.info(f"Report generated successfully: {saved_path}")

        print(f"\nReport saved to: {saved_path}")

    except Exception as error:
        logger.error(f"Failed to generate report: {error}")
        print(f"Failed to generate report: {error}")

    logger.info("Application finished")


if __name__ == "__main__":
    main()