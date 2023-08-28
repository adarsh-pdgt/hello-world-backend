Hello World
==============================

__Version:__ 0.0.0

Add a short project description here.

## Getting up and running

Minimum requirements: **pip, python3.9, poetry, redis & [PostgreSQL 14][install-postgres]**, setup is tested on Mac OSX only.

```
brew install python3 poetry libmagic postgres 
```

[install-postgres]: http://www.gotealeaf.com/blog/how-to-install-postgresql-on-a-mac

In your terminal, type or copy-paste the following:

    git clone git@github.com:PrimedigitalGlobal/hello-world-backend.git; cd hello-world-backend; make install

Go grab a cup of coffee, we bake your hot development machine.

Useful commands:

- `make djrun` - start [django server](http://localhost:8000/)
- `make deploy_docs` - deploy docs to server
- `make test` - run the test locally with ipdb

**NOTE:** Checkout `Makefile` for all the options available and how they do it.


## Docker

- Install dependencies
```commandline
docker-compose run django make install
```

- Run Docker from project directory
```commandline
docker-compose up
```

- After making new changed rebuild docker image
```commandline
docker-compose build
```

## Managing dependencies

### Poetry

To guarantee repeatable installations, all project dependencies are managed using [Poetry](https://python-poetry.org/). The project’s direct dependencies are listed in `pyproject.toml`.
Running `poetry lock` generates `poetry.lock` which has all versions pinned.

You can install Poetry by using `pip install --pre poetry` or by following the official installation guide [here](https://github.com/python-poetry/poetry#installation).

*Tip:* We recommend that you use this workflow and keep `pyproject.toml` as well as `poetry.lock` under version control to make sure all computers and environments run exactly the same code.

### Other tools

For compatibility, `requirements/production.txt` and `requirements/development.txt` can be updated by running

```bash
poetry export --without-hashes -f requirements.txt -o requirements/production.txt.txt
```

and

```bash
poetry export --without-hashes -f requirements.txt -o requirements/development.txt.txt --dev
```

, respectively.


## Deploying Project

The deployment are managed via travis, but for the first time you'll need to set the configuration values on each of the server.

Check out detailed server setup instruction [here](docs/backend/server_config.md).

## How to release Hello World

Execute the following commands:

```
git checkout master
make test
bump2version patch  # 'patch' can be replaced with 'minor' or 'major'
git push origin master
git push origin master --tags
git checkout qa
git rebase master
git push origin qa
```

## Contributing

Golden Rule:

> Anything in **master** is always **deployable**.

Avoid working on `master` branch, create a new branch with meaningful name, send pull request asap. Be vocal!

Refer to [CONTRIBUTING.md][contributing]

[contributing]: http://github.com/PrimedigitalGlobal/hello-world-backend/tree/master/CONTRIBUTING.md
