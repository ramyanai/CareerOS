#!/usr/bin/env python3
"""Convert change log markdown to a styled PDF.

Portrait orientation, letter size. Uses markdown -> HTML -> write_html()
for rich content (tables, formatted text). Includes color-coded change
type columns and verification status highlighting.

Usage: generate-changelog-pdf.py <changes.md>
"""

import re
import sys
import os

import markdown
from fpdf import FPDF

FONT_DIR = "/System/Library/Fonts/Supplemental"

# Row background colors
COLOR_GREEN = "#dcfce7"   # Unchanged / Kept / PASS
COLOR_YELLOW = "#fef9c3"  # Reworded / Added / Consolidated
COLOR_BLUE = "#dbeafe"    # Reordered
COLOR_RED = "#fee2e2"     # Gap


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


def classify_change_type(cell_text):
    """Classify a change log row by its Change Type or Status value."""
    lower = cell_text.lower().strip()
    if "unchanged" in lower or "kept" in lower:
        return "green"
    if "reordered" in lower:
        return "blue"
    if any(k in lower for k in ("reworded", "reframed", "added", "consolidated")):
        return "yellow"
    if "gap" in lower:
        return "red"
    return "yellow"


COLOR_MAP = {
    "green": COLOR_GREEN,
    "yellow": COLOR_YELLOW,
    "blue": COLOR_BLUE,
    "red": COLOR_RED,
}


def color_change_tables(html):
    """Inject background colors into change log table rows.

    Colors rows based on:
    - 'Change Type' column (index 2) in section change tables
    - 'Status' column (index 1) in skills tables
    """
    table_pattern = re.compile(r"(<table>)(.*?)(</table>)", re.DOTALL)

    def process_table(match):
        table_start = match.group(1)
        table_content = match.group(2)
        table_end = match.group(3)

        header_lower = table_content.lower()
        if "change type" in header_lower:
            color_col = 2
        elif "status" in header_lower:
            color_col = 1
        else:
            return match.group(0)

        row_pattern = re.compile(r"(<tr>)(.*?)(</tr>)", re.DOTALL)
        rows = list(row_pattern.finditer(table_content))

        new_content = table_content
        for row_match in reversed(rows):
            row_html = row_match.group(2)

            if "<th>" in row_html or "<th " in row_html:
                continue

            cells = re.findall(r"<td[^>]*>(.*?)</td>", row_html, re.DOTALL)
            if len(cells) > color_col:
                color_class = classify_change_type(cells[color_col])
                bg = COLOR_MAP[color_class]

                # Apply bgcolor attribute to each <td> (fpdf2-compatible)
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


def color_verification_notes(html):
    """Highlight PASS in green and FAIL in red within verification notes."""
    html = html.replace(
        "PASS",
        '<span style="color: #16a34a;"><b>PASS</b></span>',
    )
    html = html.replace(
        "FAIL",
        '<span style="color: #dc2626;"><b>FAIL</b></span>',
    )
    return html


class ChangeLogPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, "CareerOS \u2014 Change Log", align="R")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def main():
    if len(sys.argv) < 2:
        print("Usage: generate-changelog-pdf.py <changes.md>")
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

    html_body = strip_tags_in_cells(html_body)
    html_body = color_change_tables(html_body)
    html_body = color_verification_notes(html_body)

    # Style headings with navy blue
    html_body = re.sub(
        r"<(h[1-3])>",
        r'<\1 style="color: #1e3a5f;">',
        html_body,
    )

    pdf = ChangeLogPDF(orientation="P", unit="mm", format="letter")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

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
