#!/usr/bin/env python3
"""Streamlit pipeline dashboard for CareerOS application tracking.

Parses tracker.md and displays funnel chart, timeline, salary comparison,
follow-up alerts, and status breakdown.

Launch: python3 -m streamlit run scripts/pipeline-dashboard.py --server.port 8505
"""

import os
import re
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# Find tracker.md relative to this script's location (project root)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(_SCRIPT_DIR)
TRACKER_PATH = os.path.join(_PROJECT_DIR, "tracker.md")

# Status colors
STATUS_COLORS = {
    "Applied": "#3b82f6",       # blue
    "Screened": "#8b5cf6",      # purple
    "Interviewing": "#f59e0b",  # amber
    "Offer": "#10b981",         # green
    "Accepted": "#059669",      # dark green
    "Rejected": "#ef4444",      # red
    "Withdrawn": "#6b7280",     # gray
    "Ghosted": "#9ca3af",       # light gray
}

# Funnel order (top to bottom)
FUNNEL_ORDER = ["Applied", "Screened", "Interviewing", "Offer", "Accepted"]
TERMINAL_STATUSES = ["Rejected", "Withdrawn", "Ghosted"]


def parse_tracker(path):
    """Parse tracker.md into a DataFrame. Handles 7-column and 9-column formats."""
    if not os.path.exists(path):
        return pd.DataFrame()

    with open(path, "r") as f:
        lines = f.readlines()

    # Find header row (starts with |)
    header_line = None
    data_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|") and "Date" in stripped and "Company" in stripped:
            header_line = i
            # Skip separator row (|---|---|...)
            data_start = i + 2
            break

    if header_line is None:
        return pd.DataFrame()

    # Parse header
    headers = [h.strip() for h in lines[header_line].strip().strip("|").split("|")]
    is_9col = len(headers) >= 9

    rows = []
    for i in range(data_start, len(lines)):
        line = lines[i].strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]

        if is_9col and len(cells) >= 9:
            rows.append({
                "Date": cells[0],
                "Company": cells[1],
                "Role": cells[2],
                "Status": cells[3],
                "Last Updated": cells[4],
                "Follow-Up Due": cells[5],
                "Resume": cells[6],
                "Strategy": cells[7],
                "Notes": cells[8] if len(cells) > 8 else "",
            })
        elif len(cells) >= 7:
            rows.append({
                "Date": cells[0],
                "Company": cells[1],
                "Role": cells[2],
                "Status": cells[3],
                "Last Updated": cells[0],  # default to Date
                "Follow-Up Due": "",
                "Resume": cells[4],
                "Strategy": cells[5],
                "Notes": cells[6] if len(cells) > 6 else "",
            })

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # Parse dates
    for col in ["Date", "Last Updated", "Follow-Up Due"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def parse_salary(notes):
    """Extract salary range from notes. Returns (min, max) in thousands or (None, None)."""
    if not isinstance(notes, str):
        return None, None
    # Match patterns like $127K-$185K or $255K-$345K
    match = re.search(r"\$(\d+)K?\s*[-–]\s*\$(\d+)K?", notes)
    if match:
        lo = int(match.group(1))
        hi = int(match.group(2))
        # Normalize — if values are > 1000, they're already in dollars
        if lo > 1000:
            lo = lo // 1000
        if hi > 1000:
            hi = hi // 1000
        return lo, hi
    return None, None


def main():
    st.set_page_config(
        page_title="CareerOS Pipeline",
        page_icon="📊",
        layout="wide",
    )

    st.title("CareerOS — Application Pipeline")

    df = parse_tracker(TRACKER_PATH)
    if df.empty:
        st.warning("No applications found. Run `/apply` to add your first application.")
        return

    today = datetime.now().date()
    st.caption(f"{len(df)} applications tracked | As of {today}")

    # -- Row 1: Funnel + Status Breakdown --
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Funnel")
        status_counts = df["Status"].value_counts()

        # Funnel bars
        for status in FUNNEL_ORDER:
            count = status_counts.get(status, 0)
            if count == 0:
                continue
            color = STATUS_COLORS.get(status, "#6b7280")
            pct = f" ({count * 100 // len(df)}%)" if len(df) > 0 else ""
            st.markdown(
                f'<div style="display:flex;align-items:center;margin-bottom:4px;">'
                f'<span style="width:100px;font-weight:600;">{status}</span>'
                f'<div style="background:{color};height:24px;width:{max(count * 60, 30)}px;'
                f'border-radius:4px;display:flex;align-items:center;padding-left:8px;'
                f'color:white;font-size:14px;">{count}{pct}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        for status in TERMINAL_STATUSES:
            count = status_counts.get(status, 0)
            if count == 0:
                continue
            color = STATUS_COLORS.get(status, "#6b7280")
            st.markdown(
                f'<div style="display:flex;align-items:center;margin-bottom:4px;">'
                f'<span style="width:100px;font-weight:600;">{status}</span>'
                f'<div style="background:{color};height:24px;width:{max(count * 60, 30)}px;'
                f'border-radius:4px;display:flex;align-items:center;padding-left:8px;'
                f'color:white;font-size:14px;">{count}</div></div>',
                unsafe_allow_html=True,
            )

    with col2:
        st.subheader("Status Breakdown")
        # Pie-style summary
        for status in FUNNEL_ORDER + TERMINAL_STATUSES:
            count = status_counts.get(status, 0)
            if count == 0:
                continue
            color = STATUS_COLORS.get(status, "#6b7280")
            st.markdown(
                f'<span style="color:{color};font-size:20px;">●</span> '
                f'**{status}**: {count}',
                unsafe_allow_html=True,
            )

    # -- Row 2: Follow-Up Alerts --
    st.subheader("Follow-Up Alerts")

    active_mask = ~df["Status"].isin(["Rejected", "Withdrawn", "Accepted", "Ghosted"])
    active = df[active_mask].copy()

    alerts = []
    for _, row in active.iterrows():
        app_date = row["Date"]
        if pd.isna(app_date):
            continue
        days_ago = (pd.Timestamp(today) - app_date).days
        status = row["Status"]
        company = row["Company"]
        role = row["Role"]

        # Check follow-up due
        followup_due = row.get("Follow-Up Due")
        overdue = False
        if pd.notna(followup_due) and followup_due.date() < today:
            overdue = True

        if status == "Applied" and days_ago > 7:
            alerts.append(("🔴", f"**{company}** — {role} — Applied {days_ago} days ago. Send follow-up email!" + (" ⚠️ OVERDUE" if overdue else "")))
        elif status == "Screened" and days_ago > 3:
            alerts.append(("🟡", f"**{company}** — {role} — Screened {days_ago} days ago. Follow up on interview scheduling."))
        elif status == "Interviewing" and days_ago > 3:
            alerts.append(("🟡", f"**{company}** — {role} — Interviewing {days_ago} days ago. Send thank-you if you haven't."))
        elif status == "Offer" and days_ago > 3:
            alerts.append(("🔴", f"**{company}** — {role} — Offer pending {days_ago} days. Respond soon!"))
        elif overdue:
            alerts.append(("🟡", f"**{company}** — {role} — Follow-up overdue (was due {followup_due.date()})."))

    if alerts:
        for emoji, msg in alerts:
            st.markdown(f"{emoji} {msg}")
    else:
        st.success("No overdue follow-ups!")

    # -- Row 3: Active Applications Table --
    st.subheader("Active Applications")
    if not active.empty:
        display_df = active[["Company", "Role", "Status", "Date", "Notes"]].copy()
        display_df["Days Ago"] = display_df["Date"].apply(
            lambda d: (pd.Timestamp(today) - d).days if pd.notna(d) else ""
        )
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        display_df = display_df[["Company", "Role", "Status", "Date", "Days Ago", "Notes"]]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No active applications.")

    # -- Row 4: Salary Comparison --
    salaries = []
    for _, row in df.iterrows():
        lo, hi = parse_salary(row.get("Notes", ""))
        if lo and hi:
            salaries.append({
                "Company": row["Company"],
                "Min ($K)": lo,
                "Max ($K)": hi,
                "Midpoint ($K)": (lo + hi) // 2,
            })

    if salaries:
        st.subheader("Salary Comparison")
        sal_df = pd.DataFrame(salaries)

        # Bar chart
        chart_df = sal_df.set_index("Company")[["Min ($K)", "Max ($K)"]]
        st.bar_chart(chart_df)

        # Summary stats
        all_min = min(s["Min ($K)"] for s in salaries)
        all_max = max(s["Max ($K)"] for s in salaries)
        avg_mid = sum(s["Midpoint ($K)"] for s in salaries) // len(salaries)
        st.markdown(f"**Range:** ${all_min}K – ${all_max}K | **Avg midpoint:** ${avg_mid}K")

    # -- Row 5: Timeline --
    st.subheader("Application Timeline")
    timeline_df = df[["Date", "Company", "Status"]].dropna(subset=["Date"]).copy()
    timeline_df = timeline_df.sort_values("Date")
    if not timeline_df.empty:
        timeline_df["Date_str"] = timeline_df["Date"].dt.strftime("%Y-%m-%d")
        for _, row in timeline_df.iterrows():
            color = STATUS_COLORS.get(row["Status"], "#6b7280")
            st.markdown(
                f'<span style="color:{color};font-size:16px;">●</span> '
                f'**{row["Date_str"]}** — {row["Company"]} ({row["Status"]})',
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
