.PHONY: clean clean-test clean-pyc clean-build build help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-pyc: ## clean python cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +

clean-test: ## cleanup pytests leftovers
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr test_results/
	rm -f *report.html
	rm -f log.html
	rm -f test-results.html
	rm -f output.xml

docker-restart: ## restart containers
	docker compose down
	docker compose up --build -d

docker-test: docker-restart ## restart containers & test
	pytest -s

pre-commit-setup: ## Install pre-commit
	python3 -m pip install pre-commit
	pre-commit --version

test-requirements: ## installs pytest singular package for local testing
	python3 -m pip install pytest 
	python3 -m pip install requests 
	python3 -m pip install hypothesis
	python3 -m pip install pytest-asyncio

requirements: ## installs all requirements
	python3 -m pip install -r requirements.txt
	python3 -m pip install ruff

setup: pre-commit-setup test-requirements requirements ## setup requirements

docs: ## opens your browser to the webapps testing docs
	open http://localhost:5000/docs
	xdg-open http://localhost:5000/docs
	. http://localhost:5000/docs