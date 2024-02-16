run:
	python src/main.py
freeze:
	poetry export -o src/requirements.txt --without-hashes