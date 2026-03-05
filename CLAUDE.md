# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Honesty Rule (Non-Negotiable)

**NEVER fabricate personal experiences, stories, or claims.** When writing content in the user's voice (resumes, cover letters, pitches), NEVER invent experiences the user didn't describe. If something needs a personal anecdote, ASK first. Do not embellish, exaggerate, or assume. Honesty over everything — no making things up.

## CareerOS

Job application tailoring workspace. Takes a source resume and a job description, then generates a tailored resume, application strategy, change log, and cover letter — as markdown, PDF, and DOCX. Follows LifeOS conventions (Claude CLI custom commands, markdown-first pipeline, fpdf2/python-docx document generation).

## Anti-Hallucination Guardrails

The `/apply` command enforces strict guardrails:
1. **No new facts** — every company, title, date, degree, metric must exist in the source resume
2. **No new skills from thin air** — must exist in source or be clearly inferable
3. **Reframing only** — change verbs and framing, never add substance
4. **Gaps are gaps** — if a JD keyword can't be mapped, it goes in the gap analysis
5. **Numbers from source only** — never invent metrics
6. **Two-pass verification** — every bullet is verified against the source before saving
7. **Change log** — every modification is documented with original text, new text, and reason

## Project Structure

```
~/CareerOS/
├── CLAUDE.md
├── README-gumroad.md                 # Gumroad product listing & setup guide
├── setup.sh                          # Quick-start installation script
├── .gitignore
├── .env                              # Optional: RESEND_API_KEY for email
├── .claude/
│   ├── commands/
│   │   ├── apply.md                  # Main /apply command (8-section strategy)
│   │   ├── batch.md                  # Batch process multiple JDs from JD_CURRENT.txt
│   │   ├── gaps.md                   # Aggregate skills gaps across applications
│   │   ├── pipeline.md              # Application pipeline funnel + alerts
│   │   └── status.md                # Update application status in tracker
│   └── settings.local.json           # Project permissions
├── documents/
│   └── resume/                       # User places source resume here
│       └── {Name}_Master_{YYYY-MM-DD}.md # Recommended naming (also .pdf, .docx)
├── job-descriptions/                 # JD files for /apply and /batch
│   ├── JD_CURRENT.txt                # Paste JDs here for /batch (plain text, NOT .rtf)
│   └── JD_Archive_YYYY-MM-DD.txt     # Auto-archived after /batch runs
├── output/                           # Generated output, organized by company
│   ├── gaps_report_{YYYY-MM-DD}.md       # Skills gap report (from /gaps)
│   ├── gaps_report_{YYYY-MM-DD}.pdf      # Skills gap PDF (color-coded)
│   └── {company-slug}/
│       ├── {Name}_{Company}_{Role}_{YYYY-MM-DD}.md       # Tailored resume
│       ├── {Name}_{Company}_{Role}_{YYYY-MM-DD}.pdf      # Resume PDF
│       ├── {Name}_{Company}_{Role}_{YYYY-MM-DD}.docx     # Resume DOCX (ATS)
│       ├── {Name}_{Company}_{Role}_Strategy_{YYYY-MM-DD}.md   # Strategy doc
│       ├── {Name}_{Company}_{Role}_Strategy_{YYYY-MM-DD}.pdf  # Strategy PDF
│       ├── {Name}_{Company}_{Role}_Changes_{YYYY-MM-DD}.md    # Change log
│       ├── {Name}_{Company}_{Role}_CoverLetter_{YYYY-MM-DD}.pdf   # Cover letter PDF
│       └── {Name}_{Company}_{Role}_CoverLetter_{YYYY-MM-DD}.docx  # Cover letter DOCX
├── scripts/
│   ├── read-resume.py                # Extract text from PDF/DOCX/MD resume
│   ├── generate-resume-pdf.py        # Resume markdown -> professional PDF
│   ├── generate-resume-docx.py       # Resume markdown -> ATS-friendly DOCX
│   ├── generate-strategy-pdf.py      # Strategy doc -> styled PDF (color-coded tables)
│   ├── generate-gaps-pdf.py          # Gaps report -> color-coded PDF
│   ├── generate-cover-letter-pdf.py  # Cover letter -> letter-format PDF
│   ├── generate-cover-letter-docx.py # Cover letter -> ATS-friendly DOCX
│   ├── pipeline-dashboard.py         # Streamlit pipeline dashboard (port 8505)
│   ├── run-apply.sh                  # Orchestration: command -> all docs -> Finder
│   └── run-batch.sh                  # Batch PDF/DOCX generation for multiple companies
└── tracker.md                        # Application tracker (markdown table)
```

