"""Minimal Discord bot using either a local persona or the API.

Pass the persona path as the first command-line argument or set
``FRENZY_PERSONA_DIR`` in the environment. If no persona is provided, the bot
falls back to calling the API specified by ``FRENZY_API_URL``.
"""

import asyncio
import logging
import os
import sys

import aiohttp
import openai
import discord
from dotenv import load_dotenv
from gptfrenzy.core.spawn import launch


load_dotenv()

API_URL = os.getenv("FRENZY_API_URL", "http://localhost:8000").rstrip("/")
TOKEN = os.getenv("DISCORD_TOKEN")
PERSONA_ID = int(os.getenv("FRENZY_PERSONA_ID", "1"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

args = sys.argv[1:]
PERSONA_DIR = args[0] if args else os.getenv("FRENZY_PERSONA_DIR")
if len(args) >= 2:
    TOKEN = args[1]

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

persona = launch("discord", PERSONA_DIR) if PERSONA_DIR else None

_last = 0.0


@client.event
async def on_ready() -> None:
    log.info("Logged in as %s using persona %s", client.user, PERSONA_DIR or PERSONA_ID)


async def _persona_prompt() -> str:
    async with aiohttp.ClientSession() as s:
        async with s.post(f"{API_URL}/merge", json=PERSONA_ID) as r:
            r.raise_for_status()
            data = await r.json()
            return data.get("text") or data.get("merged", "")


async def send_stream(text: str) -> str:
    """Return a reply from OpenAI using the merged persona."""
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
    if msg.author.bot:
        return
    try:
        if persona is not None:
            reply = await persona.generate(msg.content)
        else:
            reply = await send_stream(msg.content)
    except Exception as exc:  # pragma: no cover - runtime safety
        log.exception("Bot error: %s", exc)
        reply = (
            "Error contacting the API."
            if persona is None
            else "Error generating reply."
        )
    await msg.channel.send(reply)


if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN environment variable not set")
        raise SystemExit(1)
    if not PERSONA_DIR:
        print(f"No local persona provided; using API mode with persona {PERSONA_ID}")
    client.run(TOKEN)
