clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

run:
	export FLASK_CONFIG=development
	export FLASK_APP=application
	export FLASK_ENV=development
	flask run

test:
	flask test

db:
	rm -rf  migrations
	flask db init
	flask db migrate
	flask db upgrade

migrate:
	export FLASK_CONFIG=development
	export FLASK_APP=application
	export FLASK_ENV=development
	flask db migrate
	flask db upgrade
