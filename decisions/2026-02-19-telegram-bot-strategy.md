# Decision: Telegram Bot Strategy

**Date:** 2026-02-19
**Status:** Decided — next step is claude-code-telegram setup

---

## Context

Want to access our centralized business brain (reference files, decisions, research) from mobile via Telegram. Currently all work happens in Claude Code sessions on desktop.

## Options Evaluated

### Option A: OpenClaw (generic chatbot)
- **Pros:** Already set up and running on Hostinger VPS, easy Telegram integration
- **Cons:** No access to repos/reference files, conversations don't feed back to git, would have to repeat context already captured
- **Verdict:** Good for generic AI chat on the go, not for continuing business work

### Option B: OpenClaw + RAG knowledge base
- **Pros:** Can upload reference files so it knows business context
- **Cons:** One-way only — reads your brain but can't write back to git, still a separate system
- **Verdict:** Better than vanilla OpenClaw but still disconnected

### Option C: claude-code-telegram (winner)
- **Pros:** Runs actual Claude Code, full repo access, reads AND writes reference files, session persistence, builds on all prior work
- **Cons:** More setup, runs Claude Code (uses API credits), security considerations (messages pass through Telegram servers)
- **Verdict:** This is what we want — same brain, same tools, from phone

## Decision

**Go with Option C: claude-code-telegram on the Hostinger VPS.**

Keep OpenClaw running as a separate bot for quick generic AI questions. Use claude-code-telegram as the primary mobile workflow for business work.

## Next Steps

1. Set up claude-code-telegram on Hostinger VPS
2. Clone business repos to VPS
3. Create a second Telegram bot (separate from OpenClaw bot)
4. Test full workflow: message from phone → reads reference files → writes back to git
5. Evaluate security implications (no secrets via Telegram)
