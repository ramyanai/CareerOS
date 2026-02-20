#!/bin/bash
set -e

# CareerOS apply pipeline: /apply command → PDFs → open Finder
# Usage: bash scripts/run-apply.sh "CompanyName"

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

echo "=== Generating PDFs in $LATEST_DIR ==="

# Generate resume PDF
RESUME_MD=$(ls -t "$LATEST_DIR"resume_*.md 2>/dev/null | head -1)
if [ -n "$RESUME_MD" ]; then
    echo "Resume PDF:"
    python3 scripts/generate-resume-pdf.py "$RESUME_MD"
else
    echo "Warning: No resume markdown found in $LATEST_DIR"
fi

# Generate strategy PDF
STRATEGY_MD=$(ls -t "$LATEST_DIR"*_application_strategy.md 2>/dev/null | head -1)
if [ -n "$STRATEGY_MD" ]; then
    echo "Strategy PDF:"
    python3 scripts/generate-strategy-pdf.py "$STRATEGY_MD"
else
    echo "Warning: No strategy markdown found in $LATEST_DIR"
fi

echo "=== Opening output folder ==="
open "$LATEST_DIR"

echo "=== Done ==="
