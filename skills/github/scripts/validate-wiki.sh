#!/bin/bash

# Wiki Validation Script
# Validates Wiki content for common issues before publishing

set -e

# Source shared configuration loader
SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/config.sh"

WIKI_DIR="${1:-.}"
ERRORS=0
WARNINGS=0

echo "🔍 Validating Wiki content in: $WIKI_DIR"
echo ""

# Load and display configuration
load_project_config

# Check 1: Hardcoded database counts
echo "📊 Checking for hardcoded database counts..."

# Load patterns from config or use defaults
mapfile -t PATTERNS < <(get_hardcoded_patterns)
if [ ${#PATTERNS[@]} -eq 0 ]; then
    mapfile -t PATTERNS < <(get_default_hardcoded_patterns)
fi

# Build grep pattern
PATTERN_STRING=$(IFS='|'; echo "${PATTERNS[*]}")

if [ -n "$PATTERN_STRING" ] && MATCHES=$(grep -rn "$PATTERN_STRING" "$WIKI_DIR" --include="*.md" 2>/dev/null); then
    echo -e "${RED}❌ Found hardcoded database counts${NC}"
    echo ""
    echo "   Found patterns:"
    echo "$MATCHES" | sed 's/^/     /'
    echo ""
    echo "   ✓ Available alternatives (choose one):"
    echo "     1. 'Production database (verified: $(date +%B\ %Y))'"
    echo "     2. 'Database (updated regularly)'"
    echo "     3. 'Data verified: $(date +%B\ %Y)'"
    echo ""
    echo "   💡 Tip: Use verification dates instead of counts"
    ((ERRORS++))
else
    echo -e "${GREEN}✅ No hardcoded counts found${NC}"
fi
echo ""

# Check 2: Deprecated technology references
echo "🔧 Checking for deprecated technology references..."

# Load tech from config or use defaults
mapfile -t DEPRECATED_TECH < <(get_deprecated_tech)
if [ ${#DEPRECATED_TECH[@]} -eq 0 ]; then
    mapfile -t DEPRECATED_TECH < <(get_default_deprecated_tech)
fi

FOUND_DEPRECATED=0
for tech in "${DEPRECATED_TECH[@]}"; do
    if MATCHES=$(grep -rn "$tech" "$WIKI_DIR" --include="*.md" 2>/dev/null); then
        echo -e "${YELLOW}⚠️  Found references to potentially deprecated: $tech${NC}"
        echo ""
        echo "   Found in:"
        echo "$MATCHES" | head -5 | sed 's/^/     /'
        echo ""

        # Check if current tech stack is available
        CURRENT_STACK=$(get_tech_stack)
        if [ -n "$CURRENT_STACK" ]; then
            echo "   ✓ Current tech stack: $CURRENT_STACK"
        fi

        echo "   ✓ Actions to consider:"
        echo "     1. Replace with current technology"
        echo "     2. Add deprecation warning (use templates/deprecation-warning.md)"
        echo "     3. Remove if no longer relevant"
        echo "     4. Keep if historically accurate with context"
        echo ""
        ((WARNINGS++))
        FOUND_DEPRECATED=1
    fi
done

if [ $FOUND_DEPRECATED -eq 0 ]; then
    echo -e "${GREEN}✅ No deprecated technology references found${NC}"
fi
echo ""

# Check 3: Business model consistency
echo "💼 Checking for business model consistency..."
B2C_COUNT=$(grep -rn "B2C" "$WIKI_DIR" --include="*.md" 2>/dev/null | wc -l)
B2B_COUNT=$(grep -rn "B2B" "$WIKI_DIR" --include="*.md" 2>/dev/null | wc -l)

echo "   B2C mentions: $B2C_COUNT"
echo "   B2B mentions: $B2B_COUNT"

if [ $B2B_COUNT -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found B2B references - verify these are clearly marked as not current focus${NC}"
    echo ""
    echo "   B2B mentions found:"
    grep -rn "B2B" "$WIKI_DIR" --include="*.md" 2>/dev/null | head -5 | sed 's/^/     /'
    echo ""
    echo "   ✓ Required actions:"
    echo "     1. Add business model header (see templates/business-model-header.md)"
    echo "     2. Use 'NOT Pursuing: B2B' language if not current focus"
    echo "     3. Add 'far-future possibility' context if mentioned"
    echo "     4. Check for contradictions with 'grep -r \"developing.*B2B\"'"
    echo ""
    echo "   💡 Verify current business focus:"
    echo "      jq -r '.businessFocus' memory-bank/quick-reference.json"
    ((WARNINGS++))
fi
echo ""

# Check 4: Broken internal links
echo "🔗 Checking for broken internal links..."
if MATCHES=$(grep -rn "\[.*\](\s*)" "$WIKI_DIR" --include="*.md" 2>/dev/null); then
    echo -e "${RED}❌ Found empty links${NC}"
    echo ""
    echo "   Empty links found:"
    echo "$MATCHES" | sed 's/^/     /'
    echo ""
    echo "   ✓ Fix by:"
    echo "     1. Add target URL: [Text](https://github.com/...)"
    echo "     2. Remove link formatting: Text (no brackets)"
    echo "     3. Link to Wiki page: [Text](PageName)"
    ((ERRORS++))
else
    echo -e "${GREEN}✅ No empty links found${NC}"
fi
echo ""

# Check 5: TODO/FIXME markers
echo "📝 Checking for TODO/FIXME markers..."
if MATCHES=$(grep -rn "TODO\|FIXME\|XXX\|HACK" "$WIKI_DIR" --include="*.md" 2>/dev/null); then
    echo -e "${YELLOW}⚠️  Found TODO/FIXME markers - resolve before publishing${NC}"
    echo ""
    echo "   Markers found:"
    echo "$MATCHES" | head -10 | sed 's/^/     /'
    if [ $(echo "$MATCHES" | wc -l) -gt 10 ]; then
        echo "     ... and $(($(echo "$MATCHES" | wc -l) - 10)) more"
    fi
    ((WARNINGS++))
else
    echo -e "${GREEN}✅ No TODO/FIXME markers found${NC}"
fi
echo ""

# Check 6: Business model headers in investor docs
echo "📋 Checking for business model headers in investor docs..."

# Load investor doc types from config
mapfile -t INVESTOR_DOCS < <(get_investor_doc_types)
if [ ${#INVESTOR_DOCS[@]} -eq 0 ]; then
    mapfile -t INVESTOR_DOCS < <(get_default_investor_doc_types)
fi

MISSING_HEADERS=0
for doc_type in "${INVESTOR_DOCS[@]}"; do
    if find "$WIKI_DIR" -name "*$doc_type*.md" -type f 2>/dev/null | grep -q .; then
        echo "   Found investor docs matching: $doc_type"
        for file in $(find "$WIKI_DIR" -name "*$doc_type*.md" -type f 2>/dev/null); do
            if ! grep -q "## Business Model" "$file" 2>/dev/null; then
                echo -e "${YELLOW}⚠️  Missing 'Business Model' header: $(basename "$file")${NC}"
                ((MISSING_HEADERS++))
            fi
        done
    fi
done

if [ $MISSING_HEADERS -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  $MISSING_HEADERS investor documents missing business model headers${NC}"
    echo "   Add business model section using templates/business-model-header.md"
    ((WARNINGS++))
elif find "$WIKI_DIR" -name "*Investment*.md" -o -name "*Executive*.md" -o -name "*Business*.md" -type f 2>/dev/null | grep -q .; then
    echo -e "${GREEN}✅ All investor documents have business model headers${NC}"
else
    echo -e "${GREEN}✅ No investor documents found${NC}"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All validation checks passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Validation passed with $WARNINGS warnings${NC}"
    echo "Review warnings above (non-blocking)"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS critical errors and $WARNINGS warnings${NC}"
    echo "Fix critical errors before publishing"
    exit 1
fi
