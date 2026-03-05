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
- `ROLE_SLUG` — normalized: lowercase, hyphens for spaces, truncated to key words (e.g., "senior-pm")
- `DATE_STAMP` — today in YYYY-MM-DD format
- `CANDIDATE_NAME` — extracted from resume filename (see Step 2)

## Step 2: Read Source Resume

Run:
```bash
python3 ~/CareerOS/scripts/read-resume.py
```

This extracts text from the user's resume in `documents/resume/`. The first line of output will be `NAME: First Last` if the filename follows the `{Name}_Master_*` pattern. Parse and store this as `CANDIDATE_NAME`.

If `CANDIDATE_NAME` is empty (old-format filename), extract the name from the resume content's first heading.

Save the full resume text (after the NAME line) for use in later steps.

If the script fails, tell the user to place their resume file there and stop.

## Step 3: Research the Company

Use WebSearch to gather:
1. **Company overview** — what they do, size, industry, headquarters
2. **Culture and values** — from careers page, Glassdoor reviews, LinkedIn
3. **Recent news** — last 3-6 months of notable events, product launches, funding
4. **Tech stack / tools** — if applicable to the role (from job posts, StackShare, engineering blogs)
5. **Salary data** — from Glassdoor, levels.fyi, Payscale for this specific role and location

Take notes on what you find — you'll use this in the strategy document.

## Step 4: Generate Tailored Resume

Create a tailored resume markdown file.

### Tailoring Rules (Non-Negotiable)

1. **No new facts**: Every company name, job title, date, degree, and metric in the output MUST exist in the source resume. If the source says "improved efficiency," you CANNOT write "improved efficiency by 40%."
2. **No new skills from thin air**: Skills listed must exist in the source OR be clearly inferable (e.g., source has "AWS, GCP" -> "Cloud Architecture" is OK. Source has nothing about containers -> "Kubernetes" is NOT OK).
3. **Reframing is not fabrication**: You may change verbs, reorder bullets, adjust framing. You may NOT add substance that wasn't there.
4. **Keyword handling**: If a JD keyword cannot be honestly mapped to existing experience, mark it "Gap — not in experience" in the Keyword Gap Analysis. NEVER force-fit it into the resume.
5. **Quantification rule**: Only use numbers that appear in the source. If the source has no metrics for a bullet, do not invent them.

### ATS Formatting Rules

- Section headings MUST be standard: "Summary", "Experience", "Education", "Skills" — no creative alternatives
- No tables, columns, or multi-column layouts in the resume
- Contact info as plain text at the top (never in headers/footers)
- Reverse chronological order strictly enforced
- Keywords must appear in context (inside achievement bullets), not just dumped in a skills list
- Each JD keyword should appear at least once in a bullet AND once in the skills section where possible

### Resume Content Rules

