.PHONY: run load_data

run:
	cd server && docker compose up -d --build

load_data:
	python script.py