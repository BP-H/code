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
3. Run the bot, passing the persona directory and your Discord token:
   ```bash
   python bot.py /path/to/persona YOUR_BOT_TOKEN
   ```
   The persona's `generate()` coroutine will be awaited for every message
   the bot can see and the result sent back to the same channel.

`bot.py` keeps things minimal so you can adapt it to your needs.

## API Bridge

Forward messages to the REST API instead of a local persona:

```bash
export DISCORD_BOT_TOKEN=YOUR_TOKEN
export FRENZY_API_URL=http://localhost:8000
python bridge.py
```

`bridge.py` reacts only when a user mentions the bot or starts a message with
`!gpt`. It forwards the remaining text to the API's `/chat/stream` endpoint and
posts the streamed reply back to the same channel. Any connection errors are
logged and reported in Discord instead of crashing the bot.
