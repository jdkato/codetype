# cypher

[![Build Status](https://travis-ci.org/jdkato/cypher.svg?branch=master)](https://travis-ci.org/jdkato/cypher) [![Coverage Status](https://coveralls.io/repos/github/jdkato/cypher/badge.svg?branch=master)](https://coveralls.io/github/jdkato/cypher?branch=master) [![Code Health](https://landscape.io/github/jdkato/cypher/master/landscape.svg?style=flat)](https://landscape.io/github/jdkato/cypher/master) [![Hex.pm](https://img.shields.io/hexpm/l/plug.svg?maxAge=2592000)](https://github.com/jdkato/cypher/blob/master/LICENSE.txt) ![Python Support](https://img.shields.io/badge/python-2.7,3.4,3.5-blue.svg)

`cypher` is a Python library and CLI tool for identifying the language of source code snippets and files. It's fast, simple and accurate. [You can test it out here](http://jdkato.github.io/cypher/).

## Installation

```
$ git clone https://github.com/jdkato/cypher.git
$ cd cypher
$ python setup.py install
```

## Usage

###### Python

```python
>>> from cypher import identify
>>> identify('fibs = 0 : 1 : zipWith (+) fibs (tail fibs)')
'Haskell'
>>> identify('from math import fabs')
'Python'
>>>
```

###### CLI

```
usage: cypher [-h] [--version] [-v] [-m MAX] file

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

###### Snippets

```
$ python run.py test
```

###### Repos

```
$ python run.py dev -t
```
