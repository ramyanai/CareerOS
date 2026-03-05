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
│   │   └── apply.md                  # Main /apply command (8-section strategy)
│   └── settings.local.json           # Project permissions
├── documents/
│   └── resume/                       # User places source resume here
│       └── {Name}_Master_{YYMMDD}.md # Recommended naming (also .pdf, .docx)
├── job-descriptions/                 # Optional: saved JD files for reference
├── output/                           # Generated output, organized by company
│   └── {company-slug}/
│       ├── {Name}_{Company}_{Role}_{YYMMDD}.md       # Tailored resume
│       ├── {Name}_{Company}_{Role}_{YYMMDD}.pdf      # Resume PDF
│       ├── {Name}_{Company}_{Role}_{YYMMDD}.docx     # Resume DOCX (ATS)
│       ├── {Name}_{Company}_{Role}_Strategy_{YYMMDD}.md   # Strategy doc
│       ├── {Name}_{Company}_{Role}_Strategy_{YYMMDD}.pdf  # Strategy PDF
│       ├── {Name}_{Company}_{Role}_Changes_{YYMMDD}.md    # Change log
│       ├── {Name}_{Company}_{Role}_CoverLetter_{YYMMDD}.pdf   # Cover letter PDF
│       └── {Name}_{Company}_{Role}_CoverLetter_{YYMMDD}.docx  # Cover letter DOCX
├── scripts/
│   ├── read-resume.py                # Extract text from PDF/DOCX/MD resume
│   ├── generate-resume-pdf.py        # Resume markdown -> professional PDF
│   ├── generate-resume-docx.py       # Resume markdown -> ATS-friendly DOCX
│   ├── generate-strategy-pdf.py      # Strategy doc -> styled PDF (color-coded tables)
│   ├── generate-cover-letter-pdf.py  # Cover letter -> letter-format PDF
│   ├── generate-cover-letter-docx.py # Cover letter -> ATS-friendly DOCX
│   └── run-apply.sh                  # Orchestration: command -> all docs -> Finder
└── tracker.md                        # Application tracker (markdown table)
```

## Workflow

1. Place your source resume in `documents/resume/` as `YourName_Master_YYMMDD.md` (or .pdf/.docx)
2. Run `/apply CompanyName` and paste the full job description when prompted
3. Command generates tailored resume, strategy (8 sections), and change log as markdown
4. Run `bash scripts/run-apply.sh` to generate PDF + DOCX files and open the output folder

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

## Output Files

Each `/apply` run generates 8 files:

| File | Format | Description |
|------|--------|-------------|
| Tailored Resume | MD + PDF + DOCX | Reframed for JD, ATS-optimized |
| Application Strategy | MD + PDF | 8-section strategy with color-coded keyword gap table |
| Change Log | MD | Line-by-line diff of every resume modification |
| Cover Letter | PDF + DOCX | Professional letter extracted from strategy |

## File Naming Convention

- **Source resume**: `{Name}_Master_{YYMMDD}.md` in `documents/resume/`
- **Tailored resume**: `{Name}_{Company}_{Role}_{YYMMDD}.md/.pdf/.docx`
- **Strategy**: `{Name}_{Company}_{Role}_Strategy_{YYMMDD}.md/.pdf`
- **Change log**: `{Name}_{Company}_{Role}_Changes_{YYMMDD}.md`
- **Cover letter**: `{Name}_{Company}_{Role}_CoverLetter_{YYMMDD}.pdf/.docx`

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

`tracker.md` records all applications as a markdown table. Updated automatically by `/apply`. Edit manually to update status.

## Python Dependencies

```
fpdf2          # PDF generation (native rendering)
PyMuPDF        # PDF text extraction (import fitz)
python-docx    # DOCX generation + text extraction
markdown       # Markdown -> HTML conversion (strategy PDF)
```

### Setup

```bash
pip3 install fpdf2 PyMuPDF python-docx markdown
```

Or use the quick-start script:
```bash
bash setup.sh
```

## Related Workspaces

See `~/WORKSPACES.md` for navigation. Personal automation in `~/LifeOS/`, business tools in `~/BusinessOS/`.

## Development Commands

```bash
# Extract resume text
python3 scripts/read-resume.py

# Generate documents standalone
python3 scripts/generate-resume-pdf.py output/company/Name_Company_Role_260304.md
python3 scripts/generate-resume-docx.py output/company/Name_Company_Role_260304.md
python3 scripts/generate-strategy-pdf.py output/company/Name_Company_Role_Strategy_260304.md
python3 scripts/generate-cover-letter-pdf.py output/company/Name_Company_Role_Strategy_260304.md
python3 scripts/generate-cover-letter-docx.py output/company/Name_Company_Role_Strategy_260304.md

# Full pipeline
bash scripts/run-apply.sh "CompanyName"
```
