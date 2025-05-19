# Manifest-Driven Character System

This document explains how GPT Frenzy uses `manifest.yaml` to expose its personas through the API and SDK stubs. It also covers how to add a new persona and update the manifest.

## Overview

The FastAPI server reads `manifest.yaml` at startup. Each entry defines a character that can be selected over the `/chat` endpoint. A minimal entry looks like:

```yaml
- id: blueprint-nova
  name: Blueprint Nova
  prompt_file: blueprint_nova.md
  voice_id: alloy
  avatar_url: https://example.com/blueprint_nova.png
```

The `prompt_file` path points to a Markdown (or plain text) file containing the character's instructions. When the server starts, it loads every prompt listed in the manifest and caches the text.

Clients fetch the manifest from `GET /manifest` (JSON) or from `GET /manifest.yaml` for the raw YAML. This allows any SDK or web front end to discover which characters are available without hardcoding them.

## Adding or Updating a Persona

1. **Create a prompt file** – Write the character's prompt in a new Markdown file. Place the file anywhere in the repository (e.g., `personas/blueprint_nova.md`).
2. **Edit `manifest.yaml`** – Add a new entry with a unique `id`, the human-readable `name`, and the path to your prompt file. Optionally specify `voice_id` and an `avatar_url` for clients that support them.
3. **Regenerate the manifest** – Because the manifest is a plain YAML file, "regenerating" it simply means saving your changes and committing them. No build step is required.
4. **Restart the API server** – The FastAPI app reads the manifest at startup. Restart the server so it reloads the updated manifest and primes the prompts.

Once reloaded, calling `/manifest` or `/manifest.yaml` will list the new persona.

## Interacting via the API or SDKs

1. **Retrieve the manifest** to discover character IDs:
   ```bash
   curl http://localhost:8000/manifest        # JSON
   curl http://localhost:8000/manifest.yaml   # YAML
   ```
2. **Send a chat message** using one of the IDs:
   ```bash
   curl -X POST http://localhost:8000/chat \
        -H 'Content-Type: application/json' \
        -d '{"character": "blueprint-nova", "message": "Hello"}'
   ```

The SDK stubs under [`/sdk`](../sdk) provide lightweight wrappers for Python, JavaScript, and C#. Each exposes `chat()` and `manifest()` functions that map directly to the endpoints above.

## Is this the “spawnable character system”?

The repository does not explicitly mention a separate "spawnable character system." In practice, the manifest-driven API allows clients to spawn (i.e., instantiate) any character listed in `manifest.yaml`. So the manifest serves as the basis for whatever was meant by a spawnable system.

For instructions on packaging a persona directory that can be loaded by other
hosts (for example Discord bots or game engines), see
[spawn_system.md](spawn_system.md).
