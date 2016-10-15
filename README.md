# codetype

[![Build Status](https://travis-ci.org/jdkato/codetype.svg?branch=master)](https://travis-ci.org/jdkato/codetype) [![Code Health](https://landscape.io/github/jdkato/codetype/master/landscape.svg?style=flat)](https://landscape.io/github/jdkato/codetype/master) ![Python Support](https://img.shields.io/badge/python-2.7,3.4,3.5-blue.svg)

`codetype` is a Python library and command-line tool for identifying the language of source code snippets and files. It's fast, simple and accurate. [You can test it out here](http://jdkato.github.io/codetype/).

## Installation

###### Using pip

```
pip install codetype
```

###### From source

```
$ git clone https://github.com/jdkato/codetype.git
$ cd codetype
$ python setup.py install
```

## Usage

###### Python

```python
>>> from codetype import identify
>>> identify('fibs = 0 : 1 : zipWith (+) fibs (tail fibs)')
'Haskell'
>>> identify('from math import fabs')
'Python'
>>>
```

###### CLI

```
usage: codetype [-h] [--version] [-v] [-m MAX] file

A source code identification tool.

positional arguments:
  file               path to unknown source code

optional arguments:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  -v, --verbose      use verbose output
  -m MAX, --max MAX  max number of languages to return
```

## Language Support

AppleScript, C#, C++, C, D, Go, Haskell, Java, JavaScript, Julia, Lua, OCaml, Objective-C, Perl, 
PHP, Python, R, Ruby, Rust, Scala & Swift

## Testing

```
$ python run.py dev -t
```
