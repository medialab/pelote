# Variables
SOURCE = pelote

# Functions
define clean
	rm -rf *.egg-info .mypy_cache .pytest_cache build dist
	find . -name "*.pyc" | xargs rm -f
	find . -name __pycache__ | xargs rm -rf
	rm -f *.spec
endef

# Commands
all: test
test: unit
publish: clean test upload
	$(call clean)

clean:
	$(call clean)

ci:
	python -m pip install --upgrade pip setuptools wheel
	pip3 install -r requirements.txt

deps:
	pip3 install -U pip
	pip3 install -r requirements.txt

format:
	@echo Formatting code...
	black $(SOURCE) experiments docs test *.py
	@echo

check:
	@echo Type checking...
	mypy -p pelote -p test
	@echo

unit:
	@echo Running unit tests...
	pytest -svvv
	@echo

readme:
	python -m docs.build > README.md

upload:
	python setup.py sdist bdist_wheel
	twine check dist/pelote-*
	twine upload dist/pelote-*
