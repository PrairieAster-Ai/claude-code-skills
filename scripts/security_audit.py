#!/usr/bin/env python3
"""
Deterministic security audit runner extracted from the security-audit skill.

This script handles the tool-driven portion of the workflow:
- diff discovery
- tool selection
- scanner execution
- SARIF/JSON artifact collection
- markdown/json summary generation
- optional PR commenting

It intentionally does not attempt LLM verification, deduplication, or patching.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / ".artifacts" / "security-audit"


@dataclass
class CommandResult:
    name: str
    command: list[str]
    artifact: str | None
    status: str
    returncode: int | None
    findings: int | None
    stdout: str
    stderr: str
    skipped_reason: str | None = None


def run(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=capture,
        check=check,
    )


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def git_changed_files(base: str) -> list[str]:
    try:
        result = run(["git", "diff", "--name-only", f"{base}..."])
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.stderr.strip() or exc.stdout.strip() or f"git diff failed for base {base}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def merge_base(base: str) -> str:
    try:
        result = run(["git", "merge-base", "HEAD", base])
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.stderr.strip() or exc.stdout.strip() or f"git merge-base failed for base {base}")
    return result.stdout.strip()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def count_sarif_findings(path: Path) -> int | None:
    payload = load_json(path)
    if not isinstance(payload, dict):
        return None
    count = 0
    for run_item in payload.get("runs", []):
        if isinstance(run_item, dict):
            results = run_item.get("results", [])
            if isinstance(results, list):
                count += len(results)
    return count


def count_socket_findings(path: Path) -> int | None:
    payload = load_json(path)
    if isinstance(payload, dict):
        if isinstance(payload.get("issues"), list):
            return len(payload["issues"])
        if isinstance(payload.get("findings"), list):
            return len(payload["findings"])
    return None


def count_artifact_findings(path: Path) -> int | None:
    if not path.exists():
        return None
    if path.suffix == ".sarif":
        return count_sarif_findings(path)
    if path.suffix == ".json":
        return count_socket_findings(path)
    return None


def run_tool(
    name: str,
    command: list[str],
    artifact: Path | None,
    required_binary: str,
) -> CommandResult:
    if not command_exists(required_binary):
        return CommandResult(
            name=name,
            command=command,
            artifact=str(artifact) if artifact else None,
            status="skipped",
            returncode=None,
            findings=None,
            stdout="",
            stderr="",
            skipped_reason=f"missing dependency: {required_binary}",
        )

    try:
        result = run(command, check=False)
    except OSError as exc:
        return CommandResult(
            name=name,
            command=command,
            artifact=str(artifact) if artifact else None,
            status="error",
            returncode=None,
            findings=None,
            stdout="",
            stderr=str(exc),
        )

    findings = count_artifact_findings(artifact) if artifact else None
    status = "ok" if result.returncode == 0 else "warning"

    return CommandResult(
        name=name,
        command=command,
        artifact=str(artifact) if artifact else None,
        status=status,
        returncode=result.returncode,
        findings=findings,
        stdout=result.stdout,
        stderr=result.stderr,
    )


def detect_categories(files: Iterable[str]) -> dict[str, bool]:
    files = list(files)
    return {
        "python": any(file.endswith(".py") for file in files),
        "go": any(file.endswith(".go") for file in files),
        "js": any(file.endswith((".js", ".jsx", ".ts", ".tsx")) for file in files),
        "iac": any(
            file == "Dockerfile"
            or file.endswith(".tf")
            or file.startswith("k8s/")
            or file.startswith("helm/")
            for file in files
        ),
        "deps": any(
            Path(file).name in {
                "package.json",
                "package-lock.json",
                "requirements.txt",
                "pyproject.toml",
                "go.mod",
                "Cargo.toml",
            }
            for file in files
        ),
    }


def build_tool_plan(base: str, changed_files: list[str], output_dir: Path, deep: bool) -> list[tuple[str, list[str], Path | None, str]]:
    mb = merge_base(base)
    categories = detect_categories(changed_files)
    plan: list[tuple[str, list[str], Path | None, str]] = []

    semgrep_out = output_dir / "semgrep.sarif"
    plan.append(
        (
            "semgrep",
            [
                "semgrep",
                "ci",
                f"--baseline-commit={mb}",
                "--sarif",
                f"--sarif-output={semgrep_out}",
                "--quiet",
            ],
            semgrep_out,
            "semgrep",
        )
    )

    gitleaks_out = output_dir / "gitleaks.sarif"
    # Resolve symbolic refs (origin/HEAD) to a concrete SHA before passing to
    # --log-opts; some gitleaks versions choke on two-dot ranges with symbolic
    # refs.
    plan.append(
        (
            "gitleaks",
            [
                "gitleaks",
                "git",
                "--report-format",
                "sarif",
                "--report-path",
                str(gitleaks_out),
                f"--log-opts={mb}..HEAD",
                "--no-banner",
            ],
            gitleaks_out,
            "gitleaks",
        )
    )

    osv_out = output_dir / "osv.sarif"
    plan.append(
        (
            "osv-scanner",
            [
                "osv-scanner",
                "scan",
                "source",
                "--format=sarif",
                f"--output={osv_out}",
                "--recursive",
                ".",
            ],
            osv_out,
            "osv-scanner",
        )
    )

    if changed_files:
        lizard_out = output_dir / "lizard.xml"
        plan.append(
            (
                "lizard",
                ["lizard", "-X", *changed_files],
                lizard_out,
                "lizard",
            )
        )

    if categories["iac"]:
        trivy_out = output_dir / "trivy-config.sarif"
        plan.append(
            (
                "trivy",
                ["trivy", "config", "--format=sarif", f"-o={trivy_out}", "."],
                trivy_out,
                "trivy",
            )
        )

    if categories["deps"]:
        socket_out = output_dir / "socket.json"
        plan.append(
            (
                "socket",
                ["socket", "scan", "create", "--json", "."],
                socket_out,
                "socket",
            )
        )

    if categories["python"]:
        python_files = [file for file in changed_files if file.endswith(".py")]
        bandit_out = output_dir / "bandit.sarif"
        plan.append(
            (
                "bandit",
                ["bandit", "-r", *python_files, "-f", "sarif", "-o", str(bandit_out), "--quiet"],
                bandit_out,
                "bandit",
            )
        )

    if categories["go"]:
        govuln_out = output_dir / "govulncheck.sarif"
        plan.append(
            (
                "govulncheck",
                ["govulncheck", "-format", "sarif", "./..."],
                govuln_out,
                "govulncheck",
            )
        )

    if categories["js"]:
        js_files = [file for file in changed_files if file.endswith((".js", ".jsx", ".ts", ".tsx"))]
        eslint_out = output_dir / "eslint-security.sarif"
        # ESLint 9+ removed --no-eslintrc; the modern way is a scratch flat
        # config file that opts out of project config and loads only the
        # security plugin's rules.
        eslint_config = output_dir / "eslint-security.config.mjs"
        eslint_config.write_text(
            "import security from 'eslint-plugin-security';\n"
            "export default [{\n"
            "  plugins: { security },\n"
            "  rules: {\n"
            "    'security/detect-eval-with-expression': 'error',\n"
            "    'security/detect-non-literal-fs-filename': 'warn',\n"
            "    'security/detect-child-process': 'error',\n"
            "    'security/detect-unsafe-regex': 'warn',\n"
            "  },\n"
            "}];\n",
            encoding="utf-8",
        )
        plan.append(
            (
                "eslint-security",
                [
                    "npx",
                    "--yes",
                    "eslint",
                    "--config",
                    str(eslint_config),
                    "--format",
                    "@microsoft/eslint-formatter-sarif",
                    "-o",
                    str(eslint_out),
                    *js_files,
                ],
                eslint_out,
                "npx",
            )
        )

    if deep:
        trufflehog_out = output_dir / "trufflehog.json"
        plan.append(
            (
                "trufflehog",
                ["trufflehog", "git", "file://.", "--only-verified", "--json"],
                trufflehog_out,
                "trufflehog",
            )
        )

    return plan


def persist_artifact_output(result: CommandResult, plan_artifact: Path | None) -> None:
    if result.name == "lizard" and plan_artifact:
        write_text(plan_artifact, result.stdout)
    elif result.name in {"govulncheck", "socket", "trufflehog"} and plan_artifact:
        write_text(plan_artifact, result.stdout)


def make_summary(base: str, changed_files: list[str], results: list[CommandResult]) -> dict:
    total_findings = 0
    findings_known = 0
    for result in results:
        if result.findings is not None:
            findings_known += 1
            total_findings += result.findings

    return {
        "base": base,
        "changed_files": changed_files,
        "changed_file_count": len(changed_files),
        "total_findings": total_findings if findings_known else None,
        "tool_results": [
            {
                "name": result.name,
                "status": result.status,
                "returncode": result.returncode,
                "findings": result.findings,
                "artifact": result.artifact,
                "command": result.command,
                "skipped_reason": result.skipped_reason,
            }
            for result in results
        ],
    }


def summary_markdown(summary: dict) -> str:
    lines = [
        "# Security Audit Summary",
        "",
        f"- Base: `{summary['base']}`",
        f"- Changed files: `{summary['changed_file_count']}`",
        f"- Total findings: `{summary['total_findings'] if summary['total_findings'] is not None else 'unknown'}`",
        "",
        "| Tool | Status | Findings | Artifact |",
        "|---|---|---:|---|",
    ]
    for tool in summary["tool_results"]:
        artifact = tool["artifact"] or "-"
        findings = tool["findings"] if tool["findings"] is not None else "-"
        status = tool["status"]
        if tool["skipped_reason"]:
            status = f"{status} ({tool['skipped_reason']})"
        lines.append(f"| {tool['name']} | {status} | {findings} | `{artifact}` |")
    if summary["changed_files"]:
        lines.extend(["", "## Changed Files", ""])
        lines.extend([f"- `{path}`" for path in summary["changed_files"]])
    return "\n".join(lines) + "\n"


def cmd_scan(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    changed_files = git_changed_files(args.base)
    if not changed_files:
        summary = {
            "base": args.base,
            "changed_files": [],
            "changed_file_count": 0,
            "total_findings": 0,
            "tool_results": [],
            "message": f"No changes vs {args.base}",
        }
        write_text(output_dir / "summary.json", json.dumps(summary, indent=2) + "\n")
        write_text(output_dir / "summary.md", "# Security Audit Summary\n\nNo changes to audit.\n")
        print(f"No changes vs {args.base}")
        return 0

    results: list[CommandResult] = []
    for name, command, artifact, required_binary in build_tool_plan(args.base, changed_files, output_dir, args.deep):
        result = run_tool(name, command, artifact, required_binary)
        persist_artifact_output(result, artifact)
        results.append(result)

    summary = make_summary(args.base, changed_files, results)
    write_text(output_dir / "summary.json", json.dumps(summary, indent=2) + "\n")
    write_text(output_dir / "summary.md", summary_markdown(summary))

    print(json.dumps(summary, indent=2))

    if args.fail_on_findings and summary["total_findings"]:
        return 1
    return 0


def cmd_comment(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir).resolve()
    summary_path = output_dir / "summary.md"
    if not summary_path.exists():
        print(f"Missing summary markdown: {summary_path}", file=sys.stderr)
        return 1
    if not command_exists("gh"):
        print("Missing dependency: gh", file=sys.stderr)
        return 1

    # Pre-flight: load PR metadata so we can do the cross-repo check and
    # build the dedup marker.
    try:
        pr_meta = subprocess.run(
            [
                "gh", "pr", "view", str(args.pr),
                "--json", "state,headRefOid,baseRepository",
                "-q", ".",
            ],
            cwd=ROOT, text=True, capture_output=True, check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"gh pr view failed: {exc.stderr.strip() or exc.stdout.strip()}", file=sys.stderr)
        return 1
    pr = json.loads(pr_meta.stdout)
    state = pr.get("state")
    head_sha = pr.get("headRefOid", "")
    base_repo = (pr.get("baseRepository") or {}).get("nameWithOwner")

    # Cross-repo safety: the cwd's repo must match the PR's base repo so we
    # don't post to a different repo by accident.
    cwd_repo_proc = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    cwd_repo = cwd_repo_proc.stdout.strip() if cwd_repo_proc.returncode == 0 else None
    if base_repo and cwd_repo and cwd_repo != base_repo:
        print(f"Refusing to post: cwd repo ({cwd_repo}) != PR base repo ({base_repo})", file=sys.stderr)
        return 1

    if state and state != "OPEN":
        print(f"PR #{args.pr} is {state}; skipping comment", file=sys.stderr)
        return 0

    # HTML-comment marker for deterministic dedup on subsequent pushes.
    marker = f"<!-- security-audit:sha={head_sha} -->"
    existing_proc = subprocess.run(
        ["gh", "pr", "view", str(args.pr), "--json", "comments", "-q", ".comments[].body"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if marker and marker in (existing_proc.stdout or ""):
        print(f"Already audited {head_sha}; skipping comment", file=sys.stderr)
        return 0

    body = summary_path.read_text(encoding="utf-8")
    if not body.startswith(marker):
        body = f"{marker}\n{body}"

    # Write a temp file with the marker prepended so gh --body-file sees it.
    marked_path = output_dir / "summary-pr-comment.md"
    marked_path.write_text(body, encoding="utf-8")

    result = run(
        ["gh", "pr", "comment", str(args.pr), "--body-file", str(marked_path)],
        check=False,
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def cmd_rule_stats(args: argparse.Namespace) -> int:
    """Summarize .claude/security-audit/rule-stats.jsonl to identify rules
    with poor signal-to-noise in this repo. Append-only ledger; one row
    per triage decision."""
    import datetime
    from collections import defaultdict

    ledger = ROOT / ".claude" / "security-audit" / "rule-stats.jsonl"
    if not ledger.exists():
        print(f"No ledger at {ledger}", file=sys.stderr)
        return 0

    # Parse --since: "180d" or "30d" or an ISO date
    cutoff = None
    if args.since:
        if args.since.endswith("d") and args.since[:-1].isdigit():
            days = int(args.since[:-1])
            cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        else:
            try:
                cutoff = datetime.datetime.fromisoformat(args.since.replace("Z", "+00:00"))
            except ValueError:
                print(f"Bad --since value: {args.since}", file=sys.stderr)
                return 1

    by_rule: dict[str, dict[str, int]] = defaultdict(lambda: {"tp": 0, "fp": 0, "unconfirmed": 0})
    parsed = 0
    skipped = 0

    for raw in ledger.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError:
            skipped += 1
            continue
        if cutoff is not None:
            ts = row.get("ts", "")
            try:
                row_ts = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                continue
            if row_ts.replace(tzinfo=None) < cutoff:
                continue
        rule = f"{row.get('tool', '?')}:{row.get('rule_id', '?')}"
        verdict = row.get("verdict", "unconfirmed")
        if verdict in by_rule[rule]:
            by_rule[rule][verdict] += 1
        else:
            by_rule[rule]["unconfirmed"] += 1
        parsed += 1

    if not by_rule:
        print(f"No entries in window. Parsed: {parsed}, skipped: {skipped}", file=sys.stderr)
        return 0

    rows = []
    for rule, counts in by_rule.items():
        total = sum(counts.values())
        fp_rate = counts["fp"] / total if total else 0.0
        rows.append((rule, counts, total, fp_rate))
    rows.sort(key=lambda r: r[3], reverse=True)

    for rule, counts, total, fp_rate in rows:
        print(f"Rule: {rule}")
        print(f"  Total triaged: {total}  (TP: {counts['tp']}, FP: {counts['fp']}, unconfirmed: {counts['unconfirmed']})")
        print(f"  FP rate: {fp_rate:.0%}")
        if fp_rate >= args.threshold and total >= args.min_total:
            print(
                "  Suggestion: high FP rate. Consider promoting a global memory, "
                "adjusting the confidence floor for this rule, or excluding it via "
                ".claude/security-config.yaml."
            )
        elif fp_rate == 0 and counts["tp"] >= 3:
            print("  Suggestion: high-signal rule, keep at default sensitivity.")
        print()

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Run tool-driven security audit against a git diff.")
    scan.add_argument("--base", default="origin/HEAD", help="Git base ref to diff against.")
    scan.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Artifact output directory.")
    scan.add_argument("--deep", action="store_true", help="Enable deep mode add-ons such as trufflehog.")
    scan.add_argument("--fail-on-findings", action="store_true", help="Exit non-zero if findings are detected.")
    scan.set_defaults(func=cmd_scan)

    ci = subparsers.add_parser("ci", help="CI-friendly alias for scan with non-zero exit on findings.")
    ci.add_argument("--base", default="origin/HEAD", help="Git base ref to diff against.")
    ci.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Artifact output directory.")
    ci.add_argument("--deep", action="store_true", help="Enable deep mode add-ons such as trufflehog.")
    ci.set_defaults(func=lambda args: cmd_scan(argparse.Namespace(**vars(args), fail_on_findings=True)))

    comment = subparsers.add_parser("comment", help="Post the latest markdown summary to a GitHub PR.")
    comment.add_argument("--pr", required=True, help="Pull request number.")
    comment.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Artifact output directory.")
    comment.set_defaults(func=cmd_comment)

    stats = subparsers.add_parser(
        "rule-stats",
        help="Summarize .claude/security-audit/rule-stats.jsonl to identify high-FP rules in this repo.",
    )
    stats.add_argument("--since", default="180d", help="Look-back window. Format: NNd or ISO date. Default: 180d.")
    stats.add_argument("--threshold", type=float, default=0.5, help="FP-rate threshold for the high-FP suggestion. Default: 0.5.")
    stats.add_argument("--min-total", type=int, default=3, help="Minimum triage count before suggesting changes. Default: 3.")
    stats.set_defaults(func=cmd_rule_stats)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
