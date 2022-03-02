# Variables
SOURCE = pelote

# Functions
define clean
	rm -rf *.egg-info .pytest_cache build dist
	find . -name "*.pyc" | xargs rm -f
	find . -name __pycache__ | xargs rm -rf
	rm -f *.spec
endef

# Commands
all: check test
test: unit
publish: clean lint test upload
	$(call clean)

clean:
	$(call clean)

deps:
	pip3 install -U pip
	pip3 install -r requirements.txt

format:
	@echo Formatting code...
	black $(SOURCE) test *.py
	@echo

check:
	@echo Type checking...
	MYPYPATH=./typings mypy -p pelote
	@echo

unit:
	@echo Running unit tests...
	pytest -svvv
	@echo

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
