# Code Quality Metrics Template

Use this template to track code quality metrics over time.

## Baseline Assessment Template

```markdown
# Code Quality Baseline Assessment
**Project**: [Project Name]
**Date**: [YYYY-MM-DD]
**Assessed By**: [Name/Claude]

## Summary

| Metric | Value | Target | Gap |
|--------|-------|--------|-----|
| ESLint Errors | | 0 | |
| ESLint Warnings | | 0 | |
| TypeScript Errors | | 0 | |
| Test Coverage | % | 80% | |
| Code Duplication | % | <2% | |
| `any` Types | | <50 | |
| Files >500 LOC | | 0 | |
| Avg Complexity | | <10 | |

## Test Results

- Total Tests:
- Passing:
- Failing:
- Skipped:

## Lint Breakdown

| Category | Errors | Warnings |
|----------|--------|----------|
| TypeScript | | |
| React | | |
| Import | | |
| Style | | |
| Other | | |

## Type Safety Analysis

### `any` Type Distribution
| File | Count | Priority |
|------|-------|----------|
| | | |

### TypeScript Error Locations
| File | Line | Error |
|------|------|-------|
| | | |

## File Size Analysis

### Files Exceeding 500 Lines
| File | Lines | Category |
|------|-------|----------|
| | | Service/Component/Data |

### Largest Files (Top 10)
| File | Lines |
|------|-------|
| | |

## Duplication Analysis

- **Total Duplication**: %
- **Clone Count**:

### Top Duplicate Locations
| File 1 | File 2 | Lines | Tokens |
|--------|--------|-------|--------|
| | | | |

## Complexity Hotspots

| File | Function | Complexity |
|------|----------|------------|
| | | |

## Recommended Sprint Plan

### Sprint 1: Critical (Estimated: Xh)
1. [ ] Fix [N] ESLint errors
2. [ ] Fix [N] TypeScript errors
3. [ ] Fix [N] failing tests

### Sprint 2: Quick Wins (Estimated: Xh)
1. [ ] Reduce warnings from [X] to [Y]
2. [ ] Remove [N] obvious `any` types
3. [ ] Fix [N] duplicate code blocks

### Sprint 3: Architecture (Estimated: Xh)
1. [ ] Modularize [File 1]
2. [ ] Modularize [File 2]
3. [ ] Extract [Service]

## Notes

[Any observations, concerns, or context]
```

---

## Sprint Progress Template

```markdown
# Sprint [N] Progress Report
**Sprint Theme**: [Theme]
**Period**: [Start Date] - [End Date]
**Hours Invested**: [X]h

## Goals vs Actuals

| Goal | Target | Actual | Status |
|------|--------|--------|--------|
| ESLint Warnings | X → Y | | ✅/❌ |
| TypeScript Errors | X → 0 | | ✅/❌ |
| Test Coverage | X% → Y% | | ✅/❌ |
| | | | |

## Completed Tasks

- [x] Task 1 (Xh)
- [x] Task 2 (Xh)
- [ ] Task 3 (deferred)

## Metric Changes

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| ESLint Warnings | | | |
| `any` Types | | | |
| Test Coverage | | | |
| Duplication | | | |

## Lessons Learned

1. [What went well]
2. [What was harder than expected]
3. [What to do differently]

## Carry-Forward Items

- [ ] Deferred task 1
- [ ] New issue discovered

## Next Sprint Recommendations

[Suggested focus for next sprint]
```

---

## Final Validation Template

```markdown
# Code Quality Final Validation
**Project**: [Project Name]
**Date**: [YYYY-MM-DD]
**Sprint Sequence**: [1, 2, 3, ...]

## Final Metrics

| Metric | Initial | Final | Target | Status |
|--------|---------|-------|--------|--------|
| ESLint Errors | | | 0 | |
| ESLint Warnings | | | 0 | |
| TypeScript Errors | | | 0 | |
| Test Coverage | % | % | 80% | |
| Code Duplication | % | % | <2% | |
| `any` Types | | | <50 | |
| Files >500 LOC | | | 0 | |
| Total Tests | | | N/A | |

## Improvement Summary

- **Lint**: [X] errors → [Y] errors (Z% reduction)
- **Types**: [X] `any` → [Y] `any` (Z% reduction)
- **Coverage**: [X]% → [Y]% (+Z points)
- **Duplication**: [X]% → [Y]% (Z% reduction)
- **Large Files**: [X] → [Y] files

## Validation Checklist

- [ ] `npm run lint` passes with 0 warnings
- [ ] `npm run type-check` passes with 0 errors
- [ ] `npm test` all tests pass
- [ ] `npm run build` succeeds
- [ ] Application runs correctly
- [ ] No regressions in functionality

## Remaining Technical Debt

| Item | Priority | Reason Not Addressed |
|------|----------|----------------------|
| | | |

## Recommendations

### Maintenance
- [ ] Enable pre-commit hooks
- [ ] Set CI to fail on warnings
- [ ] Schedule quarterly audits

### Future Improvements
- [ ] Suggested future work
```

---

## Quick Metrics Collection Script

Save as `collect-metrics.sh`:

```bash
#!/bin/bash
# Collect code quality metrics

echo "=== Code Quality Metrics ==="
echo "Date: $(date)"
echo ""

echo "--- Lint ---"
npm run lint 2>&1 | grep -E "problem|error|warning" || echo "Clean"

echo ""
echo "--- TypeScript ---"
npm run type-check 2>&1 | grep -E "error|Found" || echo "Clean"

echo ""
echo "--- Tests ---"
npm test 2>&1 | grep -E "Tests:|passed|failed"

echo ""
echo "--- Coverage ---"
npx vitest run --coverage 2>&1 | grep -E "All files|Coverage"

echo ""
echo "--- Any Types ---"
echo "Count: $(grep -rn ': any' src --include='*.ts' --include='*.tsx' | grep -v '.test.' | grep -v '__tests__' | wc -l)"

echo ""
echo "--- Large Files (>500 lines) ---"
find src -name "*.ts" -o -name "*.tsx" | xargs wc -l 2>/dev/null | awk '$1 > 500 {print}' | grep -v total

echo ""
echo "--- Duplication ---"
npx jscpd src --reporters json --silent 2>/dev/null && cat jscpd-report.json 2>/dev/null | grep percentage || echo "Run jscpd manually"

echo ""
echo "=== End Metrics ==="
```

---

## Comparison Table (For Presentations)

```markdown
## Code Quality Journey

| Metric | Day 1 | Sprint 1 | Sprint 2 | Sprint 3 | Final |
|--------|-------|----------|----------|----------|-------|
| Errors | | | | | |
| Warnings | | | | | |
| Coverage | | | | | |
| Duplication | | | | | |
| `any` Types | | | | | |
| Large Files | | | | | |
| Tests | | | | | |

**Key Achievements:**
-
-
-

**Time Investment:**
- Total Hours:
- Hours per Sprint:
```
