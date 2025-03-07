.PHONY: all check lint test docs clean clean-docs

all: docs check install

check: lint test

lint:
	pylint cairo_util/*.py test/*.py

test:
	NUMBA_DISABLE_JIT=1 coverage run --omit=.venv* -m pytest --durations=5
	coverage report -m --omit "/usr*","/opt*","*config*"

docs: cairo_util/*.py docs/*.rst docs/*.py
	$(MAKE) -C docs html

clean: clean-docs
	rm -rfv build *.egg-info .coverage */__pycache__ dist

clean-docs:
	rm -rfv docs/_build docs/_generated docs/__pycache__

install:
	pip install .

