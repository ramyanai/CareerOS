#!/usr/bin/env python3
"""Extract text from a resume file (PDF, DOCX, or Markdown).

Looks for *_Master_* pattern first in documents/resume/. Falls back to most recent file.
Extracts candidate name from filename and outputs as structured header line.
Prints extracted text to stdout, errors to stderr.
"""

import os
import sys
import glob
import re


RESUME_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "documents", "resume")
SUPPORTED_EXT = {".pdf", ".docx", ".md", ".txt"}


def find_resume(resume_dir):
    """Find the resume file, preferring *_Master_* pattern."""
    all_files = []
    master_files = []
    for ext in SUPPORTED_EXT:
        found = glob.glob(os.path.join(resume_dir, f"*{ext}"))
        all_files.extend(found)
        master_files.extend(f for f in found if "_Master_" in os.path.basename(f))

    if master_files:
        master_files.sort(key=os.path.getmtime, reverse=True)
        if len(master_files) > 1:
            print(f"Warning: {len(master_files)} master resume files found, using most recent", file=sys.stderr)
        return master_files[0]

    if all_files:
        if not master_files:
            print("Warning: No *_Master_* resume found, falling back to most recent file", file=sys.stderr)
        if len(all_files) > 1:
            print(f"Warning: {len(all_files)} resume files found, using most recent", file=sys.stderr)
        all_files.sort(key=os.path.getmtime, reverse=True)
        return all_files[0]

    return None


def extract_name(filename):
    """Extract candidate name from filename.

    Expected pattern: FirstName_LastName_Master_YYYY-MM-DD.ext
    Returns: "FirstName LastName" or None if pattern doesn't match.
    """
    basename = os.path.splitext(os.path.basename(filename))[0]
    match = re.match(r"^(.+?)_Master_", basename)
    if match:
        name_part = match.group(1)
        # Replace underscores with spaces
        return name_part.replace("_", " ")
    return None


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

    # Extract and output candidate name from filename
    name = extract_name(path)
    if name:
        print(f"NAME: {name}")
    else:
        print("Warning: Could not extract name from filename (expected *_Master_* pattern)", file=sys.stderr)

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
