from pathlib import Path
import json
from typing import Dict, Any, Union

from utils.logger import get_logger

logger = get_logger("ConfigLoader")


class ConfigError(Exception):
    """
    Custom exception class for configuration-related errors.
    """
    pass


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load and validate the application's configuration file (config.json).

    Parameters
    ----------
    config_path : Union[str, Path]
        Path to the configuration file.

    Returns
    -------
    Dict[str, Any]
        Parsed and validated configuration data.

    Raises
    ------
    ConfigError
        If the file does not exist, cannot be read, contains invalid JSON,
        or is missing required fields.
    """

    path = Path(config_path)

    # 1. Check if the file exists
    if not path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        raise ConfigError(f"Configuration file not found: {config_path}")

    # 2. Attempt to read and parse JSON
    try:
        with path.open("r", encoding="utf-8") as f:
            config_data = json.load(f)
        logger.info("Configuration file loaded successfully")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in configuration file: {e}")
        raise ConfigError(f"Invalid JSON format in configuration file: {e}")
    except Exception as e:
        logger.error(f"Unable to read configuration file: {e}")
        raise ConfigError(f"Unable to read configuration file: {e}")

    # 3. Validate root type
    if not isinstance(config_data, dict):
        logger.error("Configuration root must be a JSON object (dictionary)")
        raise ConfigError("Configuration root must be a JSON object (dictionary)")

    # 4. Validate required fields
    if "file_types" not in config_data:
        logger.error("Configuration error: missing required field 'file_types'")
        raise ConfigError("Configuration error: missing required field 'file_types'")

    file_types = config_data["file_types"]

    if not isinstance(file_types, dict):
        logger.error("Configuration error: 'file_types' must be a dictionary")
        raise ConfigError("Configuration error: 'file_types' must be a dictionary")

    # 5. Validate and normalize extensions
    normalized_file_types: Dict[str, list] = {}

    for category, extensions in file_types.items():
        if not isinstance(extensions, list):
            logger.error(
                f"Invalid configuration for category '{category}': "
                "extensions must be provided as a list."
            )
            raise ConfigError(
                f"Invalid configuration for category '{category}': "
                "extensions must be provided as a list."
            )

        normalized_extensions = []

        for ext in extensions:
            if not isinstance(ext, str):
                logger.error(
                    f"Invalid extension in category '{category}': "
                    "extensions must be strings."
                )
                raise ConfigError(
                    f"Invalid extension in category '{category}': "
                    "extensions must be strings."
                )

            if not ext.startswith("."):
                logger.error(
                    f"Invalid extension '{ext}' in category '{category}'. "
                    "Extensions must start with a dot (e.g., '.pdf')."
                )
                raise ConfigError(
                    f"Invalid extension '{ext}' in category '{category}'. "
                    "Extensions must start with a dot (e.g., '.pdf')."
                )

            # Normalize extension (e.g., ".PDF" → ".pdf")
            normalized_extensions.append(ext.lower())

        normalized_file_types[category] = normalized_extensions

    # Replace original with normalized version
    config_data["file_types"] = normalized_file_types

    logger.info("Configuration validated and normalized successfully")

    return config_data
