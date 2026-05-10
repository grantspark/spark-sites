---
type: signal
status: active
date: 2026-05-10
topics: [main-branch, mb-cli, claude-code, skill-discovery, smoke-test]
---
# `/mb-start` Discovery Gap Across Repos

## What Happened

Smoke-tested the v0.2 migration by running `/mb-start` in Claude Code across
the active repos. Results:

- **vip** — works natively (engine repo, `vip/.claude/skills/mb-start/` exists)
- **spark-sites, spark-coaching** — needed `mb skill link --repo .` to copy
  the 17 bundled mb skills into each repo's `.claude/skills/`. After that,
  `mb start` reports `Skills /mb-start wired` and the slash command resolves.
- **grant-sparks** — typing `/mb-start` ran `/daily-plan` instead. No
  `mb-start/` exists in `grant-sparks/.claude/skills/`, no user-level
  `~/.claude/skills/` exists, no mb plugin installed → Claude Code
  fuzzy-matched to the closest semantically similar custom skill
  (`daily-plan`).

## Why It Matters

Claude Code skill discovery is per-repo by default. Slash commands resolve in
this priority order:

1. Repo-local `<cwd>/.claude/skills/`
2. User-level `~/.claude/skills/` (didn't exist on this machine)
3. Plugins (none installed for Main Branch)

There is no `mb skill link --user` mode today; bundled mb skills must be
copied into each repo where you want `/mb-start` to resolve. The migration
tooling (`mb migrate`) does NOT auto-wire skills — that's a separate step.

## Decision (Today)

Wired mb skills into **spark-sites** and **spark-coaching** (the migrated
business repos). Did NOT wire into grant-sparks, spark-sales,
morgan-for-congress, or writing. grant-sparks is Lumen's orchestration hub
with its own custom skill set; if `/mb-start` is ever needed there,
`mb skill link --repo grant-sparks` is one command away.

## Watch For

- If/when `mb` ships a `--user` install mode or plugin manifest, revisit
  whether to centralize the bundled skills instead of copying per-repo.
- If `/daily-plan` keeps fuzzy-matching unintended slash commands in
  grant-sparks (or anywhere else), tighten its description or rename.

## Tools Used

| Tool | Role |
|------|------|
| `mb start --repo <path>` | Readiness check (no Claude Code launch) |
| `mb doctor <path>` | Full repo health check |
| `mb skill repair --repo <path>` | Inspect for shadowing skills (none found) |
| `mb skill link --repo <path>` | Copy 17 bundled mb skills into the repo |
