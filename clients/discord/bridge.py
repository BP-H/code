import asyncio
import logging
import os

import aiohttp
import discord

API_URL = os.getenv("FRENZY_API_URL", "http://localhost:8000").rstrip("/")
TOKEN = os.getenv("DISCORD_TOKEN")
CHARACTER = os.getenv("FRENZY_CHARACTER", "blueprint-nova")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

_last = 0.0


async def send_stream(text: str) -> str:
    """Return the full reply by streaming tokens from the API."""
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

    await msg.channel.send(reply)


if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN environment variable not set")
        raise SystemExit(1)
    client.run(TOKEN)
