from setuptools import setup

setup(
    name="codetype",
    packages=["codetype"],
    scripts=["bin/codetype"],
    version="1.0.0",
    description="A source code identification tool.",
    keywords=["classifying", "identification", "code"],
    install_requires=[
        "msgpack-python"
    ],
    include_package_data=True,
    author="Joseph Kato",
    author_email="joseph@jdkato.io",
    url="https://github.com/jdkato/codetype",
    download_url="https://github.com/jdkato/codetype/releases",
)
