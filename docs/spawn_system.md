# Spawnable Persona System

This guide explains how to package a persona so it can be loaded by
`gptfrenzy.spawn.launch()` and used in different hosts such as Discord,
Unreal or Unity. Each persona lives in its own directory with a
`manifest.yaml` describing the entry point, capabilities and assets.

## `manifest.yaml` fields

A minimal manifest created by `gptfrenzy.spawn.make_manifest()` looks
like:

```yaml
sap_version: "0.3"
entrypoint: gptfrenzy.spawn:launch
assets: []
capabilities:
  - text
license_ref: ./LICENSE_PERSONAS
```

* **`sap_version`** – Version of the Spawn API. `launch()` only accepts
  `"0.3"`.
* **`entrypoint`** – Import path to a launch function that returns a
  `PersonaInstance`. The default is `gptfrenzy.spawn:launch`.
* **`assets`** – Optional list of extra files required by the persona
  (models, images, etc.).
* **`capabilities`** – Flags that control which methods are exposed.
  Supported values are `text`, `voice` and `realtime_embodiment`.
* **`license_ref`** – Path to the license covering the persona files.

## How `launch()` works

`gptfrenzy.spawn.launch(host, persona_path, **kwargs)` reads the
`manifest.yaml` inside `persona_path`. It verifies the `sap_version`,
loads the `Persona` class from `persona.py` and instantiates it,
passing `host` and any extra keywords. The resulting object is wrapped in
`PersonaInstance`, which exposes only the methods allowed by the
`capabilities` list. For example, if the manifest omits `voice`, calling
`instance.speak()` raises an error.

## Directory layout

A deployable persona directory typically contains just two files:

```
my_persona/
├── manifest.yaml
└── persona.py
```

### Minimal `persona.py`

```python
class Persona:
    def __init__(self, host: str | None = None, persona_path: str | None = None, **kwargs):
        self.host = host
        self.path = persona_path

    async def generate(self, text: str):
        return text.upper()
```

Place the directory anywhere accessible by your application and call
`launch("discord", "./my_persona")` (replace the host string as needed).
The returned `PersonaInstance` exposes an async `generate()` method that
you can await in your bot or game.
