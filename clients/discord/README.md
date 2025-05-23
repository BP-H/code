# Discord Integration with Spawn System

This example shows how to load a persona with `gptfrenzy.core.spawn.launch()`
and respond to messages in Discord.

1. Install `discord.py`:
   ```bash
   pip install discord.py
   ```
2. Enable the **Message Content Intent** for your bot in the Discord
   developer portal so it can read messages. The bot sets
   `intents.message_content = True` in `bot.py`.
3. Run the bot with a persona directory and your Discord token. You can pass
   the path as the first argument or set `FRENZY_PERSONA_DIR` in the
   environment:
   ```bash
   # command-line argument
   python bot.py /path/to/persona YOUR_BOT_TOKEN

   # or environment variable
   export FRENZY_PERSONA_DIR=/path/to/persona
   python bot.py YOUR_BOT_TOKEN
   ```
   The persona's `generate()` coroutine will be awaited for every message the
   bot can see and the result sent back to the same channel.

`bot.py` keeps things minimal so you can adapt it to your needs.

## API Bridge

Forward messages to the REST API instead of a local persona:

```bash
export DISCORD_TOKEN=YOUR_TOKEN
export FRENZY_API_URL=http://localhost:8000
export FRENZY_CHARACTER=blueprint-nova
python bridge.py
```
`FRENZY_CHARACTER` controls which persona the bridge uses when forwarding
messages to the API.

`bridge.py` reacts when a user mentions the bot, starts a message with `!gpt`,
or sends the bot a direct message. It forwards the remaining text to the API's
`/chat/stream` endpoint and posts the streamed reply back to the same channel.
Any connection errors are logged and reported in Discord instead of crashing
the bot.
