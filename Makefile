up:
	poetry run uvicorn app:app --reload --port 8000

.PHONY: migrate-rev
migrate-rev:
	poetry run alembic revision --autogenerate -m $(name)

.PHONY: migrate-up
migrate-up:
	poetry run alembic upgrade $(rev)

.PHONY: local
local:
	docker compose up postgres

.PHONY: test
test:
	poetry run pytest
