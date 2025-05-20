import asyncio
import logging
import os

import aiohttp
import discord

API_URL = os.getenv("FRENZY_API_URL", "http://localhost:8000").rstrip("/")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

_last = 0.0

async def send(text: str) -> str:
    global _last
    wait = 1 - (asyncio.get_event_loop().time() - _last)
    if wait > 0:
        await asyncio.sleep(wait)
    _last = asyncio.get_event_loop().time()
    async with aiohttp.ClientSession() as s:
        async with s.post(f"{API_URL}/chat", json={"character": "blueprint-nova", "message": text}) as r:
            r.raise_for_status()
            return (await r.json()).get("reply", "")

@client.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    try:
        reply = await send(msg.content)
    except Exception as exc:  # pragma: no cover - runtime safety
        log.exception("Bridge error: %s", exc)
        reply = "Error contacting the API."
    await msg.channel.send(reply)

client.run(TOKEN)

