# Deprecation Warning Template

Use this template when deprecating outdated documentation instead of deleting it.

## Template

```markdown
## ⚠️ **DEPRECATED DOCUMENT - DO NOT USE**

**Status**: This document contains outdated information from [DATE].

**Current Information**: See [Link to Updated Doc]

### **Outdated Information in This Document**:
- ❌ [Specific outdated claim 1 - e.g., "FastAPI backend (replaced with Vercel Functions)"]
- ❌ [Specific outdated claim 2 - e.g., "138 POI locations (count no longer accurate)"]
- ❌ [Specific outdated claim 3 - e.g., "B2B tourism features (not in current business model)"]

**Deprecation Date**: [DATE]
**Replacement Document**: [Link to current documentation]

---

## Reason for Deprecation

[Brief explanation of why this document is being deprecated]

## Migration Guide

For users relying on this documentation:
1. [Step 1 to migrate to new approach]
2. [Step 2...]
3. [Step 3...]

---

*Original outdated content preserved below for historical reference:*

---
```

## Usage Instructions

1. **Copy template** to top of outdated document
2. **Fill in placeholders**:
   - [DATE] - When info became outdated
   - [Link to Updated Doc] - Current documentation
   - List specific outdated claims
   - Brief reason for deprecation
   - Migration steps if applicable

3. **Keep original content** below the warning

4. **Commit with message**:
   ```
   docs: deprecate [document-name] - outdated since [date]

   Added deprecation warning to preserve history.
   Current info now in: [link]
   ```

## Why Use Deprecation Warnings?

✅ **DO** use deprecation warnings because:
- Preserves historical context
- Prevents confusion
- Provides migration path
- Shows evolution of project

❌ **DON'T** just delete outdated docs because:
- Loses historical context
- Creates dead links
- Confuses users with bookmarks
- No migration guidance

## Example

```markdown
## ⚠️ **DEPRECATED DOCUMENT - DO NOT USE**

**Status**: This document contains outdated information from September 2025.

**Current Information**: See [Architecture-Overview.md](Architecture-Overview.md)

### **Outdated Information in This Document**:
- ❌ FastAPI backend (replaced with Vercel Serverless Functions in October 2025)
- ❌ 138 POI locations (production count varies, see API for current count)
- ❌ B2B tourism operator features (current model is 100% B2C ad-supported)

**Deprecation Date**: October 23, 2025
**Replacement Document**: [Architecture-Overview.md](Architecture-Overview.md)

---

## Reason for Deprecation

This document described the original FastAPI + Directus architecture which was replaced with a simplified Vercel + Neon stack in October 2025 for better deployment velocity.

## Migration Guide

For developers relying on this architecture:
1. Review current [Architecture-Overview.md](Architecture-Overview.md) for Vercel Functions approach
2. Database operations now use Neon serverless driver instead of PostgreSQL connection pools
3. API endpoints remain similar but are now serverless functions in `apps/web/api/`

---

*Original outdated content preserved below for historical reference:*

---

# FastAPI Backend Architecture (OUTDATED)

[Original content...]
```

---

**Template Version**: 1.0.0
**Purpose**: Prevent information loss while guiding users to current docs
