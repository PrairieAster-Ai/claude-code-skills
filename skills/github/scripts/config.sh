#!/bin/bash

# Shared Configuration Loader
# Source this file from other validation scripts
# Usage: source "$(dirname "$0")/config.sh"

# Configuration file location (can be overridden via environment)
CONFIG_FILE="${SKILL_CONFIG_PATH:-memory-bank/skill-config.json}"

# Project configuration (loaded on demand)
PROJECT_CONFIG=""

# Color codes for output
export RED='\033[0;31m'
export YELLOW='\033[1;33m'
export GREEN='\033[0;32m'
export BLUE='\033[0;34m'
export NC='\033[0m' # No Color

# Worktree Detection (obra/superpowers integration)
# Returns "worktree" if in git worktree, "standard" otherwise
detect_worktree_context() {
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        local worktree_dir=$(git rev-parse --git-common-dir 2>/dev/null)
        if [ -n "$worktree_dir" ] && [[ "$worktree_dir" == *".git/worktrees"* ]]; then
            echo "worktree"
            return 0
        fi
    fi
    echo "standard"
    return 1
}

# Get worktree-aware Wiki directory
# Supports obra/superpowers worktree workflows
get_wiki_directory() {
    # Priority 1: Environment variable (explicit override)
    if [ -n "$GITHUB_WIKI_WORKTREE" ]; then
        echo "$GITHUB_WIKI_WORKTREE"
        return 0
    fi

    # Priority 2: Detect if current directory is a worktree
    local context=$(detect_worktree_context)
    if [ "$context" == "worktree" ]; then
        echo "$(pwd)"
        return 0
    fi

    # Priority 3: Check for standard worktree paths
    if [ -d "worktrees/docs" ]; then
        find worktrees/docs -name "*wiki*" -type d 2>/dev/null | head -1
        return 0
    fi

    # Priority 4: Standard location
    local repo_name=$(basename "$(git remote get-url origin 2>/dev/null | sed 's/\.git$//')" 2>/dev/null || echo "project")
    echo "/tmp/${repo_name}-wiki"
}

# Load project configuration from JSON file
# Sets PROJECT_CONFIG variable
load_project_config() {
    if [ -f "$CONFIG_FILE" ]; then
        echo -e "${BLUE}📚 Loading project config from: $CONFIG_FILE${NC}"

        # Validate JSON before loading
        if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
            echo -e "${RED}❌ Invalid JSON in config file${NC}"
            echo "   Run: ./scripts/validate-config.sh"
            exit 1
        fi

        PROJECT_CONFIG=$(cat "$CONFIG_FILE")
        echo -e "${GREEN}✅ Configuration loaded${NC}"
    else
        echo -e "${YELLOW}ℹ️  No project config found, using defaults${NC}"
        echo "   Expected: $CONFIG_FILE"
        PROJECT_CONFIG='{}'
    fi
    echo ""
}

# Get deprecated technology list
# Returns: Array of technology names (one per line)
get_deprecated_tech() {
    if [ -z "$PROJECT_CONFIG" ]; then
        load_project_config
    fi

    echo "$PROJECT_CONFIG" | jq -r '.validation.deprecatedTech[]? // empty' 2>/dev/null
}

# Get hardcoded pattern list
# Returns: Array of regex patterns (one per line)
get_hardcoded_patterns() {
    if [ -z "$PROJECT_CONFIG" ]; then
        load_project_config
    fi

    echo "$PROJECT_CONFIG" | jq -r '.validation.hardcodedPatterns[]? // empty' 2>/dev/null
}

# Get investor document types
# Returns: Array of document type keywords (one per line)
get_investor_doc_types() {
    if [ -z "$PROJECT_CONFIG" ]; then
        load_project_config
    fi

    echo "$PROJECT_CONFIG" | jq -r '.validation.investorDocTypes[]? // empty' 2>/dev/null
}

# Get project name
# Returns: Project name string
get_project_name() {
    if [ -z "$PROJECT_CONFIG" ]; then
        load_project_config
    fi

    echo "$PROJECT_CONFIG" | jq -r '.projectSpecific.name // "unknown"' 2>/dev/null
}

# Get primary business focus
# Returns: Business focus string
get_business_focus() {
    if [ -z "$PROJECT_CONFIG" ]; then
        load_project_config
    fi

    echo "$PROJECT_CONFIG" | jq -r '.projectSpecific.primaryFocus // ""' 2>/dev/null
}

# Get tech stack
# Returns: Tech stack string
get_tech_stack() {
    if [ -z "$PROJECT_CONFIG" ]; then
        load_project_config
    fi

    echo "$PROJECT_CONFIG" | jq -r '.projectSpecific.techStack // ""' 2>/dev/null
}

# Get default deprecated tech list (fallback)
# Returns: Array of default technologies
get_default_deprecated_tech() {
    cat <<EOF
FastAPI
Directus
PostGIS
Docker Compose
Flask
Django
EOF
}

# Get default hardcoded patterns (fallback)
# Returns: Array of default patterns
get_default_hardcoded_patterns() {
    cat <<EOF
138 POI
169 locations
[0-9]\+ POI locations
[0-9]\+ items
[0-9]\+ projects
EOF
}

# Get default investor doc types (fallback)
# Returns: Array of default document types
get_default_investor_doc_types() {
    cat <<EOF
Investment
Executive
Financial
Business
Strategy
Pitch
Deck
EOF
}

# Check if configuration file exists
# Returns: 0 if exists, 1 if not
has_config_file() {
    [ -f "$CONFIG_FILE" ]
}

# Display configuration summary
show_config_summary() {
    if [ -z "$PROJECT_CONFIG" ]; then
        load_project_config
    fi

    echo "📊 Configuration Summary:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Config file: $CONFIG_FILE"
    echo "Project: $(get_project_name)"
    echo "Focus: $(get_business_focus)"
    echo "Tech Stack: $(get_tech_stack)"
    echo ""
    echo "Deprecated Tech: $(get_deprecated_tech | wc -l) items"
    echo "Hardcoded Patterns: $(get_hardcoded_patterns | wc -l) items"
    echo "Investor Doc Types: $(get_investor_doc_types | wc -l) items"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Export functions for use in other scripts
export -f load_project_config
export -f get_deprecated_tech
export -f get_hardcoded_patterns
export -f get_investor_doc_types
export -f get_project_name
export -f get_business_focus
export -f get_tech_stack
export -f get_default_deprecated_tech
export -f get_default_hardcoded_patterns
export -f get_default_investor_doc_types
export -f has_config_file
export -f show_config_summary
