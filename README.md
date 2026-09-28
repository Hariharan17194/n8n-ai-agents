<div align="center">

<img src="docs/assets/banner.png" alt="n8n AI Agents" width="100%"/>

# n8n AI Agents

**Importable, production-style n8n workflows: a voice assistant, an MCP tool-calling agent, a Slack bot and an LLM-powered ETL pipeline.**

[![Validate workflows](https://github.com/Hariharan17194/n8n-ai-agents/actions/workflows/validate-n8n.yml/badge.svg)](https://github.com/Hariharan17194/n8n-ai-agents/actions/workflows/validate-n8n.yml)
![n8n](https://img.shields.io/badge/n8n-workflows-EA4B71?style=flat-square&logo=n8n&logoColor=white&labelColor=080B10)
![MCP](https://img.shields.io/badge/MCP-tools-42E6D4?style=flat-square&labelColor=080B10)
[![License: MIT](https://img.shields.io/badge/license-MIT-FFB454?style=flat-square&labelColor=080B10)](LICENSE)

</div>

---

## ✦ Workflows

| # | Workflow | What it does | Key nodes | Demo |
|---|---|---|---|---|
| 01 | [**Jarvis voice assistant**](workflows/01-jarvis-voice-assistant) | Telegram bot that takes voice or text, thinks with memory + tools, replies in **text and synthesized voice** | Telegram · OpenAI STT/TTS · AI Agent · SerpApi · Gmail · Calculator | [▶ video](https://github.com/Hariharan17194/n8n-ai-agents/releases/download/demos/jarvis-voice-assistant-demo.mp4) |
| 02 | [**MCP tool-calling agent**](workflows/02-mcp-agent) | Chat agent that calls tools exposed by a custom **MCP server** — search, Calendar, Sheets, Gmail | MCP Client · AI Agent · Simple Memory | [▶ video](https://github.com/Hariharan17194/n8n-ai-agents/releases/download/demos/mcp-agent-demo.mp4) |
| 03 | [**Slack recipe bot**](workflows/03-slack-recipe-bot) | Replies to a dish name with its ingredient list — curated table first, LLM fallback | Slack Trigger · Data Tables · LLM Chain | [▶ video](https://github.com/Hariharan17194/n8n-ai-agents/releases/download/demos/slack-recipe-bot-demo.mp4) |
| 04 | [**AI ETL pipeline**](workflows/04-ai-etl-pipeline) | Upload a messy CSV → LLM cleans/validates rows → split into clean output files | Form Trigger · Extract from File · LLM Chain · Code | — |

## ✦ Architecture — Jarvis voice assistant

```mermaid
flowchart LR
    TG([Telegram message]) --> SW{Voice or text?}
    SW -- voice --> DL[Download audio] --> STT[OpenAI speech-to-text]
    SW -- text --> SET[Normalise text]
    STT --> AG[AI Agent · GPT + window memory]
    SET --> AG
    AG <--> T1[SerpApi search]
    AG <--> T2[Gmail send]
    AG <--> T3[Calculator]
    AG --> TXT[Reply as text]
    AG --> TTS[OpenAI text-to-speech] --> VOI[Reply as voice note]

    classDef accent fill:#0C1017,stroke:#42E6D4,color:#E9EDF2;
    class AG accent;
```

## ✦ Import a workflow

1. In n8n: **Workflows → Import from File** → pick `workflows/<name>/workflow.json`.
2. Open every node showing a ⚠️ and attach **your own** credentials (OpenAI, Telegram, Slack, Google, SerpApi).
3. Follow that workflow's `README.md` for any extra setup (Slack app scopes, Data Table seed, MCP server URL).
4. Activate.

> **No secrets are committed.** CI fails the build if a workflow export contains credential values or hard-coded API keys.

## ✦ Repository layout

```text
workflows/
├── 01-jarvis-voice-assistant/
│   ├── workflow.json
│   ├── README.md
│   └── screenshot.png
├── 02-mcp-agent/
├── 03-slack-recipe-bot/
└── 04-ai-etl-pipeline/
    └── workflow.json
```

## ✦ Requirements

- n8n ≥ 1.x (self-hosted or cloud) — Data Tables needed for workflow 03
- API credentials for the services each workflow uses

## ✦ License

[MIT](LICENSE) © 2026 Hariharan Padmanabhan
