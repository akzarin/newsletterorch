# Tech Curator Bot (Experiment)

> A Python-based automation project designed to curate and send tech newsletters (Software Engineering, QA/Playwright, and AI/LLMs) to a Discord channel.

## Project Overview
This project was initially architected to run as a scheduled cloud job using **GitHub Actions** and the **Google Gemini API**. The goal was to build an autonomous system that searches the web for the latest tech news, compiles a markdown newsletter, and pushes it to Discord via Webhooks.

## System Architecture (Multi-Agent Design)
The core architecture was designed around an **Orchestrator Pattern (Actor-Critic Loop)** using AI Agents:
1. **Curator Agent (Actor):** Responsible for fetching web news and writing the initial Markdown draft.
2. **Validator (Python Script):** A programmatic dry-run step to validate formatting, Markdown structure, and length constraints.
3. **Reviewer Agent (Critic):** Triggered only if the Validator catches formatting errors, responsible for refactoring the output before the final Discord push.

## Tech Stack & Concepts Applied
- **Language:** Python 3
- **Environment Management:** `python-dotenv` for secure secret handling.
- **CLI Design:** `argparse` for modular execution and dry-run validation (`--validate-split`).
- **Integrations:** Discord Webhooks for rich Markdown message delivery.
- **Standard Library Delivery:** Built using native `urllib.request` and `json` to keep webhook execution lightweight and free of unnecessary runtime dependencies.

## Status & Learnings
The core Python infrastructure (Webhook delivery, CLI arguments, and `.env` security) is fully functional. 

However, the Cloud AI generation phase was paused. During architectural validation, it was identified that Google disabled the `google_search` grounding feature for Free Tier API accounts (resulting in `HTTP 429 Quota Exceeded` errors). Rather than forcing a costly cloud architecture or building complex web scrapers, the project was kept as a local scheduled task.

This repository serves as a foundational study in **Multi-Agent System Design, Webhook Integrations, and API limitations**.

## Authorship & Methodology
All application code, data structures, CLI logic, and error-handling routines in this repository were written directly by the author. AI was used exclusively as an architectural sparring partner, code reviewer, and Socratic mentor—no code was auto-generated.
