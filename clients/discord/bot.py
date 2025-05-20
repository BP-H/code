"""Minimal Discord bot using the spawn system."""

import asyncio
import sys

try:
    import discord
except ImportError:  # pragma: no cover - optional dependency
    print("Install discord.py (`pip install discord.py`) to use this bot")
    raise SystemExit(1)

from gptfrenzy.spawn import launch


async def main(persona_dir: str, token: str) -> None:
    persona = launch("discord", persona_dir)
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message: discord.Message) -> None:
        if message.author.bot:
            return
        reply = persona.generate(message.content)
        await message.channel.send(reply)

    await client.start(token)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bot.py <persona_dir> <discord_token>")
        raise SystemExit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))
