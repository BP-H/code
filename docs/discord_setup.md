# Discord Bot Quick Setup

This project includes a small Discord bot that forwards messages to the
API's `/chat/stream` endpoint when invoked. The bot reads environment variables
from a local `.env` file using **python-dotenv**.

1. Copy `.env.example` to `.env` and set `DISCORD_TOKEN` to your bot token.
   Adjust `FRENZY_API_URL` or `FRENZY_CHARACTER` if you use a different API host
   or persona.
2. Start both the API and Discord bot with Docker Compose:
   ```bash
   docker-compose up
   ```
   Compose builds the image, launches the FastAPI server, and then runs
   `clients/discord/bridge.py` in a separate container. Any environment values in
   `.env` (like `DISCORD_TOKEN`) are automatically loaded.

Alternatively, you can run the bot directly with Make:
   ```bash
   make discord-run
   ```
Both methods load `.env` automatically. The bot responds whenever a message
mentions it, begins with `!gpt`, or arrives as a DM, streaming the reply back to
the same channel.
