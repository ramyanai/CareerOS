#!/bin/bash
set -e

# CareerOS apply pipeline: /apply command -> PDFs + DOCX -> open Finder
# Usage: bash scripts/run-apply.sh "CompanyName"
#    or: bash scripts/run-apply.sh /path/to/job-description.txt

export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
cd /Users/ramyanair/CareerOS

# Source .env if it exists (optional, for email support)
if [ -f .env ]; then
    source .env
fi

ARGS="$*"
if [ -z "$ARGS" ]; then
    echo "Usage: bash scripts/run-apply.sh \"CompanyName\""
    echo "   or: bash scripts/run-apply.sh /path/to/job-description.txt"
    exit 1
fi

echo "=== CareerOS: Running /apply $ARGS ==="
claude -p "/apply $ARGS"

# Find the most recently modified output directory
LATEST_DIR=$(ls -td output/*/ 2>/dev/null | head -1)
if [ -z "$LATEST_DIR" ]; then
    echo "Error: No output directory found"
    exit 1
fi

echo "=== Generating documents in $LATEST_DIR ==="

# --- Resume PDF ---
# Try new naming pattern first (*_YYMMDD.md without Strategy/Changes/CoverLetter)
RESUME_MD=$(ls -t "$LATEST_DIR"*.md 2>/dev/null | grep -v -E '(Strategy|Changes|CoverLetter|application_strategy)' | head -1)
# Fall back to old naming
if [ -z "$RESUME_MD" ]; then
    RESUME_MD=$(ls -t "$LATEST_DIR"resume_*.md 2>/dev/null | head -1)
fi

if [ -n "$RESUME_MD" ]; then
    echo "Resume PDF:"
    python3 scripts/generate-resume-pdf.py "$RESUME_MD"
    echo "Resume DOCX:"
    python3 scripts/generate-resume-docx.py "$RESUME_MD"
else
    echo "Warning: No resume markdown found in $LATEST_DIR"
fi

# --- Strategy PDF ---
# Try new naming pattern first (*_Strategy_*.md)
STRATEGY_MD=$(ls -t "$LATEST_DIR"*_Strategy_*.md 2>/dev/null | head -1)
# Fall back to old naming
if [ -z "$STRATEGY_MD" ]; then
    STRATEGY_MD=$(ls -t "$LATEST_DIR"*_application_strategy.md 2>/dev/null | head -1)
fi

if [ -n "$STRATEGY_MD" ]; then
    echo "Strategy PDF:"
    python3 scripts/generate-strategy-pdf.py "$STRATEGY_MD"

    # --- Cover Letter PDF + DOCX (extracted from strategy) ---
    echo "Cover Letter PDF:"
    python3 scripts/generate-cover-letter-pdf.py "$STRATEGY_MD"
    echo "Cover Letter DOCX:"
    python3 scripts/generate-cover-letter-docx.py "$STRATEGY_MD"
else
    echo "Warning: No strategy markdown found in $LATEST_DIR"
fi

# --- Summary ---
echo ""
echo "=== Output files ==="
ls -la "$LATEST_DIR"
echo ""

echo "=== Opening output folder ==="
open "$LATEST_DIR"

echo "=== Done ==="
