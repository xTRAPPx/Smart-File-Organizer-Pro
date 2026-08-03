from pathlib import Path
import shutil
from typing import Dict, Any, Union

from utils.logger import get_logger

logger = get_logger("Organizer")


def get_category(extension: str, file_types: Dict[str, list]) -> str:
    """
    Determine the category of a file based on its extension.

    Parameters
    ----------
    extension : str
        File extension (e.g., '.pdf').
    file_types : Dict[str, list]
        Mapping of categories to lists of extensions.

    Returns
    -------
    str
        Category name or 'others' if unknown.
    """
    for category, extensions in file_types.items():
        if extension in extensions:
            logger.info(f"Extension '{extension}' categorized as '{category}'")
            return category

    logger.warning(f"Unknown extension '{extension}' categorized as 'others'")
    return "others"


def safe_move_file(source: Path, target: Path) -> Path:
    """
    Move a file to the target path safely.

    If a file with the same name already exists, append a numeric suffix.

    Parameters
    ----------
    source : Path
        Original file path.
    target : Path
        Desired target file path.

    Returns
    -------
    Path
        Final target path where the file was moved.
    """
    if not target.exists():
        shutil.move(str(source), str(target))
        logger.info(f"Moved file: {source.name} -> {target}")
        return target

    # Duplicate handling
    stem = target.stem
    suffix = target.suffix
    parent = target.parent

    counter = 1
    new_target = parent / f"{stem}_{counter}{suffix}"

    while new_target.exists():
        counter += 1
        new_target = parent / f"{stem}_{counter}{suffix}"

    shutil.move(str(source), str(new_target))
    logger.warning(
        f"Duplicate detected. Renamed and moved: {source.name} -> {new_target}"
    )
    return new_target


def organize_files(
    source_folder: Union[str, Path],
    config: Dict[str, Any],
    dry_run: bool = False
) -> Dict[str, int]:
    """
    Organize files in the given folder based on the configuration.

    Parameters
    ----------
    source_folder : Union[str, Path]
        Folder to organize.
    config : Dict[str, Any]
        Configuration dictionary.
    dry_run : bool
        If True, simulate actions without moving files.

    Returns
    -------
    Dict[str, int]
        Statistics of processed files per category.
    """
    source_path = Path(source_folder)

    if not source_path.exists():
        logger.error(f"Source folder does not exist: {source_folder}")
        raise FileNotFoundError(f"Source folder does not exist: {source_folder}")

    logger.info(f"Starting organization in folder: {source_path}")

    file_types = config.get("file_types", {})
    stats: Dict[str, int] = {category: 0 for category in file_types.keys()}
    stats["others"] = 0

    for item in source_path.iterdir():
        if not item.is_file():
            logger.warning(f"Skipping non-file item: {item.name}")
            continue

        extension = item.suffix.lower()
        category = get_category(extension, file_types)

        target_folder = source_path / category
        target_folder.mkdir(exist_ok=True)

        target_path = target_folder / item.name

        if dry_run:
            logger.info(f"[DRY-RUN] {item.name} -> {category}/")
            stats[category] += 1
            continue

        try:
            safe_move_file(item, target_path)
            stats[category] += 1
        except Exception as error:
            logger.error(f"Failed to move {item.name}: {error}")

    logger.info(f"Organization completed. Stats: {stats}")
    return stats
