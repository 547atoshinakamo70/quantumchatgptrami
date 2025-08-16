.PHONY: run docker-up test

run:
	bash scripts/run_local.sh

docker-up:
	docker compose up --build -d

test:
	pytest -q
