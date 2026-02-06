# Job Apply — Web Chat Setup

Generate tailored cover letters and resumes using Claude's free web chat. No install required.

## Quick Start

1. Go to [claude.ai](https://claude.ai) and create a new **Project**
2. Download these 2 files from the [`webchat/`](https://github.com/PrairieAster-Ai/claude-code-skills/tree/main/skills/job-apply/webchat) folder:
   - **SKILL-webchat.md** — add as Project instructions
   - **generate_word_docs_web.py** — add to Project knowledge
3. Start a conversation — upload your resume (.docx or .pdf) and paste a job description

## What to Expect

- Claude scores your fit, shows strengths and gaps, and asks if you want to proceed
- Say "Yes" and Claude generates .docx cover letter + resume for download
- **3-4 messages total** per application

## Returning Users

After your first run, Claude offers a `profile.yaml` file. Save it. Next time, upload `profile.yaml` instead of your resume to skip parsing and save a message.

## More Info

This is the web chat edition of the [job-apply skill](https://github.com/PrairieAster-Ai/claude-code-skills/tree/main/skills/job-apply) for Claude Code. See the [full README](../README.md) for CLI setup, configuration, and troubleshooting.
