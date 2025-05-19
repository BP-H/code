# Architecture Overview

The project follows a lightweight pipeline so that each persona stays consistent when you load it into ChatGPT or another LLM. The flow centers on the **persona selector**, which merges the instruction file with its knowledge file before you upload anything to the model.

```
Selector → Merged Prompt → LLM
```

**1. Persona Selector**

`persona_selector.py` lets you pick a persona by number and automatically combines the two text files that define it. The script ensures you do not forget the deep-knowledge section. Run it with `--merge` to create a single output file.

**2. Merged Prompt**

The merged file contains both instructions and backstory. This text is what you paste into ChatGPT or any LLM interface. Keeping the files merged avoids losing important context about tone, vocabulary and privacy rules.

**3. LLM**

The language model uses the merged prompt as its initial system message. Every reply should respect that prompt until you reset or supply new instructions. The model itself never sees the selector script; it only sees the combined text you uploaded.

This architecture keeps the repository simple while making sure each persona speaks with its full voice.
