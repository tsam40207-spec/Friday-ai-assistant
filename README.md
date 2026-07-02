# F.R.I.D.A.Y. — Voice AI Assistant

Tony Stark-inspired voice AI assistant powered by LiveKit, Deepgram, Gemini, and FastMCP.

## Architecture
- **STT:** Deepgram (real-time speech recognition)
- **LLM:** Google Gemini 2.0 Flash
- **TTS:** Deepgram
- **Tools:** FastMCP server (web search, news, system info)
- **Voice Pipeline:** LiveKit Agents

## Setup

### 1. Install dependencies
```bash
pip install uv
uv sync
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in your API keys
```

### 3. Run
```bash
# Terminal 1 - MCP Tool Server
uv run friday

# Terminal 2 - Voice Agent
uv run python agent_friday_new.py
```

## Required API Keys
- `LIVEKIT_URL` + `LIVEKIT_API_KEY` + `LIVEKIT_API_SECRET` — livekit.io
- `GOOGLE_API_KEY` — aistudio.google.com
- `DEEPGRAM_API_KEY` — console.deepgram.com
- `GROQ_API_KEY` — console.groq.com

## Connect
Open LiveKit Playground → Start session → Talk to FRIDAY!
