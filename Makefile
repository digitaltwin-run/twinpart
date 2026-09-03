SHELL := /bin/bash

.PHONY: test lint check list install

test:
	pytest -q

lint:
	ruff check src tests

check:
	python3 -m twinpart.cli check

list:
	python3 -m twinpart.cli list
