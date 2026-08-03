# Smart File Organizer Pro

A modular Python automation tool for intelligent file organization, folder analysis, and report generation.

The application scans folders, classifies files, organizes them into categories, and generates structured reports in multiple formats.

The project is designed with a modular architecture to support future extensions, including dashboard and GUI integration.

---

## Features

### File Organization

The application automatically organizes files based on their type.

Supported categories:

- Images
- Documents
- Videos
- Audio files
- Archives
- Other files

---

## Reporting System

The reporting system is built around a shared ReportData model.

Supported output formats:

- TXT reports
- JSON reports
- HTML dashboard reports

The same data model is used for every format, ensuring consistency between outputs.

---

## HTML Dashboard

Version 1.6.0 introduces a professional HTML dashboard.

Features:

- Embedded CSS styling
- Statistics cards
- Pre-scan analysis
- Post-organization comparison
- Category distribution tables
- Human-readable file sizes
- Large file overview

The generated HTML report is completely standalone and can be opened directly in any browser.

---

## Architecture

The project follows a modular structure:

Smart-File-Organizer-Pro/

├── src/
│   ├── main.py
│   ├── organizer.py
│   ├── config_loader.py
│   └── utils/
│       ├── scanner.py
│       ├── report.py
│       └── logger.py

├── config/
│   └── config.json

├── reports/

└── README.md

---

## Core Components

### ReportData

Central data model containing:

- source folder information
- organization statistics
- scanner results
- timestamps

### ReportFormatter

Responsible for converting report data into:

- TXT format
- JSON format
- HTML format

### ReportWriter

Handles saving generated reports to disk.

Supported files:

- .txt
- .json
- .html

### ScannerEngine

Analyzes folders before organization:

- file count
- total size
- category distribution
- large files

---

## Installation

Clone the repository:

git clone https://github.com/xTRAPPx/Smart-File-Organizer-Pro.git

Install requirements if available:

pip install -r requirements.txt

---

## Usage

Run:

python src/main.py --folder "path/to/folder"

The application will generate reports in the reports directory.

Example output:

reports/

- report_timestamp.txt
- report_timestamp.json
- report_timestamp.html

---

## Testing

Syntax validation:

python -m py_compile src/main.py

python -m py_compile src/utils/report.py

The application has been tested with:

- sample folders
- multiple file categories
- report generation
- HTML dashboard output

---

## Roadmap

### Version 1.6.0

Completed:

- HTML dashboard
- embedded styling
- report comparison tables
- improved size formatting

### Version 1.7.0

Planned:

- charts
- data visualization
- report analytics

### Version 2.0.0

Planned:

- GUI dashboard
- interactive interface
- advanced file management

---

## Project Goals

The goal of Smart File Organizer Pro is to provide a maintainable automation tool with:

- clean architecture
- modular design
- extensible reporting
- future GUI compatibility

---

## Development Notes

Technologies used:

- Python
- Object-oriented programming
- Modular architecture
- Git version control

The project structure allows new features to be added without major changes to existing components.

---

## License

This project is currently intended for educational and portfolio purposes.