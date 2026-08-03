import logging
from pathlib import Path
from typing import Optional


def _create_log_directory(log_dir: Path) -> None:
    """
    Create the log directory if it does not exist.

    Parameters
    ----------
    log_dir : Path
        Path to the directory where log files should be stored.
    """
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)


def get_logger(name: Optional[str] = "SmartFileOrganizer") -> logging.Logger:
    """
    Configure and return a logger instance for the Smart File Organizer Pro project.

    This logger:
    - writes logs to logs/organizer.log
    - supports INFO, WARNING, and ERROR levels
    - is safe to import from any module (main.py, organizer.py, config_loader.py)
    - avoids duplicate handlers when imported multiple times

    Parameters
    ----------
    name : Optional[str], default="SmartFileOrganizer"
        Name of the logger. Modules may override this for more specific logging.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    log_dir = Path("logs")
    log_file = log_dir / "organizer.log"

    # Ensure log directory exists
    _create_log_directory(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if logger is reused
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
