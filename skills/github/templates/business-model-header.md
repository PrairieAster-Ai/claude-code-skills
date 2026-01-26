# Business Model Header Template

Use this template in investor-facing documents to ensure business model consistency.

## Template

```markdown
## Business Model

**Current Focus**: 100% [B2C/B2B] [brief description of revenue model]

**Revenue Strategy**: [Ad-supported / Subscription / Transaction fees / etc.]

**Target Market**: [Geographic scope, user segment, market size]

**NOT Pursuing**: [Alternative business models] are documented as far-future possibilities only.

**Last Updated**: [DATE]
```

## Usage Instructions

**When to use:**
- Investment decks
- Executive summaries
- Financial projections
- Strategic planning documents
- Any investor-facing Wiki pages

**Where to place:**
- Near the top of the document (after title/summary)
- Before detailed technical or financial content
- In a clearly visible section

## Examples

### Example 1: B2C Ad-Supported Model

```markdown
## Business Model

**Current Focus**: 100% B2C ad-supported platform for outdoor enthusiasts

**Revenue Strategy**: Google AdSense integration targeting 10,000+ monthly active users

**Target Market**: Minneapolis metro area casual outdoor recreation seekers

**NOT Pursuing**: B2B tourism operator features are far-future possibilities only.

**Last Updated**: October 2025
```

### Example 2: B2B SaaS Model

```markdown
## Business Model

**Current Focus**: 100% B2B SaaS platform for enterprise document automation

**Revenue Strategy**: Subscription tiers ($99-$999/month) with usage-based pricing

**Target Market**: US-based mid-market companies (50-500 employees)

**NOT Pursuing**: B2C consumer features are not in current roadmap.

**Last Updated**: October 2025
```

### Example 3: Marketplace Model

```markdown
## Business Model

**Current Focus**: 100% two-sided marketplace connecting service providers and customers

**Revenue Strategy**: 15% transaction fee on completed bookings

**Target Market**: Metro areas with 500k+ population, initially launching in Minneapolis

**NOT Pursuing**: Direct service provision - we remain a platform only.

**Last Updated**: October 2025
```

## Why This Matters

**Investor Perspective:**
- Needs clarity on revenue model
- Wants to see focused strategy
- Avoids confusion about market positioning
- Demonstrates clear thinking

**Team Alignment:**
- Prevents feature drift
- Clarifies what NOT to build
- Guides prioritization decisions
- Ensures consistent messaging

## Common Mistakes to Avoid

❌ **DON'T:**
- Leave business model implicit
- Mix B2C and B2B language
- Contradict yourself across documents
- Use vague terms like "might pursue"

✅ **DO:**
- State explicitly what you ARE doing
- State explicitly what you're NOT doing
- Be specific about revenue strategy
- Update date when model changes

## Validation Checklist

Before publishing investor documents:

- [ ] Business model header is present
- [ ] Revenue strategy is clear
- [ ] Target market is specific
- [ ] Excluded approaches are listed
- [ ] No contradictions with other docs
- [ ] Update date is current

## Integration with Memory-Bank

If your project has a memory-bank:

```json
// memory-bank/quick-reference.json
{
  "businessFocus": "B2C outdoor recreation",
  "revenueModel": "Ad-supported",
  "targetMarket": "Minneapolis metro casual users",
  "notPursuing": ["B2B tourism operators", "Premium subscriptions"]
}
```

The GitHub skill will auto-check for consistency with this reference.

---

**Template Version**: 1.0.0
**Purpose**: Ensure investor-facing documentation has consistent business model messaging
