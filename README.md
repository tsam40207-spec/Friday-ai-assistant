# F.R.I.D.A.Y. — Voice AI Assistant

![Python](https://img.shields.io/badge/python-3.11-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![LiveKit](https://img.shields.io/badge/voice-LiveKit-red)

Tony Stark-inspired voice AI assistant powered by LiveKit, Deepgram, Gemini, and FastMCP. Includes a custom Ultron-style command dashboard.

## Architecture

- **STT:** Deepgram (real-time speech recognition)
- **LLM:** Google Gemini 2.0 Flash
- **TTS:** Deepgram
- **Tools:** FastMCP server (web search, news, system info)
- **Voice Pipeline:** LiveKit Agents
- **Dashboard:** Custom HTML/Canvas Ultron-style command interface

## Project Structure

friday-assistant/
- src/agent_friday_new.py (Voice agent entrypoint)
- src/server.py (MCP tool server)
- src/gen_token.py (LiveKit token generator)
- friday-dashboard.html (Command dashboard UI)
- .env.example
- pyproject.toml
- README.md

## Setup

### 1. Install dependencies

    pip install uv
    uv sync
    uv add livekit-api

### 2. Configure environment

    cp .env.example .env

Fill in your API keys after copying.

### 3. Run the agent

    # Terminal 1 - MCP Tool Server
    uv run python src/server.py

    # Terminal 2 - Voice Agent
    uv run python src/agent_friday_new.py

### 4. Launch the dashboard

    uv run python src/gen_token.py

Open friday-dashboard.html in your browser, paste the LiveKit URL and generated token, and click Establish Uplink.

## Required API Keys

| Key | Source |
|---|---|
| LIVEKIT_URL + LIVEKIT_API_KEY + LIVEKIT_API_SECRET | livekit.io |
| GOOGLE_API_KEY | aistudio.google.com |
| DEEPGRAM_API_KEY | console.deepgram.com |
| GROQ_API_KEY | console.groq.com |

## Dashboard Features

- Real-time audio-reactive core animation (particle sphere + rotating rings)
- Live mic/voice level meters
- Live comms transcript (voice + text)
- System status panel (uplink, agent presence, neural load)
- Text chat fallback alongside voice

## License

MIT — see [LICENSE](LICENSE)
