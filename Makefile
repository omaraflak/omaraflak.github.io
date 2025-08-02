all:
	python src/cli.py markdown articles

install:
	pip install -e src/

.DEFAULT:
	python src/cli.py markdown articles --only="$@.md"
