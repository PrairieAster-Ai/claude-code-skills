# Example Skill Configurations

This directory contains example `skill-config.json` files for different project types.

## Usage

1. **Choose a template** that matches your project type
2. **Copy to your project**: `cp examples/configs/[template].json memory-bank/skill-config.json`
3. **Customize** the values for your specific project
4. **Test**: Run validation scripts to verify configuration

## Available Templates

### nearest-nice-weather-config.json
**Project Type**: B2C Travel/Weather Platform

**Use for**:
- Travel planning applications
- Weather-integrated services
- Location-based services
- POI/destination databases

**Key Features**:
- Deprecated tech: MapQuest, old OpenWeather versions
- Patterns: Location counts, POI counts
- Business: B2C messaging validation
- Tech stack: React, FastAPI, PostgreSQL

### portfolio-factory-config.json
**Project Type**: B2B Portfolio Automation

**Use for**:
- Portfolio generation platforms
- Client management systems
- Template-based services
- B2B SaaS products

**Key Features**:
- Deprecated tech: Jekyll, WordPress, Gatsby
- Patterns: Project counts, client counts
- Business: B2B messaging validation
- Tech stack: Next.js, Vercel, PostgreSQL

## Configuration Structure

```json
{
  "validation": {
    "deprecatedTech": [
      "List of technologies to flag as deprecated"
    ],
    "hardcodedPatterns": [
      "Regex patterns to detect hardcoded numbers"
    ],
    "investorDocTypes": [
      "Document types to validate for business model headers"
    ]
  },
  "projectSpecific": {
    "name": "your-project-name",
    "primaryFocus": "B2C/B2B description",
    "techStack": "Current technologies"
  }
}
```

## Creating Your Own Config

### Step 1: Identify Deprecated Technologies
List technologies your project no longer uses or is migrating away from:
```json
"deprecatedTech": [
  "OldFramework v1.x",
  "DeprecatedLibrary",
  "LegacyService"
]
```

### Step 2: Define Hardcoded Pattern Rules
Regex patterns to catch numbers that should use verification dates:
```json
"hardcodedPatterns": [
  "[0-9]+ items",
  "[0-9]+ users",
  "[0-9]+ records"
]
```

**Why?**: "138 users" goes stale quickly. Better: "User database (verified: November 2025)"

### Step 3: Specify Investor Doc Types
Keywords in filenames to identify investor-facing documents:
```json
"investorDocTypes": [
  "Investment",
  "Pitch",
  "Executive",
  "Business"
]
```

These documents will be checked for business model headers.

### Step 4: Set Project Metadata
```json
"projectSpecific": {
  "name": "my-project",
  "primaryFocus": "B2C social platform for pet owners",
  "techStack": "Python, Django, PostgreSQL, AWS"
}
```

## Testing Your Config

After creating your configuration:

```bash
# Validate config syntax
./.claude/skills/github/scripts/validate-config.sh

# Test Wiki validation with your config
./.claude/skills/github/scripts/validate-wiki.sh /tmp/your-project-wiki

# Test tech stack checks
./.claude/skills/github/scripts/check-tech-stack.sh /tmp/your-project-wiki

# Test business model validation
./.claude/skills/github/scripts/verify-business-model.sh /tmp/your-project-wiki
```

## Common Patterns

### E-Commerce Platform
```json
{
  "validation": {
    "deprecatedTech": ["Magento 1.x", "WooCommerce 3.x"],
    "hardcodedPatterns": ["[0-9]+ products", "[0-9]+ orders"],
    "investorDocTypes": ["Investment", "Pitch"]
  },
  "projectSpecific": {
    "name": "my-ecommerce",
    "primaryFocus": "B2C e-commerce platform",
    "techStack": "React, Node.js, MongoDB"
  }
}
```

### SaaS Application
```json
{
  "validation": {
    "deprecatedTech": ["Ruby on Rails 4.x", "Angular v1"],
    "hardcodedPatterns": ["[0-9]+ customers", "[0-9]+ subscriptions"],
    "investorDocTypes": ["Executive", "Business", "Technical"]
  },
  "projectSpecific": {
    "name": "my-saas",
    "primaryFocus": "B2B SaaS for team collaboration",
    "techStack": "Vue.js, Python, FastAPI, PostgreSQL"
  }
}
```

### Mobile App
```json
{
  "validation": {
    "deprecatedTech": ["React Native 0.60", "Firebase SDK v8"],
    "hardcodedPatterns": ["[0-9]+ downloads", "[0-9]+ users"],
    "investorDocTypes": ["Investment", "Pitch"]
  },
  "projectSpecific": {
    "name": "my-mobile-app",
    "primaryFocus": "B2C mobile fitness tracking",
    "techStack": "React Native, Expo, Firebase"
  }
}
```

## Graceful Fallbacks

If you don't create a config file, the skill uses these defaults:

- **Deprecated Tech**: Common old frameworks (AngularJS, Backbone, etc.)
- **Hardcoded Patterns**: Generic number patterns
- **Investor Docs**: Investment, Executive, Business
- **Business Focus**: Inferred from memory-bank if available

The skill will issue a warning but continue to work.

## Tips

1. **Start small**: Begin with 2-3 deprecated technologies, expand later
2. **Be specific**: "React Router v5" instead of just "React Router"
3. **Review quarterly**: Update deprecated tech as you migrate
4. **Share configs**: Team members can reuse the same configuration
5. **Version control**: Commit skill-config.json to your repo

## Support

If you create a config for a new project type and want to contribute it:
1. Add to `examples/configs/`
2. Update this README
3. Submit a PR to the skill repository

---

**Last Updated**: November 6, 2025
**Skill Version**: 2.0.0
