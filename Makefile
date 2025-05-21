.PHONY: openapi check-openapi discord-run
openapi:
	python scripts/generate_openapi.py

check-openapi:
	python scripts/generate_openapi.py
	git diff --exit-code openapi.json

discord-run:
	python clients/discord/bot.py
