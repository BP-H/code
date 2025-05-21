# Discord Bot Quick Setup

This project includes a small Discord bot that forwards every message to the
API's `/chat/stream` endpoint. The bot reads environment variables from a local
`.env` file using **python-dotenv**.

1. Copy `.env.example` to `.env` and set `DISCORD_TOKEN` to your bot token.
   Adjust `FRENZY_API_URL` if your server runs on a different host.
2. Run the bot:
   ```bash
   make discord-run
   ```

The command above loads the `.env` file automatically and starts the bot.  It
will listen to messages it can see and send the streamed reply back to the same
channel.
