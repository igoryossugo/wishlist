PORT ?= 8080
WORKER_PROCESSES ?= 1
TEST_SETTINGS ?= genie.settings.test
SIMPLE_SETTINGS ?= genie.settings.development
SANDBOX_SETTINGS ?= genie.settings.sandbox


run:
	@gunicorn genie:app --bind localhost:${PORT} --workers ${WORKER_PROCESSES} --worker-class aiohttp.worker.GunicornUVLoopWebWorker -t 0 -e SIMPLE_SETTINGS=${SIMPLE_SETTINGS}

requirements-test:
	@pip install -r requirements/test.txt

requirements-dev:
	@pip install -r requirements/dev.txt

requirements-prod:
	@pip install -r requirements/prod.txt

test:
	@pytest genie -s -v -p no:warnings

test-coverage:
	@SIMPLE_SETTINGS=${TEST_SETTINGS} pytest --cov=genie genie --cov-report term-missing

test-matching:
	@pytest -rxs -k${Q} genie

lint:
	@flake8
	@isort --check
	@mypy --ignore-missing-imports genie

release-patch: ## Create patch release
	SIMPLE_SETTINGS=${SIMPLE_SETTINGS} bump2version patch --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bump2version patch

release-minor: ## Create minor release
	SIMPLE_SETTINGS=${SIMPLE_SETTINGS} bump2version minor --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bump2version minor

release-major: ## Create major release
	SIMPLE_SETTINGS=${SIMPLE_SETTINGS} bump2version major --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bump2version major

