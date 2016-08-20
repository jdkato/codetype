from setuptools import setup

setup(
    name="cypher",
    packages=["cypher"],
    scripts=["bin/cypher"],
    version="0.0.1",
    description="A source code identification tool.",
    install_requires=[
        "msgpack-python"
    ],
    include_package_data=True,
    author="Joseph Kato"
)
