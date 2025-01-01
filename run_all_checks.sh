#!/bin/bash

source "$(poetry env info --path)"/bin/activate

echo -e "\n##########################\n# Sorting imports alphabetically\n##########################"
isort .

echo -e "\n##########################\n# Upgrading syntax if possible\n##########################"
fd 'py$' --exclude=.venv --exclude=.mypy_cache --exclude=.pytest_cache \
  -X pyupgrade --py38-plus --keep-runtime-typing

echo -e "\n##########################\n# Running black\n##########################"
black src tests

echo -e "\n##########################\n# mypy on src\n##########################"
mypy src

echo -e "\n##########################\n# pylint on src\n##########################"
ruff src

echo -e "\n##########################\n# tests \n##########################"
PYTHONPATH=src python -m pytest tests