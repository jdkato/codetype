# cypher

[![Build Status](https://travis-ci.org/jdkato/cypher.svg?branch=master)](https://travis-ci.org/jdkato/cypher) [![Coverage Status](https://coveralls.io/repos/github/jdkato/cypher/badge.svg?branch=master)](https://coveralls.io/github/jdkato/cypher?branch=master) [![Code Health](https://landscape.io/github/jdkato/cypher/master/landscape.svg?style=flat)](https://landscape.io/github/jdkato/cypher/master) [![Hex.pm](https://img.shields.io/hexpm/l/plug.svg?maxAge=2592000)](https://github.com/jdkato/cypher/blob/master/LICENSE.txt) ![Python Support](https://img.shields.io/badge/python-2.7,3.4,3.5-blue.svg)

[`cypher`](https://en.wikipedia.org/wiki/Cypher_(Marvel_Comics)) is a Python library and CLI tool for identifying the language of source code snippets and files. It's fast, simple and accurate. [You can test it out here](http://jdkato.github.io/cypher/).

## Installation

## Usage

###### Python

```python
>>> from cypher import identify
>>> identify('fibs = 0 : 1 : zipWith (+) fibs (tail fibs)')
'Haskell'
>>> identify('from math import fabs')
'Python'
>>> identify("""
... pred_prey_euler <- function(a, b, h, x0, y0, const) {
...   n <- ((b - a) / h)
...   X <- Y <- T <- double(n + 1)
...   X[1] <- x0; Y[1] <- y0; T[1] <- a
...   for (i in 1:n) {
...     X[i + 1] <- X[i] + h * X[i] * (const[1] - const[2] * Y[i])
...     Y[i + 1] <- Y[i] + h * Y[i] * (const[4] * X[i] - const[3])
...     T[i + 1] <- T[i] + h
...   }
...   return(list("T" = T, "X" = X, "Y" = Y))
... }
... """)
'R'
>>>
```

###### Command line

```
$ cypher path/to/file
```

## Strategy

## Performance

| # of Files Tested | Time Per File (sec) | Average Accuracy | Lowest Score |
|:-----------------:|:-------------------:|:----------------:|:------------:|
|       16698       |        0.013        |       0.994      |  0.963 (C)   |

## Support

|   Language    |       Status          |
|:-----------:  |:------------------:   |
| AppleScript   |         :x:           |
|      C#       | :white_check_mark:    |
|     C++       | :white_check_mark:    |
|      C        | :white_check_mark:    |
|   Clojure     |         :x:           |
|      D        | :white_check_mark:    |
|    Erlang     |         :x:           |
|      Go       | :white_check_mark:    |
|   Groovy      | :x:                   |
|   Haskell     | :white_check_mark:    |
|     Java      | :white_check_mark:    |
|  JavaScript   |         :x:           |
|    Julia      |         :x:           |
|     Lisp      |         :x:           |
|     Lua       | :white_check_mark:    |
|    Matlab     |         :x:           |
|    OCaml      |         :x:           |
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
