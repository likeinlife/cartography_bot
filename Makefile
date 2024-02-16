run-python:
	python src/main.py

run-docker:
	docker compose up -d

down-docker:
	docker compose down -v

freeze:
	poetry export -o requirements.txt --without-hashes
