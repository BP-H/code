# GPTFrenzy SDK stubs
Thin, dependency-free wrappers around the `/chat` and `/manifest` endpoints.  
Use whichever language matches your engine:

| Language | File | Example |
|----------|------|---------|
|Python    | `python/gptfrenzy_client.py` | `bot.chat("blueprint-nova", "Hello")` |
|JavaScript| `js/gptfrenzy-client.js`     | `await chat(url,"blueprint-nova","Hi")` |
|C# (.NET / Unity / UE)| `csharp/GptFrenzyClient.cs` | `await client.Chat("blueprint-nova","Hi");` |

All wrappers assume the FastAPI server is reachable at `http://localhost:8000`
(or whatever base URL you pass).
Calls that result in non-2xx responses will reject their returned promises with
an `Error` containing the HTTP status code.
