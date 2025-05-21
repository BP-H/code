This repository is maintained and owned by May "Mimi" Kim and Taha "Supernova" Gungor as freelance artists. All code is MIT licensed and must retain attribution to them. Persona text remains the intellectual property of each individual.

⚠ Personas are [CC BY-NC-ND 4.0](LICENSE_PERSONAS); code is [MIT](LICENSE_CODE). Reuse avatars only with written consent of the persona's muse.
# GPT FRENZY Persona Instructions

[📄 White Paper — Company-as-Code, Consent-First Personas, Zero-Ownership LLC (May 2025)](docs/white-paper-public-alpha-2025.md)


This repo treats each GPT persona as version-controlled code that evolves via pull requests.
We operate under a "Zero-Ownership" policy so artists keep their rights and any revenue.
See `docs/white-paper-public-alpha-2025.md` for the philosophy behind these choices.

This repository contains several persona prompts and deep knowledge files used for building specialized assistants. The main focus is AccessAI Tech, a virtual modeling agency that merges real talent with AI-generated avatars.

Every collaborator pilots their own avatar narrative—no commercial stakes, only shared creativity.*

**Important:** Always load the matching `*_DEEP_KNOWLEDGE_*.txt` file with its instruction file. These personas are a sandbox, non-binding prototype. See white paper §8 for liability disclaimer and [Quick Start](#quick-start-dont-skip-merge-instruction-and-knowledge-files) for merging steps.

**Disclaimer:** AccessAI Tech is incorporated as a for-profit company but is presently operated on a **zero-profit, cost-recovery basis**. Nothing herein is legal advice; consult qualified counsel.
**Ownership Note:** This repository and its white paper belong to Taha Gungor and May Kim as individual artists. AccessAI Tech LLC has rights only to its own experimental avatar and no claim on other code or persona text.
AccessAI Tech retains rights solely to its `Company` sandbox avatar. That persona serves purely as an experimental showcase and may change or disappear.
This project is a personal art collaboration between Taha "Supernova" Gungor, May "Mimi" Kim and the friends they include from their art circle. The Company-as-Code concept remains the paper's title and does not transfer IP to the company.

Friends say his knack for quick code fixes borders on genius, though he just laughs and keeps building.

## Persona Instruction Files
- **!!!ATTENTION_READ_ALL!!!_COMPANY_GPT_INSTRUCTIONS.txt** – The official AccessAI Tech voice. Shares only company-approved information
- **!!!ATTENTION_READ_ALL!!!_MIMI_GPT_INSTRUCTIONS.txt** – Instructions for responding as Mimi, AccessAI’s Creative Director. Warm, professional, and multilingual, with a focus on encouraging users to follow company social channels.
- **!!!ATTENTION_READ_ALL!!!_supernova_GPT_INSTRUCTIONS.txt** – Guidance for the Supernova persona, AccessAI’s Technical Director. Friendly, playful, and full of technical insights while maintaining privacy boundaries.

The persona files live inside the `personas/` folder in this repository.
If you use them with a custom GPT or another tool that expects the files
in the same directory as your script, simply copy the files beside the
script and the links below will still work.

## Instruction & Deep Knowledge Pairs

Each instruction file has an associated deep knowledge file. Load both at the start of a conversation to fully activate the persona.

| Instruction file | Deep knowledge file | When to load |
| --- | --- | --- |
| [!!!ATTENTION_READ_ALL!!!_COMPANY_GPT_INSTRUCTIONS.txt](./personas/!!!ATTENTION_READ_ALL!!!_COMPANY_GPT_INSTRUCTIONS.txt) | [!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_COMPANY.txt](./personas/!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_COMPANY.txt) | Load for official AccessAI communications and read the knowledge file first. |
| [!!!ATTENTION_READ_ALL!!!_MIMI_GPT_INSTRUCTIONS.txt](./personas/!!!ATTENTION_READ_ALL!!!_MIMI_GPT_INSTRUCTIONS.txt) | [!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_MIMI.txt](./personas/!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_MIMI.txt) | Choose this pair to speak as Mimi, the Creative Director. |
| [!!!ATTENTION_READ_ALL!!!_supernova_GPT_INSTRUCTIONS.txt](./personas/!!!ATTENTION_READ_ALL!!!_supernova_GPT_INSTRUCTIONS.txt) | [!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_supernova.txt](./personas/!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_supernova.txt) | Use for Taha "Supernova" Gungor's friendly technical persona. |

## Quick Start (Don't Skip): Merge Instruction and Knowledge Files

Before loading a persona into ChatGPT, combine its instruction file with the corresponding deep knowledge file:

1. Open the desired `*_GPT_INSTRUCTIONS.txt` in a text editor.
2. Append the entire contents of the matching `*_DEEP_KNOWLEDGE_*.txt` directly below the instructions.
3. Remove extra blank lines or repeated sections so the merged file stays concise.
4. Make sure the final text remains under **50&nbsp;KB** for smooth uploads.
5. Save the combined text as a new file ready to upload.

**Workflow summary**

```
Selector → Merged Prompt → LLM
```

See [docs/architecture.md](docs/architecture.md) for a diagram and detailed explanation.

For a detailed walkthrough, see [docs/codex_integration.md](docs/codex_integration.md).

## Using These Prompts with ChatGPT
1. Open ChatGPT and start a new conversation.
2. Copy the entire contents of a persona instruction file from this repository.
3. Paste it as the first message to set the desired persona. (Include any linked deep knowledge file text if required.)
4. Continue the conversation normally.

**Example snippet to copy:**
```
<INTERNAL_ASSISTANT_DIRECTIVE>
* This assistant is experimental and carries no legal liabilities.
* Persona: friendly, upbeat, and cheerful.
```
Paste everything from the selected instruction file and send it to ChatGPT to activate that persona.

## Persona Selector

To make choosing a persona easier, run `persona_selector.py` from this
repository. The script shows a numbered list of available personas and
reminds you which instruction and knowledge files to combine. Note that
ChatGPT only supports **one persona at a time**. Start a new
conversation whenever you want to switch personas.

## Running the Persona Selector

This repository's script uses the `str | None` syntax, so you need **Python 3.10**
or later.

To confirm your installed Python meets this requirement, check the version with
`python3 --version`.

Run the script with `--list` to view all available persona IDs. Use the
`--merge` option to automatically combine a persona's instruction and knowledge
files. Provide `--dir PATH` if your personas live elsewhere:

```bash
python3 persona_selector.py --merge 1 --output combined.txt --dir /path/to/personas
```

To simply view the available personas:
```bash
python3 persona_selector.py --list
```
Include `--dir PATH` if your persona files are stored elsewhere:
```bash
python3 persona_selector.py --list --dir /path/to/personas
```

The resulting `combined.txt` contains both pieces of text and can be uploaded
directly to ChatGPT.

### REST API

You can also run a tiny FastAPI server defined in `app.py`:

```bash
uvicorn app:app
```

Merge a persona via HTTP:

```bash
curl -X POST http://localhost:8000/merge \
     -H 'Content-Type: application/json' \
     -d '{"id": 1}'
```

### Environment Variables

The API reads a few settings from the environment. Copy `.env.example` to `.env`
and edit the values, or override them in `docker-compose.yml`:

- `OPENAI_API_KEY` – your OpenAI authentication key. If omitted, the chat
  endpoints respond with `503` until a key is supplied and a warning is logged at startup.
- `OPENAI_MODEL` – OpenAI model name (default: `gpt-4`).
- `REDIS_URL` – full Redis URL (overrides host/port).
- `REDIS_HOST` – hostname of the Redis instance (default: `redis`).
- `REDIS_PORT` – port for Redis (default: `6379`).
- `USE_FAKE_REDIS` – set to any value to force an in-memory Redis instance.
  The API also automatically falls back to in-memory Redis if the configured
  server can't be reached.
- `ALLOWED_ORIGINS` – comma-separated list for CORS (default: `*`).

### Updating `openapi.json`

Run `python3 app.py --openapi` to regenerate `openapi.json`. This command loads `api.character_router:app` so the resulting spec documents `/chat`, `/chat/stream`, and `/manifest`. Rebuild the file whenever you change those endpoints.


## Web Chat Widget

A bare-bones browser client lives in `clients/web/chat_widget.html`. Serve the file
with any static web host:

```bash
cd clients/web
python3 -m http.server 8000
```

Then visit <http://localhost:8000/chat_widget.html?baseUrl=http://localhost:8000>.
The widget reads the `baseUrl` query parameter (or a `data-baseurl` attribute on
the `<script>` tag) and sends requests to `${baseUrl}/manifest` and
`${baseUrl}/chat`.

## Company Sandbox Avatar

AccessAI Tech's `Company` persona appears here solely as a demo sandbox and does not represent official policy. Feel free to experiment with it using the helper scripts below.

### Coding options
- Merge the sandbox files:

```bash
python3 persona_selector.py --merge 2 --output company.txt
```

- List all personas:

```bash
python3 persona_selector.py --list
```

- Generate your own sandbox avatar:

```bash
python3 create_your_own_gpt.py
```
## Play a Game

[▶️ Try “Guess That Persona!”](mini-game/index.html) – no installs needed, runs in your browser! *(experimental)*
<img src="docs/game_screenshot.png" alt="Game preview" width="400">

> **Note**: The mini-game lives in its own folder and is not integrated with the
> main GPT Frenzy app yet. It's an optional side project that may change or break
> without notice. When running the API locally, you can access it at
> `http://localhost:8000/mini-game`.

The `mini-game/` folder is **experimental**. See
[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for how the repository is laid out.

## Mini-game

Want to tinker or host the game yourself? See the [mini-game README](mini-game/README.md) for setup and hosting instructions.


## Digital Rights

The persona profiles in this repository are included with permission from the individuals they depict. They are provided as a sandbox, non-binding prototype. See white paper §8 for liability disclaimer.

Each persona remains the personal property of the person who inspired it. Do not reuse, redistribute, or create derivative works from these personas without explicit permission from the respective individual, even for non‑commercial projects, as far as legally possible.

No private information is included, and all generated responses should be treated as a sandbox, non-binding prototype. For any commercial usage or derivative works, please obtain written consent from AccessAI Tech LLC and the respective owners. See white paper §8 and [DISCLAIMER.md](DISCLAIMER.md) for full details.

We keep a simple data-processing log and offer a self-service deletion tool so models can remove their photos and trained avatars at any time. See [privacy-policy.md](privacy-policy.md) for details. An example popup form for requesting deletion is provided in [docs/deletion_popup_example.html](docs/deletion_popup_example.html). You can link to this page from a custom GPT assistant or embed the snippet in your own site.

## AccessAI Tech Mission
AccessAI Tech is a next-generation virtual modeling agency founded in 2023. Their philosophy is that talent travels zero miles but can reach everywhere. Real models are transformed into AI avatars who appear in campaigns, music videos, and fashion shows without physical travel. The company prioritizes inclusivity, safety, and creative freedom. Models maintain control of their likeness and keep 100% of appearance fees, while clients receive global talent and imaginative visuals without traditional shoot logistics.

## Company Background
AccessAI Tech was founded in 2023 as a software R&D startup focused on building an AI-powered visual tool, similar in spirit to Stable Diffusion.

When the original SaaS vision didn’t gain traction, the founders continued independently as digital artists on Instagram.
It wasn’t until April–May 2025 that we officially pivoted the project into a creative studio, aiming to monetize our artistic work.

All models and personas created before this pivot were purely artistic collaborations with no corporate affiliation. We make it a priority to respect and preserve the artistic nature of those early collaborations. Unless otherwise agreed, these collaborators are not associated with any commercial aspect of AccessAI Tech. Their presence on Instagram remains purely artistic unless explicitly featured on our official website.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on code style, adding personas, and running tests.

## License
Code: MIT. Persona text: CC BY-NC-ND 4.0 (see LICENSE_PERSONAS).
See the [LICENSE_CODE](LICENSE_CODE) file for the full MIT license that applies to the code. The MIT-licensed code in this repository was authored by Taha "Supernova" Gungor and May "Mimi" Kim, who provide it as freelance artists.

The persona names, likenesses, and personal story content are included here with
permission from their respective owners. They remain the property of their respective owners
and are not covered by the code's MIT license. Do not commercialize or
redistribute these persona files without explicit consent.

All persona text—both the files in `/personas` and the three `!!!PUBLIC_READ!!!_*`
profiles—is licensed under the
[Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/)
license as noted in [LICENSE_PERSONAS](LICENSE_PERSONAS).

| Folder or file pattern | License | What it means |
|------------------------|---------|---------------|
| `/docs/`, any `*.py` file, and general project docs | [MIT](LICENSE_CODE) – free for any purpose, including commercial. |
| `/personas/` and `!!!PUBLIC_READ!!!_*` files | [CC BY-NC-ND 4.0](LICENSE_PERSONAS) – persona text is non‑commercial and no derivatives. |

For a directory-by-directory summary of which license applies, see [LICENSE_SCOPE.md](LICENSE_SCOPE.md).

> **Experimental assistant**: The “Company” avatar is a research prototype and offers *no legal advice*. See `DISCLAIMER.md`.


## Fan-Art / Transformative-Use Notice
This project produces purely **transformative fan art of Taha "Supernova" Gungor and May "Mimi" Kim**. All real-world brands, trademarks, and music references (e.g., aespa, Doja Cat) remain the property of their respective owners; no affiliation or endorsement is implied.
If you are a rights holder and wish removal, email **taha.gung@gmail.com** and we will comply within 30 days.

> ## **Safety & Privacy**
> This is an experimental art project. You own your prompts and outputs. We log nothing except basic error stats.

## Star, Contribute & Connect
If you enjoy these experimental personas, please **star this repo** and consider contributing improvements. Pull requests are welcome.

### Chat with the Avatars
- [Mimi GPT](https://chatgpt.com/g/g-681c5724c660819196e26b14870c3726-mimi)
- [Supernova GPT](https://chatgpt.com/g/g-681bd489d38c8191b6977adfd079c15a-supernova-2177-avatar-taeha)

### Follow us on Instagram
- Mimi: <https://www.instagram.com/studiomimi_style/>
- Taha (Supernova): <https://www.instagram.com/blueprint_nova/>

For questions or collaborations, reach out via Instagram DM.

## Glossary
- **Persona** – A "character sheet" that tells GPT how to speak and behave.
- **Deep-Knowledge** – Extra facts that only this persona's real life circle knows (kept in a separate file and it is still public).
- **Public Info / Public Profile** – Safe-to-share facts (name, pronouns, job title, fun trivia) that anyone can read on GitHub; never includes emails, phone numbers, or private data.
- **Private Info** – Sensitive details that stay offline (e.g., real contact info). We **do not** store these in the repo.
- **Selector** – The Python tool that picks and merges the right persona files before sending the prompt to GPT.
- **Avatar** – The visual or text likeness of a real or fictional person / both or one.

### Universal SDKs
Need this in a game, robot, or chatbot?
Grab the stubs in **`/sdk`** and call `/chat`, `/manifest` (JSON), or `/manifest.yaml` (YAML) from Python, JS, C#, or any language that can hit HTTP — no extra dependencies required.

For details on how the `manifest.yaml` file powers the character system and how to add your own entries, see [docs/manifest_system.md](docs/manifest_system.md).
To deploy a persona directory in another host (Discord, Unreal, Unity), follow the steps in [docs/spawn_system.md](docs/spawn_system.md).
For a Unity-specific C# example using `GptFrenzyClient`, see [docs/unity_integration.md](docs/unity_integration.md).
For a quick Discord bot setup, see [docs/discord_setup.md](docs/discord_setup.md).
