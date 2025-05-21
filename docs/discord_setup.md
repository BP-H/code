# Discord Bot Quick Start

This repository includes a simple Discord bot that forwards messages to the GPT Frenzy API.

1. Copy `.env.example` to `.env` and set your credentials:
   ```
   DISCORD_TOKEN=your_bot_token
   FRENZY_API_URL=http://localhost:8000
   ```
2. Install the requirements:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. Run the bot with Make:
   ```bash
   make discord-run
   ```

The script loads the `.env` file automatically thanks to `python-dotenv`. Each message is sent to `/chat/stream` and the reply is posted back to the channel.
