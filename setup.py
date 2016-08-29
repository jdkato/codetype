from setuptools import setup

setup(
    name="cypher",
    packages=["cypher"],
    scripts=["bin/cypher"],
    version="1.0.0",
    description="A source code identification tool.",
    install_requires=[
        "msgpack-python"
    ],
    include_package_data=True,
    author="Joseph Kato"
)
