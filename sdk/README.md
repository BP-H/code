# GPTFrenzy SDK stubs
Lightweight wrappers around the `/chat`, `/chat/stream`, and `/manifest` endpoints.
Use whichever language matches your engine. The Python client relies on the `requests` library (see `python/requirements.txt`). Install it with:

```bash
pip install -r python/requirements.txt
```

| Language | File | Example |
|----------|------|---------|
|Python    | `python/gptfrenzy_client.py` | `bot.chat("blueprint-nova", "Hello")` |
|JavaScript| `js/gptfrenzy-client.js`     | `await chat(url,"blueprint-nova","Hi")` |
|C# (.NET / Unity / UE)| `csharp/GptFrenzyClient.cs` | `await client.Chat("blueprint-nova","Hi");` |

All wrappers assume the FastAPI server is reachable at `http://localhost:8000`
(or whatever base URL you pass).
Calls that result in non-2xx responses will reject their returned promises with
an `Error` containing the HTTP status code.

## Streaming usage

To consume streaming replies, use the `chat_stream`/`chatStream`/`ChatStream` helpers:

```js
for await (const tok of chatStream(url, 'blueprint-nova', 'Hi')) {
  console.log(tok);
}
```

```python
for tok in bot.chat_stream('blueprint-nova', 'Hi'):
    print(tok, end='')
```

```csharp
await foreach (var tok in client.ChatStream("blueprint-nova", "Hi"))
{
    Console.Write(tok);
}
```