- **Reorder bullets** to lead with experiences most relevant to the JD
- **Mirror JD keywords** naturally in bullet points (don't keyword-stuff)
- **Adjust the summary/objective** to align with this specific role
- **Quantify achievements** where possible — but ONLY with numbers from the source
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

Save to: `~/CareerOS/output/{COMPANY_SLUG}/{CANDIDATE_NAME_SLUG}_{COMPANY_SLUG}_{ROLE_SLUG}_{YYYY-MM-DD}.md`

Where `CANDIDATE_NAME_SLUG` is the candidate's name with underscores (e.g., "Ram_Yanamandra").

Create the output directory if it doesn't exist:
```bash
mkdir -p ~/CareerOS/output/{COMPANY_SLUG}
```

## Step 4.5: Verify Resume Integrity

Before saving the tailored resume, perform a line-by-line verification:

1. Read the source resume text (from Step 2) and the tailored resume you just wrote
2. For EACH bullet in the tailored resume, confirm it maps to a specific bullet or fact in the source
3. For EACH skill listed, confirm it exists in the source or is directly inferable (document the inference)
4. Check: no new company names, job titles, dates, or degrees were added
5. If ANY line fails verification, rewrite it to be traceable to the source
6. Only after verification passes, save the file

If you had to fix any lines, note them — they'll go in the change log.

## Step 5: Generate Application Strategy Document

Create a comprehensive strategy document with these 8 sections:

### Strategy Markdown Format
```markdown
# Application Strategy: {COMPANY_NAME} — {ROLE_TITLE}

*Generated {today's date}*

## 1. Keyword Gap Analysis

| JD Keyword / Phrase | Found in Resume? | Action Taken |
|---------------------|-------------------|--------------|
| keyword from JD     | Yes / No / Partial | Added to bullet X / Already present / Reframed / Gap — not in experience |
| ...                 | ...               | ... |

**Match Score: X/Y keywords addressed (Z%)**

## 2. Cover Letter Draft

### Opening
Hook paragraph connecting personal motivation to company mission. Reference something specific about the company (recent news, product, value).

### Body
2-3 paragraphs mapping your strongest qualifications to the role's top requirements. Use specific examples.

### Close
Call to action, enthusiasm for next steps, thank you.

Signed:
{CANDIDATE_NAME}

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

- [ ] Submit tailored resume (PDF + DOCX)
- [ ] Submit cover letter (PDF + DOCX)
- [ ] Review change log for accuracy
- [ ] Customize LinkedIn headline for this role
- [ ] Connect with 2-3 people at {COMPANY_NAME}
- [ ] Research interviewer backgrounds before each round
- [ ] Prepare 3 STAR stories (see above)
- [ ] Prepare behavioral question responses (see Section 7)
- [ ] Research recent company news before interview
- [ ] Prepare thoughtful questions to ask interviewer
- [ ] Send thank-you email within 24 hours of interview (see Section 8)

## 7. Interview Preparation

### Predicted Behavioral Questions
5-7 questions based on JD requirements, each with a response framework:

**Q: "Tell me about a time you [JD requirement]"**
- Lead with: [specific experience from resume]
- Pivot to: [relevant skill/outcome]
- Close with: [quantified result or lesson]

(Repeat for each predicted question)

### Technical / Domain Questions
3-5 questions specific to the role's technical requirements, with brief answer frameworks.

### Questions to Ask Them
5 smart questions tailored to company/role (not generic). Examples:
- Questions about team structure, growth plans, challenges
- Questions that demonstrate research (reference recent news/launches)
- Questions about success metrics for the role

## 8. Follow-Up Email Templates

### Post-Interview Thank You (send within 24 hours)
Subject: Thank you — {ROLE_TITLE} interview

Hi [Interviewer Name],

Thank you for taking the time to speak with me today about the {ROLE_TITLE} role. I especially enjoyed our discussion about [specific topic from interview].

[1-2 sentences reinforcing fit, referencing something discussed]

I'm very excited about the opportunity to [specific contribution]. Please don't hesitate to reach out if you need any additional information.

Best regards,
{CANDIDATE_NAME}

### "Haven't Heard Back" Follow-Up (1 week after interview)
Subject: Following up — {ROLE_TITLE} application

Hi [Recruiter/Hiring Manager Name],

I hope this message finds you well. I wanted to follow up on my application for the {ROLE_TITLE} position. I remain very enthusiastic about the opportunity and would welcome the chance to discuss how my experience in [key area] can contribute to [team/goal].

Please let me know if there's any additional information I can provide.

Best regards,
{CANDIDATE_NAME}

### Negotiation Response (counter-offer template)
Subject: Re: {ROLE_TITLE} Offer

Hi [Name],

Thank you for the offer — I'm excited about joining {COMPANY_NAME}. After reviewing the details and considering [market data / competing offers / scope of the role], I'd like to discuss [base salary / equity / sign-on / start date].

Based on my research and experience level, I was hoping for [specific number/range]. I believe this reflects [reasoning].

I'm confident we can find an arrangement that works for both sides. Looking forward to discussing further.

Best regards,
{CANDIDATE_NAME}

### Acceptance Email
Subject: Accepting the {ROLE_TITLE} offer

Hi [Name],

I'm thrilled to formally accept the offer for the {ROLE_TITLE} position at {COMPANY_NAME}. I appreciate the team's time throughout the interview process and I'm excited to contribute to [specific goal/team].

Please let me know the next steps for onboarding. I'm looking forward to starting on [date].

Best regards,
{CANDIDATE_NAME}

### Decline Email (professional bridge-keeping)
Subject: Re: {ROLE_TITLE} Offer

Hi [Name],

Thank you so much for the offer to join {COMPANY_NAME} as {ROLE_TITLE}. After careful consideration, I've decided to pursue another opportunity that more closely aligns with my current career goals.

I have a great deal of respect for what {COMPANY_NAME} is building, and I hope our paths cross again in the future. Thank you for your time and consideration throughout the process.

Best regards,
{CANDIDATE_NAME}
```

Save to: `~/CareerOS/output/{COMPANY_SLUG}/{CANDIDATE_NAME_SLUG}_{COMPANY_SLUG}_{ROLE_SLUG}_Strategy_{YYYY-MM-DD}.md`

## Step 5.5: Generate Change Log

Create a change log documenting every modification made to the resume:

### Change Log Format
```markdown
# Change Log: {CANDIDATE_NAME} — {COMPANY_NAME} {ROLE_TITLE}

*Generated {today's date}*

## Summary

- **Bullets reworded:** N
- **Bullets reordered:** N
- **Bullets unchanged:** N
- **Skills kept as-is:** N
- **Skills consolidated/reframed:** N
- **Keywords addressed:** X/Y (Z%)
- **Gaps identified:** N

## Section-by-Section Changes

### Summary
| Original | Tailored | Change Type | Reason |
|----------|----------|-------------|--------|
| Original summary text | New summary text | Reworded | Aligned to JD emphasis on X |

### Experience — {Job Title at Company}
| Original Bullet | Tailored Bullet | Change Type | Reason |
|-----------------|-----------------|-------------|--------|
| Original text   | Tailored text   | Reworded / Reordered / Unchanged | Keyword "X" from JD / Prioritized for relevance |

(Repeat for each job in Experience)

### Skills
| Skill | Status | Notes |
|-------|--------|-------|
| Skill A | Kept | Already matches JD |
| Skill B | Consolidated | Combined "X" and "Y" into "Z" |
| Skill C | Gap | JD requires it, not in experience — listed in gap analysis |

## Verification Notes

- All company names verified against source: PASS
- All dates verified against source: PASS
- All metrics verified against source: PASS
- No fabricated skills: PASS
- Lines corrected during verification: N (list if any)
```

Save to: `~/CareerOS/output/{COMPANY_SLUG}/{CANDIDATE_NAME_SLUG}_{COMPANY_SLUG}_{ROLE_SLUG}_Changes_{YYYY-MM-DD}.md`

## Step 6: Update Application Tracker

Read `~/CareerOS/tracker.md`. If it doesn't exist or is empty, create it with the 9-column header:

```
# Application Tracker

| Date | Company | Role | Status | Last Updated | Follow-Up Due | Resume | Strategy | Notes |
|------|---------|------|--------|--------------|---------------|--------|----------|-------|
```

If the file exists with the old 7-column format (no `Last Updated` / `Follow-Up Due` columns), upgrade the header to 9 columns and backfill existing rows: set `Last Updated` to their `Date` value and `Follow-Up Due` to empty.

Calculate `FOLLOW_UP_DATE` as today's date + 7 days (YYYY-MM-DD format).

Append a new row:

```
| {today's date} | {COMPANY_NAME} | {ROLE_TITLE} | Applied | {today's date} | {FOLLOW_UP_DATE} | {CANDIDATE_NAME_SLUG}_{COMPANY_SLUG}_{ROLE_SLUG}_{YYYY-MM-DD}.md | {CANDIDATE_NAME_SLUG}_{COMPANY_SLUG}_{ROLE_SLUG}_Strategy_{YYYY-MM-DD}.md | |
```

## Step 7: Generate Documents

Run the document generation pipeline:
```bash
bash ~/CareerOS/scripts/run-apply.sh {COMPANY_SLUG}
```

This generates PDF + DOCX files for the resume, strategy, cover letter, and change log, then opens the output folder in Finder. Since the output directory already exists, `run-apply.sh` skips the `/apply` step and goes straight to document generation.

## Step 8: Display Summary

Print a concise summary:

```
## Application Package Ready

**Company:** {COMPANY_NAME}
**Role:** {ROLE_TITLE}
**Candidate:** {CANDIDATE_NAME}

### Files Created
- Resume: `output/{COMPANY_SLUG}/` (MD + PDF + DOCX)
- Strategy: `output/{COMPANY_SLUG}/` (MD + PDF)
- Change Log: `output/{COMPANY_SLUG}/` (MD + PDF)
- Cover Letter: `output/{COMPANY_SLUG}/` (PDF + DOCX)

### Match Score
- X/Y JD keywords addressed (Z%)

### Salary Range
- Market: $X - $Y
- Recommended ask: $X
```
