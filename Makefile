all:
	python src/cli.py markdown public/articles

install:
	pip install -e src/

.DEFAULT:
	python src/cli.py markdown public/articles --only="$@.md"
