#!/usr/bin/env python3
"""Convert application strategy markdown to a styled PDF.

Portrait orientation, letter size. Uses markdown -> HTML -> write_html()
for rich content (tables, formatted text). Includes color-coded keyword
gap analysis table and match score summary.

Usage: generate-strategy-pdf.py <strategy.md>
"""

import re
import sys
import os

import markdown
from fpdf import FPDF

FONT_DIR = "/System/Library/Fonts/Supplemental"

# Row background colors for keyword gap table
COLOR_GREEN = "#dcfce7"   # Yes / Already present / HIGH / Excellent
COLOR_YELLOW = "#fef9c3"  # Reframed / Added / Partial / MODERATE
COLOR_ORANGE = "#ffedd5"  # LOW
COLOR_RED = "#fee2e2"     # No / Cannot add / Gap / VERY LOW


def strip_tags_in_cells(html):
    """Remove nested HTML tags from inside <td> and <th> elements,
    since fpdf2 doesn't support them."""
    def clean_cell(match):
        tag = match.group(1)
        attrs = match.group(2) or ""
        content = match.group(3)
        clean = re.sub(r"<[^>]+>", "", content)
        return f"<{tag}{attrs}>{clean}</{tag}>"

    html = re.sub(
        r"<(td|th)((?:\s[^>]*)?)>(.*?)</\1>",
        clean_cell,
        html,
        flags=re.DOTALL,
    )
    return html


def classify_row(cell_text):
    """Classify a keyword gap row by its 'Found in Resume?' value."""
    lower = cell_text.lower().strip()
    if lower in ("yes", "already present"):
        return "green"
    elif lower in ("no", "gap", "cannot add"):
        return "red"
    elif lower in ("partial", "reframed", "added"):
        return "yellow"
    # Heuristic fallback
    if "yes" in lower or "already" in lower or "present" in lower:
        return "green"
    if "no" in lower or "gap" in lower or "cannot" in lower or "not in" in lower:
        return "red"
    return "yellow"


def classify_ats_rating(cell_text):
    """Classify an ATS score row by its Rating value."""
    lower = cell_text.lower().strip()
    if any(k in lower for k in ("excellent", "high", "good")):
        return "green"
    if "moderate" in lower:
        return "yellow"
    if "low" in lower and "very" not in lower:
        return "orange"
    if "very low" in lower:
        return "red"
    return "yellow"


def color_ats_score_table(html):
    """Color-code the ATS Compatibility Assessment table rows."""
    table_pattern = re.compile(r"(<table>)(.*?)(</table>)", re.DOTALL)

    def process_table(match):
        table_start = match.group(1)
        table_content = match.group(2)
        table_end = match.group(3)

        # Only process ATS score tables
        if "ATS Format Score" not in table_content and "Overall ATS" not in table_content:
            return match.group(0)

        row_pattern = re.compile(r"(<tr>)(.*?)(</tr>)", re.DOTALL)
        rows = list(row_pattern.finditer(table_content))

        new_content = table_content
        for row_match in reversed(rows):
            row_html = row_match.group(2)

            if "<th>" in row_html or "<th " in row_html:
                continue

            cells = re.findall(r"<td[^>]*>(.*?)</td>", row_html, re.DOTALL)
            if len(cells) >= 3:
                rating_cell = cells[2]  # Rating is the 3rd column
                color_class = classify_ats_rating(rating_cell)

                bg = {
                    "green": COLOR_GREEN,
                    "yellow": COLOR_YELLOW,
                    "orange": COLOR_ORANGE,
                    "red": COLOR_RED,
                }[color_class]

                colored_html = re.sub(
                    r"<td([^>]*)>",
                    f'<td\\1 bgcolor="{bg}">',
                    row_html,
                )
                colored_row = f"<tr>{colored_html}</tr>"
                start = row_match.start()
                end = row_match.end()
                new_content = new_content[:start] + colored_row + new_content[end:]

        return table_start + new_content + table_end

    return table_pattern.sub(process_table, html)


