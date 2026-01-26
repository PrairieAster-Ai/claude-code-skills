#!/bin/bash

# Business Model Validation Script
# Ensures consistent business model messaging across investor-facing documentation

set -e

# Source shared configuration loader
SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/config.sh"

WIKI_DIR="${1:-.}"
ERRORS=0
WARNINGS=0

echo "💼 Validating business model consistency in: $WIKI_DIR"
echo ""

# Load and display configuration
load_project_config

# Display business context if available
BUSINESS_FOCUS=$(get_business_focus)
if [ -n "$BUSINESS_FOCUS" ]; then
    echo "📚 Current business focus: $BUSINESS_FOCUS"
    echo ""
fi

# Check 1: B2C vs B2B consistency
echo "📊 Checking B2C/B2B consistency..."
B2C_COUNT=$(grep -rn "B2C" "$WIKI_DIR" --include="*.md" 2>/dev/null | wc -l)
B2B_COUNT=$(grep -rn "B2B" "$WIKI_DIR" --include="*.md" 2>/dev/null | wc -l)

echo "   B2C mentions: $B2C_COUNT"
echo "   B2B mentions: $B2B_COUNT"

if [ $B2B_COUNT -gt 0 ] && [ $B2C_COUNT -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found both B2C and B2B references${NC}"
    echo "   Verify these are clearly distinguished (current focus vs future possibilities)"
    echo ""
    echo "B2B references found in:"
    grep -rn "B2B" "$WIKI_DIR" --include="*.md" 2>/dev/null | head -5 | sed 's/^/     /'
    ((WARNINGS++))
fi
echo ""

# Check 2: Investor-facing documents have business model headers
echo "📋 Checking for business model headers in investor docs..."

mapfile -t INVESTOR_DOCS < <(get_investor_doc_types)
if [ ${#INVESTOR_DOCS[@]} -eq 0 ]; then
    mapfile -t INVESTOR_DOCS < <(get_default_investor_doc_types)
fi

MISSING_HEADERS=0
for doc_type in "${INVESTOR_DOCS[@]}"; do
    if find "$WIKI_DIR" -name "*$doc_type*.md" -type f 2>/dev/null | grep -q .; then
        echo "   Found investor doc type: $doc_type"

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
else
    echo -e "${GREEN}✅ All investor documents have business model headers${NC}"
fi
echo ""

# Check 3: Contradictory claims
echo "🔍 Checking for contradictory claims..."
CONTRADICTIONS=0

# Check for "not pursuing" language
NOT_PURSUING=$(grep -rn "NOT Pursuing\|not pursuing\|are not in current" "$WIKI_DIR" --include="*.md" 2>/dev/null)
if [ -n "$NOT_PURSUING" ]; then
    echo "Found explicit exclusions:"
    echo "$NOT_PURSUING" | head -5 | sed 's/^/   /'
    echo ""
fi

# Check if excluded items are mentioned elsewhere positively
if echo "$NOT_PURSUING" | grep -q "B2B"; then
    if grep -rn "B2B.*feature\|B2B.*capability\|developing.*B2B" "$WIKI_DIR" --include="*.md" 2>/dev/null | grep -v "NOT Pursuing" >/dev/null; then
        echo -e "${RED}❌ Found contradictory B2B claims${NC}"
        echo "   Document says 'NOT Pursuing B2B' but also mentions developing B2B features"
        ((ERRORS++))
        CONTRADICTIONS=1
    fi
fi

if [ $CONTRADICTIONS -eq 0 ]; then
    echo -e "${GREEN}✅ No contradictory claims found${NC}"
fi
echo ""

# Check 4: Revenue model consistency
echo "💰 Checking revenue model consistency..."
REVENUE_MODELS=$(grep -roh "ad-supported\|subscription\|SaaS\|transaction fee\|marketplace\|freemium" "$WIKI_DIR" --include="*.md" -i 2>/dev/null | sort | uniq -c | sort -rn)

if [ -n "$REVENUE_MODELS" ]; then
    echo "Revenue model mentions:"
    echo "$REVENUE_MODELS" | sed 's/^/   /'
    echo ""

    MODEL_COUNT=$(echo "$REVENUE_MODELS" | wc -l)
    if [ $MODEL_COUNT -gt 2 ]; then
        echo -e "${YELLOW}⚠️  Multiple revenue models mentioned${NC}"
        echo "   Clarify which is primary vs future possibilities"
        ((WARNINGS++))
    fi
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Business model validation passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Validation passed with $WARNINGS warnings${NC}"
    echo "Review business model consistency warnings"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS business model issues${NC}"
    echo "Fix critical business model inconsistencies before publishing"
    exit 1
fi
