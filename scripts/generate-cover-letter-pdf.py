#!/usr/bin/env python3
"""Extract cover letter from strategy markdown and render as professional PDF.

Parses Section 2 (Cover Letter Draft) from strategy document.
Renders as a letter-format PDF with navy color scheme matching resume.

Usage: generate-cover-letter-pdf.py <strategy.md>
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


def extract_cover_letter(md_content):
    """Extract cover letter section from strategy markdown.

    Returns dict with keys: opening, body, close, candidate_name
    """
    lines = md_content.split("\n")
    in_cover_letter = False
    in_subsection = None
    sections = {"opening": [], "body": [], "close": []}
    candidate_name = None

    for line in lines:
        stripped = line.strip()

        # Detect start of cover letter section
        if re.match(r"^##\s+2\.\s+Cover Letter", stripped):
            in_cover_letter = True
            continue

        # Detect end of cover letter section (next ## section)
        if in_cover_letter and re.match(r"^##\s+\d+\.", stripped):
            break

        if not in_cover_letter:
            continue

        # Subsection headers
        if stripped.lower().startswith("### opening"):
            in_subsection = "opening"
            continue
        elif stripped.lower().startswith("### body"):
            in_subsection = "body"
            continue
        elif stripped.lower().startswith("### close"):
            in_subsection = "close"
            continue

        # Look for "Signed:" line to extract candidate name
        if stripped.startswith("Signed:"):
            continue
        if candidate_name is None and in_subsection == "close" and stripped and not stripped.startswith("#"):
            # Check if this is a name line (after "Signed:")
            prev_lines = sections["close"]
            if prev_lines and "signed" in md_content.lower():
                # The line after "Signed:" might be the name
                pass

        if in_subsection and stripped:
            sections[in_subsection].append(clean(stripped))

    # Try to extract candidate name from the close section or the document
    # Look for a line that's just a name (after the closing)
    if sections["close"]:
        # Last non-empty line in close is often the name
        for line in reversed(sections["close"]):
            if line and not any(word in line.lower() for word in ["thank", "look forward", "please", "best", "sincerely", "regards", "excited"]):
                candidate_name = line
                sections["close"].remove(line)
                break

    return sections, candidate_name


def extract_contact_from_strategy(md_content):
    """Try to extract contact info and candidate name from strategy title."""
    title_match = re.search(r"^#\s+Application Strategy:\s*(.+?)\s*[-\u2014]\s*(.+)", md_content, re.MULTILINE)
    company = title_match.group(1).strip() if title_match else ""
    role = title_match.group(2).strip() if title_match else ""
    return company, role


class CoverLetterPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass


def main():
    if len(sys.argv) < 2:
        print("Usage: generate-cover-letter-pdf.py <strategy.md>")
        sys.exit(1)

    md_path = sys.argv[1]
    if not os.path.exists(md_path):
        print(f"File not found: {md_path}")
        sys.exit(1)

    with open(md_path, "r") as f:
        md_content = f.read()

    sections, candidate_name = extract_cover_letter(md_content)
    company, role = extract_contact_from_strategy(md_content)

    if not any(sections.values()):
        print("Error: No cover letter section found in strategy document", file=sys.stderr)
        sys.exit(1)

    # Try to find resume in same directory for contact info
    strategy_dir = os.path.dirname(md_path)
    resume_files = [f for f in os.listdir(strategy_dir)
                    if f.endswith(".md") and "Strategy" not in f and "Changes" not in f and "CoverLetter" not in f]

    contact_line = None
    if resume_files:
        resume_path = os.path.join(strategy_dir, sorted(resume_files)[0])
        with open(resume_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    if not candidate_name:
                        candidate_name = clean(line[2:])
                elif "|" in line and ("@" in line or re.search(r"\d{3}", line)):
                    contact_line = clean(line)
                    break

    pdf = CoverLetterPDF(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_font("Arial", "", os.path.join(FONT_DIR, "Arial.ttf"))
    pdf.add_font("Arial", "B", os.path.join(FONT_DIR, "Arial Bold.ttf"))
    pdf.add_font("Arial", "I", os.path.join(FONT_DIR, "Arial Italic.ttf"))
    pdf.add_font("Arial", "BI", os.path.join(FONT_DIR, "Arial Bold Italic.ttf"))

    pdf.add_page()
    usable = pdf.w - pdf.l_margin - pdf.r_margin

    # Candidate name at top
    if candidate_name:
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(*DARK_TEXT)
        pdf.cell(0, 8, candidate_name, align="C")
        pdf.ln(7)

    # Contact line
    if contact_line:
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(*GRAY_TEXT)
        pdf.cell(0, 5, contact_line, align="C")
        pdf.ln(6)

    # Horizontal rule
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + usable, pdf.get_y())
    pdf.ln(8)

    # Date
    from datetime import date
    today = date.today().strftime("%B %d, %Y")
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*BODY_TEXT)
    pdf.cell(0, 5, today)
    pdf.ln(8)

    # Salutation
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*DARK_TEXT)
    pdf.cell(0, 5, "Dear Hiring Team,")
    pdf.ln(8)

    # Body paragraphs
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*BODY_TEXT)

    for section_name in ["opening", "body", "close"]:
        paragraphs = sections[section_name]
        for para in paragraphs:
            pdf.multi_cell(usable, 5, para)
            pdf.ln(3)

    # Sign-off
    pdf.ln(4)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*DARK_TEXT)
    pdf.cell(0, 5, "Sincerely,")
    pdf.ln(8)

    if candidate_name:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 5, candidate_name)

    # Determine output path
    # Replace _Strategy_ with _CoverLetter_ in filename, keep .pdf
    base = os.path.basename(md_path)
    if "_Strategy_" in base:
        out_name = base.replace("_Strategy_", "_CoverLetter_").replace(".md", ".pdf")
    else:
        out_name = base.replace("_application_strategy", "_CoverLetter").replace(".md", ".pdf")

    pdf_path = os.path.join(strategy_dir, out_name)
    pdf.output(pdf_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
