SHELL = /bin/sh

build:
	python3 -m build

install:
	pip install -e .

build-push:
	rm -rf build && \
	rm -rf dist && \
	python3 -m build && \
	python3 -m twine upload --repository testpypi dist/*
