#!/bin/bash
# CareerOS Quick-Start Setup
# Installs dependencies and creates directory structure

set -e

echo "=== CareerOS Setup ==="
echo ""

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Install it from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python 3 found: $PYTHON_VERSION"

# Check Claude Code
if command -v claude &>/dev/null; then
    echo "Claude Code found: $(claude --version 2>/dev/null || echo 'installed')"
else
    echo "Warning: Claude Code not found. Install it with:"
    echo "  npm install -g @anthropic-ai/claude-code"
    echo ""
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install fpdf2 python-docx PyMuPDF markdown

echo ""
echo "Installing optional dependencies (pipeline dashboard)..."
pip3 install streamlit pandas 2>/dev/null || echo "Optional: streamlit/pandas not installed. Pipeline dashboard won't work, but everything else will."

# Create directory structure
echo ""
echo "Creating directory structure..."
mkdir -p documents/resume
mkdir -p job-descriptions
mkdir -p output

# Create tracker if it doesn't exist
if [ ! -f tracker.md ]; then
    echo "Creating application tracker..."
    cat > tracker.md << 'TRACKER'
# Application Tracker

| Date | Company | Role | Status | Last Updated | Follow-Up Due | Resume | Strategy | Notes |
|------|---------|------|--------|--------------|---------------|--------|----------|-------|
TRACKER
fi

# Create .env template if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env template..."
    cat > .env << 'ENVFILE'
# CareerOS Environment Variables (optional)
# RESEND_API_KEY=your-key-here
ENVFILE
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Place your master resume in documents/resume/"
echo "     Naming: YourName_Master_YYYY-MM-DD.md (e.g., Jane_Doe_Master_2026-03-04.md)"
echo ""
echo "  2. Make sure you have a Claude Pro/Max subscription (usage included)"
echo "     Or set an API key: export ANTHROPIC_API_KEY=\"your-key-here\""
echo ""
echo "  3. Run your first application:"
echo "     cd $(pwd)"
echo "     claude"
echo "     /apply CompanyName"
echo ""
echo "  For a sample resume format, see:"
echo "     documents/resume/EXAMPLE_Master_Resume.md"
echo ""
