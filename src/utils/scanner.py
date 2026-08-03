from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Union

from utils.logger import get_logger

logger = get_logger("Scanner")


class ScannerData:
    """
    Data model representing the result of a folder scan.

    Attributes
    ----------
    source_folder : str
        The folder that was scanned.
    total_files : int
        Total number of files found in the folder.
    total_size_bytes : int
        Sum of all file sizes in bytes.
    category_distribution : Dict[str, int]
        Number of files per category (based on config file_types).
    large_files : List[Dict[str, Any]]
        List of large files with metadata (path, size, category).
    timestamp : str
        Timestamp when the scan was performed.
    """

    def __init__(
        self,
        source_folder: str,
        total_files: int,
        total_size_bytes: int,
        category_distribution: Dict[str, int],
        large_files: List[Dict[str, Any]],
    ) -> None:
        self.source_folder = source_folder
        self.total_files = total_files
        self.total_size_bytes = total_size_bytes
        self.category_distribution = category_distribution
        self.large_files = large_files
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger.info(
            f"ScannerData created for folder '{self.source_folder}' "
            f"with {self.total_files} files and total size {self.total_size_bytes} bytes"
        )


class ScannerEngine:
    """
    Engine responsible for scanning a folder and collecting file statistics.

    The engine uses the same file_types configuration as the organizer module
    to categorize files consistently.

    Attributes
    ----------
    file_types : Dict[str, List[str]]
        Mapping of category names to lists of file extensions.
    large_file_threshold_bytes : int
        Size threshold in bytes above which a file is considered "large".
    """

    def __init__(
        self,
        config: Dict[str, Any],
        large_file_threshold_mb: int = 50,
    ) -> None:
        """
        Initialize the scanner engine.

        Parameters
        ----------
        config : Dict[str, Any]
            Configuration dictionary loaded from config.json.
        large_file_threshold_mb : int, default=50
            Threshold in megabytes for large file detection.
        """
        self.file_types: Dict[str, List[str]] = config.get("file_types", {})
        self.large_file_threshold_bytes: int = large_file_threshold_mb * 1024 * 1024

        logger.info(
            f"ScannerEngine initialized with large file threshold "
            f"{large_file_threshold_mb} MB ({self.large_file_threshold_bytes} bytes)"
        )

    def _get_category(self, extension: str) -> str:
        """
        Determine the category of a file based on its extension.

        Parameters
        ----------
        extension : str
            File extension (e.g., '.pdf').

        Returns
        -------
        str
            Category name or 'others' if unknown.
        """
        for category, extensions in self.file_types.items():
            if extension in extensions:
                return category
        return "others"

    def scan_folder(self, source_folder: Union[str, Path]) -> ScannerData:
        """
        Scan the given folder and collect file statistics.

        Parameters
        ----------
        source_folder : Union[str, Path]
            Path to the folder to be scanned.

        Returns
        -------
        ScannerData
            Data object containing scan results.

        Raises
        ------
        FileNotFoundError
            If the source folder does not exist.
        """
        source_path = Path(source_folder)

        if not source_path.exists():
            logger.error(f"Source folder does not exist: {source_folder}")
            raise FileNotFoundError(f"Source folder does not exist: {source_folder}")

        logger.info(f"Starting scan for folder: {source_path}")

        # Initialize statistics
        category_distribution: Dict[str, int] = {
            category: 0 for category in self.file_types.keys()
        }
        if "others" not in category_distribution:
            category_distribution["others"] = 0

        total_files: int = 0
        total_size_bytes: int = 0
        large_files: List[Dict[str, Any]] = []

        # Iterate over files
        for item in source_path.iterdir():
            if not item.is_file():
                logger.warning(f"Skipping non-file item during scan: {item.name}")
                continue

            try:
                size = item.stat().st_size
            except OSError as error:
                logger.warning(f"Unable to read file size for {item.name}: {error}")
                continue

            extension = item.suffix.lower()
            category = self._get_category(extension)

            total_files += 1
            total_size_bytes += size
            category_distribution[category] = category_distribution.get(category, 0) + 1

            if size >= self.large_file_threshold_bytes:
                large_files.append(
                    {
                        "path": str(item),
                        "size_bytes": size,
                        "category": category,
                    }
                )
                logger.info(
                    f"Large file detected: {item.name} "
                    f"({size} bytes, category: {category})"
                )

        logger.info(
            f"Scan completed for folder '{source_path}'. "
            f"Total files: {total_files}, total size: {total_size_bytes} bytes"
        )

        return ScannerData(
            source_folder=str(source_path),
            total_files=total_files,
            total_size_bytes=total_size_bytes,
            category_distribution=category_distribution,
            large_files=large_files,
        )


class ScannerFormatter:
    """
    Formatter class responsible for converting ScannerData into text format.

    This is compatible with the existing report system and can later be extended
    to support JSON, HTML, or GUI representations.
    """

    @staticmethod
    def to_text(scanner_data: ScannerData) -> str:
        """
        Convert ScannerData into a human-readable text summary.

        Parameters
        ----------
        scanner_data : ScannerData
            The scanner data object.

        Returns
        -------
        str
            Formatted text summary of the scan.
        """
        logger.info("Formatting scanner data as TXT")

        lines = [
            "Smart File Organizer Pro - Scanner Summary",
            "------------------------------------------",
            f"Source folder: {scanner_data.source_folder}",
            f"Scanned at: {scanner_data.timestamp}",
            "",
            f"Total files: {scanner_data.total_files}",
            f"Total size: {scanner_data.total_size_bytes} bytes",
            "",
            "Category distribution:",
        ]

        for category, count in scanner_data.category_distribution.items():
            lines.append(f"- {category}: {count}")

        if scanner_data.large_files:
            lines.append("")
            lines.append("Large files (over threshold):")
            for entry in scanner_data.large_files:
                lines.append(
                    f"- {entry['path']} "
                    f"({entry['size_bytes']} bytes, category: {entry['category']})"
                )

        lines.append("------------------------------------------")

        return "\n".join(lines)
