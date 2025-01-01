# cashkollab

## Name
Cashflow visualization

## Dependency Management

We use `poetry` to manage our dependencies. To install `poetry` you can use [(more infos here)](https://python-poetry.org/docs/):
```shell
$ curl -sSL https://install.python-poetry.org | python -
```

Our dependencies are documented in the [pyproject.toml](pyproject.toml), the explicit versions with hashes for the libraries you can find in [poetry.lock](poetry.lock).


## Installation
```shell
poetry shell # to change to the poetry shell/venv (or creating it)
poetry env use python3.10
poetry install # install all dependency for the project
python src/hellcash/manage.py migrate  # migrate/create sqlite db
```

## Usage

```shell
poetry run src/manage.py runserver # run project
```

## Docker

```shell
make # builds docker container
make start # runs docker container interactive
```


## development tools

run the tools when needed
```shell
isort .
black src tools tests
mypy src
pylint src/*
```

or all in script
```shell
./run_all_checks.sh
```

and fix the errors :-)

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

## Authors and acknowledgment
 + Ströte
 + debauer

## License
TDB
