#!/usr/bin/env python3
"""Convert tailored resume markdown to a professional ATS-friendly PDF.

Portrait orientation, letter size, simple top-down layout.
Uses fpdf2 native rendering (cell/multi_cell), not write_html().

Usage: generate-resume-pdf.py <resume.md>
"""

import re
import sys
import os

from fpdf import FPDF

FONT_DIR = "/System/Library/Fonts/Supplemental"

# Colors
NAVY = (30, 58, 95)
DARK_TEXT = (15, 23, 42)
GRAY_TEXT = (100, 116, 139)
BODY_TEXT = (51, 65, 85)


def clean(text):
    """Strip markdown bold/italic markers."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", text)
    return text.strip()


class ResumePDF(FPDF):

    def header(self):
        pass  # No header on resume

    def footer(self):
        pass  # No footer on resume — clean ATS layout


def parse_resume(md):
    """Parse resume markdown into structured sections."""
    lines = md.split("\n")
    sections = []
    current_section = None
    current_subsection = None
    name = None
    contact = None

    for line in lines:
        stripped = line.strip()

        # Top-level heading = name
        if stripped.startswith("# ") and not stripped.startswith("## "):
            name = clean(stripped[2:])
            continue

        # Contact line (usually right after name, contains | or @ or phone patterns)
        if name and not sections and not stripped.startswith("#") and stripped and (
            "|" in stripped or "@" in stripped or re.search(r"\d{3}[-.]?\d{3}[-.]?\d{4}", stripped)
        ):
            contact = clean(stripped)
            continue

        # Section heading (## )
        if stripped.startswith("## "):
            current_section = {"title": clean(stripped[3:]), "subsections": [], "bullets": [], "text": []}
            current_subsection = None
            sections.append(current_section)
            continue

        # Subsection heading (### )
        if stripped.startswith("### ") and current_section is not None:
            current_subsection = {"title": clean(stripped[4:]), "bullets": [], "text": []}
            current_section["subsections"].append(current_subsection)
            continue

        # Bullet point
        if (stripped.startswith("- ") or stripped.startswith("* ")) and current_section is not None:
            bullet_text = clean(stripped[2:])
            if current_subsection is not None:
                current_subsection["bullets"].append(bullet_text)
            else:
                current_section["bullets"].append(bullet_text)
            continue

        # Regular text
        if stripped and current_section is not None:
            if current_subsection is not None:
                current_subsection["text"].append(clean(stripped))
            else:
                current_section["text"].append(clean(stripped))

    return name, contact, sections


def main():
    if len(sys.argv) < 2:
        print("Usage: generate-resume-pdf.py <resume.md>")
        sys.exit(1)

    md_path = sys.argv[1]
    if not os.path.exists(md_path):
        print(f"File not found: {md_path}")
        sys.exit(1)

    with open(md_path) as f:
        md = f.read()

    name, contact, sections = parse_resume(md)

    pdf = ResumePDF(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("Arial", "", os.path.join(FONT_DIR, "Arial.ttf"))
    pdf.add_font("Arial", "B", os.path.join(FONT_DIR, "Arial Bold.ttf"))
    pdf.add_font("Arial", "I", os.path.join(FONT_DIR, "Arial Italic.ttf"))
    pdf.add_font("Arial", "BI", os.path.join(FONT_DIR, "Arial Bold Italic.ttf"))

    pdf.add_page()
    usable = pdf.w - pdf.l_margin - pdf.r_margin

    # Name
    if name:
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(*DARK_TEXT)
        pdf.cell(0, 8, name, align="C")
        pdf.ln(7)

    # Contact line
    if contact:
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(*GRAY_TEXT)
        pdf.cell(0, 5, contact, align="C")
        pdf.ln(6)

    # Sections
    for section in sections:
        # Section heading with underline rule
        pdf.ln(2)
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(*NAVY)
        pdf.cell(0, 6, section["title"])
        pdf.ln(1)
        pdf.set_draw_color(*NAVY)
        pdf.set_line_width(0.3)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + usable, pdf.get_y())
        pdf.ln(3)

        # Section-level text
        for text in section["text"]:
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(*BODY_TEXT)
            pdf.multi_cell(usable, 4.5, text)
            pdf.ln(1)

        # Section-level bullets
        for bullet in section["bullets"]:
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(*BODY_TEXT)
            pdf.set_x(pdf.l_margin + 3)
            pdf.cell(4, 4.5, "-")
            pdf.multi_cell(usable - 7, 4.5, bullet)

        # Subsections (e.g., job titles under Experience)
        for sub in section["subsections"]:
            pdf.ln(1)
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(*DARK_TEXT)
            pdf.cell(0, 5, sub["title"])
            pdf.ln()

            for text in sub["text"]:
                pdf.set_font("Arial", "I", 9)
                pdf.set_text_color(*GRAY_TEXT)
                pdf.multi_cell(usable, 4.5, text)

            for bullet in sub["bullets"]:
                pdf.set_font("Arial", "", 9)
                pdf.set_text_color(*BODY_TEXT)
                pdf.set_x(pdf.l_margin + 3)
                pdf.cell(4, 4.5, "-")
                pdf.multi_cell(usable - 7, 4.5, bullet)

    # Output
    pdf_path = md_path.replace(".md", ".pdf")
    pdf.output(pdf_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
