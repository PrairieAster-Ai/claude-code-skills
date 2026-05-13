# Job Apply Skill — Product Requirements Document

**Version:** 1.0
**Date:** 2026-02-22
**Author:** Robert Speer / PrairieAster.Ai
**Status:** Draft

---

## 1. Product Overview

The Job Apply Skill is a multi-edition AI-powered job application tool that assesses job fit, generates tailored cover letters and resumes, and provides coaching — all designed for job seekers who may not have money yet for premium tools.

### 1.1 Editions

| | Artifact | Web Chat | CLI |
|---|---|---|---|
| **Platform** | claude.ai published artifact | Claude Projects | Claude Code |
| **Tier** | Free | Free | Pro/Max/Team/Enterprise |
| **Target user** | Job seekers, non-technical | Job seekers, slightly technical | Power users, developers |
| **Assessment** | Claude API → structured JSON | Claude conversational | Claude conversational |
| **Doc generation** | Claude API → HTML preview → .doc | Analysis tool → python-docx | generate_word_docs.py → .docx |
| **Interactivity** | Full (toggle levels, move chips, recalculate) | Conversational | Conversational + config.yaml |
| **Persistence** | window.storage | profile.yaml (user saves/uploads) | config.yaml + applications.log |
| **Style presets** | 7 (3 professional + 4 fun) | 3 professional | 3 professional |
| **Current version** | v5 (Feb 2026) | v1 (Feb 2026) | v1 (Feb 2026) |

### 1.2 Architectural Difference

The **Artifact** is fully AI-powered — Claude handles all content intelligence (assessment, doc writing, coaching). The **CLI** and **Web Chat** editions use Claude conversationally but rely on Python scripts for .docx generation. The artifact's v5 improvements (client-side score recomputation, HTML sanitization, word-boundary matching, credential normalization) are code patterns that need to be translated into prompt improvements for the other two editions.

---

## 2. Completed Work (Artifact v5)

These items shipped in the artifact's v5 release and inform the requirements below.

