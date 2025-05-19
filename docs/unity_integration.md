# Using GptFrenzyClient.cs in Unity

This quick guide shows how to drop the **C#** SDK into a Unity project and send messages to your GPT Frenzy server.

1. Copy `sdk/csharp/GptFrenzyClient.cs` into your Unity project's `Assets` folder (any location is fine).
2. When you create the client, set the base URL for your running server:
   ```csharp
   var client = new GptFrenzyClient("http://localhost:8000");
   ```
3. The `Chat()` and `ChatStream()` methods return `Task` values, so you must handle them asynchronously in Unity (e.g., use `async` methods or coroutines).

Below is a minimal `MonoBehaviour` that sends a message every time the **Space** key is pressed and prints the reply to the console:

```csharp
using UnityEngine;
using System.Threading.Tasks;

public class FrenzyExample : MonoBehaviour
{
    GptFrenzyClient client;

    void Start()
    {
        // Point this URL to your running GPT Frenzy server
        client = new GptFrenzyClient("http://localhost:8000");
    }

    async void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            string reply = await client.Chat("demo-character", "Hello!");
            Debug.Log(reply);
        }
    }
}
```

To stream tokens instead of waiting for the full reply, call `ChatStream()` inside an `async` method and iterate with `await foreach`.
