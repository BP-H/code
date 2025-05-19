# Unity Integration

Import the lightweight C# client so your game can talk to the GPT Frenzy server.

## Importing `GptFrenzyClient.cs`
1. Copy `sdk/csharp/GptFrenzyClient.cs` into your Unity project (for example
   into `Assets/Scripts`).
2. The file only depends on `Newtonsoft.Json` and `System.Net.Http`, which are
   included with recent Unity versions.

## Example `MonoBehaviour`
Below is a simple component that sends a message whenever you press the Space
bar. The reply is printed to the Console.

```csharp
using UnityEngine;

public class ChatExample : MonoBehaviour
{
    private GptFrenzyClient _client;

    void Start()
    {
        // Point to your API base URL
        _client = new GptFrenzyClient("http://localhost:8000");
    }

    async void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            string reply = await _client.Chat("blueprint-nova", "Hello from Unity!");
            Debug.Log(reply);
        }
    }
}
```

## Base URL and async notes
- Pass the server address to the constructor if it is not running on
  `http://localhost:8000`.
- `Chat` returns a `Task<string>` so you can `await` it inside an async method.
- To stream partial tokens, implement a `ChatStream` method that consumes
  `/chat/stream` and yield each token as it arrives.
