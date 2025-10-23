PORT ?= 8000

install:
	uv sync

build:
	./build.sh

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

test:
	uv run pytest tests/