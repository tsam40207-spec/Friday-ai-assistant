# F.R.I.D.A.Y. — Voice AI Assistant

Tony Stark-inspired voice AI assistant powered by LiveKit, Deepgram, Gemini, and FastMCP. Includes a custom Ultron-style command dashboard.

## Architecture
- **STT:** Deepgram (real-time speech recognition)
- **LLM:** Google Gemini 2.0 Flash
- **TTS:** Deepgram
- **Tools:** FastMCP server (web search, news, system info)
- **Voice Pipeline:** LiveKit Agents
- **Dashboard:** Custom HTML/Canvas Ultron-style command interface

## Setup

### 1. Install dependencies
```bash
pip install uv
uv sync
uv add livekit-api
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in your API keys
```

### 3. Run the agent
```bash
# Terminal 1 - MCP Tool Server
uv run friday

# Terminal 2 - Voice Agent
uv run python agent_friday_new.py
```

### 4. Launch the dashboard
Generate a connection token:
```bash
uv run python gen_token.py
```

Open `friday-dashboard.html` in your browser, paste the LiveKit URL and generated token, and click **Establish Uplink**.

## Required API Keys
- `LIVEKIT_URL` + `LIVEKIT_API_KEY` + `LIVEKIT_API_SECRET` — livekit.io
- `GOOGLE_API_KEY` — aistudio.google.com
- `DEEPGRAM_API_KEY` — console.deepgram.com
- `GROQ_API_KEY` — console.groq.com

## Screenshot
![FRIDAY Dashboard](dashboard-screenshot.png)

## Dashboard Features
- Real-time audio-reactive core animation (particle sphere + rotating rings)
- Live mic/voice level meters
- Live comms transcript (voice + text)
- System status panel (uplink, agent presence, neural load)
- Text chat fallback alongside voice

## Connect
Run `uv run python gen_token.py`, then open the dashboard and paste in your credentials — or use LiveKit Playground directly.

