# Smart File Organizer Pro

Professional Python automation tool that organizes files automatically based on file type, reducing manual work and improving workflow efficiency.

## Overview

Smart File Organizer Pro is a Python-based automation utility designed to organize files into structured folders automatically.

The application analyzes file extensions, creates category folders, safely moves files, prevents accidental overwriting, and provides a command-line interface for efficient usage.

The project was built with a focus on clean architecture, maintainable code, and practical real-world automation.

## Features

* Automatic file organization by extension
* Configurable file categories through JSON configuration
* Safe file moving with duplicate name protection
* Dry-run mode for previewing actions
* Command-line interface (CLI)
* File statistics after processing
* Modular Python architecture

## Project Structure

```text
Smart-File-Organizer-Pro/

├── config/
│   └── config.json

├── src/
│   ├── main.py
│   ├── organizer.py
│   └── config_loader.py

└── README.md
```

## Technologies

* Python 3.14
* pathlib
* shutil
* argparse
* json

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Smart-File-Organizer-Pro.git
```

Navigate into the project folder:

```bash
cd Smart-File-Organizer-Pro
```

## Usage

Run the application:

```bash
python src/main.py --folder "PATH_TO_FOLDER"
```

Example:

```bash
python src/main.py --folder "C:\Users\User\Desktop\Test_Files"
```

## Preview Mode

Before moving files, you can test the operation safely:

```bash
python src/main.py --folder "PATH_TO_FOLDER" --dry-run
```

Example output:

```text
[DRY-RUN] photo.jpg -> images/
[DRY-RUN] document.pdf -> documents/
```

## Configuration

File categories can be customized in:

```text
config/config.json
```

Example:

```json
{
    "file_types": {
        "images": [".jpg", ".png"],
        "documents": [".pdf", ".txt"]
    }
}
```

## Example Result

Before:

```text
Test_Files/

photo.jpg
report.pdf
music.mp3
```

After:

```text
Test_Files/

images/
 └── photo.jpg

documents/
 └── report.pdf

audio/
 └── music.mp3
```

## Development Goals

Future improvements:

* Logging system
* File analysis reports
* Graphical user interface
* Automated testing
* Advanced duplicate detection

## Author

Python Automation Developer

Focused on building practical automation tools, data processing solutions, and productivity software.
