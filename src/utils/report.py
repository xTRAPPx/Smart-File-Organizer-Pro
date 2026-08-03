from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import json

from utils.logger import get_logger
from utils.scanner import ScannerData

logger = get_logger("Report")


class ReportData:
    """
    Data model for storing report information.

    Supports:
    - post-organization statistics
    - pre-scan analysis results
    """

    def __init__(
        self,
        source_folder: str,
        stats: Dict[str, int],
        scan_data: Optional[ScannerData] = None
    ) -> None:

        self.source_folder = source_folder
        self.stats = stats
        self.total_files = sum(stats.values())
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.scan_data = scan_data

        logger.info(
            f"ReportData created for '{self.source_folder}' "
            f"with {self.total_files} files "
            f"(scan_data={'yes' if scan_data else 'no'})"
        )


class ReportFormatter:
    """
    Converts ReportData into:

    - TXT
    - JSON
    - HTML Dashboard
    """


    @staticmethod
    def _format_size(size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} bytes"

        kb = size_bytes / 1024

        if kb < 1024:
            return f"{kb:.2f} KB"

        mb = kb / 1024

        if mb < 1024:
            return f"{mb:.2f} MB"

        gb = mb / 1024

        return f"{gb:.2f} GB"


    # -------------------------
    # TXT
    # -------------------------

    @staticmethod
    def to_text(report: ReportData) -> str:

        logger.info("Formatting TXT report")

        lines = [
            "Smart File Organizer Pro - Report",
            "----------------------------------",
            f"Source folder: {report.source_folder}",
            f"Generated at: {report.timestamp}",
        ]


        if report.scan_data:

            sd = report.scan_data

            lines.extend([
                "",
                "=== Pre-scan summary ===",
                f"Total files: {sd.total_files}",
                f"Total size: {sd.total_size_bytes} bytes",
                "",
                "Category distribution:"
            ])

            for category, count in sd.category_distribution.items():
                lines.append(f"- {category}: {count}")


        lines.extend([
            "",
            "=== Post-organization summary ==="
        ])


        for category, count in report.stats.items():
            lines.append(f"- {category}: {count}")


        lines.extend([
            "",
            f"Total files processed: {report.total_files}",
            "----------------------------------"
        ])

        return "\n".join(lines)



    # -------------------------
    # JSON
    # -------------------------

    @staticmethod
    def to_json(report: ReportData) -> Dict[str, Any]:

        logger.info("Formatting JSON report")


        data = {
            "source_folder": report.source_folder,
            "generated_at": report.timestamp,
            "post_organization": {
                "categories": report.stats,
                "total_files_processed": report.total_files
            }
        }


        if report.scan_data:

            sd = report.scan_data

            data["pre_scan"] = {
                "total_files": sd.total_files,
                "total_size_bytes": sd.total_size_bytes,
                "categories": sd.category_distribution,
                "large_files": sd.large_files
            }


        return data



    # -------------------------
    # HTML DASHBOARD v1.6.0
    # -------------------------

    @staticmethod
    def to_html(report: ReportData) -> str:

        logger.info("Formatting HTML Dashboard v1.6.0")


        pre_files = 0
        pre_size = 0
        pre_categories = {}

        large_html = ""


        if report.scan_data:

            sd = report.scan_data

            pre_files = sd.total_files
            pre_size = sd.total_size_bytes
            pre_categories = sd.category_distribution


            if sd.large_files:

                items = ""

                for file in sd.large_files:

                    items += f"""
                    <li>
                        <b>{file['path']}</b><br>
                        Size: {ReportFormatter._format_size(file['size_bytes'])}<br>
                        Category: {file['category']}
                    </li>
                    """


                large_html = f"""
                <div class="section">
                    <h2>Large Files</h2>
                    <ul>
                        {items}
                    </ul>
                </div>
                """



        categories = (
            set(pre_categories.keys())
            |
            set(report.stats.keys())
        )


        rows = ""


        for category in sorted(categories):

            rows += f"""
            <tr>
                <td>{category}</td>
                <td>{pre_categories.get(category,0)}</td>
                <td>{report.stats.get(category,0)}</td>
            </tr>
            """


        html = f"""
<html>
<head>

<meta charset="utf-8">

<title>
Smart File Organizer Pro Dashboard
</title>


<style>

body {{
    font-family: Arial, sans-serif;
    background:#f4f6f8;
    margin:0;
}}

.container {{
    max-width:1000px;
    margin:auto;
    padding:30px;
}}

.header,
.section,
.card {{
    background:white;
    border-radius:10px;
    box-shadow:0 2px 8px #ddd;
}}

.header {{
    padding:20px;
    margin-bottom:25px;
}}

.cards {{
    display:flex;
    gap:20px;
    flex-wrap:wrap;
}}

.card {{
    padding:20px;
    flex:1;
    min-width:220px;
}}

.card-title {{
    color:#666;
}}

.card-value {{
    font-size:28px;
    font-weight:bold;
    margin-top:10px;
}}

.section {{
    padding:20px;
    margin-top:25px;
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th,td {{
    padding:10px;
    border-bottom:1px solid #ddd;
    text-align:left;
}}

th {{
    background:#eee;
}}

tr:nth-child(even) {{
    background:#fafafa;
}}

</style>

</head>


<body>

<div class="container">


<div class="header">

<h1>
Smart File Organizer Pro - Dashboard
</h1>

<p><b>Source:</b> {report.source_folder}</p>

<p><b>Generated:</b> {report.timestamp}</p>

</div>



<div class="cards">


<div class="card">
<div class="card-title">
Pre-scan files
</div>

<div class="card-value">
{pre_files}
</div>
</div>



<div class="card">
<div class="card-title">
Pre-scan size
</div>

<div class="card-value">
{ReportFormatter._format_size(pre_size)}
</div>
</div>



<div class="card">
<div class="card-title">
Processed files
</div>

<div class="card-value">
{report.total_files}
</div>
</div>


</div>



<div class="section">

<h2>
Category Comparison
</h2>


<table>

<tr>
<th>Category</th>
<th>Before</th>
<th>After</th>
</tr>

{rows}

</table>


</div>


{large_html}


</div>

</body>

</html>
"""

        return html.strip()



class ReportWriter:

    def __init__(self, output_dir: str = "reports"):

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def save_text_report(self, text: str) -> Path:

        path = self.output_dir / (
            f"report_{datetime.now():%Y-%m-%d_%H-%M-%S}.txt"
        )

        path.write_text(
            text,
            encoding="utf-8"
        )

        logger.info(f"TXT saved: {path}")

        return path



    def save_json_report(self, data: Dict[str, Any]) -> Path:

        path = self.output_dir / (
            f"report_{datetime.now():%Y-%m-%d_%H-%M-%S}.json"
        )


        with path.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=2
            )


        logger.info(f"JSON saved: {path}")

        return path



    def save_html_report(self, html: str) -> Path:

        path = self.output_dir / (
            f"report_{datetime.now():%Y-%m-%d_%H-%M-%S}.html"
        )


        path.write_text(
            html,
            encoding="utf-8"
        )


        logger.info(f"HTML saved: {path}")

        return path