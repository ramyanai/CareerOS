---
description: Show application pipeline funnel, follow-up alerts, and salary summary
allowed-tools: Read, Bash(*)
argument-hint: (no arguments needed)
---

# /pipeline — Application Pipeline Dashboard

You are a career pipeline analyst. Your job is to read the application tracker and display a comprehensive pipeline view with funnel metrics, follow-up alerts, and salary analysis.

## Step 1: Get Today's Date

Run `date +%Y-%m-%d` to get today's date. Store as `TODAY`.

## Step 2: Read Tracker

Read `~/CareerOS/tracker.md`.

If the file doesn't exist or has no data rows, tell the user: "No applications tracked yet. Run `/apply` to add your first application." and stop.

## Step 3: Parse Tracker Format

Handle both old (7-column) and new (9-column) formats:

**Old format (7 columns):**
```
| Date | Company | Role | Status | Resume | Strategy | Notes |
```

**New format (9 columns):**
```
| Date | Company | Role | Status | Last Updated | Follow-Up Due | Resume | Strategy | Notes |
```

Detect which format by counting columns in the header row. Parse each data row accordingly.

For old-format rows without `Last Updated` or `Follow-Up Due`, use `Date` as Last Updated and calculate Follow-Up Due as Date + 7 days.

## Step 4: Calculate Metrics

### Funnel Counts
Count applications by status. Valid statuses: `Applied`, `Screened`, `Interviewing`, `Offer`, `Accepted`, `Rejected`, `Withdrawn`, `Ghosted`.

### Conversion Rates
- Applied → Screened: (Screened + Interviewing + Offer + Accepted) / Total
- Screened → Interviewing: (Interviewing + Offer + Accepted) / (Screened + Interviewing + Offer + Accepted)
- Interviewing → Offer: (Offer + Accepted) / (Interviewing + Offer + Accepted)

Only show rates when the denominator > 0.

### Days Since Application
For each active application (not Rejected/Withdrawn/Accepted/Ghosted), calculate days since the Date column.

### Follow-Up Alerts
Flag applications needing attention:
- **Applied** > 7 days ago with no status change → "Send follow-up email"
- **Screened** > 3 days ago → "Prepare for interview, follow up if no scheduling"
- **Interviewing** > 3 days ago → "Send thank-you note if you haven't"
- **Offer** > 3 days ago → "Respond to offer soon"
- Any application past its Follow-Up Due date → "Follow-up overdue!"

### Salary Summary
Parse salary ranges from the Notes column. Look for patterns like `$XXK-$XXXK` or `$XXX,XXX`. Extract min and max values. Calculate:
- Range across all applications (lowest min to highest max)
- Average midpoint

## Step 5: Display Pipeline

Print the following output:

```
## Application Pipeline

*{N} applications tracked | As of {TODAY}*

### Funnel

Applied:        ████████ N
Screened:       ████     N  (XX%)
Interviewing:   ██       N  (XX%)
Offer:          █        N  (XX%)
Accepted:                N
---
Rejected:       ██       N
Withdrawn:      █        N
Ghosted:                 N
```

For the ASCII bars, use `█` characters. Scale so the largest count gets 8 blocks and others are proportional. Skip statuses with 0 count (except in the divider section).

```
### Follow-Up Alerts

🔴 {Company} — {Role} — Applied {N} days ago, no update. Send follow-up?
🟡 {Company} — {Role} — Screened {N} days ago. Follow up on interview scheduling.
✅ No overdue follow-ups! (if none)

### Active Applications

| Company | Role | Status | Applied | Days Ago | Follow-Up Due | Notes |
|---------|------|--------|---------|----------|---------------|-------|
| ...     | ...  | ...    | ...     | ...      | ...           | ...   |

Only show active applications (exclude Rejected, Withdrawn, Accepted, Ghosted).

### Salary Summary

- Range: $XXK – $XXXK (across all applications)
- Average midpoint: $XXXK
- Highest: {Company} at $XXXK
- Lowest: {Company} at $XXXK
```

If no salary data is found in Notes, skip this section.

```
### Visual Dashboard

For a visual dashboard with charts, run:
`python3 -m streamlit run ~/CareerOS/scripts/pipeline-dashboard.py --server.port 8505`
```
