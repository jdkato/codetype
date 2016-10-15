from setuptools import setup

setup(
    name="codetype",
    packages=["codetype"],
    scripts=["bin/codetype"],
    version="1.0.0",
    description="A source code identification tool.",
    install_requires=[
        "msgpack-python"
    ],
    include_package_data=True,
    author="Joseph Kato"
)
