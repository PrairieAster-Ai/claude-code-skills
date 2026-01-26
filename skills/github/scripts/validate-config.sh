#!/bin/bash

# Configuration Validation Script
# Validates memory-bank/skill-config.json before running other validations

set -e

CONFIG_FILE="${SKILL_CONFIG_PATH:-memory-bank/skill-config.json}"
ERRORS=0
WARNINGS=0

echo "🔍 Validating skill configuration: $CONFIG_FILE"
echo ""

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check 1: File exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠️  No config file found at: $CONFIG_FILE${NC}"
    echo "   Using built-in defaults"
    echo ""
    echo "   ✓ To customize validation rules, create:"
    echo "     memory-bank/skill-config.json"
    echo ""
    echo "   💡 Template:"
    cat <<'EOF'
{
  "validation": {
    "deprecatedTech": ["Technology1", "Technology2"],
    "hardcodedPatterns": ["pattern1", "pattern2"],
    "investorDocTypes": ["Investment", "Executive"]
  },
  "projectSpecific": {
    "name": "your-project",
    "primaryFocus": "B2C description",
    "techStack": "Tech + Stack + Here"
  }
}
EOF
    exit 0
fi

# Check 2: Valid JSON syntax
echo "📄 Checking JSON syntax..."
if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
    echo -e "${RED}❌ Invalid JSON syntax in: $CONFIG_FILE${NC}"
    echo ""
    echo "   Error details:"
    jq empty "$CONFIG_FILE" 2>&1 | sed 's/^/     /'
    echo ""
    echo "   ✓ Common JSON errors:"
    echo "     1. Missing comma between elements"
    echo "     2. Trailing comma after last element"
    echo "     3. Unquoted strings"
    echo "     4. Single quotes instead of double quotes"
    echo ""
    echo "   💡 Validate JSON online:"
    echo "      https://jsonlint.com/"
    ((ERRORS++))
    exit 1
fi
echo -e "${GREEN}✅ JSON syntax valid${NC}"
echo ""

# Check 3: Required top-level structure
echo "📋 Checking structure..."
REQUIRED_SECTIONS=("validation")
for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! jq -e ".$section" "$CONFIG_FILE" >/dev/null 2>&1; then
        echo -e "${RED}❌ Missing required section: $section${NC}"
        ((ERRORS++))
    else
        echo -e "${GREEN}✅ Section found: $section${NC}"
    fi
done
echo ""

# Check 4: Validation section fields
echo "🔍 Checking validation fields..."
VALIDATION_FIELDS=("deprecatedTech" "hardcodedPatterns" "investorDocTypes")
for field in "${VALIDATION_FIELDS[@]}"; do
    if ! jq -e ".validation.$field" "$CONFIG_FILE" >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Missing recommended field: validation.$field${NC}"
        echo "   Will use built-in defaults"
        ((WARNINGS++))
    else
        # Check if array
        if ! jq -e ".validation.$field | type == \"array\"" "$CONFIG_FILE" >/dev/null 2>&1; then
            echo -e "${RED}❌ Field validation.$field must be an array${NC}"
            ((ERRORS++))
        else
            COUNT=$(jq -r ".validation.$field | length" "$CONFIG_FILE")
            echo -e "${GREEN}✅ validation.$field: $COUNT items${NC}"
        fi
    fi
done
echo ""

# Check 5: Project-specific section (optional but recommended)
echo "📦 Checking project-specific fields..."
if jq -e ".projectSpecific" "$CONFIG_FILE" >/dev/null 2>&1; then
    PROJECT_FIELDS=("name" "primaryFocus" "techStack")
    for field in "${PROJECT_FIELDS[@]}"; do
        if ! jq -e ".projectSpecific.$field" "$CONFIG_FILE" >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  Missing recommended field: projectSpecific.$field${NC}"
            ((WARNINGS++))
        else
            VALUE=$(jq -r ".projectSpecific.$field" "$CONFIG_FILE")
            echo -e "${GREEN}✅ projectSpecific.$field: $VALUE${NC}"
        fi
    done
else
    echo -e "${YELLOW}⚠️  No projectSpecific section found${NC}"
    echo "   This section helps document project context"
    ((WARNINGS++))
fi
echo ""

# Check 6: Validate array contents
echo "🔍 Validating array contents..."

# Check deprecatedTech for empty strings
if jq -e ".validation.deprecatedTech" "$CONFIG_FILE" >/dev/null 2>&1; then
    EMPTY_COUNT=$(jq -r '.validation.deprecatedTech[] | select(. == "")' "$CONFIG_FILE" 2>/dev/null | wc -l)
    if [ "$EMPTY_COUNT" -gt 0 ]; then
        echo -e "${RED}❌ Found $EMPTY_COUNT empty strings in validation.deprecatedTech${NC}"
        ((ERRORS++))
    else
        echo -e "${GREEN}✅ No empty strings in deprecatedTech${NC}"
    fi
fi

# Check hardcodedPatterns for valid regex
if jq -e ".validation.hardcodedPatterns" "$CONFIG_FILE" >/dev/null 2>&1; then
    PATTERN_ERRORS=0
    while IFS= read -r pattern; do
        # Basic regex validation (check if grep accepts it)
        if ! echo "test" | grep -E "$pattern" >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  Potentially invalid regex pattern: $pattern${NC}"
            ((WARNINGS++))
            PATTERN_ERRORS=1
        fi
    done < <(jq -r '.validation.hardcodedPatterns[]' "$CONFIG_FILE" 2>/dev/null)

    if [ $PATTERN_ERRORS -eq 0 ]; then
        echo -e "${GREEN}✅ All regex patterns valid${NC}"
    fi
fi
echo ""

# Check 7: Display configuration summary
echo "📊 Configuration Summary:"
echo ""
jq -r '
  "Deprecated Technologies: " + (.validation.deprecatedTech | length | tostring),
  "Hardcoded Patterns: " + (.validation.hardcodedPatterns | length | tostring),
  "Investor Doc Types: " + (.validation.investorDocTypes | length | tostring),
  "",
  "Project: " + (.projectSpecific.name // "not specified"),
  "Focus: " + (.projectSpecific.primaryFocus // "not specified"),
  "Tech Stack: " + (.projectSpecific.techStack // "not specified")
' "$CONFIG_FILE" | sed 's/^/   /'
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Configuration validation passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Configuration valid with $WARNINGS warnings${NC}"
    echo "Review warnings above (non-blocking)"
    exit 0
else
    echo -e "${RED}❌ Configuration validation failed with $ERRORS errors${NC}"
    echo "Fix errors above before running other validation scripts"
    exit 1
fi
