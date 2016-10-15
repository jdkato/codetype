from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert("README.md", "rst")
except ImportError:
    long_description = None

setup(
    name="codetype",
    packages=["codetype"],
    scripts=["bin/codetype"],
    version="1.0.0",
    description="A source code identification tool.",
    long_description=long_description,
    keywords=["classifying", "identification", "code"],
    install_requires=[
        "msgpack-python"
    ],
    include_package_data=True,
    author="Joseph Kato",
    author_email="joseph@jdkato.io",
    url="https://github.com/jdkato/codetype",
    download_url="https://github.com/jdkato/codetype/releases",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ],
)
