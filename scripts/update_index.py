#!/usr/bin/env python3
"""
Regenerates index.html from the HTML files in noticias/ (daily news) and
pasado/ (weekly "Noticias del pasado" digests).

Usage:
    python scripts/update_index.py

Run this script after adding new date files to noticias/ or pasado/.
"""

import os
import re
from pathlib import Path

MONTHS_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Noticias de Minerva's owl</title>
    <style>
        :root {{
            --bg-color: #ffffff;
            --text-color: #1a1a1a;
            --link-color: #0066cc;
            --link-hover: #004499;
            --border-color: #e0e0e0;
            --card-bg: #f8f8f8;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-color: #1a1a1a;
                --text-color: #e8e8e8;
                --link-color: #66b3ff;
                --link-hover: #99ccff;
                --border-color: #333333;
                --card-bg: #252525;
            }}
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 1rem;
            padding-bottom: env(safe-area-inset-bottom, 1rem);
            min-height: 100vh;
            -webkit-text-size-adjust: 100%;
        }}

        header {{
            text-align: center;
            padding: 2rem 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem;
        }}

        h1 {{
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            font-size: 0.9rem;
            opacity: 0.7;
        }}

        .news-list {{
            list-style: none;
            max-width: 600px;
            margin: 0 auto;
        }}

        .news-list li {{
            margin-bottom: 0.75rem;
        }}

        .news-list a {{
            display: block;
            padding: 1rem;
            background-color: var(--card-bg);
            border-radius: 8px;
            color: var(--link-color);
            text-decoration: none;
            font-size: 1.1rem;
            transition: transform 0.15s ease, background-color 0.15s ease;
            -webkit-tap-highlight-color: transparent;
        }}

        .news-list a:hover,
        .news-list a:focus {{
            color: var(--link-hover);
            transform: translateX(4px);
        }}

        .news-list a:active {{
            transform: scale(0.98);
        }}

        .list-title {{
            max-width: 600px;
            margin: 2.5rem auto 1rem;
            font-size: 1.25rem;
            font-weight: 600;
        }}

        .list-title:first-child {{
            margin-top: 0;
        }}

        .date-label {{
            font-weight: 500;
        }}

        footer {{
            text-align: center;
            padding: 2rem 0;
            margin-top: 2rem;
            border-top: 1px solid var(--border-color);
            font-size: 0.85rem;
            opacity: 0.6;
        }}

        @media (min-width: 768px) {{
            body {{
                padding: 2rem;
            }}

            h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Noticias de Minerva's owl</h1>
        <p class="subtitle">Resumen diario de noticias</p>
    </header>

    <main>
{sections}
    </main>

    <footer>
        <p>© 2026 Minerva's owl</p>
    </footer>
</body>
</html>
'''


def format_date_spanish(date_str: str) -> str:
    """Convert YYYY-MM-DD to 'D de mes de YYYY' format."""
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if not match:
        return date_str
    year, month, day = match.groups()
    day_num = int(day)
    month_name = MONTHS_ES.get(int(month), month)
    return f"{day_num} de {month_name} de {year}"


def find_news_files(noticias_dir: Path) -> list[str]:
    """Find all YYYY-MM-DD.html files and return dates sorted newest first."""
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.html$")
    dates = []
    if not noticias_dir.is_dir():
        return dates
    for f in noticias_dir.iterdir():
        if f.is_file() and pattern.match(f.name):
            dates.append(f.stem)
    return sorted(dates, reverse=True)


def generate_list_items(dates: list[str], folder: str = "noticias") -> str:
    """Generate HTML list items for all dates in the given folder."""
    items = []
    for date in dates:
        label = format_date_spanish(date)
        item = f'            <li><a href="{folder}/{date}.html"><span class="date-label">{label}</span></a></li>'
        items.append(item)
    return "\n".join(items)


def generate_section(title: str, dates: list[str], folder: str) -> str:
    """One titled list (same .news-list style). The daily list keeps its old
    untitled markup when there are no past digests, so index.html is unchanged."""
    head = f'        <h2 class="list-title">{title}</h2>\n' if title else ""
    return (f"{head}        <ul class=\"news-list\">\n"
            f"{generate_list_items(dates, folder)}\n        </ul>")


def main():
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    noticias_dir = repo_root / "noticias"
    pasado_dir = repo_root / "pasado"
    index_path = repo_root / "index.html"

    if not noticias_dir.is_dir():
        print(f"Error: Directory '{noticias_dir}' not found.")
        return 1

    dates = find_news_files(noticias_dir)
    if not dates:
        print("Warning: No news files found in noticias/")
        return 1

    past_dates = find_news_files(pasado_dir)  # empty if pasado/ is missing

    sections = []
    if past_dates:
        sections.append(generate_section("Noticias del día", dates, "noticias"))
        sections.append(generate_section("Noticias del pasado", past_dates, "pasado"))
    else:
        sections.append(generate_section("", dates, "noticias"))
    html = INDEX_TEMPLATE.format(sections="\n\n".join(sections))

    index_path.write_text(html, encoding="utf-8")
    print(f"Updated {index_path} with {len(dates)} news entries"
          f" and {len(past_dates)} past-news entries.")
    return 0


if __name__ == "__main__":
    exit(main())
