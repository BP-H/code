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
import discord
from dotenv import load_dotenv
from gptfrenzy.core.spawn import launch


load_dotenv()

API_URL = os.getenv("FRENZY_API_URL", "http://localhost:8000").rstrip("/")
TOKEN = os.getenv("DISCORD_TOKEN")
CHARACTER = os.getenv("FRENZY_CHARACTER", "blueprint-nova")

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
    log.info("Logged in as %s using persona %s", client.user, PERSONA_DIR or CHARACTER)


async def send_stream(text: str) -> str:
    """Return a full reply by streaming tokens from the API."""
    global _last
    wait = 1 - (asyncio.get_event_loop().time() - _last)
    if wait > 0:
        await asyncio.sleep(wait)
    _last = asyncio.get_event_loop().time()
    async with aiohttp.ClientSession() as s:
        async with s.post(
            f"{API_URL}/chat/stream",
            json={"character": CHARACTER, "message": text},
        ) as r:
            r.raise_for_status()
            buf = ""
            reply_parts: list[str] = []
            async for chunk in r.content.iter_chunked(1024):
                buf += chunk.decode("utf-8")
                while "\n\n" in buf:
                    line, buf = buf.split("\n\n", 1)
                    if line.startswith("data: "):
                        reply_parts.append(line[6:])
            if buf.startswith("data: "):
                reply_parts.append(buf[6:])
            return "".join(reply_parts)


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
    client.run(TOKEN)
