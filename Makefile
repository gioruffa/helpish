.PHONY: lint fix test build publish

lint:
	uv run ruff check .
	uv run ty check .

fix:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest --cov=src tests

mutate:
	uv run mutmut run

build:
	uv build

publish: build
	uv publish --token $$PIPL_TOKEN
