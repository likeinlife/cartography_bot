run-python:
	python src/main.py

run-docker:
	docker build -t cartography_bot .
	docker run -d cartography_bot

freeze:
	poetry export -o requirements.txt --without-hashes
