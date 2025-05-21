.PHONY: openapi
openapi:
	PYTHONPATH=. python scripts/generate_openapi.py openapi.json

.PHONY: openapi-check
openapi-check:
	@temp_file=$$(mktemp); \
	PYTHONPATH=. python scripts/generate_openapi.py $$temp_file; \
	diff -u openapi.json $$temp_file; \
	rm $$temp_file
