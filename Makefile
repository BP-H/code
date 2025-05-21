.PHONY: openapi openapi-check check-openapi discord-run
openapi:
	@python -m pip show PyYAML >/dev/null 2>&1 || pip install --quiet PyYAML
	python scripts/generate_openapi.py

openapi-check: openapi
	git diff --exit-code openapi.json

check-openapi: openapi-check

discord-run:
       python clients/discord/bridge.py
