# GPT Frenzy Project Structure

This overview summarizes how the repository is organized. For a deeper explanation of the dual-layer licensing approach, see [docs/white-paper-public-alpha-2025.md](docs/white-paper-public-alpha-2025.md).

The project separates operational code from persona text. All code is MIT licensed to May "Mimi" Kim and Taha "Supernova" Gungor, while each persona's files remain the property of the person depicted and are shared under CC BY-NC-ND 4.0. This setup lets anyone fork the code without taking ownership of the personas.
## Directory Map

| Path or file | Purpose | License |
|--------------|---------|---------|
| `/docs/` | Guides, white paper, mini game, integration notes | MIT |
| `/personas/` | Persona instruction and deep knowledge files | CC BY-NC-ND 4.0 (per owner) |
| `persona_selector.py` | Script to merge persona instruction and knowledge files | MIT |
| `LICENSE_CODE` | MIT license text for all code | MIT |
| `LICENSE_PERSONAS` | Creative Commons license for persona text | CC BY-NC-ND 4.0 |
| `LICENSE_SCOPE.md` | Summary table showing which license covers each folder | MIT |
| `README.md` and other root docs | Quick start info, disclaimers, templates | MIT |
| `DATA_PROCESSING_LOG_TEMPLATE.md` | Template to record data processing events | MIT |
| `privacy-policy.md` | How to request deletion of personal data | MIT |
| `RESOURCE.txt` / `websiteinfo.txt` | Additional background and resource links | MIT |

## Persona Loading Flow

```text
[persona files] --merge--> persona_selector.py --output combined.txt --> load into ChatGPT
```

1. Choose a persona from `/personas/`.
2. Merge the instruction and knowledge files:

```bash
python3 persona_selector.py --merge ID --output combined.txt
```

3. Upload `combined.txt` to ChatGPT (or your preferred tool).
4. Start the conversation.

## License

```
MIT License

Copyright (c) 2025 May "Mimi" Kim
Copyright (c) 2025 Taha "Supernova" Gungor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
