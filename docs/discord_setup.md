# Discord Bot Quick Setup

This project includes a small Discord bot that forwards messages to the
API's `/chat/stream` endpoint when invoked. The bot reads environment variables
from a local `.env` file using **python-dotenv**.

**Make sure to enable the "Message Content Intent" for your bot in the Discord
developer portal so it can read messages.**

1. Copy `.env.example` to `.env` and set `DISCORD_TOKEN` to your bot token.
   Adjust `FRENZY_API_URL` if your server runs on a different host.
2. Run the bot (recommended method uses `bridge.py` to connect to the running API):
   ```bash
   make discord-run
   ```

The command above loads the `.env` file automatically and starts the bot. It
only responds when a message begins with `!gpt` or mentions the bot, sending the
streamed reply back to the same channel.

For detailed usage and customization options, see
[clients/discord/README.md](../clients/discord/README.md).