## Workflow

### Single Application
1. Place your source resume in `documents/resume/` as `YourName_Master_YYYY-MM-DD.md` (or .pdf/.docx)
2. Run `/apply CompanyName` and paste the full job description when prompted
3. Command generates tailored resume, strategy (8 sections), and change log as markdown
4. Run `bash scripts/run-apply.sh` to generate PDF + DOCX files and open the output folder

### Batch Processing (Multiple JDs)
1. Paste multiple JDs into `job-descriptions/JD_CURRENT.txt` (plain text, **not** RTF) separated by `=== COMPANY NAME ===` markers
2. Run `/batch` — parses all JDs, confirms the batch plan, then processes each sequentially
3. After completion, JD_CURRENT.txt is archived to `JD_Archive_YYYY-MM-DD.txt` and cleared for reuse
4. Run `bash scripts/run-batch.sh` to generate PDFs + DOCX for all companies

**Key rule:** Commands write markdown only. Shell scripts handle PDF/DOCX generation.

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

### `/batch`
Process multiple job descriptions from `JD_CURRENT.txt` in one session. Generates a complete application package (resume + strategy + change log) for each JD, updates the tracker, then archives the source file.

```bash
# Paste JDs into job-descriptions/JD_CURRENT.txt first, then:
/batch
```

**JD_CURRENT.txt format:**
```
=== Adobe ===

[Full job description text]

=== Google | Senior PM ===

[Full job description text]
```

- Separator: `=== COMPANY NAME ===` (role title optional after `|`)
- Save as plain text (`.txt`), not RTF
- After processing, file is archived as `JD_Archive_YYYY-MM-DD.txt` and cleared

### `/gaps`
Aggregate skills gaps across all applications into a prioritized upskilling report. Reads all strategy docs, parses keyword gap tables, and produces a color-coded matrix showing strengths, addressed skills, and gaps. Outputs markdown + PDF.

```bash
/gaps
```

### `/pipeline`
Show application pipeline funnel, follow-up alerts, and salary summary. Reads `tracker.md` and displays ASCII funnel with conversion rates, flags overdue follow-ups, and summarizes salary data.

```bash
/pipeline
```

### `/status`
Update application status in `tracker.md`. Fuzzy-matches company name, updates status + Last Updated + Follow-Up Due, and prints next action reminder.

```bash
/status Anthropic Screened
/status Amazon Rejected
```

Valid statuses: `Applied`, `Screened`, `Interviewing`, `Offer`, `Accepted`, `Rejected`, `Withdrawn`, `Ghosted`

## Output Files

Each `/apply` run generates 8 files:

| File | Format | Description |
|------|--------|-------------|
| Tailored Resume | MD + PDF + DOCX | Reframed for JD, ATS-optimized |
| Application Strategy | MD + PDF | 8-section strategy with color-coded keyword gap table |
| Change Log | MD | Line-by-line diff of every resume modification |
| Cover Letter | PDF + DOCX | Professional letter extracted from strategy |

## File Naming Convention

- **Source resume**: `{Name}_Master_{YYYY-MM-DD}.md` in `documents/resume/`
- **Tailored resume**: `{Name}_{Company}_{Role}_{YYYY-MM-DD}.md/.pdf/.docx`
- **Strategy**: `{Name}_{Company}_{Role}_Strategy_{YYYY-MM-DD}.md/.pdf`
- **Change log**: `{Name}_{Company}_{Role}_Changes_{YYYY-MM-DD}.md`
- **Cover letter**: `{Name}_{Company}_{Role}_CoverLetter_{YYYY-MM-DD}.pdf/.docx`

