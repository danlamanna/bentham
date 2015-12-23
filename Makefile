test:
	py.test $(TESTARGS) tests/

coverage:
	py.test -q --cov-report html --cov=bentham tests/
