test-all: clean test coverage style-test

test:
	py.test $(TESTARGS) tests/

style-test:
	flake8 .

coverage:
	py.test -q --cov-report html --cov=bentham tests/

clean:
	find . -name "*.pyc" -delete
	rm -rf .cache .coverage htmlcov tests/__pycache__
