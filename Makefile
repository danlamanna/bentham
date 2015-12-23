SRCS=.
TESTS=tests/

FLAKE8=flake8
PYTEST=py.test

test-all: clean test coverage style-test

test:
	$(PYTEST) $(TESTARGS) $(TESTS)

style-test:
	$(FLAKE8) $(TESTARGS) $(SRCS)

coverage:
	$(PYTEST) -q --cov=bentham $(TESTARGS) $(TESTS)

coverage-html:
	$(MAKE) coverage TESTARGS="--cov-report html"

clean:
	find $(SRCS) -name "*.pyc" -delete
	rm -rf .cache .coverage htmlcov tests/__pycache__
