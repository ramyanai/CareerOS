# CareerOS -- AI Resume Tailoring Engine

Paste a job description. Get a complete application package -- tailored resume, cover letter, strategy doc, and change log. Every change is traceable to your original resume. No AI hallucinations.

## What You Get

- **`/apply` command** -- takes a JD, generates a complete application package (resume + strategy + cover letter + change log)
- **`/batch` command** -- process multiple JDs at once from a single file
- **`/gaps` command** -- aggregate skills gaps across all applications into a prioritized upskilling report
- **`/pipeline` command** -- pipeline funnel, follow-up alerts, salary summary
- **`/status` command** -- update application status and set follow-up reminders
- **Anti-hallucination guardrails** -- two-pass verification ensures nothing is fabricated
- **Change log** -- see exactly what was modified, why, and how it maps to the JD
- **ATS-optimized output** -- DOCX + PDF with standard formatting and keyword placement
- **8-section strategy** -- keyword gap analysis, cover letter, interview prep, salary research, networking tips, follow-up templates
- **Color-coded keyword gap table** -- green (matched), yellow (reframed), red (gap) at a glance

## Output Files (per application)

| File | Formats | What It Does |
|------|---------|-------------|
| Tailored Resume | MD + PDF + DOCX | Your resume reframed for the JD, ATS-optimized |
| Application Strategy | MD + PDF | 8-section strategy with ATS score and color-coded keyword analysis |
| Change Log | MD + PDF | Line-by-line diff of every modification with color-coded change types |
| Cover Letter | PDF + DOCX | Professional letter personalized to the company |

## Requirements

- **Claude Code** -- free CLI from Anthropic ([install guide](https://docs.anthropic.com/en/docs/claude-code/overview))
- **Anthropic API key** -- pay-per-use, ~$0.50-1.00 per application
- **Python 3.9+** with: `fpdf2`, `python-docx`, `PyMuPDF`, `markdown`

## Setup (5 minutes)

### 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 2. Run the setup script

```bash
cd CareerOS
bash setup.sh
```

This installs Python dependencies and creates the directory structure.

### 3. Set your API key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 4. Place your master resume

Save your resume in `documents/resume/` using this naming format:

```
documents/resume/Your_Name_Master_2026-03-04.md
```

Supported formats: `.md` (recommended), `.pdf`, `.docx`

See `documents/resume/EXAMPLE_Master_Resume.md` for the expected format.

### 5. Run your first application

```bash
claude
/apply Google
```

Paste the full job description when prompted. All files (MD + PDF + DOCX) are generated automatically and the output folder opens in Finder when complete.

## How It Works

1. **Parse** -- extracts company, role, and keywords from the JD
2. **Research** -- searches for company culture, salary data, recent news
3. **Tailor** -- reframes your resume for the JD (reorder bullets, mirror keywords, adjust summary)
4. **Verify** -- two-pass integrity check ensures nothing was fabricated
5. **Strategy** -- generates 8-section strategy doc with ATS scoring and keyword gap analysis
6. **Change Log** -- documents every modification with original vs. tailored text
7. **Documents** -- generates PDF + DOCX for resume, cover letter, strategy, and change log

## The Guardrail System

Most AI resume tools hallucinate. They add skills you don't have, inflate numbers, and invent experience. CareerOS is built differently:

- **No new facts**: Every company, title, date, and metric must exist in your original resume
- **No invented skills**: Skills must exist in your resume or be directly inferable
- **No fake numbers**: If your resume doesn't have a metric, the output won't either
- **Gaps are gaps**: If a JD keyword doesn't match your experience, it's flagged honestly
- **Change log**: Every modification is documented -- you can audit the AI's work

## Batch Processing

Process multiple JDs in one session:

1. Paste JDs into `job-descriptions/JD_CURRENT.txt` separated by `=== COMPANY NAME ===` markers
2. Run `/batch` -- processes each JD sequentially, then archives the file
3. Run `bash scripts/run-batch.sh` to generate PDFs + DOCX for all companies

## Pipeline Management

Track applications across your entire search:

- `/status Anthropic Screened` -- update status, auto-set follow-up reminders
- `/pipeline` -- see funnel metrics, overdue follow-ups, salary ranges
- `/gaps` -- find which skills to develop based on gap patterns across applications

## Strategy Sections

1. **Keyword Gap Analysis** -- color-coded table showing JD coverage
2. **Cover Letter Draft** -- personalized opening, body, and close
3. **Interview Talking Points** -- why this company, why this role, 3 STAR stories
4. **Networking Tips** -- who to connect with, outreach templates
5. **Salary Research** -- multi-source data with recommended ask
6. **Application Checklist** -- comprehensive pre/post-interview tasks
7. **Interview Preparation** -- predicted behavioral + technical questions with response frameworks
8. **Follow-Up Templates** -- thank you, follow-up, negotiation, acceptance, decline emails

## File Structure

```
CareerOS/
├── .claude/commands/           # All 5 custom commands
│   ├── apply.md                # /apply -- single application
│   ├── batch.md                # /batch -- batch processing
│   ├── gaps.md                 # /gaps -- skills gap report
│   ├── pipeline.md             # /pipeline -- pipeline dashboard
│   └── status.md               # /status -- update tracker
├── documents/resume/           # Your master resume goes here
├── job-descriptions/           # JD files for /apply and /batch
├── output/{company}/           # Generated output per company
├── scripts/                    # PDF/DOCX generation scripts
├── setup.sh                    # Quick-start installer
└── tracker.md                  # Application tracker
```

## Tips

- **Markdown resume recommended**: `.md` format gives the best results since the AI can read it perfectly. PDF extraction can lose formatting.
- **One master resume**: Keep a comprehensive master resume with ALL your experience. The AI will select and reframe the most relevant parts for each JD.
- **Review the change log**: Before submitting, open the change log to verify every modification makes sense.
- **Edit the cover letter**: The generated cover letter is a strong draft -- personalize it with your voice before sending.

## Cost

Each `/apply` run uses approximately:
- ~$0.50-1.00 in Anthropic API credits (varies by resume length and JD complexity)
- Claude Code itself is free

## Support

Questions? Issues? Open a GitHub issue or reach out on X.

---

Built with Claude Code. Keep building.
