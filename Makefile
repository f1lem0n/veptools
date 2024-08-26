# Author: Filip Hajdyła
# Date of creation: 15/11/2023
# Description: Automation of common tasks for the project

SHELL := /bin/bash

.PHONY: help test format lint clean checksum verify install

help:
	@echo
	@echo "MAKE TARGETS ARE FOR DEVELOPMENT PURPOSES ONLY."
	@echo "PLEASE USE CONDA ENV FOR RUNNING ANY OF THE MAKE TARGETS."
	@echo
	@echo "Available targets:"
	@echo "help - display this help message"
	@echo "test - measure code coverage with pytest"
	@echo "format - format package with black and isort"
	@echo "lint - static code analysis with flake8 and mypy"
	@echo "clean - remove common artifacts from the directory tree as well as built and installed package"
	@echo "checksum - generate md5 checksum of the repository"
	@echo "diff - verify md5 checksum of the repository (if stdout is empty then checksums are equal)"
	@echo "install - build and install current development version in a virtual environment"

test:
	@time coverage run -m pytest -sxv --log-level=DEBUG && \
		echo "" && \
		echo "COVERAGE REPORT:" && \
		echo "" && \
		coverage report -m;

format:
	@echo "Sorting imports..."
	@isort --profile black -l 79 veptools/ tests/ setup.py
	@echo "Formatting code..."
	@black -l 79 -t py312 --safe veptools/ tests/ setup.py

lint:
	@flake8 veptools/ tests/ setup.py
	@mypy --install-types --non-interactive veptools/ tests/ setup.py

clean:
	@rm -rf .coverage .pytest-monitor .pytest_cache .mypy_cache
	@rm -rf \
		__pycache__ \
		veptools/__pycache__ \
		veptools/modules/__pycache__ \
		tests/output \
		tests/__pycache__ \
		tests/logs \
		veptools-build \
		veptools.egg-info \
		dist

checksum:
	@echo "Generating repository checksum..."
	@export LC_ALL=C
	@find . -type f \
		\! -path "./.vscode/*" \
		\! -path "./.git/*" \
		\! -path "./tests/logs/*" \
		\! -path "./.pytest_cache/*" \
		\! -path "./.mypy_cache/*" \
		\! -path "./.pytest-monitor/*" \
		\! -path "./.coverage" \
		\! -path "*__pycache__*" \
		\! -path "./md5" \
		\! -path "./veptools-build/*" \
		\! -path "./veptools.egg-info/*" \
		\! -path "./dist/*" \
		\! -path "./tests/output/*" \
		-exec md5sum {} \; | sort -k 2 > md5
	@echo "Checksum generated!"

diff:
	@echo "Verifying repository checksum..."
	@export LC_ALL=C
	@find . -type f \
		\! -path "./.vscode/*" \
		\! -path "./.git/*" \
		\! -path "./.pytest_cache/*" \
		\! -path "./.mypy_cache/*" \
		\! -path "./.pytest-monitor/*" \
		\! -path "./.coverage" \
		\! -path "*__pycache__*" \
		\! -path "./md5" \
		\! -path "./veptools-build/*" \
		\! -path "./veptools.egg-info/*" \
		\! -path "./dist/*" \
		\! -path "./tests/output/*" \
		-exec md5sum {} \; | sort -k 2 | diff - md5
	@echo "Checksums are equal!"

install:
	@echo "BUILDING PACKAGE..."
	@python3 -m build
	@echo "INSTALLING PACKAGE IN VENV..."
	@python3 -m venv veptools-build
	@source veptools-build/bin/activate && \
		pip install dist/veptools-*.whl && \
		deactivate
	@echo
	@echo "PACKAGE INSTALLED!"
	@echo "To use, first activate venv:"
	@echo
	@echo "	source veptools-build/bin/activate"
