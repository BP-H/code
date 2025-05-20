.PHONY: openapi
openapi:
	python scripts/generate_openapi.py > openapi.json
	git add openapi.json
