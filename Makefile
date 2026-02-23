run-python:
	python src/main.py

run-docker:
	docker compose up -d

down-docker:
	docker compose down -v

freeze:
	uv export --no-hashes -o requirements.txt --no-editable --no-emit-project > requirements.txt
