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

_create-make-env: ## Create make.env file
	@echo 'Enter implementation name: ' && \
	read implementation && \
	if [ -z "$$implementation" ]; then \
		echo "Implementation name cannot be empty."; \
		exit 1; \
	fi && \
	echo "implementation=$$implementation" > make.env && \
	echo "Created make.env"



# Target to stop all Docker containers in the src directory
docker-down: ## Stop all containers in src folders
	@for dir in src/*/ ; do \
		if [ -f "$${dir}docker-compose.yml" ]; then \
			echo "Stopping Docker containers in $${dir}..." && \
			docker compose -f "$${dir}docker-compose.yml" down ; \
		fi \
	done

# Target to restart Docker containers
docker-restart: _create-make-env docker-down## Restart containers
	@export implementation=$$(grep implementation make.env | cut -d '=' -f 2) && \
	compose_file="src/$$implementation/docker-compose.yml" && \
	if [ ! -f "$$compose_file" ]; then \
		echo "docker-compose.yml not found for implementation: $$implementation"; \
		exit 1; \
	fi && \
	echo "Using: $$compose_file" && \
	docker compose -f "$$compose_file" up -d

# Target to restart Docker containers and run tests
docker-test: docker-restart## Restart containers & test
	@export implementation=$$(grep implementation make.env | cut -d '=' -f 2) && \
	implementation=$$implementation pytest -s tests/

# Target to restart Docker containers and run benchmark	
docker-benchmark: docker-restart
	@export implementation=$$(grep implementation make.env | cut -d '=' -f 2) && \
	implementation=$$implementation python3 performance_test/main.py

# Target to test all Docker containers in the src directory
docker-benchmark-all: docker-down ## Stop all containers in src folders and test
	@for dir in src/*/ ; do \
		if [ -f "$${dir}docker-compose.yml" ]; then \
			echo "Starting Docker containers in $${dir}..." ; \
			docker compose -f "$${dir}docker-compose.yml" up -d ; \
			dir_name=$$(basename "$${dir}") ; \
			for i in 1 2 3; do \
				echo "Running performance test $${i} for $${dir_name}..." ; \
				implementation=$${dir_name} python3 performance_test/main.py ; \
			done ; \
			echo "Stopping Docker containers in $${dir}..." ; \
			docker compose -f "$${dir}docker-compose.yml" down ; \
		fi \
	done
	
docker-grafana:
	docker compose -f performance_test/docker-compose.yml down
	docker compose -f performance_test/docker-compose.yml up -d --build

requirements: ## installs all requirements
	python3 -m pip install -r requirements.txt
	python3 -m pip install pytest requests hypothesis pytest-asyncio precommit ruff
	pre-commit --version
