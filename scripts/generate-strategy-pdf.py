#!/usr/bin/env python3
"""Convert application strategy markdown to a styled PDF.

Portrait orientation, letter size. Uses markdown → HTML → write_html()
for rich content (tables, formatted text). Pattern follows LifeOS tax-review PDF.

Usage: generate-strategy-pdf.py <strategy.md>
"""

import re
import sys
import os

import markdown
from fpdf import FPDF

FONT_DIR = "/System/Library/Fonts/Supplemental"


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
