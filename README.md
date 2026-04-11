# DevSentinel 🛡️

> ⚠️ **Work in progress** — Active development.

An autonomous monitoring, diagnosis, and incident remediation system for Docker-based infrastructures. DevSentinel watches your containers in real time, detects anomalies, analyzes them with AI, and lets you resolve issues directly from Telegram — no need to touch the server.

## What problem does it solve?

When something breaks in production, a DevOps engineer has to manually: review logs, correlate with recent deployments, identify the root cause, apply the fix, and write a post-mortem. All of that, usually, at 3am.

DevSentinel automates that entire workflow.

## Features (planned)

- 🔍 **Real-time monitoring** of Docker containers (CPU, memory, status)
- 🤖 **AI-powered diagnosis** — when something fails, an LLM analyzes logs and metrics and explains what happened
- 📲 **Telegram alerts** with approval buttons to trigger fixes
- 🔧 **Automatic remediation** with human-in-the-loop (restart container, scale replicas...)
- 📄 **Auto-generated post-mortems** in PDF after each incident
- 📊 **Web dashboard** to visualize infrastructure status in real time

## Tech stack

- **Backend:** Python · FastAPI · Docker SDK
- **AI:** OpenAI API / Gemini
- **Database:** SQLite
- **Alerts:** Telegram Bot API
- **Frontend:** HTML · CSS · JavaScript
- **Environment:** uv · Docker · OrbStack

## Roadmap

- [ ] Phase 1 — Docker container monitoring and basic Telegram alerts
- [ ] Phase 2 — LLM-powered incident analysis
- [ ] Phase 3 — Remediation with Telegram approval flow
- [ ] Phase 4 — Web dashboard and automatic PDF post-mortem generation

## Getting started

```bash
git clone https://github.com/amandabz/devsentinel.git
cd devsentinel
uv sync
cp .env.example .env  # Fill in your keys
uv run uvicorn src.devsentinel.main:app --reload
```

## Environment variables

Copy `.env.example` to `.env` and fill in the values:

```
OPENAI_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

Built by [Amanda](https://github.com/amandabz).
