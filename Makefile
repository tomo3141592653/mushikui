
SRC = .
TEST = .

## Format code using black/isort
format:
	poetry run black $(SRC) --config pyproject.toml --exclude="__init__.py"
	poetry run isort $(SRC) --profile black 
	poetry run black $(TEST) --config pyproject.toml
	poetry run isort $(TEST) --profile black


test:
	poetry run pytest --cov=$(SRC) --cov-branch --cov-report html:./htmlcov --cov-fail-under 65 
