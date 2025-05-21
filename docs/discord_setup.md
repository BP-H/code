# Discord Bot Quick Setup

This project includes a small Discord bot that forwards messages to the
API's `/chat/stream` endpoint when invoked. The bot reads environment variables
from a local `.env` file using **python-dotenv**.

1. Copy `.env.example` to `.env` and set `DISCORD_TOKEN` to your bot token.
   Adjust `FRENZY_API_URL` if your server runs on a different host.
2. Run the bot:
   ```bash
   make discord-run
   ```

The command above loads the `.env` file automatically and starts the bot. It
only responds when a message begins with `!gpt` or mentions the bot, sending the
streamed reply back to the same channel.
