# DevSentinel 🛡️

> ⚠️ **Work in progress** — Active development.

An autonomous monitoring, diagnosis, and incident remediation system for Docker-based infrastructures. DevSentinel watches your containers in real time, detects anomalies, analyzes them with AI, and lets you resolve issues directly from Telegram — no need to touch the server.

## What problem does it solve?

When something breaks in production, a DevOps engineer has to manually: review logs, correlate with recent deployments, identify the root cause, apply the fix, and write a post-mortem. All of that, usually, at 3am.

DevSentinel automates that entire workflow.

## Features

- 🔍 **Real-time event monitoring** — reacts instantly to Docker container events (crash, stop, kill, OOM) with no polling delay
- 📊 **Metrics monitoring** — checks CPU and memory usage every 30 seconds and alerts if thresholds are exceeded
- 🤖 **AI-powered diagnosis** — when a container crashes unexpectedly, Groq analyzes logs and metrics and explains what happened, the probable cause, and a suggested fix
- 🧠 **Smart alert routing** — manual stops get a simple notification; unexpected crashes get the full AI analysis
- 📲 **Telegram alerts** with approval buttons to trigger fixes _(coming in Phase 3)_
- 🔧 **Automatic remediation** with human-in-the-loop (restart container, scale replicas...) _(coming in Phase 3)_
- 📄 **Auto-generated post-mortems** in PDF after each incident _(coming in Phase 4)_
- 📊 **Web dashboard** to visualize infrastructure status in real time _(coming in Phase 4)_

## Tech stack

- **Backend:** Python · FastAPI · Docker SDK
- **AI:** Groq API (llama-3.1-8b-instant)
- **Database:** SQLite
- **Alerts:** Telegram Bot API
- **Frontend:** HTML · CSS · JavaScript
- **Environment:** uv · Docker · OrbStack

## Roadmap

- [x] Phase 1 — Docker container monitoring and basic Telegram alerts
- [x] Phase 2 — LLM-powered incident analysis
- [ ] Phase 3 — Remediation with Telegram approval flow
- [ ] Phase 4 — Web dashboard and automatic PDF post-mortem generation

## Getting started

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- [Docker](https://www.docker.com/) or [OrbStack](https://orbstack.dev/) (recommended for Mac)
- A [Telegram bot](https://t.me/BotFather) — create one with BotFather and get your token
- Your Telegram Chat ID — get it by messaging [@userinfobot](https://t.me/userinfobot)
- A [Groq API key](https://console.groq.com) — free tier is enough

### Installation

```bash
git clone https://github.com/amandabz/devsentinel.git
cd devsentinel
uv sync
cp .env.example .env  # Fill in your keys (see below)
```

### Environment variables

Copy `.env.example` to `.env` and fill in the values:

```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
GROQ_API_KEY=your_groq_api_key
```

### Run

```bash
uv run python -m devsentinel.main
```

You should see the following in the terminal:

```
🛡️ DevSentinel started.
👂 Event listener started.
📊 Metrics polling started.
```

DevSentinel runs two parallel processes: one that listens to Docker events in real time, and one that checks CPU and memory every 30 seconds.

### How alerts work

| Situation | Alert |
|---|---|
| Container stopped manually (`docker stop`) | Simple notification, no AI |
| Container crashed unexpectedly | AI diagnosis with probable cause and suggested fix |
| CPU or memory exceeds 80% | AI diagnosis with metrics and logs |

### Test it

Start a sample container:

```bash
docker run -d --name test-nginx nginx
```

Then stop it to trigger an alert:

```bash
docker stop test-nginx
```

You should receive a Telegram notification instantly.

To simulate a crash, kill the container directly:

```bash
docker kill test-nginx
```

This time the alert will include an AI-powered diagnosis.

---

Built by [Amanda](https://github.com/amandabz).
