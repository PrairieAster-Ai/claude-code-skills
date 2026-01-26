#!/bin/bash

# Technology Stack Validation Script
# Checks Wiki content for outdated or deprecated technology references

set -e

# Source shared configuration loader
SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/config.sh"

WIKI_DIR="${1:-.}"
ERRORS=0
WARNINGS=0

echo "🔧 Checking technology stack references in: $WIKI_DIR"
echo ""

# Load and display configuration
load_project_config

# Display current tech stack if available
CURRENT_STACK=$(get_tech_stack)
if [ -n "$CURRENT_STACK" ]; then
    echo "📚 Current tech stack: $CURRENT_STACK"
    echo ""
fi

# Load deprecated technologies from config or use defaults
mapfile -t DEPRECATED_TECH < <(get_deprecated_tech)
if [ ${#DEPRECATED_TECH[@]} -eq 0 ]; then
    echo "ℹ️  No project-specific deprecated tech, using defaults"
    mapfile -t DEPRECATED_TECH < <(get_default_deprecated_tech)
fi

echo "🔍 Scanning for technology references..."
echo "   Checking for: ${DEPRECATED_TECH[*]}"
echo ""

FOUND_TECH=0
for tech in "${DEPRECATED_TECH[@]}"; do
    if MATCHES=$(grep -rn "$tech" "$WIKI_DIR" --include="*.md" 2>/dev/null); then
        echo -e "${YELLOW}⚠️  Found references to: $tech${NC}"
        echo ""
        echo "   Found in:"
        echo "$MATCHES" | head -5 | sed 's/^/     /'
        echo ""
        echo "   ✓ Action: Verify if these references are current or should be deprecated"
        ((WARNINGS++))
        FOUND_TECH=1
    fi
done

if [ $FOUND_TECH -eq 0 ]; then
    echo -e "${GREEN}✅ No deprecated technology references found${NC}"
fi
echo ""

# Check for consistency across Wiki pages
echo "🔄 Checking for technology consistency..."
TECH_MENTIONS=$(grep -roh "\(FastAPI\|Vercel\|Neon\|PostgreSQL\|React\|Next\.js\|Vite\)" "$WIKI_DIR" --include="*.md" 2>/dev/null | sort | uniq -c | sort -rn)

if [ -n "$TECH_MENTIONS" ]; then
    echo "Technology mention counts:"
    echo "$TECH_MENTIONS" | sed 's/^/   /'
    echo ""
    echo "Review: Ensure consistent terminology across all Wiki pages"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Technology stack validation passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Validation passed with $WARNINGS warnings${NC}"
    echo "Review technology mentions for consistency"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS technology issues${NC}"
    echo "Check if these technologies are still in use or need deprecation warnings"
    exit 1
fi
