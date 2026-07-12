.phony: test coverage static

test:
	tox run

coverage:
	tox run -e coverage

static:
	tox run -e static
