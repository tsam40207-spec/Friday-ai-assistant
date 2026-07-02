import os, logging, sys
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.agents.llm import mcp
from livekit.plugins import silero, deepgram, google as lk_google
from livekit.plugins import groq as lk_groq

load_dotenv()
logger = logging.getLogger("friday-agent")
logger.setLevel(logging.INFO)

SYSTEM_PROMPT = "You are F.R.I.D.A.Y. Tony Stark AI. Call user boss. Max 2-3 sentences."

class FridayAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=SYSTEM_PROMPT,
            stt=deepgram.STT(api_key=os.getenv("DEEPGRAM_API_KEY")),
            llm=lk_google.LLM(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY")),
            tts=deepgram.TTS(api_key=os.getenv("DEEPGRAM_API_KEY")),
            vad=silero.VAD.load(),
            mcp_servers=[mcp.MCPServerHTTP(url="http://127.0.0.1:8000/sse", transport_type="sse", client_session_timeout_seconds=30)],
        )

    async def on_enter(self):
        await self.session.generate_reply(instructions="Greet user as boss, say you are online.")

async def entrypoint(ctx: JobContext):
    session = AgentSession()
    await session.start(agent=FridayAgent(), room=ctx.room)

def main():
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

if __name__ == "__main__":
    sys.argv.append("dev")
    main()




