# cypher

[![Build Status](https://travis-ci.org/jdkato/cypher.svg?branch=master)](https://travis-ci.org/jdkato/cypher) [![Coverage Status](https://coveralls.io/repos/github/jdkato/cypher/badge.svg?branch=master)](https://coveralls.io/github/jdkato/cypher?branch=master) [![Code Health](https://landscape.io/github/jdkato/cypher/master/landscape.svg?style=flat)](https://landscape.io/github/jdkato/cypher/master)


[`cypher`](https://en.wikipedia.org/wiki/Cypher_(Marvel_Comics)) is a Python library that can identify the language of source code snippets and files. [You can test it out here](http://jdkato.github.io/cypher/).

## Installation

## Usage

```python
>>> import cypher
>>> cypher.identify('fibs = 0 : 1 : zipWith (+) fibs (tail fibs)')
'Haskell'
>>>
```

## Strategy

## Support

|   Language    |       Status          |      Unit tests   | Base Project (% identified)   |
|:-----------:  |:------------------:   |:---------------:  |:---------------------------:  |
|     ASP       |         :x:           |        0          |                               |
| AppleScript   |         :x:           |        0          |                               |
|      C#       | :white_check_mark:    |        10         | [Nancy](https://github.com/NancyFx/Nancy.git) (0.995)                             |
|     C++       | :white_check_mark:    |        11         | [Electron](https://github.com/apple/swift) (0.973)          |
|      C        | :white_check_mark:    |        10         | [Git](https://github.com/git/git) (0.962)            |
|     CSS       |         :x:           |        0          |                               |
|   Clojure     |         :x:           |        0          |                               |
|      D        |         :x:           |        0          |                               |
|    Erlang     |         :x:           |        0          |                               |
|      Go       | :white_check_mark:    |        10         | [Lantern](https://github.com/getlantern/lantern.git) (1.00)                              |
|     HTML      |         :x:           |        0          |                               |
|   Haskell     | :white_check_mark:    |        10         | [Cabal](https://github.com/haskell/cabal) (0.995)          |
|     Java      | :white_check_mark:    |        10         | [Spring](https://github.com/spring-projects/spring-framework.git) (1.00)                              |
|  JavaScript   |         :x:           |        0          |                               |
|    LaTeX      |         :x:           |        0          |                               |
|     Lisp      |         :x:           |        0          |                               |
|     Lua       |         :x:           |        0          |                               |
|   Markdown    |         :x:           |        0          |                               |
|    Matlab     |         :x:           |        0          |                               |
|    OCaml      |         :x:           |        0          |                               |
| Objective-C   | :white_check_mark:    |        10         | [Adium](https://github.com/adium/adium.git) (0.993)                             |
|     Perl      | :white_check_mark:    |        10         | [Mojolicious](https://github.com/kraih/mojo) (1.00)                          |
|     PHP       | :white_check_mark:    |        10         | [WordPress](https://github.com/WordPress/WordPress) (1.00) |
|    Python     | :white_check_mark:    |        11         | [Django](https://github.com/django/django) (0.982)            |
|      R        | :white_check_mark:    |        11         | [Shiny](https://github.com/rstudio/shiny) (0.964)             |
|     Ruby      | :white_check_mark:    |        10         | [Ruby on Rails](https://github.com/rails/rails) (0.990)          |
|     Rust      | :white_check_mark:    |        10         | [Cargo](https://github.com/rust-lang/cargo.git) (1.00)    |
|    Scala      |         :x:           |        0          |                               |
|    Swift      |         :x:           |        0          |                               |
|     XML       |         :x:           |        0          |                               |
