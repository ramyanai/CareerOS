# CareerOS User Guide

A step-by-step guide to tailoring your resume and generating complete application packages.

## Prerequisites

Before you start, you need:

1. **Python 3.9+** — check with `python3 --version`
2. **Claude Code CLI** — install with `npm install -g @anthropic-ai/claude-code`
3. **Anthropic API key** — get one at [console.anthropic.com](https://console.anthropic.com/)

## Setup

```bash
# Clone the repo
git clone https://github.com/ramyanai/CareerOS.git
cd CareerOS

# Run setup (installs Python dependencies, creates directories)
bash setup.sh

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"
```

Setup installs: `fpdf2`, `python-docx`, `PyMuPDF`, `markdown`. Optional: `streamlit` and `pandas` for the pipeline dashboard.

## Step 1: Prepare Your Master Resume

Place your resume in `documents/resume/`. Supported formats:

| Format | Notes |
|--------|-------|
| `.md` (recommended) | Best results — Claude reads it perfectly |
| `.pdf` | Extracted via PyMuPDF |
| `.docx` | Extracted via python-docx |

**Naming convention:** `YourName_Master_YYYY-MM-DD.md`

Example: `Jane_Doe_Master_2026-03-06.md`

See `documents/resume/EXAMPLE_Master_Resume.md` for the expected format.

**Tip:** Make your master resume comprehensive — include ALL your experience, skills, and achievements. The tool selects and reframes the most relevant parts for each job description. A longer master resume gives the AI more to work with.

## Step 2: Run Your First Application

```bash
# Start Claude Code from the CareerOS directory
cd CareerOS
claude

# Run the apply command
/apply Google
```

When prompted, paste the **full job description** (copy the entire text from the job posting).

The tool will:
1. Read your master resume
2. Research the company (culture, tech stack, recent news, salary data)
3. Map every keyword in the job description to your real experience
4. Tailor your resume — reorder bullets, mirror keywords, adjust your summary
5. Verify every line against your source resume (two-pass check)
6. Generate all documents (PDF + DOCX)
7. Open the output folder in Finder

**Cost:** ~$0.50-1.00 per application in Anthropic API credits.

## Step 3: Review Your Output

Each application generates 9 files in `output/{company-name}/`:

```
output/google/
  Jane_Doe_google_senior-pm_2026-03-06.md        # Tailored resume (markdown)
  Jane_Doe_google_senior-pm_2026-03-06.pdf        # Tailored resume (PDF)
  Jane_Doe_google_senior-pm_2026-03-06.docx       # Tailored resume (DOCX, ATS-friendly)
  Jane_Doe_google_senior-pm_Strategy_2026-03-06.md   # Strategy doc
  Jane_Doe_google_senior-pm_Strategy_2026-03-06.pdf   # Strategy doc (PDF)
  Jane_Doe_google_senior-pm_Changes_2026-03-06.md     # Change log
  Jane_Doe_google_senior-pm_Changes_2026-03-06.pdf     # Change log (PDF)
  Jane_Doe_google_senior-pm_CoverLetter_2026-03-06.pdf   # Cover letter (PDF)
  Jane_Doe_google_senior-pm_CoverLetter_2026-03-06.docx  # Cover letter (DOCX)
```

### What to check first

1. **Change log** — read this first. Every modification is documented: original text, new text, and why it changed. If anything looks wrong, you'll catch it here.
2. **Keyword gap analysis** — in the strategy doc. Shows which job description keywords were matched (green), partially matched (yellow), or missing from your experience (red). Gaps are honest — the tool won't fake a match.
3. **Tailored resume** — review the PDF or DOCX. Check that nothing was added that isn't in your master resume.

### What's in the strategy doc

- ATS compatibility score (format + keyword match + experience fit)
- Keyword gap analysis (color-coded table)
- Cover letter draft
- Interview talking points with 3 STAR stories
- Networking tips and outreach templates
- Salary research from multiple sources
- Predicted interview questions with response frameworks
- Follow-up email templates (thank you, negotiation, acceptance, decline)

## Batch Processing (Multiple Applications)

Applying to several jobs at once? Use batch mode.

### 1. Create a batch file

Add your job descriptions to `job-descriptions/JD_CURRENT.txt`, separated by company markers:

```
=== Adobe ===

Senior Product Manager - Creative Cloud

About the Role:
We're looking for a Senior PM to lead...
[full job description text]

=== Google | Senior PM ===

[full job description text]

=== Stripe | Product Manager, Payments ===

[full job description text]
```

**Important:** Save as plain text (`.txt`), not RTF.

### 2. Run the batch

```bash
claude
/batch
```

The tool shows you a batch plan (companies + roles detected) and asks for confirmation before processing. Each application runs sequentially — full package for each.

### 3. Generate all documents

After the batch completes:

```bash
# Generate PDFs + DOCX for all companies processed today
bash scripts/run-batch.sh

# Or for specific companies only
bash scripts/run-batch.sh adobe google
```

### 4. Archive

After processing, `JD_CURRENT.txt` is automatically archived to `JD_Archive_YYYY-MM-DD.txt` and cleared for reuse.

## Tracking Your Applications

Every `/apply` run adds a row to `tracker.md`:

```
| Date | Company | Role | Status | Last Updated | Follow-Up Due | Resume | Strategy | Notes |
```

### Update status

```bash
claude
/status Anthropic Screened
/status Amazon Rejected
```

Valid statuses: `Applied`, `Screened`, `Interviewing`, `Offer`, `Accepted`, `Rejected`, `Withdrawn`, `Ghosted`

Follow-up dates are set automatically:
- Applied: +7 days
- Screened: +3 days
- Interviewing: +1 day
- Offer: +3 days

### View your pipeline

```bash
claude
/pipeline
```

Shows:
- Funnel metrics (how many at each stage, conversion rates)
- Overdue follow-ups flagged for action
- Salary ranges across all applications

### Skills gap report

```bash
claude
/gaps
```

Aggregates keyword gaps across all your applications into a prioritized upskilling report. Shows which skills keep coming up as gaps — useful for deciding what to learn next.

## The 7 Anti-Hallucination Guardrails

These are enforced automatically. You don't need to configure anything.

1. **No new facts** — every company, title, date, metric must exist in your source resume
2. **No skills from thin air** — must exist in your resume or be clearly inferable
3. **Reframing only** — the tool changes verbs and framing, never adds substance
4. **Gaps are gaps** — unmapped keywords go in the gap analysis, not your resume
5. **Numbers from source only** — metrics are never invented
6. **Two-pass verification** — every bullet is checked against your source before saving
7. **Change log** — every modification documented with original text, new text, and reason

## Tips

- **Longer master resume = better results.** Include everything — old roles, side projects, certifications. The AI picks what's relevant.
- **Markdown resumes work best.** PDF extraction can lose formatting. If you have a DOCX, convert to markdown for best results.
- **Review the change log before submitting.** It takes 2 minutes and catches any issues.
- **Use `/gaps` after 5+ applications.** The pattern of missing skills becomes clear and actionable.
- **Keep one master resume updated.** When you learn a new skill or finish a project, add it to your master. Every future application benefits.

## Troubleshooting

**"Claude Code not found"**
```bash
npm install -g @anthropic-ai/claude-code
```

**"No resume found"**
Place your resume in `documents/resume/` with the naming pattern `YourName_Master_YYYY-MM-DD.md` (or `.pdf` / `.docx`).

**PDF generation fails**
```bash
pip3 install fpdf2 python-docx PyMuPDF markdown
```

**DOCX resume not reading correctly**
Convert to markdown — it gives the best results. You can use any text editor or ask Claude to help convert it.

## Project Structure

```
CareerOS/
  .claude/commands/     # The AI commands (apply, batch, gaps, pipeline, status)
  documents/resume/     # Your master resume goes here
  job-descriptions/     # JD files for /apply and /batch
  output/               # Generated output, organized by company
  scripts/              # PDF/DOCX generation and pipeline tools
  tracker.md            # Your application tracker (auto-generated)
  setup.sh              # Quick-start installer
```

## License

MIT — use it, fork it, improve it.
