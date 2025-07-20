# Omar Aflak

My personal blogging website.

# Dev

1) Enter the source directory
2) Compile the ProtoBuffer classes
3) Create a Python virtual environment
4) Enter the virtual environment
5) Install the Python requirements
6) Parse the Markdown and generate the Html files

```
cd src/
make
python -m venv .venv
source .venv/bin/activate
pip install -e .
python cli.py generate_all ../md/ ../articles/
```
