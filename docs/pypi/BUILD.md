# Building and pushing to pypi

## Build:

    python3 -m pip install --upgrade build

    python3 -m build

## Push

    python3 -m twine upload --repository testpypi dist/*
