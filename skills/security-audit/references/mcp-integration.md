# Semgrep MCP integration

The Semgrep team ships an MCP server at [`github.com/semgrep/mcp`](https://github.com/semgrep/mcp). Where the current `scripts/security_audit.py` invokes Semgrep via subprocess, the same operations can run through the MCP protocol with better error handling, typed responses, and access to capabilities that subprocess doesn't expose.

This document describes the integration pattern. The actual pivot lands incrementally; this is the architectural setup.

## What the Semgrep MCP server exposes

Seven tools, all callable from any MCP client (Claude Code with MCP enabled, Cursor, the helper in this skill, etc.):

| Tool | Purpose | Replaces subprocess of |
|---|---|---|
| `semgrep_scan` | Scan a directory or files against a named rule pack | `semgrep scan --config=X` |
| `semgrep_scan_with_custom_rule` | Scan against a custom rule YAML | `semgrep scan --config=<file>` |
| `security_check` | Bundled "best practice" scan with a default rule set | `semgrep scan --config=auto` |
| `get_abstract_syntax_tree` | Inspect the AST of a code snippet for any supported language | (no subprocess equivalent) |
| `semgrep_findings` | Pull historical findings from a connected AppSec Platform tenant | (requires login) |
| `supported_languages` | List languages Semgrep can scan | `semgrep show supported-languages` |
| `semgrep_rule_schema` | Return the rule YAML grammar with examples | (no subprocess equivalent) |

The two that justify the pivot:

- **`get_abstract_syntax_tree`** lets the rule-authoring flow inspect the actual AST before drafting patterns. Subprocess Semgrep doesn't expose this.
- **`semgrep_rule_schema`** lets the LLM look up the grammar before writing a rule, instead of guessing. Used by Trail of Bits' `semgrep-rule-creator` skill internally.

## Integration pattern

Three tiers, in order of preference:

### Tier 1: Claude Code with Semgrep MCP server configured

When the user has the Semgrep MCP server in their `~/.claude/config.json` (or `.mcp.json` in the project), Claude Code routes Semgrep calls through MCP transparently. The skill makes regular tool-use calls (`semgrep_scan(...)`) and the MCP infrastructure handles transport.

```bash
# Add to ~/.claude/config.json or project .mcp.json
{
  "mcpServers": {
    "semgrep": {
      "command": "uvx",
      "args": ["semgrep-mcp"]
    }
  }
}
```

This is the recommended path for users running `/security-audit` interactively.

### Tier 2: Script calls MCP server via stdio

For CI mode (`--tools-only`), `scripts/security_audit.py` spawns the MCP server as a subprocess and communicates over stdin/stdout using JSON-RPC. See `mcp_client.py` (sibling module) for the thin wire-protocol implementation.

```python
from scripts.mcp_client import SemgrepMCPClient

client = SemgrepMCPClient.spawn()
try:
    findings = client.call(
        "semgrep_scan_with_custom_rule",
        {"path": "src/", "rule": rule_yaml},
    )
finally:
    client.close()
```

Falls back to subprocess if MCP server can't be spawned (missing `uvx` or `semgrep-mcp` package). The skill never errors out when MCP is unavailable; it just runs the legacy path.

### Tier 3: Plain subprocess (current behavior)

For environments where neither Claude Code MCP nor the MCP server install is available, the script keeps the existing subprocess flow. This is the fallback. The pivot doesn't remove it.

## Why pivot gradually

The Semgrep subprocess interface is stable and the existing script works. The case for MCP is:

1. **Better error handling.** Subprocess returns rc + stdout/stderr; MCP returns typed errors with structured detail.
2. **Capabilities subprocess doesn't expose.** AST inspection, rule schema, AppSec Platform integration.
3. **Forward compatibility.** Cursor, Vercel Agent, and other MCP-enabled tools consume the same surface. A skill that's MCP-native works in more places.
4. **Simpler authoring loop.** The Trail of Bits skills (`semgrep-rule-creator`) already use MCP; the skill can compose with them more naturally if we share the transport.

Reasons not to do the full pivot in one PR:

1. Requires the user to have `uvx` or the Semgrep MCP server installed; the subprocess path needs zero setup.
2. Error modes are different and the script's tests assume the subprocess shape.
3. MCP server startup adds 1 to 3 seconds; in CI runs this matters.

The plan is: ship the MCP-aware helper alongside the existing subprocess path. Let `--use-mcp` opt in. Measure performance and reliability. Once MCP is the more reliable path in practice, flip the default.

## Roadmap

- [x] Document the integration pattern (this file).
- [x] Add `scripts/mcp_client.py` as a thin stdio JSON-RPC client.
- [ ] Add `--use-mcp` flag to `scan` subcommand; route through MCP when set.
- [ ] Add `--use-mcp` to `validate-rule` (Phase 6 / PR-F integration).
- [ ] Add a project-profiler subcommand that uses `supported_languages` + manifest detection to recommend rule packs.
- [ ] Use `semgrep_rule_schema` in the Phase 6 LLM rule-authoring prompt (auto-include the grammar so the model doesn't guess).
- [ ] Flip default once MCP path is stable.

## Reading list

- [Semgrep MCP server (GitHub)](https://github.com/semgrep/mcp)
- [Semgrep blog: Cursor Hooks + MCP](https://semgrep.dev/blog/2025/cursor-hooks-mcp-server/)
- [MCP specification](https://spec.modelcontextprotocol.io/)
- [Trail of Bits semgrep-rule-creator skill](https://github.com/trailofbits/skills/tree/main/plugins/semgrep-rule-creator) (uses Semgrep MCP internally)
