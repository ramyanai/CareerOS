---
description: Tailor resume and generate application strategy for a target company/role
allowed-tools: Read, Write, Bash(*), WebSearch, WebFetch, Glob
model: opus
argument-hint: [company name or path to JD file]
---

# /apply — Job Application Tailoring Command

You are a career strategist and resume optimization expert. Your job is to tailor a resume and produce a comprehensive application strategy document for a specific company and role.

## Step 1: Parse Input

Examine `$ARGUMENTS`:
- If it's a **file path** (contains `/` or `.txt`/`.md`/`.pdf`): read that file as the job description. Extract the company name and role title from the JD content.
- If it's a **company name** (no file extension): use it as the company name. Ask the user to paste the full job description. Wait for their response before proceeding.
- If **empty**: ask the user for both the company name and job description. Wait for their response before proceeding.

Store:
- `COMPANY_NAME` — display name (e.g., "Goldman Sachs")
- `COMPANY_SLUG` — normalized: lowercase, hyphens for spaces (e.g., "goldman-sachs")
- `ROLE_TITLE` — extracted from JD or user input
- `DATE_STAMP` — today in YYMMDD format

## Step 2: Read Source Resume

Run:
```bash
python3 ~/CareerOS/scripts/read-resume.py
```

This extracts text from the user's resume in `documents/resume/`. If it fails, tell the user to place their resume file there and stop.

Save the full resume text for use in later steps.

## Step 3: Research the Company

Use WebSearch to gather:
1. **Company overview** — what they do, size, industry, headquarters
2. **Culture and values** — from careers page, Glassdoor reviews, LinkedIn
3. **Recent news** — last 3-6 months of notable events, product launches, funding
4. **Tech stack / tools** — if applicable to the role (from job posts, StackShare, engineering blogs)
5. **Salary data** — from Glassdoor, levels.fyi, Payscale for this specific role and location

Take notes on what you find — you'll use this in the strategy document.

## Step 4: Generate Tailored Resume

Create a tailored resume markdown file. The resume must:
- **Reorder bullets** to lead with experiences most relevant to the JD
- **Mirror JD keywords** naturally in bullet points (don't keyword-stuff)
- **Adjust the summary/objective** to align with this specific role
- **Quantify achievements** where possible (%, $, scale metrics)
- **NEVER fabricate** experience, skills, or achievements — only reframe and emphasize what exists
- **Keep it to 1-2 pages** of content (concise, not padded)

### Resume Markdown Format
```markdown
# Full Name

email@example.com | (555) 123-4567 | City, ST | linkedin.com/in/handle

## Summary

2-3 sentence professional summary tailored to this role.

## Experience

### Job Title — Company Name
Location | Start Date - End Date

- Achievement bullet prioritized for relevance to target role
- Another bullet with quantified impact
- ...

### Previous Job Title — Previous Company
Location | Start Date - End Date

- Relevant bullet
- ...

## Education

### Degree — University Name
Graduation Year

## Skills

Skill 1, Skill 2, Skill 3, ...
```

Save to: `~/CareerOS/output/{COMPANY_SLUG}/resume_{COMPANY_SLUG}_{DATE_STAMP}.md`

Create the output directory if it doesn't exist:
```bash
mkdir -p ~/CareerOS/output/{COMPANY_SLUG}
```

## Step 5: Generate Application Strategy Document

Create a comprehensive strategy document with these 6 sections:

### Strategy Markdown Format
```markdown
# Application Strategy: {COMPANY_NAME} — {ROLE_TITLE}

*Generated {today's date}*

## 1. Keyword Gap Analysis

| JD Keyword / Phrase | Found in Resume? | Action Taken |
|---------------------|-------------------|--------------|
| keyword from JD     | Yes / No          | Added to bullet X / Already present / Cannot add (not in experience) |
| ...                 | ...               | ... |

## 2. Cover Letter Draft

### Opening
Hook paragraph connecting personal motivation to company mission. Reference something specific about the company (recent news, product, value).

### Body
2-3 paragraphs mapping your strongest qualifications to the role's top requirements. Use specific examples.

### Close
Call to action, enthusiasm for next steps, thank you.

## 3. Interview Talking Points

### Why This Company?
- 3-4 specific, researched reasons

### Why This Role?
- 3-4 points connecting your experience to role requirements

### STAR Stories
Prepare 3 stories in Situation-Task-Action-Result format:

**Story 1: [Title]**
- **Situation:** ...
- **Task:** ...
- **Action:** ...
- **Result:** ... (quantified)

**Story 2: [Title]**
...

**Story 3: [Title]**
...

## 4. Networking Tips

### LinkedIn Connections
- Search for: [specific titles/departments to connect with]
- Mutual connections to leverage: [if discoverable]

### Outreach Template
> Hi [Name], I noticed you work on [team/product] at {COMPANY_NAME}. I'm applying for the {ROLE_TITLE} position and would love to hear about your experience there. Would you have 15 minutes for a quick chat? Thanks!

### Communities
- Relevant Slack/Discord communities
- Industry events or meetups
- Professional associations

## 5. Salary Research

| Source | Range | Notes |
|--------|-------|-------|
| Glassdoor | $X - $Y | Based on N reports |
| levels.fyi | $X - $Y | Total comp including equity |
| Payscale | $X - $Y | For location/experience |
| **Recommended Ask** | **$X** | Based on experience level |
| **Walk-Away Number** | **$X** | Minimum acceptable |

## 6. Application Checklist

- [ ] Submit tailored resume (PDF)
- [ ] Write cover letter (use draft above as starting point)
- [ ] Customize LinkedIn headline for this role
- [ ] Connect with 2-3 people at {COMPANY_NAME}
- [ ] Research interviewer backgrounds before each round
- [ ] Prepare 3 STAR stories (see above)
- [ ] Research recent company news before interview
- [ ] Prepare thoughtful questions to ask interviewer
- [ ] Send thank-you email within 24 hours of interview
```

Save to: `~/CareerOS/output/{COMPANY_SLUG}/{COMPANY_SLUG}_application_strategy.md`

## Step 6: Update Application Tracker

Read `~/CareerOS/tracker.md`. If it doesn't exist or is empty, create it with the header row. Append a new row:

```
| {today's date} | {COMPANY_NAME} | {ROLE_TITLE} | Applied | resume_{COMPANY_SLUG}_{DATE_STAMP}.md | {COMPANY_SLUG}_application_strategy.md | |
```

## Step 7: Display Summary

Print a concise summary:

```
## Application Package Ready

**Company:** {COMPANY_NAME}
**Role:** {ROLE_TITLE}

### Files Created
- `output/{COMPANY_SLUG}/resume_{COMPANY_SLUG}_{DATE_STAMP}.md`
- `output/{COMPANY_SLUG}/{COMPANY_SLUG}_application_strategy.md`

### Key Keywords Added
- keyword1, keyword2, keyword3, ...

### Salary Range
- Market: $X - $Y
- Recommended ask: $X

### Next Steps
Run `bash scripts/run-apply.sh` to generate PDFs and open the output folder.
```

**IMPORTANT:** Do NOT generate PDFs. The shell script `run-apply.sh` handles PDF generation after this command finishes. Only write the markdown files and display the summary.
