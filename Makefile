.PHONY: openapi
openapi:
	python app.py --openapi
	git add openapi.json
	git diff --cached --quiet openapi.json || git commit -m "Update openapi.json" openapi.json
