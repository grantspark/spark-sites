# OpenClaw + Telegram Setup Research

**Date:** 2026-02-19
**Status:** Complete — bot running on Hostinger VPS

---

## What is OpenClaw?

Self-hosted AI assistant that connects to messaging apps (Telegram, WhatsApp, Slack, Discord, etc.). Runs as a Docker container on a VPS. Uses AI APIs (Anthropic, OpenAI, etc.) as the backend.

## Setup Completed

- **Host:** Hostinger VPS
- **Model:** claude-sonnet-4-6 via Anthropic API
- **Channel:** Telegram (bot created via @BotFather)
- **Status:** Running, paired, functional

## Setup Steps (for reference)

1. SSH into VPS
2. `sudo apt install git -y`
3. `git clone https://github.com/openclaw/openclaw.git && cd openclaw`
4. `./docker-setup.sh` — Quick Start, Anthropic, Telegram
5. Fix permissions: `sudo chown -R 1000:1000 ~/.openclaw`
6. Re-run `sudo ./docker-setup.sh`
7. Approve Telegram user: `docker compose exec openclaw-gateway node dist/index.js pairing approve telegram <CODE>`
8. Verify: `docker compose ps`

## Known Issues

- EACCES permission error on fresh install — fix with `sudo chown -R 1000:1000 ~/.openclaw`
- `CLAUDE_WEB_COOKIE` / `CLAUDE_WEB_SESSION_KEY` warnings are harmless (optional web integration)
- SSH timeout during setup if you leave terminal idle — have API key ready before starting
- Right-click to paste in terminal (Ctrl+V can break it)

## Limitations Discovered

- OpenClaw is a **generic chatbot** — no access to local files, git repos, or reference docs
- Conversations don't feed back into git/reference files
- One-way knowledge only: you can upload docs to its memory (RAG) but it can't write back
- **Not suitable for continuing Claude Code work on the go**

## Better Alternative Found: claude-code-telegram

A project that connects actual Claude Code to Telegram with full repo access:

- **Repo:** https://github.com/RichardAtCT/claude-code-telegram
- **What it does:** Runs Claude Code behind a Telegram bot
- **Key advantage:** Full access to reference files, git history, can read AND write to repos
- **Where to run:** VPS (always on) or local machine (only when PC is on)
- **Also see:** https://github.com/JessyTsui/Claude-Code-Remote (multi-channel: email, Discord, Telegram)

## Sources

- [Hostinger OpenClaw Tutorial](https://www.hostinger.com/tutorials/how-to-set-up-openclaw)
- [OpenClaw Pairing Docs](https://docs.openclaw.ai/channels/pairing)
- [OpenClaw Docker Docs](https://docs.openclaw.ai/install/docker)
- [claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram)
- [Claude Code from Phone (Medium)](https://medium.com/@amirilovic/how-to-use-claude-code-from-your-phone-with-a-telegram-bot-dde2ac8783d0)
