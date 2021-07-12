SHELL := /bin/bash
TEMP_FOLDER = tmp/
DATASET_PATH = data/

build:
	pip install -r requirements.txt
	# prepare data for the database (filter out corrupted records and fix the format)
	python scripts/prepare_data.py -d ${DATASET_PATH} -o $(TEMP_FOLDER)/database/data.csv
	docker-compose build

up:
	docker-compose up --detach client
	docker-compose logs client

down:
	docker-compose down

test:
	python -m pytest tests/