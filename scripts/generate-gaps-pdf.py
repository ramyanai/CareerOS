#!/usr/bin/env python3
"""Convert skills gap report markdown to a color-coded PDF.

Portrait orientation, letter size. Color-codes the keyword matrix:
  green  = Strength (consistently matched)
  yellow = Addressed (reframed/partial)
  red    = Gap (missing from experience)
  gray   = N/A (keyword not in that JD)

Usage: generate-gaps-pdf.py <gaps_report.md>
"""

import re
import sys
import os

import markdown
from fpdf import FPDF

FONT_DIR = "/System/Library/Fonts/Supplemental"

# Row/cell background colors
COLOR_GREEN = "#dcfce7"   # Strength
COLOR_YELLOW = "#fef9c3"  # Addressed
COLOR_RED = "#fee2e2"     # Gap
COLOR_GRAY = "#f1f5f9"    # N/A


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


def classify_cell(text):
    """Classify a cell value in the keyword matrix."""
    lower = text.lower().strip()
    if lower == "n/a" or lower == "—" or lower == "-" or lower == "":
        return "gray"
    if lower in ("strength", "yes", "already present"):
        return "green"
    if lower in ("gap", "no", "cannot add"):
        return "red"
    if lower in ("addressed", "partial", "reframed", "added"):
        return "yellow"
    # Heuristic fallback
    if "strength" in lower or "yes" in lower:
        return "green"
    if "gap" in lower or "no" in lower or "cannot" in lower or "not in" in lower:
        return "red"
    if "n/a" in lower:
        return "gray"
    return "yellow"


def color_gap_tables(html):
    """Inject background colors into gap report tables.

    Colors the Priority Gaps table rows red, Strengths green,
    and the Full Keyword Matrix cells by classification.
    """
    table_pattern = re.compile(r"(<table>)(.*?)(</table>)", re.DOTALL)

    def process_table(match):
        table_start = match.group(1)
        table_content = match.group(2)
        table_end = match.group(3)

        # Detect which table this is by checking headers
        header_text = table_content.lower()

        is_strengths = "matched in" in header_text and "times" in header_text
        is_gaps = "gap in" in header_text and ("frequency" in header_text or "suggested" in header_text)
        is_addressed = "addressed in" in header_text and "how" in header_text
        is_matrix = not is_strengths and not is_gaps and not is_addressed

        row_pattern = re.compile(r"(<tr>)(.*?)(</tr>)", re.DOTALL)
        rows = list(row_pattern.finditer(table_content))

        new_content = table_content
        for row_match in reversed(rows):
            row_html = row_match.group(2)

            # Skip header rows
            if "<th>" in row_html or "<th " in row_html:
                continue

            cells = re.findall(r"<td[^>]*>(.*?)</td>", row_html, re.DOTALL)

            if is_strengths and cells:
                bg = COLOR_GREEN
            elif is_gaps and cells:
                bg = COLOR_RED
            elif is_addressed and cells:
                bg = COLOR_YELLOW
            elif is_matrix and len(cells) >= 2:
                # Color each cell individually based on its value
                colored_cells = []
                for i, cell_content in enumerate(cells):
                    if i == 0:
                        # First column is the skill name — no color
                        colored_cells.append(f"<td>{cell_content}</td>")
                    else:
                        cell_class = classify_cell(cell_content)
                        if cell_class == "green":
                            bg_cell = COLOR_GREEN
                        elif cell_class == "red":
                            bg_cell = COLOR_RED
                        elif cell_class == "gray":
                            bg_cell = COLOR_GRAY
                        else:
                            bg_cell = COLOR_YELLOW
                        colored_cells.append(
                            f'<td style="background-color: {bg_cell};">{cell_content}</td>'
                        )

                new_row = f"<tr>{''.join(colored_cells)}</tr>"
                start = row_match.start()
                end = row_match.end()
                new_content = new_content[:start] + new_row + new_content[end:]
                continue
            else:
                continue

            colored_row = f'<tr style="background-color: {bg};">{row_html}</tr>'
            start = row_match.start()
            end = row_match.end()
            new_content = new_content[:start] + colored_row + new_content[end:]

        return table_start + new_content + table_end

    return table_pattern.sub(process_table, html)


class GapsPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, "CareerOS \u2014 Skills Gap Report", align="R")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def main():
    if len(sys.argv) < 2:
        print("Usage: generate-gaps-pdf.py <gaps_report.md>")
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

    # Color-code gap tables
    html_body = color_gap_tables(html_body)

    # Style headings with navy blue
    html_body = re.sub(
        r"<(h[1-3])>",
        r'<\1 style="color: #1e3a5f;">',
        html_body,
    )

    pdf = GapsPDF(orientation="P", unit="mm", format="letter")
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
