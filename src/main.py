import argparse
from pathlib import Path
from typing import Union, Dict, Any

from config_loader import load_config, ConfigError
from organizer import organize_files
from utils.logger import get_logger
from utils.report import ReportData, ReportFormatter, ReportWriter
from utils.scanner import ScannerEngine

# Project root detection (riport mindig a gyökérbe kerül)
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

    print("Smart File Organizer Pro v1.5.0")
    print("--------------------------------")

    # Load configuration
    try:
        config: Dict[str, Any] = load_config("config/config.json")
        logger.info("Configuration loaded successfully")
    except ConfigError as error:
        logger.error(f"Configuration error: {error}")
        print(f"Configuration error: {error}")
        return

    # --- ScannerEngine pre-scan ---
    try:
        logger.info("Starting pre-scan analysis")
        scanner = ScannerEngine(config)
        scan_data = scanner.scan_folder(folder_path)
        logger.info("Pre-scan analysis completed successfully")
    except Exception as error:
        logger.error(f"Scanner error: {error}")
        print(f"Scanner error: {error}")
        return

    # Organizer
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
    print("Post-organization statistics:")
    for category, count in stats.items():
        print(f"- {category}: {count}")

    logger.info(f"Post-organization statistics: {stats}")

    # --- Report generation (TXT + JSON + HTML) ---
    try:
        logger.info("Generating reports (TXT + JSON + HTML)")

        report = ReportData(
            source_folder=str(folder_path),
            stats=stats,
            scan_data=scan_data
        )

        writer = ReportWriter(output_dir=PROJECT_ROOT / "reports")

        # TXT report
        text_report = ReportFormatter.to_text(report)
        saved_txt = writer.save_text_report(text_report)

        # JSON report
        json_report = ReportFormatter.to_json(report)
        saved_json = writer.save_json_report(json_report)

        # HTML report
        html_report = ReportFormatter.to_html(report)
        saved_html = writer.save_html_report(html_report)

        logger.info(f"TXT report saved: {saved_txt}")
        logger.info(f"JSON report saved: {saved_json}")
        logger.info(f"HTML report saved: {saved_html}")

        print(f"\nTXT report saved to: {saved_txt}")
        print(f"JSON report saved to: {saved_json}")
        print(f"HTML report saved to: {saved_html}")

    except Exception as error:
        logger.error(f"Failed to generate reports: {error}")
        print(f"Failed to generate reports: {error}")

    logger.info("Application finished")


if __name__ == "__main__":
    main()
