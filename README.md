# cypher

[![Build Status](https://travis-ci.org/jdkato/cypher.svg?branch=master)](https://travis-ci.org/jdkato/cypher) [![Coverage Status](https://coveralls.io/repos/github/jdkato/cypher/badge.svg?branch=master)](https://coveralls.io/github/jdkato/cypher?branch=master) [![Code Health](https://landscape.io/github/jdkato/cypher/master/landscape.svg?style=flat)](https://landscape.io/github/jdkato/cypher/master) [![Hex.pm](https://img.shields.io/hexpm/l/plug.svg?maxAge=2592000)](https://github.com/jdkato/cypher/blob/master/LICENSE.txt) ![Python Support](https://img.shields.io/badge/python-2.7,3.4,3.5-blue.svg)

`cypher` is a Python library and CLI tool for identifying the language of source code snippets and files. It's fast, simple and accurate. [You can test it out here](http://jdkato.github.io/cypher/).

## Installation

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

## Performance

| # of Files Tested | Time Per File (sec) | Average Accuracy | Lowest Accuracy |
|:-----------------:|:-------------------:|:----------------:|:---------------:|
|       17684       |        0.017        |       0.993      |     0.963 (C)   |

## Support

|   Language    |       Status          |
|:-----------:  |:------------------:   |
| AppleScript   | :white_check_mark:    |
|      C#       | :white_check_mark:    |
|     C++       | :white_check_mark:    |
|      C        | :white_check_mark:    |
| Clojure       | :x:                   |
|CoffeeScript   |         :x:           |
|      D        | :white_check_mark:    |
|    Erlang     |         :x:           |
|      Go       | :white_check_mark:    |
|   Groovy      | :x:                   |
|   Haskell     | :white_check_mark:    |
|     Java      | :white_check_mark:    |
|  JavaScript   |         :x:           |
|    Julia      | :white_check_mark:    |
|     Lisp      |         :x:           |
|     Lua       | :white_check_mark:    |
|    Matlab     |         :x:           |
|    OCaml      | :white_check_mark:    |
| Objective-C   | :white_check_mark:    |
|    Pascal     |         :x:           |
|     Perl      | :white_check_mark:    |
|     PHP       | :white_check_mark:    |
|    Python     | :white_check_mark:    |
|      R        | :white_check_mark:    |
|     Ruby      | :white_check_mark:    |
|     Rust      | :white_check_mark:    |
|    Scala      | :white_check_mark:    |
|    Swift      |         :x:           |
| TypeScript    |         :x:           |
| Visual Basic  |         :x:           |
