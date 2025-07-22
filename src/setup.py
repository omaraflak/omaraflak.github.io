import setuptools

setuptools.setup(
    name="blog",
    version="0.1",
    packages=setuptools.find_packages(),
    install_requires=[
        "fire",
        "marko",
        "link_preview"
    ],
)
