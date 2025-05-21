import asyncio
import logging
import os

import aiohttp
import openai
import discord
from dotenv import load_dotenv

load_dotenv()

DEFAULT_API = "http://localhost:8000/merge"
API_URL = os.getenv("FRENZY_API_URL", DEFAULT_API).rstrip("/")
TOKEN = os.getenv("DISCORD_TOKEN")
PERSONA_ID = int(os.getenv("FRENZY_PERSONA_ID", "1"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

_last = 0.0


async def _persona_prompt() -> str:
    async with aiohttp.ClientSession() as s:
        async with s.post(API_URL, json=PERSONA_ID) as r:
            r.raise_for_status()
            data = await r.json()
            return data.get("text") or data.get("merged", "")


async def send_stream(text: str) -> str:
    """Return the reply text from OpenAI using the merged persona."""
    global _last
    wait = 1 - (asyncio.get_event_loop().time() - _last)
    if wait > 0:
        await asyncio.sleep(wait)
    _last = asyncio.get_event_loop().time()

    prompt = await _persona_prompt()
    resp = await openai.ChatCompletion.acreate(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content


@client.event
async def on_message(msg: discord.Message) -> None:
    """Respond to DMs or when the bot is mentioned or `!gpt` is used."""
    if msg.author.bot:
        return

    content = msg.content.strip()
    trigger = False

    # Treat direct messages to the bot as triggers
    if msg.guild is None:
        recipients = getattr(msg.channel, "recipients", None)
        if recipients is None:
            recipient = getattr(msg.channel, "recipient", None)
            recipients = [recipient] if recipient else []
        if len(recipients) <= 1:
            trigger = True

    if not trigger and content.startswith("!gpt"):
        trigger = True
        content = content[4:].strip()
    elif not trigger and client.user and client.user.mentioned_in(msg):
        trigger = True
        content = content.replace(client.user.mention, "").strip()

    if not trigger or not content:
        return

    try:
        reply = await send_stream(content)
    except Exception as exc:  # pragma: no cover - runtime safety
        log.exception("Bridge error: %s", exc)
        reply = "Error contacting the API."
        if isinstance(exc, aiohttp.ClientConnectionError) or (
            isinstance(exc, aiohttp.ClientResponseError) and exc.status == 503
        ):
            reply += " (Is the API server running and accessible?)"

    await msg.channel.send(reply)


if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN environment variable not set")
        raise SystemExit(1)
    client.run(TOKEN)
