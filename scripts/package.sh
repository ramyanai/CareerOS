#!/bin/bash
# CareerOS Distribution Packager
# Creates a clean .zip for Gumroad and GitHub release distribution
# Usage: bash scripts/package.sh [version]
# Example: bash scripts/package.sh 1.0.0

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

VERSION="${1:-1.0.0}"
PACKAGE_NAME="CareerOS-v${VERSION}"
BUILD_DIR="/tmp/${PACKAGE_NAME}"
ZIP_FILE="${PROJECT_DIR}/dist/${PACKAGE_NAME}.zip"

echo "=== CareerOS Packager ==="
echo "Version: $VERSION"
echo ""

# Clean previous build
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "${PROJECT_DIR}/dist"

# Copy distributable files
echo "Copying files..."

# Core files
cp README.md "$BUILD_DIR/"
cp README-gumroad.md "$BUILD_DIR/"
cp setup.sh "$BUILD_DIR/"
cp CLAUDE.md "$BUILD_DIR/"
cp .gitignore "$BUILD_DIR/"
cp LICENSE "$BUILD_DIR/" 2>/dev/null || true

# Commands
mkdir -p "$BUILD_DIR/.claude/commands"
cp .claude/commands/*.md "$BUILD_DIR/.claude/commands/"
cp .claude/settings.local.json "$BUILD_DIR/.claude/" 2>/dev/null || true

# Scripts
mkdir -p "$BUILD_DIR/scripts"
cp scripts/*.py "$BUILD_DIR/scripts/"
cp scripts/*.sh "$BUILD_DIR/scripts/"

# Empty directories with .gitkeep
mkdir -p "$BUILD_DIR/documents/resume"
mkdir -p "$BUILD_DIR/job-descriptions"
mkdir -p "$BUILD_DIR/output"
touch "$BUILD_DIR/documents/resume/.gitkeep"
touch "$BUILD_DIR/job-descriptions/.gitkeep"
touch "$BUILD_DIR/output/.gitkeep"

# Sample resume
cp documents/resume/EXAMPLE_Master_Resume.md "$BUILD_DIR/documents/resume/"

# Exclude personal data
echo "Excluding personal data..."
# No tracker.md (user creates via setup.sh)
# No .env (user creates via setup.sh)
# No output files
# No personal resumes
# No JD files (except template instruction)

# Remove hardcoded paths (safety check)
echo "Verifying no hardcoded paths..."
if grep -r "/Users/" "$BUILD_DIR" --include="*.sh" --include="*.py" --include="*.md" -l 2>/dev/null | grep -v package.sh; then
    echo "WARNING: Found hardcoded user paths in the above files!"
    echo "Fix these before distributing."
    exit 1
fi

# Create zip
echo "Creating archive..."
cd /tmp
zip -r "$ZIP_FILE" "$PACKAGE_NAME" -x "*.DS_Store" "*__pycache__*"
cd "$PROJECT_DIR"

# Clean up
rm -rf "$BUILD_DIR"

# Stats
ZIP_SIZE=$(du -h "$ZIP_FILE" | cut -f1)
FILE_COUNT=$(zipinfo -1 "$ZIP_FILE" 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "=== Package Ready ==="
echo "File: $ZIP_FILE"
echo "Size: $ZIP_SIZE"
echo "Files: $FILE_COUNT"
echo ""
echo "Upload to:"
echo "  Gumroad: https://app.gumroad.com/products"
echo "  GitHub:  gh release create v${VERSION} ${ZIP_FILE} --title \"CareerOS v${VERSION}\""
