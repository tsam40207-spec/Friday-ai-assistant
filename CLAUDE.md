# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repository.

## What this project is

F.R.I.D.A.Y. is a small, self-hosted, Tony Stark-inspired voice AI assistant demo. A user
talks into a browser dashboard; audio flows over LiveKit to a Python voice agent, which
pipes speech through STT → LLM → TTS and can call tools exposed by a local MCP server.
This is a single-author hobby/demo project, not a production service — expect a thin,
loosely-wired codebase rather than a large application.

## Architecture

```
Browser (friday-dashboard.html)
   |  WebRTC via LiveKit
   v
LiveKit Cloud/Server  <---->  src/agent_friday_new.py (voice Agent)
                                   |        |        |
                                  STT      LLM       TTS
                               (Deepgram) (Gemini) (Deepgram)
                                            |
                                            v
                                   MCP server (SSE, http://127.0.0.1:8000/sse)
                                   started via src/server.py
```

- **`friday-dashboard.html`** — Standalone, dependency-free (besides the LiveKit UMD
  script from a CDN) HTML/CSS/JS "Ultron-style" command console. Connects directly to a
  LiveKit room using a URL + token pasted in by the user, renders an audio-reactive
  particle visualizer, a comms log, and a text-chat fallback. No build step.
- **`src/agent_friday_new.py`** — The voice agent entrypoint (LiveKit Agents framework).
  Defines `FridayAgent`, wires up Silero VAD, Deepgram STT/TTS, and Google Gemini
  (`gemini-2.5-flash`) as the LLM, and points the agent at the local MCP server over SSE.
  Run directly with `python src/agent_friday_new.py` (it force-appends the LiveKit CLI
  `dev` subcommand at the bottom of the file).
- **`src/server.py`** — Entry point for the MCP tool server (FastMCP, SSE transport on
  port 8000) that the voice agent's LLM calls into for tools like web search, news, and
  system info.
- **`src/gen_token.py`** — One-off script that prints a LiveKit room URL + JWT access
  token (room `"friday-room"`, identity `"boss"`) for pasting into the dashboard.

## ⚠️ Known gap: the `friday` package does not exist in this repo

`src/server.py` imports from `friday.tools`, `friday.prompts`, `friday.resources`, and
`friday.config` (`register_all_tools`, `register_all_prompts`, `register_all_resources`,
`config.SERVER_NAME`), but **no `friday/` package exists anywhere in this repository**.
Running `src/server.py` as-is will fail with `ModuleNotFoundError: No module named 'friday'`.
Similarly, `pyproject.toml`'s script entries reference `server:main` and
`agent_friday:dev`, but the actual file is `src/agent_friday_new.py` (not
`agent_friday.py`), and `[tool.hatch.build.targets.wheel] packages = ["server.py"]` points
at a root-level file that doesn't exist (the real file is `src/server.py`).

If you're asked to "run the MCP server" or "add a tool," check whether the `friday`
package has been added since this file was last updated — if not, you will likely need to
either create that package (`tools.py`/`prompts.py`/`resources.py`/`config.py` with the
functions above) or flag the gap to the user rather than silently assuming it works.

## Repository layout

```
.
├── src/
│   ├── agent_friday_new.py   # LiveKit voice agent (STT/LLM/TTS pipeline)
│   ├── server.py              # MCP tool server entry point (imports missing `friday` pkg — see above)
│   └── gen_token.py           # LiveKit token generator CLI script
├── friday-dashboard.html      # Standalone browser UI, connects via LiveKit client SDK
├── assets/friday-preview.png  # Screenshot used in README
├── pyproject.toml             # uv/hatchling project config (has stale script/package refs)
├── .env.example                # Template for required API keys
├── LICENSE                     # MIT
└── README.md                   # User-facing setup + feature docs
```

There is no test suite, no CI config, and no linter config in this repo.

## Development workflow

Dependencies are managed with **uv** (see README):

```bash
pip install uv
uv sync
uv add livekit-api   # not in pyproject.toml's declared deps but required by gen_token.py
cp .env.example .env # then fill in API keys
```

Running the pieces (each in its own terminal):

```bash
uv run python src/server.py            # MCP tool server (SSE on :8000) — currently broken, see gap above
uv run python src/agent_friday_new.py  # LiveKit voice agent (starts in `dev` mode)
uv run python src/gen_token.py         # prints a LiveKit URL + JWT for the dashboard
```

Then open `friday-dashboard.html` directly in a browser (no dev server needed), paste in
the printed LiveKit URL and token, and click "Establish Uplink."

## Required environment variables (`.env`)

See `.env.example` for the full list and where to obtain each key:
`LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `GROQ_API_KEY`,
`SARVAM_API_KEY`, `OPENAI_API_KEY`, `DEEPGRAM_API_KEY`,
`GOOGLE_APPLICATION_CREDENTIALS` (or `gcloud auth application-default login`),
`SUPABASE_URL`, `SUPABASE_API_KEY`, `GOOGLE_API_KEY`. Not all of these are consumed by
the current code (e.g. Supabase, OpenAI, Groq, and Sarvam keys are present in the
template but unused by `agent_friday_new.py`/`server.py` today) — they appear to be
placeholders for the roadmap items below.

## Conventions to follow

- **Keep it minimal.** This is a small demo codebase; avoid introducing frameworks,
  build tooling, or abstractions the project doesn't already use.
- **No test suite exists.** Don't assume `pytest`/CI will catch regressions — manually
  reason through changes, and mention to the user when something can't be verified
  automatically (voice/audio flows especially can't be tested without live API keys and
  a browser).
- **`src/` files are standalone scripts**, not a proper installable package (there's no
  `src/__init__.py`). Keep imports consistent with that reality unless you're
  deliberately restructuring into a package (e.g. to fix the `friday` import gap above).
- **Secrets:** never commit real API keys. `.env` is gitignored; only edit
  `.env.example` with placeholder-style values, matching its existing format.
- **Dashboard (`friday-dashboard.html`) is a single self-contained file** — inline
  `<style>` and `<script>`, one external CDN script for the LiveKit client. Keep new UI
  changes in this same single-file style rather than splitting into separate assets,
  unless asked to restructure.
- **Persona:** the agent's system prompt and dashboard copy consistently use the
  Tony Stark/F.R.I.D.A.Y. "boss" framing (crimson/Ultron visual theme, calls the user
  "boss," short 2-3 sentence replies). Preserve this tone in prompt or UI copy changes
  unless told otherwise.
- **Commit messages** in this repo's history are short, imperative, and describe a single
  visible change (e.g. "Add dashboard screenshot and Ultron-style command interface",
  "Fix README formatting"). Follow that style.

## Roadmap context (from README)

Unimplemented, so don't assume they exist: persistent conversation memory, custom
wake-word detection, multi-agent tool routing, mobile-friendly dashboard layout, local
LLM fallback (Ollama). These likely explain the unused Supabase/OpenAI/Groq/Sarvam keys
in `.env.example`.
