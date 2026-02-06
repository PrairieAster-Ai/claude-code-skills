---
name: code-quality
description: Assess and improve code quality in TypeScript/React projects. Runs lint, type-check, coverage, duplication, and complexity analysis with sprint planning.
allowed-tools: "Bash(npm:*),Bash(npx:*),Read,Grep,Glob"
---

# Code Quality Assessment & Improvement Skill

Systematic code quality analysis, metric tracking, and improvement sprint planning for TypeScript/React projects.

## Quick Commands

- `/code-quality assess` - Run full assessment and generate report
- `/code-quality metrics` - Show current metrics vs targets
- `/code-quality hotspots` - Identify highest-priority improvement areas
- `/code-quality sprint` - Plan a focused improvement sprint

## Workflow

### Phase 1: Assessment

Run comprehensive code quality checks and establish baseline metrics.

**Required Checks:**

1. **Lint Analysis**
   ```bash
   npm run lint 2>&1 | tee lint-report.txt
   ```
   - Target: 0 errors, 0 warnings
   - Track: Total warnings by category

2. **Type Safety**
   ```bash
   npm run type-check 2>&1 | tee typecheck-report.txt
   ```
   - Target: 0 TypeScript errors
   - Track: Error count and locations

3. **Test Coverage**
   ```bash
   npx vitest run --coverage 2>&1 | grep -E "All files|Coverage"
   ```
   - Target: 80%+ line coverage
   - Track: Coverage by directory

4. **Code Duplication**
   ```bash
   npx jscpd src --reporters json --output duplication-report
   ```
   - Target: <2% duplication
   - Track: Percentage and clone locations

5. **`any` Type Count**
   ```bash
   grep -rn ": any" src --include="*.ts" --include="*.tsx" | grep -v ".test." | grep -v "__tests__" | wc -l
   ```
   - Target: <50 `any` types
   - Track: Count by file

6. **Large File Detection**
   ```bash
   find src -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -n | tail -20
   ```
   - Target: No files >500 lines (excluding data files)
   - Track: Files exceeding threshold

7. **Complexity Analysis** (if eslint-plugin-complexity configured)
   ```bash
   npx eslint src --rule 'complexity: [warn, 15]' 2>&1 | grep -c "complexity"
   ```
   - Target: No functions with complexity >15
   - Track: High-complexity function locations

### Phase 2: Hotspot Identification

Prioritize issues using the **Impact/Effort Matrix**:

| Priority | Impact | Effort | Examples |
|----------|--------|--------|----------|
| **P0** | High | Low | ESLint errors, TypeScript errors |
| **P1** | High | Medium | Large files blocking changes, high `any` concentration |
| **P2** | Medium | Low | Duplicate code in same file |
| **P3** | Medium | Medium | Missing test coverage for critical paths |
| **P4** | Low | Any | Minor style inconsistencies |

**Hotspot Detection Commands:**

```bash
# Files with most any types
grep -rn ": any" src --include="*.ts" --include="*.tsx" | grep -v ".test." | cut -d: -f1 | sort | uniq -c | sort -rn | head -10

# Largest non-test files
find src -name "*.ts" -o -name "*.tsx" | grep -v ".test." | grep -v "__tests__" | xargs wc -l | sort -n | tail -15

# Duplicate code locations
cat duplication-report/jscpd-report.json | jq '.duplicates[].firstFile.name' | sort | uniq -c | sort -rn | head -10
```

### Phase 3: Sprint Planning

Structure improvement work into focused sprints:

**Sprint Template:**
```markdown
## Sprint [N]: [Theme]

**Duration**: [X] hours
**Goal**: [Specific, measurable objective]

### Tasks
| ID | Task | Effort | Impact |
|----|------|--------|--------|
| 1 | [Task description] | [hours] | [metric improvement] |

### Success Criteria
- [ ] Metric A: [before] → [target]
- [ ] Metric B: [before] → [target]

### Validation
- [ ] All tests pass
- [ ] Lint clean
- [ ] Type-check clean
- [ ] No regressions
```

**Sprint Sizing Guidelines:**
- Quick Win Sprint: 4-8 hours, targets easy P0/P1 items
- Standard Sprint: 16-24 hours, tackles systematic issues
- Deep Dive Sprint: 40+ hours, major architectural refactoring

### Phase 4: Execution Patterns

**Pattern: File Modularization**
When a file exceeds 500 lines:
1. Identify cohesive groups of functions
2. Create subdirectory with same name as file
3. Extract groups into focused modules
4. Create `index.ts` re-exporting public API
5. Update original file to re-export from index
6. Verify all imports still work

**Pattern: Type Safety Improvement**
When fixing `any` types:
1. Start with files having highest `any` concentration
2. Create interface definitions for external data
3. Use type guards for runtime validation
4. Prefer `unknown` over `any` when type is truly unknown
5. Add JSDoc for complex types

**Pattern: Duplication Elimination**
When reducing code duplication:
1. Identify semantic similarity (same purpose, not just similar code)
2. Extract to shared utility only if used 3+ times
3. Prefer composition over inheritance
4. Keep extracted code in appropriate layer (utils, hooks, services)

**Pattern: Component Consolidation**
When multiple components share similar structure/styling:
1. Identify shared visual patterns (card layout, icon placement, theming)
2. Create a base component with configurable props (title, icon, theme, children, footer)
3. Compose specialized components using the base
4. Extract shared logic to utils (e.g., color theme helpers)
5. Add comprehensive tests for the base component

### Phase 5: Validation

After each sprint, run full validation:

```bash
# Full validation script
npm run lint && \
npm run type-check && \
npm test && \
echo "✅ All checks pass"
```

**Regression Checklist:**
- [ ] All existing tests pass
- [ ] No new lint warnings introduced
- [ ] No new TypeScript errors
- [ ] Build succeeds
- [ ] Application runs correctly

## Metric Targets Reference

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| ESLint Errors | 0 | 0 | 0 |
| ESLint Warnings | <50 | <20 | 0 |
| TypeScript Errors | 0 | 0 | 0 |
| Test Coverage | 60% | 80% | 90%+ |
| Code Duplication | <5% | <2% | <1% |
| `any` Types | <100 | <50 | <20 |
| Files >500 LOC | <10 | <5 | 0 |
| Complexity >15 | <10 | <5 | 0 |

## Output Format

When reporting assessment results, use this format:

```markdown
## Code Quality Assessment - [Date]

### Summary
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Lint Errors | X | 0 | ✅/❌ |
| Lint Warnings | X | 0 | ✅/❌ |
| TypeScript Errors | X | 0 | ✅/❌ |
| Test Coverage | X% | 80% | ✅/❌ |
| Code Duplication | X% | <2% | ✅/❌ |
| `any` Types | X | <50 | ✅/❌ |
| Large Files | X | 0 | ✅/❌ |

### Top Hotspots
1. [File/Issue]: [Description] - [Recommended action]
2. ...

### Recommended Sprint
[Sprint plan based on hotspots]
```

## Related Files

- `methodology.md` - Detailed methodology and lessons learned
- `metrics-template.md` - Tracking templates
- `refactoring-patterns.md` - Common refactoring patterns with examples
