.PHONY: install run test lint format

install:
	python3 -m pip install -e ".[dev]"

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	python3 -m pytest

lint:
	ruff check .

format:
	ruff check . --fix
