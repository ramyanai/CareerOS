---
description: Process multiple job descriptions from JD_CURRENT.txt and generate application packages for each
allowed-tools: Read, Write, Bash(*), WebSearch, WebFetch, Glob, Edit
model: opus
---

# /batch — Batch Job Application Processing

You are a career strategist and resume optimization expert. Your job is to process multiple job descriptions from a single file and generate a complete application package for each.

## Step 1: Read Source Resume

Run:
```bash
python3 scripts/read-resume.py
```

Parse `CANDIDATE_NAME` from the first line (`NAME: First Last`). Save the full resume text for reuse across all JDs.

If the script fails, tell the user to place their resume in `documents/resume/` and stop.

## Step 2: Read and Parse JD_CURRENT.txt

### File Location

Read the file at `job-descriptions/JD_CURRENT.txt`.

**If the file doesn't exist or is empty (or contains only the template instructions):**
- Check if `job-descriptions/JD_CURRENT.rtf` exists. If so, convert it:
  ```bash
  textutil -convert txt job-descriptions/JD_CURRENT.rtf -output job-descriptions/JD_CURRENT.txt
  ```
  Then read the converted `.txt` file.
- If neither exists or both are empty, tell the user:
  ```
  No job descriptions found. Paste JDs into job-descriptions/JD_CURRENT.txt
  separated by === COMPANY NAME === markers, then re-run /batch.
  ```
  Stop here.

### Parsing Rules

Split the file by `=== ... ===` markers. Each marker defines the start of a new JD.

**Marker format:** `=== COMPANY NAME ===` or `=== COMPANY NAME | ROLE TITLE ===`

