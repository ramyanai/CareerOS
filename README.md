# CareerOS

AI-powered job application tailoring engine built on Claude Code. Paste a job description, get a complete application package — tailored resume, cover letter, strategy doc, and change log — with every modification traceable to your original resume. No hallucinated skills. No invented metrics. Gaps are gaps.

## Why CareerOS?

Most AI resume tools hallucinate. They add skills you don't have, inflate numbers, and invent experience. CareerOS is different:

- **No fabrication** — every fact in the output must exist in your source resume
- **Change log** — every modification is documented with original text, new text, and reason
- **Two-pass verification** — the AI audits its own work before saving
- **Gaps are gaps** — if a JD keyword doesn't match your experience, it's flagged honestly

## What You Get

**Per application (9 files):**

| File | Formats | Description |
|------|---------|-------------|
| Tailored Resume | MD + PDF + DOCX | Reframed for the JD, ATS-optimized |
| Application Strategy | MD + PDF | ATS score, keyword gap analysis, interview prep, salary research |
| Change Log | MD + PDF | Line-by-line diff of every modification |
| Cover Letter | PDF + DOCX | Professional letter personalized to the company |

**Pipeline tools:**

| Command | What It Does |
|---------|-------------|
| `/apply` | Tailor resume + generate full application package for one company |
| `/batch` | Process multiple JDs at once from a single file |
| `/gaps` | Aggregate skills gaps across all applications into upskilling report |
| `/pipeline` | Pipeline funnel, follow-up alerts, salary summary |
| `/status` | Update application status and set follow-up reminders |

## User Guide

New to CareerOS? Read the **[User Guide](USER-GUIDE.md)** for a detailed walkthrough — from setup to your first application to batch processing.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) CLI from Anthropic
- A Claude Pro ($20/mo), Max ($100/mo), or Max 5x ($200/mo) subscription — or an Anthropic API key
- Python 3.9+ with: `fpdf2`, `python-docx`, `PyMuPDF`, `markdown`

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/ramyanai/CareerOS.git
cd CareerOS

# 2. Run setup (installs Python deps, creates directories)
bash setup.sh

# 3. Place your master resume
cp ~/your-resume.md documents/resume/Your_Name_Master_2026-03-04.md

# 4. Launch Claude Code and run your first application
claude
/apply Google
```

Paste the full job description when prompted. The command generates all 9 files and opens the output folder when complete.

## Resume Format

Your master resume goes in `documents/resume/`. Supported formats: `.md` (recommended), `.pdf`, `.docx`.

**Naming convention:** `YourName_Master_YYYY-MM-DD.md`

A markdown resume gives the best results since Claude can read it perfectly. See `documents/resume/EXAMPLE_Master_Resume.md` for the expected format.

**Tip:** Keep a comprehensive master resume with ALL your experience. The AI selects and reframes the most relevant parts for each JD.

## Batch Processing

Process multiple JDs in one session:

1. Paste JDs into `job-descriptions/JD_CURRENT.txt` separated by `=== COMPANY NAME ===` markers:

```
=== Adobe ===

[Full job description text]

=== Google | Senior PM ===

[Full job description text]
```

2. Run `/batch` — parses all JDs, generates application packages sequentially
3. Run `bash scripts/run-batch.sh` to generate PDFs + DOCX for all companies

## Application Tracker

Every `/apply` run adds a row to `tracker.md`:

```
| Date | Company | Role | Status | Last Updated | Follow-Up Due | Resume | Strategy | Notes |
```

Update status with `/status`:
```
/status Anthropic Screened
/status Amazon Rejected
```

View your pipeline with `/pipeline` — shows funnel metrics, overdue follow-ups, and salary ranges.

## Strategy Sections

Each application strategy includes:

1. **Keyword Gap Analysis** — color-coded table (green/yellow/red) with match score
2. **Cover Letter Draft** — personalized opening, body, and close
3. **Interview Talking Points** — why this company, why this role, 3 STAR stories
4. **Networking Tips** — who to connect with, outreach templates
5. **Salary Research** — multi-source data with recommended ask
6. **Application Checklist** — pre/post-interview tasks
7. **Interview Preparation** — predicted questions with response frameworks
8. **Follow-Up Templates** — thank you, follow-up, negotiation, acceptance, decline

## ATS Compatibility Scoring

Each strategy doc opens with an ATS assessment:

- **Format Score** — standard headings, contact info, no complex formatting
- **Keyword Match Score** — weighted coverage of JD keywords (Yes=1.0, Partial=0.5, Gap=0)
- **Experience Fit Score** — years, qualifications, industry, seniority
- **Overall Pass Likelihood** = Format x 20% + Keywords x 60% + Experience x 20%

## Project Structure

```
CareerOS/
├── .claude/commands/          # Claude Code custom commands
│   ├── apply.md               # /apply — single application
│   ├── batch.md               # /batch — batch processing
│   ├── gaps.md                # /gaps — skills gap report
│   ├── pipeline.md            # /pipeline — pipeline dashboard
│   └── status.md              # /status — update tracker
├── documents/resume/          # Your master resume goes here
├── job-descriptions/          # JD files for /apply and /batch
├── output/                    # Generated output per company
├── scripts/                   # PDF/DOCX generation scripts
├── setup.sh                   # Quick-start installer
├── tracker.md                 # Application tracker
├── USER-GUIDE.md              # Step-by-step walkthrough
└── README.md
```

## Cost

If you have a Claude Pro or Max subscription, there's nothing extra to pay — Claude Code usage is included. If using an API key instead, each `/apply` run costs approximately $0.50-1.00 depending on resume length and JD complexity.

## License

MIT

---

Built with [Claude Code](https://claude.com/claude-code).
