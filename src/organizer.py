from pathlib import Path
import shutil
from typing import Dict, Any, Union


def get_category(extension: str, file_types: Dict[str, list]) -> str:
    """
    Determine the category of a file based on its extension.

    Parameters
    ----------
    extension : str
        The file extension (e.g., '.pdf', '.jpg').
    file_types : Dict[str, list]
        Mapping of categories to lists of extensions from the configuration.

    Returns
    -------
    str
        The category name if found, otherwise 'others'.
    """
    for category, extensions in file_types.items():
        if extension in extensions:
            return category
    return "others"


def safe_move_file(source: Path, target: Path) -> Path:
    """
    Move a file to the target path safely.

    If a file with the same name already exists at the target location,
    this function will append a numeric suffix to the filename to avoid overwriting.

    Example:
        report.pdf      -> report_1.pdf
        report_1.pdf    -> report_2.pdf

    Parameters
    ----------
    source : Path
        The original file path.
    target : Path
        The desired target file path.

    Returns
    -------
    Path
        The final target path where the file was moved.
    """
    if not target.exists():
        shutil.move(str(source), str(target))
        return target

    stem = target.stem
    suffix = target.suffix
    parent = target.parent

    counter = 1
    new_target = parent / f"{stem}_{counter}{suffix}"

    while new_target.exists():
        counter += 1
        new_target = parent / f"{stem}_{counter}{suffix}"

    shutil.move(str(source), str(new_target))
    return new_target


def organize_files(
    source_folder: Union[str, Path],
    config: Dict[str, Any],
    dry_run: bool = False
) -> Dict[str, int]:
    """
    Organize files in the given folder based on the configuration.

    Files are categorized by extension, moved into corresponding subfolders,
    and a statistics dictionary is returned.

    Parameters
    ----------
    source_folder : Union[str, Path]
        Path to the folder that should be organized.
    config : Dict[str, Any]
        Configuration data loaded via config_loader.load_config().
        Expected to contain a 'file_types' dictionary.
    dry_run : bool, optional
        If True, no files are actually moved; actions are only simulated.

    Returns
    -------
    Dict[str, int]
        A dictionary containing counts of files per category.

    Raises
    ------
    FileNotFoundError
        If the source folder does not exist.
    """

    source_path = Path(source_folder)

    if not source_path.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source_folder}")

    file_types = config.get("file_types", {})
    stats: Dict[str, int] = {category: 0 for category in file_types.keys()}
    stats["others"] = 0

    for item in source_path.iterdir():
        if not item.is_file():
            continue

        extension = item.suffix.lower()
        category = get_category(extension, file_types)

        target_folder = source_path / category
        target_folder.mkdir(exist_ok=True)

        target_path = target_folder / item.name

        if dry_run:
            print(f"[DRY-RUN] {item.name} -> {category}/")
            stats[category] += 1
            continue

        try:
            final_path = safe_move_file(item, target_path)
            print(f"Moved: {item.name} -> {final_path}")
            stats[category] += 1
        except Exception as error:
            print(f"Failed to move {item.name}: {error}")

    return stats
