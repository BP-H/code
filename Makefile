.PHONY: openapi discord-run
openapi:
	python scripts/generate_openapi.py

discord-run:
	python clients/discord/bot.py