Name extracted from master resume filename. Company and Role from JD parsing. Company slug: lowercase, hyphens for spaces.

## Strategy Sections

1. **Keyword Gap Analysis** — color-coded table (green/yellow/red) with match score
2. **Cover Letter Draft** — opening, body, close
3. **Interview Talking Points** — why company, why role, 3 STAR stories
4. **Networking Tips** — LinkedIn, outreach template, communities
5. **Salary Research** — multi-source table with recommended ask
6. **Application Checklist** — comprehensive pre/post-interview tasks
7. **Interview Preparation** — predicted behavioral + technical questions with frameworks
8. **Follow-Up Email Templates** — thank you, follow-up, negotiation, acceptance, decline

## Resume Formats Supported

- **PDF**: Extracted via PyMuPDF (`fitz`)
- **DOCX**: Extracted via python-docx
- **Markdown**: Read directly

The `scripts/read-resume.py` script prefers `*_Master_*` pattern files. Falls back to most recent file with a warning. Extracts candidate name from filename.

## Application Tracker

`tracker.md` records all applications in a 9-column markdown table:

```
| Date | Company | Role | Status | Last Updated | Follow-Up Due | Resume | Strategy | Notes |
```

- Updated automatically by `/apply` (adds row) and `/status` (updates status/dates)
- **Last Updated** — date of most recent status change
- **Follow-Up Due** — next action date (Applied +7d, Screened +3d, Interviewing +1d, Offer +3d)
- Old 7-column format (without Last Updated / Follow-Up Due) is auto-upgraded by `/status`

## Python Dependencies

```
fpdf2          # PDF generation (native rendering)
PyMuPDF        # PDF text extraction (import fitz)
python-docx    # DOCX generation + text extraction
markdown       # Markdown -> HTML conversion (strategy PDF)
```

### Setup

```bash
pip3 install fpdf2 PyMuPDF python-docx markdown streamlit pandas
```

Or use the quick-start script:
```bash
bash setup.sh
```

## Related Workspaces

See `~/WORKSPACES.md` for navigation. Personal automation in `~/LifeOS/`, business tools in `~/BusinessOS/`.

## Mistakes & Lessons Learned

- **2026-03-04: v1 had zero verification on resume tailoring** — The original `/apply` relied entirely on a prompt-level "NEVER fabricate" instruction with no validation pass, no diff output, and no transparency into what changed. → Rule: any AI-generated content in the user's voice MUST have a verification step AND a human-readable change log. Prompt-level constraints alone are insufficient.
- **2026-03-04: Cover letter was buried in strategy doc** — Users had to copy-paste the cover letter from the strategy markdown. No standalone file existed. → Rule: if a section of output is independently useful (submitted separately), generate it as its own file.

## Development Commands

```bash
# Extract resume text
python3 scripts/read-resume.py

# Generate documents standalone
python3 scripts/generate-resume-pdf.py output/company/Name_Company_Role_2026-03-04.md
python3 scripts/generate-resume-docx.py output/company/Name_Company_Role_2026-03-04.md
python3 scripts/generate-strategy-pdf.py output/company/Name_Company_Role_Strategy_2026-03-04.md
python3 scripts/generate-gaps-pdf.py output/gaps_report_2026-03-04.md
python3 scripts/generate-cover-letter-pdf.py output/company/Name_Company_Role_Strategy_2026-03-04.md
python3 scripts/generate-cover-letter-docx.py output/company/Name_Company_Role_Strategy_2026-03-04.md

# Full pipeline (single company)
bash scripts/run-apply.sh "CompanyName"

# Generate docs for existing output dir (skip /apply)
bash scripts/run-apply.sh company-slug

# Batch PDF/DOCX generation (all dirs modified today)
bash scripts/run-batch.sh

# Batch PDF/DOCX for specific companies
bash scripts/run-batch.sh adobe google

# Pipeline dashboard (Streamlit on port 8505)
python3 -m streamlit run ~/CareerOS/scripts/pipeline-dashboard.py --server.port 8505
```
