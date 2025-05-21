"""Discord bot that forwards messages to the `/chat/stream` endpoint."""

import asyncio
import logging
import os

import aiohttp
import discord
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("FRENZY_API_URL", "http://localhost:8000").rstrip("/")
TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

_last = 0.0


async def chat_stream(text: str) -> str:
    global _last
    wait = 1 - (asyncio.get_event_loop().time() - _last)
    if wait > 0:
        await asyncio.sleep(wait)
    _last = asyncio.get_event_loop().time()
    url = f"{API_URL}/chat/stream"
    payload = {"character": "blueprint-nova", "message": text}
    reply = []
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=payload) as r:
            r.raise_for_status()
            async for line in r.content:
                if line.startswith(b"data: "):
                    reply.append(line[6:].decode("utf-8"))
    return "".join(reply)


@client.event
async def on_message(msg: discord.Message) -> None:
    if msg.author.bot:
        return
    try:
        reply = await chat_stream(msg.content)
    except Exception as exc:  # pragma: no cover - runtime safety
        log.exception("Bridge error: %s", exc)
        reply = "Error contacting the API."
    await msg.channel.send(reply)


def main() -> None:
    if not TOKEN:
        log.error("DISCORD_TOKEN is not set")
        raise SystemExit(1)
    client.run(TOKEN)


if __name__ == "__main__":
    main()
