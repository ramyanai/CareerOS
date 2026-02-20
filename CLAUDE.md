# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CareerOS

Job application tailoring workspace. Takes a source resume and a job description, then generates a tailored resume and comprehensive application strategy document — both as markdown and PDF. Follows LifeOS conventions (Claude CLI custom commands, markdown-first pipeline, fpdf2 PDF generation).

## Project Structure

```
~/CareerOS/
├── CLAUDE.md
├── .gitignore
├── .env                              # Optional: RESEND_API_KEY for email
├── .claude/
│   ├── commands/
│   │   └── apply.md                  # Main /apply command
│   └── settings.local.json           # Project permissions
├── documents/
│   └── resume/                       # User places source resume here (.pdf, .docx, or .md)
├── job-descriptions/                 # Optional: saved JD files for reference
├── output/                           # Generated output, organized by company
│   └── {companyname}/
│       ├── resume_{companyname}_{YYMMDD}.md
│       ├── resume_{companyname}_{YYMMDD}.pdf
│       ├── {companyname}_application_strategy.md
│       └── {companyname}_application_strategy.pdf
├── scripts/
│   ├── read-resume.py                # Extract text from PDF/DOCX/MD resume
│   ├── generate-resume-pdf.py        # Tailored resume markdown → professional PDF
│   ├── generate-strategy-pdf.py      # Strategy doc markdown → styled PDF
│   └── run-apply.sh                  # Orchestration: command → PDFs → open Finder
└── tracker.md                        # Application tracker (markdown table)
```

## Workflow

1. Place your source resume in `documents/resume/` (PDF, DOCX, or Markdown)
2. Run `/apply CompanyName` and paste the job description when prompted
3. Command generates tailored resume and strategy markdown files in `output/{companyname}/`
4. Shell script `run-apply.sh` handles PDF generation and opens the output folder

**Key rule:** Commands write markdown only. Shell scripts handle PDF generation.

## Custom Commands

### `/apply`
Tailor resume and generate application strategy for a target company/role.

```bash
# With company name (will prompt for JD)
/apply Anthropic

# With path to JD file
/apply ~/Downloads/anthropic-swe-jd.txt

# No args (will prompt for both)
/apply
```

## Output Naming

- Resume: `resume_{companyname}_{YYMMDD}.md` / `.pdf`
- Strategy: `{companyname}_application_strategy.md` / `.pdf`
- Company name normalization: lowercase, hyphens replace spaces (e.g., "Goldman Sachs" → `goldman-sachs`)

## Resume Formats Supported

- **PDF**: Extracted via PyMuPDF (`fitz`)
- **DOCX**: Extracted via python-docx
- **Markdown**: Read directly

The `scripts/read-resume.py` script auto-detects the format from files in `documents/resume/`. If multiple files exist, it picks the most recently modified one.

## Application Tracker

`tracker.md` records all applications as a markdown table:

| Date | Company | Role | Status | Resume | Strategy | Notes |
|------|---------|------|--------|--------|----------|-------|

Updated automatically by `/apply`. Edit manually to update status.

## Python Dependencies

```
fpdf2          # PDF generation (native rendering)
PyMuPDF        # PDF text extraction (import fitz)
python-docx    # DOCX text extraction
markdown       # Markdown → HTML conversion (strategy PDF)
```

### Setup

```bash
pip3 install python-docx
```

All other dependencies (fpdf2, PyMuPDF, markdown) should already be installed. If not:
```bash
pip3 install fpdf2 PyMuPDF markdown
```

## Development Commands

```bash
# Extract resume text
python3 scripts/read-resume.py

# Generate PDFs standalone
python3 scripts/generate-resume-pdf.py output/companyname/resume_companyname_260220.md
python3 scripts/generate-strategy-pdf.py output/companyname/companyname_application_strategy.md

# Full pipeline
bash scripts/run-apply.sh "CompanyName"
```