def color_keyword_gap_table(html):
    """Inject background colors into keyword gap analysis table rows.

    Identifies the keyword gap table by looking for the header containing
    'Found in Resume?' and colors each data row based on the second column value.
    """
    # Find all tables
    table_pattern = re.compile(r"(<table>)(.*?)(</table>)", re.DOTALL)

    def process_table(match):
        table_start = match.group(1)
        table_content = match.group(2)
        table_end = match.group(3)

        # Check if this is the keyword gap table
        if "Found in Resume?" not in table_content and "found in resume" not in table_content.lower():
            return match.group(0)

        # Process each row
        row_pattern = re.compile(r"(<tr>)(.*?)(</tr>)", re.DOTALL)
        rows = list(row_pattern.finditer(table_content))

        new_content = table_content
        for row_match in reversed(rows):  # Reverse to preserve positions
            row_html = row_match.group(2)

            # Skip header rows (contain <th>)
            if "<th>" in row_html or "<th " in row_html:
                continue

            # Extract cells
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row_html, re.DOTALL)
            if len(cells) >= 2:
                status_cell = cells[1]  # "Found in Resume?" is the second column
                color_class = classify_row(status_cell)

                if color_class == "green":
                    bg = COLOR_GREEN
                elif color_class == "red":
                    bg = COLOR_RED
                else:
                    bg = COLOR_YELLOW

                # Replace <tr> with styled <tr>
                colored_row = f'<tr style="background-color: {bg};">{row_html}</tr>'
                start = row_match.start()
                end = row_match.end()
                new_content = new_content[:start] + colored_row + new_content[end:]

        return table_start + new_content + table_end

    return table_pattern.sub(process_table, html)


def inject_match_score_bar(html):
    """Find the match score line and add a colored bar before the table.

    Looks for a line like: **Match Score: 12/15 keywords addressed (80%)**
    and injects a visual bar representation.
    """
    score_pattern = re.compile(
        r"<strong>Match Score:\s*(\d+)/(\d+)\s+keywords?\s+addressed\s*\((\d+)%\)</strong>"
    )

    match = score_pattern.search(html)
    if not match:
        return html

    addressed = int(match.group(1))
    total = int(match.group(2))
    pct = int(match.group(3))

    # Build a colored bar using HTML table (fpdf2 compatible)
    green_width = max(pct, 5)  # Minimum width for visibility
    red_width = 100 - green_width

    bar_html = (
        f'<p><strong>Match Score: {addressed}/{total} keywords addressed ({pct}%)</strong></p>'
        f'<table width="100%"><tr>'
        f'<td width="{green_width}%" style="background-color: {COLOR_GREEN};">&nbsp;</td>'
        f'<td width="{red_width}%" style="background-color: {COLOR_RED};">&nbsp;</td>'
        f'</tr></table><br/>'
    )

    # Replace the original match score line
    original = match.group(0)
    # Find the paragraph containing it
    para_pattern = re.compile(rf"<p>{re.escape(original)}</p>")
    if para_pattern.search(html):
        html = para_pattern.sub(bar_html, html)
    else:
        # Just replace inline
        html = html.replace(original, bar_html)

    return html


class StrategyPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, "CareerOS \u2014 Application Strategy", align="R")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def main():
    if len(sys.argv) < 2:
        print("Usage: generate-strategy-pdf.py <strategy.md>")
        sys.exit(1)

    md_path = sys.argv[1]
    if not os.path.exists(md_path):
        print(f"File not found: {md_path}")
        sys.exit(1)

    with open(md_path, "r") as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "sane_lists"],
    )

    # fpdf2 doesn't support nested tags in table cells
    html_body = strip_tags_in_cells(html_body)

    # Color-code ATS score table rows
    html_body = color_ats_score_table(html_body)

    # Color-code keyword gap table rows
    html_body = color_keyword_gap_table(html_body)

    # Add match score bar
    html_body = inject_match_score_bar(html_body)

    # Style headings with navy blue instead of default red
    html_body = re.sub(
        r"<(h[1-3])>",
        r'<\1 style="color: #1e3a5f;">',
        html_body,
    )

    pdf = StrategyPDF(orientation="P", unit="mm", format="letter")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Register Unicode-capable Arial fonts
    pdf.add_font("Arial", "", os.path.join(FONT_DIR, "Arial.ttf"))
    pdf.add_font("Arial", "B", os.path.join(FONT_DIR, "Arial Bold.ttf"))
    pdf.add_font("Arial", "I", os.path.join(FONT_DIR, "Arial Italic.ttf"))
    pdf.add_font("Arial", "BI", os.path.join(FONT_DIR, "Arial Bold Italic.ttf"))

    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.write_html(html_body)

    pdf_path = md_path.replace(".md", ".pdf")
    pdf.output(pdf_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
