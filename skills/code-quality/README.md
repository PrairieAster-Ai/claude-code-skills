# Code Quality Skill

A systematic approach to assessing, tracking, and improving code quality in TypeScript/React projects.

## Overview

This skill provides:
- **Assessment methodology** for evaluating codebase health
- **Metric targets** based on industry best practices
- **Sprint planning** framework for improvement work
- **Refactoring patterns** for common issues
- **Tracking templates** for measuring progress

## Quick Start

1. **Assess current state**:
   ```
   /code-quality assess
   ```

2. **Identify hotspots**:
   ```
   /code-quality hotspots
   ```

3. **Plan improvement sprint**:
   ```
   /code-quality sprint
   ```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill prompt with workflow and commands |
| `methodology.md` | Refactoring patterns, sprint structure, prioritization, lessons learned |
| `metrics-template.md` | Templates for baseline, sprint progress, and final validation |

## Key Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| ESLint Errors | 0 | `npm run lint` |
| ESLint Warnings | 0 | `npm run lint` |
| TypeScript Errors | 0 | `npm run type-check` |
| Test Coverage | 80%+ | `npx vitest run --coverage` |
| Code Duplication | <2% | `npx jscpd src --reporters json` |
| `any` Types | <50 | Grep tool: pattern `: any`, glob `*.{ts,tsx}` |
| Large Files | 0 (>500 LOC) | Glob tool + Read to count lines |

## Sprint Model

1. **Sprint 1: Critical Blockers** - Get to green CI
2. **Sprint 2: Quick Wins** - Build momentum
3. **Sprint 3: Architecture** - Modularization
4. **Sprint 4: Testing** - Coverage improvement
5. **Sprint 5: Polish** - Documentation

## Usage Examples

### Full Assessment
```
Run code quality assessment for this project, generate a baseline report,
and recommend a sprint plan.
```

### Specific Metric
```
Find all files with more than 5 any types and prioritize them for fixing.
```

### Sprint Planning
```
We have 8 hours. Plan a quick-wins sprint targeting the highest-impact
improvements.
```
