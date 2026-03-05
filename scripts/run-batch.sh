#!/bin/bash
set -e

# CareerOS batch document generation: PDFs + DOCX for multiple companies
# Usage: bash scripts/run-batch.sh                    # Process all dirs modified today
#    or: bash scripts/run-batch.sh adobe google        # Process specific company slugs

export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
cd /Users/ramyanair/CareerOS

# Source .env if it exists (optional, for email support)
if [ -f .env ]; then
    source .env
fi

TODAY=$(date +%Y-%m-%d)
PROCESSED=0
FAILED=0

# Build list of directories to process
DIRS=()

if [ $# -gt 0 ]; then
    # Specific company slugs provided
    for SLUG in "$@"; do
        if [ -d "output/$SLUG" ]; then
            DIRS+=("output/$SLUG/")
        else
            echo "Warning: No output directory found for '$SLUG' — skipping"
            FAILED=$((FAILED + 1))
        fi
    done
else
    # Find all output directories with .md files modified today
    for DIR in output/*/; do
        [ -d "$DIR" ] || continue
        # Check if any .md files were modified today
        if find "$DIR" -maxdepth 1 -name "*.md" -newer /dev/null -newermt "$TODAY" -print -quit 2>/dev/null | grep -q .; then
            DIRS+=("$DIR")
        fi
    done
fi

if [ ${#DIRS[@]} -eq 0 ]; then
    echo "No output directories to process."
    echo "Usage: bash scripts/run-batch.sh              # All dirs modified today"
    echo "   or: bash scripts/run-batch.sh adobe google  # Specific company slugs"
    exit 0
fi

echo "=== CareerOS Batch Document Generation ==="
echo "Processing ${#DIRS[@]} director(ies)..."
echo ""

for DIR in "${DIRS[@]}"; do
    COMPANY=$(basename "$DIR")
    echo "--- [$((PROCESSED + 1))/${#DIRS[@]}] Generating documents for: $COMPANY ---"

    # --- Resume PDF + DOCX ---
    RESUME_MD=$(ls -t "$DIR"*.md 2>/dev/null | grep -v -E '(Strategy|Changes|CoverLetter|application_strategy)' | head -1)
    if [ -z "$RESUME_MD" ]; then
        RESUME_MD=$(ls -t "$DIR"resume_*.md 2>/dev/null | head -1)
    fi

    if [ -n "$RESUME_MD" ]; then
        echo "  Resume PDF:"
        python3 scripts/generate-resume-pdf.py "$RESUME_MD"
        echo "  Resume DOCX:"
        python3 scripts/generate-resume-docx.py "$RESUME_MD"
    else
        echo "  Warning: No resume markdown found in $DIR"
    fi

    # --- Strategy PDF ---
    STRATEGY_MD=$(ls -t "$DIR"*_Strategy_*.md 2>/dev/null | head -1)
    if [ -z "$STRATEGY_MD" ]; then
        STRATEGY_MD=$(ls -t "$DIR"*_application_strategy.md 2>/dev/null | head -1)
    fi

    if [ -n "$STRATEGY_MD" ]; then
        echo "  Strategy PDF:"
        python3 scripts/generate-strategy-pdf.py "$STRATEGY_MD"

        # --- Cover Letter PDF + DOCX ---
        echo "  Cover Letter PDF:"
        python3 scripts/generate-cover-letter-pdf.py "$STRATEGY_MD"
        echo "  Cover Letter DOCX:"
        python3 scripts/generate-cover-letter-docx.py "$STRATEGY_MD"
    else
        echo "  Warning: No strategy markdown found in $DIR"
    fi

    # --- Change Log PDF ---
    CHANGES_MD=$(ls -t "$DIR"*_Changes_*.md 2>/dev/null | head -1)
    if [ -n "$CHANGES_MD" ]; then
        echo "  Change Log PDF:"
        python3 scripts/generate-changelog-pdf.py "$CHANGES_MD"
    fi

    PROCESSED=$((PROCESSED + 1))
    echo "  Done: $DIR"
    echo ""
done

# --- Summary ---
echo "=== Batch Complete ==="
echo "Processed: $PROCESSED  |  Skipped: $FAILED"
echo ""
echo "Output directories:"
for DIR in "${DIRS[@]}"; do
    echo "  $DIR"
    ls -1 "$DIR" 2>/dev/null | sed 's/^/    /'
    echo ""
done

echo "=== Opening output folder ==="
open output/

echo "=== Done ==="
