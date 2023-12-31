.DEFAULT_GOAL := help
SHELL := bash
.ONESHELL:

PROJECT_NAME=hello_world
DB_NAME=$(PROJECT_NAME)
INVENTORY=infra/provisioner/hosts
PLAYBOOK=infra/provisioner/deploy-service.yml
ENV_PREFIX=$(shell echo 'poetry run ')


.PHONY: help
help:            ## show the help
	@echo "Usage: make <target>"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'


.PHONY: fmt
fmt:             ## Format code using black & isort.
	${ENV_PREFIX}isort .
	${ENV_PREFIX}black .


.PHONY: lint
lint:            ## Run pep8, black, mypy linters.
	${ENV_PREFIX}flake8 .
	${ENV_PREFIX}black --check .
	${ENV_PREFIX}mypy --ignore-missing-imports ${PROJECT_NAME}/
	${ENV_PREFIX}ansible-playbook -i infra/provisioner/hosts infra/provisioner/deploy-service.yml --syntax-check


run_all:  ## Run all the servers in parallel, requires GNU Make
	make -j djrun doc redis
.PHONY: run_all

virtualenv:     ## Create a virtual environment.
	@echo "creating virtualenv using poetry..."
	@pip install -U pip poetry
	@poetry env use python3
	@echo
	@echo "!!! Please run 'poetry shell' to enable the environment !!!"


regenerate:  ## Delete and create new database.
	-dropdb $(DB_NAME)
	createdb $(DB_NAME)
	${ENV_PREFIX}python manage.py migrate
.PHONY: regenerate

generate_requirements:
	poetry export -f requirements.txt -o requirements/development.txt --dev
	poetry export -f requirements.txt -o requirements/production.txt

update_libs:  ## update libs + generate new lockfile & requirements
	poetry update
	make generate_requirements
.PHONY: update-libs

install: virtualenv  ## Install and setup project dependencies
	python3 -m pip install --upgrade pip wheel
	make generate_requirements
	poetry install
	${ENV_PREFIX}pre-commit install
ifneq ($(CI),True)
	-createdb $(DB_NAME)
	${ENV_PREFIX}python manage.py migrate
endif
.PHONY: install


.PHONY: clean
clean:  ## Remove all temporary files like pycache
	find . -name \*.rdb -type f -ls -delete
	find . -name \*.pyc -type f -ls -delete
	find . -name __pycache__ -ls -delete

# == Django Helpers
# ===================================================
djrun:  ## Start Django server locally
	${ENV_PREFIX}python manage.py runserver


test: ARGS=--pdb --cov  ## Run all the tests
test: lint
	${ENV_PREFIX}pytest $(ARGS)

djmm:  ## Create Django migrations
	${ENV_PREFIX}python manage.py makemigrations

djmigrate:  # Run Django migrations
	${ENV_PREFIX}python manage.py migrate

djurls:  ## Displays all the django urls
	${ENV_PREFIX}python manage.py show_urls

shell:  ## Enter the django shell
	${ENV_PREFIX}python manage.py shell_plus

db_schema:  ## Create db schema
	${ENV_PREFIX}python bin/generate_db_schema.py

doc: db_schema  ## Start documentation server locally
	${ENV_PREFIX}mkdocs serve

redis:  ## Start redis server
	redis-server

# Ansible related things
# ------------------------------------------------------
# Usages:
# 	ENV=dev make configure
# 	ENV=dev make deploy
# 	ENV=dev make deploy_docs

run_ansible:
	@[ "${ENV}" ] || ( echo ">> ENV is not set"; exit 1 )
	${ENV_PREFIX}ansible-playbook -i $(INVENTORY) $(PLAYBOOK) --limit=$(ENV) $(ANSIBLE_ARGS)

configure: ANSIBLE_ARGS=--skip-tags=deploy
configure: run_ansible

deploy: ANSIBLE_ARGS=--tags=deploy
deploy: run_ansible

deploy_docs: ANSIBLE_ARGS=--tags=documentation  ## Deploy Documentation
deploy_docs: run_ansible

deploy_dev: ENV=dev  ## Deploy to Development Server
deploy_dev: deploy

deploy_qa: ENV=qa  ## Deploy to QA server
deploy_qa: deploy

deploy_prod: ENV=prod  ## Deploy to production server
deploy_prod: deploy
