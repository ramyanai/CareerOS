---
description: Update application status in tracker.md
allowed-tools: Read, Edit, Bash(date*)
argument-hint: <company> <new status> (e.g., "Anthropic Screened")
---

# /status — Update Application Status

You update the status of an application in `tracker.md` and set follow-up dates.

## Step 1: Get Today's Date

Run `date +%Y-%m-%d` to get today's date. Store as `TODAY`.

## Step 2: Parse Arguments

Parse `$ARGUMENTS` to extract:
- **Company name** — everything before the last word
- **New status** — the last word

Valid statuses (case-insensitive, normalize to title case):
- `Applied`, `Screened`, `Interviewing`, `Offer`, `Accepted`, `Rejected`, `Withdrawn`, `Ghosted`

If `$ARGUMENTS` is empty or doesn't contain a valid status as the last word, ask the user:
"Usage: `/status <company> <new status>`\nExample: `/status Anthropic Screened`\nValid statuses: Applied, Screened, Interviewing, Offer, Accepted, Rejected, Withdrawn, Ghosted"

## Step 3: Read Tracker

Read `tracker.md`.

If the file doesn't exist or is empty, tell the user: "No tracker.md found. Run `/apply` first." and stop.

## Step 4: Find Matching Row

Search for a row where the Company column matches the user's input. Use case-insensitive fuzzy matching:
- Exact match first (case-insensitive)
- Then substring match (e.g., "anthro" matches "Anthropic")

If no match found, list all companies in the tracker and ask the user to clarify.
If multiple matches found, list them and ask the user to be more specific.

## Step 5: Update the Row

Detect the tracker format (7-column vs 9-column) by counting columns in the header.

### For 9-column format:
Update these columns in the matched row:
- **Status** → new status
- **Last Updated** → `TODAY`
- **Follow-Up Due** → calculated based on new status:
  - Applied → TODAY + 7 days
  - Screened → TODAY + 3 days
  - Interviewing → TODAY + 1 day (send thank-you)
  - Offer → TODAY + 3 days (respond to offer)
  - Accepted → (leave empty — no follow-up needed)
  - Rejected → (leave empty)
  - Withdrawn → (leave empty)
  - Ghosted → (leave empty)

### For 7-column format:
Upgrade the row to 9-column format:
1. Update the header to add `Last Updated` and `Follow-Up Due` columns (and separator row)
2. Update existing rows: set Last Updated = their Date, Follow-Up Due = (empty for past entries)
3. Update the matched row with the new status, Last Updated = TODAY, Follow-Up Due as above

Use the Edit tool to make the changes in `tracker.md`.

## Step 6: Confirm Update

Print:

```
## Status Updated

**{Company}** — {Role}
  {Old Status} → **{New Status}**
  Last Updated: {TODAY}
  Follow-Up Due: {Follow-Up Date or "None"}

### Next Action
{Context-specific reminder based on new status}
```

Next action reminders by status:
- **Screened** → "Prepare your STAR stories and review the strategy doc. Interview scheduling likely coming soon."
- **Interviewing** → "Send a thank-you email within 24 hours. Check your strategy doc Section 8 for templates."
- **Offer** → "Review the salary research in your strategy doc Section 5. Respond within 3 days."
- **Accepted** → "Congratulations! Send a gracious decline to any other active applications."
- **Rejected** → "Send a professional bridge-keeping email. Check strategy doc Section 8 for the template."
- **Withdrawn** → "Send a professional withdrawal notice if you haven't already."
- **Ghosted** → "Consider sending one final follow-up, then move on. Focus on active applications."
- **Applied** → "Follow up in 7 days if you haven't heard back."
