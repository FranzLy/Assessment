.PHONY: install run test lint format docker-build docker-run

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

docker-build:
	docker build -t openstack-vm-lifecycle-api:latest .

docker-run:
	docker run --rm -p 8000:8000 \
		-e APP_DB_PATH=/data/vms.db \
		-v "$(PWD)/data:/data" \
		openstack-vm-lifecycle-api:latest
