# CareerOS — AI Resume Tailoring Engine

Paste a job description. Get 5 tailored documents in 90 seconds. Every change is traceable to your original resume — no AI hallucinations.

## What You Get

- **`/apply` command** — takes a JD, generates a complete application package
- **Anti-hallucination guardrails** — every change is verified against your original resume
- **Change log** — see exactly what was modified, why, and how it maps to the JD
- **ATS-optimized output** — DOCX + PDF with standard formatting and keyword placement
- **8-section strategy** — keyword gap analysis, cover letter, interview prep, salary research, networking tips, follow-up templates
- **Color-coded keyword gap table** — green (matched), yellow (reframed), red (gap) at a glance

## Output Files (per application)

| File | Formats | What It Does |
|------|---------|-------------|
| Tailored Resume | MD + PDF + DOCX | Your resume reframed for the JD, ATS-optimized |
| Application Strategy | MD + PDF | 8-section strategy with color-coded keyword analysis |
| Change Log | MD | Line-by-line diff of every modification with reasons |
| Cover Letter | PDF + DOCX | Professional letter extracted from strategy |

## Requirements

- **Claude Code** — free CLI from Anthropic ([install guide](https://docs.anthropic.com/en/docs/claude-code/overview))
- **Anthropic API key** — pay-per-use, ~$0.50-1.00 per application
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
documents/resume/Your_Name_Master_260304.md
```

Supported formats: `.md` (recommended), `.pdf`, `.docx`

### 5. Run your first application

```bash
/apply Google
```

Paste the full job description when prompted. Wait ~90 seconds.

Then generate all document formats:

```bash
bash scripts/run-apply.sh
```

## How It Works

1. **Parse** — extracts company, role, and keywords from the JD
2. **Research** — searches for company culture, salary data, recent news
3. **Tailor** — reframes your resume for the JD (reorder bullets, mirror keywords, adjust summary)
4. **Verify** — two-pass integrity check ensures nothing was fabricated
5. **Strategy** — generates 8-section strategy doc with keyword gap analysis
6. **Change Log** — documents every modification with original vs. tailored text
7. **Documents** — generates PDF + DOCX for resume and cover letter

## The Guardrail System

Most AI resume tools hallucinate. They add skills you don't have, inflate numbers, and invent experience. CareerOS is built differently:

- **No new facts**: Every company, title, date, and metric must exist in your original resume
- **No invented skills**: Skills must exist in your resume or be directly inferable
- **No fake numbers**: If your resume doesn't have a metric, the output won't either
- **Gaps are gaps**: If a JD keyword doesn't match your experience, it's flagged honestly
- **Change log**: Every modification is documented — you can audit the AI's work

## Strategy Sections

1. **Keyword Gap Analysis** — color-coded table showing JD coverage
2. **Cover Letter Draft** — personalized opening, body, and close
3. **Interview Talking Points** — why this company, why this role, 3 STAR stories
4. **Networking Tips** — who to connect with, outreach templates
5. **Salary Research** — multi-source data with recommended ask
6. **Application Checklist** — comprehensive pre/post-interview tasks
7. **Interview Preparation** — predicted behavioral + technical questions with response frameworks
8. **Follow-Up Templates** — thank you, follow-up, negotiation, acceptance, decline emails

## File Structure

```
CareerOS/
├── .claude/commands/apply.md    # The /apply command
├── documents/resume/            # Your master resume goes here
├── job-descriptions/            # Optional: save JD files
├── output/{company}/            # Generated output per company
├── scripts/                     # PDF/DOCX generation scripts
├── setup.sh                     # Quick-start installer
└── tracker.md                   # Application tracker
```

## Tips

- **Markdown resume recommended**: `.md` format gives the best results since the AI can read it perfectly. PDF extraction can lose formatting.
- **One master resume**: Keep a comprehensive master resume with ALL your experience. The AI will select and reframe the most relevant parts for each JD.
- **Review the change log**: Before submitting, open the change log to verify every modification makes sense.
- **Edit the cover letter**: The generated cover letter is a strong draft — personalize it with your voice before sending.

## Cost

Each `/apply` run uses approximately:
- ~$0.50-1.00 in Anthropic API credits (varies by resume length and JD complexity)
- Claude Code itself is free

## Support

Questions? Issues? Open a GitHub issue or reach out on X.

---

Built with Claude Code. Keep building.
