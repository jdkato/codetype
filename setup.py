from setuptools import setup
from cypher import __version__

setup(
    name="cypher",
    packages=["cypher"],
    scripts=["bin/cypher"],
    version=__version__,
    description="A source code identification tool.",
    install_requires=[
        "msgpack-python"
    ],
    include_package_data=True,
    author="Joseph Kato"
)
