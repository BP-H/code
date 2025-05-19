## Contributing to GPT Frenzy
GPT Frenzy welcomes pull requests that improve the code or the collection of persona files. This document outlines basic guidelines for contributors.
By submitting code you agree it remains MIT-licensed and you keep your copyright.

### Code style

* Format all Python code with **[Black](https://black.readthedocs.io/)**.
  Run `black .` before submitting a pull request.
* Keep the repository compatible with Python 3.10 or newer.

### Adding a persona

1. Create two files inside the `personas/` directory:
   * `!!!ATTENTION_READ_ALL!!!_<NAME>_GPT_INSTRUCTIONS.txt`
   * `!!!ATTENTION_READ_ALL!!!_DEEP_KNOWLEDGE_<NAME>.txt`
2. Include the short license notice at the top of each file, as shown in the existing personas.
3. Use the same tone and structure as the other persona files so the `persona_selector.py` script can merge them.
4. Test your files by running:

   ```bash
   python3 persona_selector.py --list
   python3 persona_selector.py --merge ID --output combined.txt
   ```
   Replace `ID` with the number assigned to your persona.

### Running tests

Automated tests use [pytest](https://pytest.readthedocs.io/). After installing
pytest, run:

```bash
python3 -m pytest
```

All tests live in the `tests/` directory.

