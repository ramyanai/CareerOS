#!/usr/bin/env python3
"""Extract text from a resume file (PDF, DOCX, or Markdown).

Auto-detects the most recent file in documents/resume/ or accepts a path as argument.
Prints extracted text to stdout, errors to stderr.
"""

import os
import sys
import glob


RESUME_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "documents", "resume")
SUPPORTED_EXT = {".pdf", ".docx", ".md", ".txt"}


def find_resume(resume_dir):
    """Find the most recently modified resume file."""
    files = []
    for ext in SUPPORTED_EXT:
        files.extend(glob.glob(os.path.join(resume_dir, f"*{ext}")))
    if not files:
        return None
    if len(files) > 1:
        print(f"Warning: {len(files)} resume files found, using most recent", file=sys.stderr)
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]


def extract_pdf(path):
    """Extract text from PDF using PyMuPDF."""
    import fitz
    doc = fitz.open(path)
    text = []
    for page in doc:
        text.append(page.get_text())
    doc.close()
    return "\n".join(text)


def extract_docx(path):
    """Extract text from DOCX using python-docx."""
    from docx import Document
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_md(path):
    """Read markdown/text file directly."""
    with open(path, "r") as f:
        return f.read()


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(f"Error: File not found: {path}", file=sys.stderr)
            sys.exit(1)
    else:
        path = find_resume(RESUME_DIR)
        if not path:
            print(f"Error: No resume found in {RESUME_DIR}", file=sys.stderr)
            print("Place a .pdf, .docx, or .md file in documents/resume/", file=sys.stderr)
            sys.exit(1)

    print(f"Reading: {os.path.basename(path)}", file=sys.stderr)
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        text = extract_pdf(path)
    elif ext == ".docx":
        text = extract_docx(path)
    elif ext in (".md", ".txt"):
        text = extract_md(path)
    else:
        print(f"Error: Unsupported format: {ext}", file=sys.stderr)
        sys.exit(1)

    print(text)


if __name__ == "__main__":
    main()
