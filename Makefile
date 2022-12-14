SHELL = /bin/sh

build:
	python3 -m build

install:
	pip install -e .

build-push-pypi:
	rm -rf build && \
	rm -rf dist && \
	python3 -m build && \
	python3 -m twine upload --repository pypi dist/*

build-push-testpypi:
	rm -rf build && \
	rm -rf dist && \
	python3 -m build && \
	python3 -m twine upload --repository testpypi dist/*

bump:
	cz bump --check-consistency --changelog