- Client-side score recomputation (Claude's math unreliable)
- Assessment token limit 2048 → 3072 (prevents JSON truncation)
- HTML sanitization on doc gen output (defense in depth)
- Word-boundary matching for skill → requirement linking
- Credential normalization moved to one-time post-parse
- Shared constants (LEVEL_DISPLAY_MAP, SCORE_MAP)
- status.claude.com → status.anthropic.com (6 URLs)
- Health check timeout (15s)
- Comprehensive code comments for future Claude editing
- Prompt hardening: "EXACT quotes" for recruiter language

---

## 3. Requirements

### REQ-1: Sync Scoring Framework Across Editions

**Priority:** P1
**Effort:** Small (prompt edits only)

#### Problem

The artifact now uses an 8-level matchLevel vocabulary and client-side score recomputation. The CLI and Web Chat editions still use the original 3-level system (strong/partial/gap) with Claude computing scores directly.

| Aspect | Artifact (current) | Web Chat / CLI (current) |
|---|---|---|
| Score formula | Client-side, always recomputed | Claude computes, trusted |
| matchLevel vocab | 8 levels (expert/capable/learning/none/have + strong/partial/gap) | 3 levels (strong/partial/gap) |
| Credential handling | Binary have/none normalized from Claude output | Not differentiated |
| User corrections | Toggle levels, move chips, recalculate | Conversational / config.yaml |

#### Requirements

**Web Chat (SKILL-webchat.md):**
- Add credential vs. skill type distinction to assessment output format
- Add instruction: "After presenting assessment, ask user to confirm or correct any skill levels before proceeding to document generation"
- Add instruction: "If user corrects a level, recompute scores before generating documents"
- Update scoring formula comment to match artifact's 70/30 weighting

**CLI (SKILL.md):**
- Same assessment format updates as Web Chat
- Add fit-assessment.md reference to use credential/skill distinction

#### Acceptance Criteria

- [ ] Both editions distinguish credentials from skills in assessment output
- [ ] Both editions prompt users to confirm/correct levels before doc gen
- [ ] Scores recalculate when users correct levels
- [ ] 70/30 must-have/nice-to-have weighting documented in both editions

---

### REQ-2: Recruiter Language Hallucination Prevention

**Priority:** P2
**Effort:** Tiny (one line per edition)

#### Problem

All three editions ask Claude to decode recruiter phrases, but Claude frequently paraphrases or invents phrases not verbatim in the JD. The artifact now enforces "EXACT quotes — copy-paste" but the other editions don't.

#### Requirements

**Web Chat:** Add to Phase 2 assessment instructions: "recruiterLanguage phrases must be EXACT copy-paste from the job description. Do not paraphrase."

**CLI:** Update SKILL.md Phase 2 with the same language.

#### Acceptance Criteria

- [ ] Both editions include exact-quote instruction for recruiter language
- [ ] Generated assessments contain only verbatim JD phrases in recruiterLanguage fields

---

### REQ-3: ATS Optimization for Document Generation

**Priority:** P3
**Effort:** Medium (prompt edits + Python code review)

#### Problem

The artifact's v5 doc gen prompts include detailed ATS compatibility instructions (semantic contact links, standard section headers, date formatting, no pipes/delimiters). The Web Chat and CLI editions have some of this but not all.

#### Requirements

**Web Chat (SKILL-webchat.md):**
- Add ATS contact info rules: "each field on own line, use mailto/tel/URL links, NEVER use pipes or bullets between contact fields"
- Add ATS section header list: "Summary", "Skills", "Experience", "Education", "Certifications"
- Add date format rule: "Month YYYY – Month YYYY (en-dash, not hyphen)"

**CLI:**
- Update resume-template.md with same ATS rules
- Update generate_word_docs.py contact section to use semantic fields instead of pipe-delimited strings
- Verify .docx output uses proper heading styles (Word's built-in Heading 1, Heading 2) for ATS parsing

#### Acceptance Criteria

- [ ] Contact info renders one field per line, no pipe delimiters, in both editions
- [ ] Section headers use standard ATS-parseable names
- [ ] Date ranges use en-dash format consistently
- [ ] CLI .docx uses Word built-in heading styles (verified)

---

### REQ-4: Gap-to-Cover-Letter Bridge

**Priority:** P4
**Effort:** Small (prompt additions)

#### Problem

The artifact feeds coaching output (gap mitigation strategies) into the cover letter prompt, so the cover letter addresses gaps using the same specific framings coaching recommended. The other editions don't have this connection.

#### Requirements

**Web Chat:** Add to Phase 3: "When writing the cover letter, reference the specific gap mitigation strategies from the assessment. Address the top 1–2 gaps using the framing you recommended."

**CLI:** Ensure SKILL.md Phase 5 doc generation references gap strategies from Phase 2 assessment.

#### Acceptance Criteria

- [ ] Cover letters in both editions address the top 1–2 gaps using framing from the assessment phase
- [ ] Gap strategies from assessment are explicitly referenced in cover letter generation prompts

---

### REQ-5: Update README Artifact Description

**Priority:** P5
**Effort:** Tiny

#### Problem

README.md describes the artifact as "~3,100 lines" with "4-step wizard", "localStorage persistence", and "no API calls." All are wrong for v5:
- Now ~1,467 lines
- 3-step wizard (Input → Assessment → Documents)
- window.storage persistence (not localStorage)
- Fully Claude API-powered (not standalone)

#### Requirements

- Update README.md Artifact Edition section to accurately describe v5
- Correct line count, step count, storage mechanism, and API dependency

#### Acceptance Criteria

- [ ] README accurately describes v5 artifact architecture
- [ ] No references to "standalone" or "no API" for the artifact edition

---

### REQ-6: Update Artifact Source in Repo

**Priority:** P6
**Effort:** Small (file management + README edit)

#### Problem

The repo contains the old pre-v5 artifact (`job-apply-artifact.html`, ~3,100 lines, client-side heuristic parsing, localStorage). The published claude.ai artifact is v5 — a completely different codebase.

#### Decision

Archive old artifact, replace with v5, document the change. The old artifact was standalone (no API) but non-functional for real job applications (heuristic matching was poor). v5 is dramatically better.

#### Requirements

- Replace `job-apply-artifact.html` with v5 artifact source
- Add note in README that the artifact now requires claude.ai
- Document the breaking change for anyone using the old standalone version

#### Acceptance Criteria

- [ ] `job-apply-artifact.html` contains v5 source
- [ ] README documents the claude.ai requirement
- [ ] Change is noted in commit history

---

### REQ-7: CLI Tier Requirements Documentation

**Priority:** P7
**Effort:** Tiny (documentation) — re-architecture decision deferred

#### Problem

The README doesn't mention that Claude Code Skills require Pro/Max/Team/Enterprise. Free tier users can't use the CLI edition. This matters because the project's mission is helping job seekers who "don't have money yet."

#### Requirements

- Add clear tier requirements to README
- Direct free-tier users to the Artifact or Web Chat editions
- Evaluate whether CLI edition should be re-architected as a Claude Code command/prompt rather than a Skill (decision deferred)

#### Acceptance Criteria

- [ ] README clearly states tier requirements for each edition
- [ ] Free-tier users are directed to appropriate editions

---

### REQ-8: Profile Portability Across Editions

**Priority:** P8
**Effort:** Medium

#### Problem

The Web Chat edition generates `profile.yaml` for persistence across sessions. The CLI uses `config.yaml`. These formats aren't documented or interchangeable. There's no path between editions.

#### Requirements

- Document profile.yaml schema
- Evaluate making CLI config.yaml and Web Chat profile.yaml interchangeable (or at least importable between editions)

#### Acceptance Criteria

- [ ] profile.yaml schema is documented
- [ ] Import path between editions is defined (even if not yet implemented)

---

## 4. Future Considerations

### Competitive Feature Gaps

| Feature | Priority | Notes |
|---|---|---|
| Batch job processing (3–5 JDs) | Low | Competitors support this |
| Company research via web search | Medium | Adds culture context |
| Interview question generation | Medium | Artifact-only today — port to CLI/Web Chat |
| Application tracking/history | Medium | CLI-only today — add to artifact via window.storage |
| LinkedIn contact matching | Low | Privacy concerns |
| LaTeX/PDF output | Low | .docx is more ATS-compatible |

### Artifact Code Debt

| Item | Severity | Description |
|---|---|---|
| `_skillLevels` dead code | Low | Initialized empty, never populated. Remove or implement. |
| `skillProfile` storage key | Low | Referenced in clearAll but never written. Remove or implement. |
| `_parseJSON` attempt 4 regex | Low | Uses lookbehind — works in modern browsers but fragile. |
| Coaching stale scores | Medium | If user has pending overrides, coaching sees stale scores. Run `_recomputeScores` before coaching API call. |
| Recruiter phrase validation | Medium | Verify phrases actually appear in JD text. Flag unverified. |

---

## 5. Out of Scope

- **Server-side deployment** — Artifact stays client-only. No backend.
- **User accounts / cloud sync** — Conflicts with privacy-first architecture.
- **PDF generation in artifact** — Browser sandbox limitations. .doc download is sufficient.
- **Mobile app** — Artifact is already mobile-responsive.
- **Monetization** — Free tool for job seekers. Revenue comes from demonstrating capabilities.
