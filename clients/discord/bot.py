"""Minimal Discord bot using the spawn system."""

import asyncio
import logging
import sys

try:
    import discord
except ImportError:  # pragma: no cover - optional dependency
    print("Install discord.py (`pip install discord.py`) to use this bot")
    raise SystemExit(1)

from gptfrenzy.spawn import launch

log = logging.getLogger(__name__)


async def main(persona_dir: str, token: str) -> None:
    persona = launch("discord", persona_dir)
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message: discord.Message) -> None:
        if message.author.bot:
            return
        try:
            reply = await persona.generate(message.content)
        except Exception as exc:  # pragma: no cover - runtime safety
            log.exception("Error generating reply: %s", exc)
            try:
                await message.channel.send(
                    "An error occurred while generating a response."
                )
            except Exception as send_exc:  # pragma: no cover - logging only
                log.exception("Failed to send error message: %s", send_exc)
        else:
            await message.channel.send(reply)

    try:
        await client.start(token)
    except discord.LoginFailure:
        log.error("Invalid Discord token")
        raise SystemExit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bot.py <persona_dir> <discord_token>")
        raise SystemExit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))