- Text before the first marker is ignored (instructions/comments)
- Everything between two markers (or between the last marker and EOF) is one JD
- Blank lines within a JD are preserved (they're part of the JD text)
- If the marker includes `|`, split into company name and role title
- If the marker has no `|`, extract the role title from the JD content

For each parsed JD, store:
- `COMPANY_NAME` — display name from marker
- `COMPANY_SLUG` — lowercase, hyphens for spaces
- `ROLE_TITLE` — from marker (after `|`) or extracted from JD content
- `ROLE_SLUG` — lowercase, hyphens for spaces, truncated to key words
- `JD_TEXT` — full job description text
- `DATE_STAMP` — today in YYYY-MM-DD format

## Step 3: Display Batch Plan and Confirm

Show the user what was parsed:

```
## Batch Processing Plan

Found N job descriptions in JD_CURRENT.txt:

| # | Company | Role |
|---|---------|------|
| 1 | Adobe | AI Evangelist |
| 2 | Google | Senior PM |
| ... | ... | ... |

Proceed with all N applications?
```

Wait for user confirmation before continuing. If the user wants to skip any, note which ones.

## Step 4: Process Each JD

Process each JD **sequentially**, reusing the same source resume text from Step 1.

For each JD, print progress:
```
---
[2/5] Processing Adobe — AI Evangelist...
---
```

Then follow the exact same steps as `/apply`:

### Step 4a: Research the Company (same as /apply Step 3)

Use WebSearch to gather:
1. Company overview — what they do, size, industry, headquarters
2. Culture and values — from careers page, Glassdoor reviews, LinkedIn
3. Recent news — last 3-6 months
4. Tech stack / tools — if applicable
5. Salary data — from Glassdoor, levels.fyi, Payscale

### Step 4b: Generate Tailored Resume (same as /apply Step 4)

Create tailored resume markdown following ALL the same rules:

**Tailoring Rules (Non-Negotiable):**
1. **No new facts**: Every company name, job title, date, degree, metric must exist in source
2. **No new skills from thin air**: Must exist in source or be clearly inferable
3. **Reframing only**: Change verbs/order, never add substance
4. **Keyword handling**: If JD keyword can't be mapped, mark as gap — never force-fit
5. **Quantification**: Only use numbers from source

**ATS Formatting:** Standard headings (Summary, Experience, Education, Skills), no tables, contact info plain text, reverse chronological, keywords in context.

Save to: `output/{COMPANY_SLUG}/{CANDIDATE_NAME_SLUG}_{COMPANY_SLUG}_{ROLE_SLUG}_{YYYY-MM-DD}.md`

Create the output directory:
```bash
mkdir -p output/{COMPANY_SLUG}
```

### Step 4c: Verify Resume Integrity (same as /apply Step 4.5)

Line-by-line verification:
1. For EACH bullet: confirm it maps to source
2. For EACH skill: confirm it exists in source or is inferable
3. Check: no new company names, titles, dates, degrees
4. If any line fails: rewrite to be traceable
5. Only save after verification passes

### Step 4d: Generate Application Strategy (same as /apply Step 5)

Create the 8-section strategy document:
1. Keyword Gap Analysis (color-coded table with match score)
2. Cover Letter Draft (opening, body, close)
3. Interview Talking Points (why company, why role, 3 STAR stories)
4. Networking Tips (LinkedIn, outreach template, communities)
5. Salary Research (multi-source table with recommended ask)
6. Application Checklist
7. Interview Preparation (predicted questions with frameworks)
8. Follow-Up Email Templates (thank you, follow-up, negotiation, acceptance, decline)

Save to: `output/{COMPANY_SLUG}/{CANDIDATE_NAME_SLUG}_{COMPANY_SLUG}_{ROLE_SLUG}_Strategy_{YYYY-MM-DD}.md`

### Step 4e: Generate Change Log (same as /apply Step 5.5)

Document every modification: original vs tailored text, change type, reason.

Save to: `output/{COMPANY_SLUG}/{CANDIDATE_NAME_SLUG}_{COMPANY_SLUG}_{ROLE_SLUG}_Changes_{YYYY-MM-DD}.md`

### Step 4f: Update Application Tracker (same as /apply Step 6)

Read `tracker.md`. Append a new row for this application:
```
| {today's date} | {COMPANY_NAME} | {ROLE_TITLE} | Applied | {today's date} | {FOLLOW_UP_DATE} | {resume filename} | {strategy filename} | |
```

Where `FOLLOW_UP_DATE` = today + 7 days.

If tracker doesn't exist or is empty, create with 9-column header. Handle old 7-column format migration.

## Step 5: Verify All Outputs

After processing all JDs, verify that each expected output directory exists and contains the required files:

```bash
ls output/{COMPANY_SLUG}/
```

For each company, confirm:
- Resume markdown exists
- Strategy markdown exists
- Changes markdown exists

Report any missing files.

## Step 6: Archive JD_CURRENT.txt

After all JDs are processed:

1. Determine archive filename: `job-descriptions/JD_Archive_YYYY-MM-DD.txt` (using today's date in ISO 8601)

2. If the archive file already exists (user ran /batch twice today), **append** with a separator:
   ```
   \n\n--- Batch 2 ---\n\n
   ```
   Then append the contents of JD_CURRENT.txt.

3. If the archive doesn't exist, **copy** JD_CURRENT.txt to the archive filename.

4. **Clear** JD_CURRENT.txt to empty (write an empty string — don't delete the file so it stays for reuse).

## Step 7: Display Batch Summary

Print a summary table:

```
## Batch Complete

Processed N/N applications successfully.

| # | Company | Role | Match Score | Files | Output |
|---|---------|------|-------------|-------|--------|
| 1 | Adobe | AI Evangelist | 18/22 (82%) | 3 | output/adobe/ |
| 2 | Google | Senior PM | 15/20 (75%) | 3 | output/google/ |

### Archived
- JD_CURRENT.txt → JD_Archive_YYYY-MM-DD.txt
- JD_CURRENT.txt cleared for reuse

### Next Steps
Run `bash scripts/run-batch.sh` to generate PDFs + DOCX for all applications.
```

**IMPORTANT:** Do NOT generate PDFs or DOCX files. The shell script `run-batch.sh` handles all document generation after this command finishes. Only write the markdown files and display the summary.
