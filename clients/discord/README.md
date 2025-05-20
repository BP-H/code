# Discord Integration with Spawn System

This example shows how to load a persona with `gptfrenzy.spawn.launch()`
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
