EXTRACT_RE = r"""
    NS| # Objective-C, Swift
    [@|#]?[\w]+[\(|!]?|
    \}\)| # Swift
    \$\(| # JavaScript
    \+\+| # Scala
    :::| # Scala
    ::~| # C++
    ::| # C++, Haskell, Ruby, R, PHP
    =>| # C#, Rust, PHP
    <<(?!-)| # C++
    >>| # C++
    :$| # Python
    <-| # Haskell, R
    ->| # Haskell, Rust, PHP, OCaml, Swift
    !!| # Haskell
    <<-| # R
    {-| # Haskell
    :=| # Go, OCaml
    <%| # Ruby
    %w| # Ruby
    ===| # PHP, JavaScript
    !==| # PHP, JavaScript
    \s\.\s| # PHP, Perl
    &&| # PHP
    =~| # Perl
    ~=| # Lua
    !\(| # Rust
    \[\]| # Java
    \.\.\.| # R, Swift
    \.\.| # Haskell
    \(\)| # Haskell, OCaml, JavaScript
    \$_| # PHP
    \#\[| # Rust
    1;| # Perl
    ;;| # OCaml
    \?\?\?| # Scala
    [~.@!?;:&\{\}\[\]\\#\/\|%\$`\*\)\(-,+]
"""
BLOCK_IGNORES = {
    "/*": [r"\/\*.*$", r".*\*\/$"],
    "/+": [r"\/\+.*$", r".*\+\/$"],
    "(*": [r"\(\*[^)]*$", r".*\*\)$"],
    "'''": [r"[\']{3}.*$", r".*[\']{3}$"],
    '"""': [r"[\"]{3}.*$", r".*[\"]{3}$"],
    "{-": [r"^{-.*$", r"^.*-}$"],
    "=": [r"^=[^#]*$", r"^=.*$"],
    "--[[": [r"^-{2,}\[{1,3}(.*)?$", r"^-{2,}\]{1,3}(.*)?$"],
    'r#"': [r'.*r#".*', r'\s*"#.*']
}
STRING_RE = r"(?<!'|\")('|\")[^'\"]*\1(?!'|\")"
INLINE_COMMENTS = {
    "/*": r"/\*.*\*/",
    "(*": r"\(\*.*\*\)",
    "/+": r"/\+.*\+/",
    "{-": r"{-.*-}",
    "#": r"(?<!{-)(?<!r)#(?!-}).*",
    "//": r"\/\/.*",
    "--": r"(?<!\w)--.*"
}
INLINE_STRINGS = {
    "'''": r"'{3}.*'{3}",
    '"""': r'"{3}.*"{3}',
    '"': r"(?<!\")(?<!include\s)(?<!import\s)(?<!require\s)\"[^\"]*\"(?!\")",
    "'": r"(?<!')(?<!require\s)(')[^']*\1(?!')",
    "`": r"(?<!`)(`)[^']+\1(?!`)",
    r"%w[": r"%w\[[^\]]+\]"
}
INLINE_EXCEPTIONS = {
    "#": [
        # C/C++
        r"^\s*#(include|define|undef|if|elif|else|endif|error|line)",
        # Objective-C
        r"^\s*#(import|pragma)",
        # C#
        r"^\s*#(region|endregion|warning)",
        # Rust
        r"^\s*#(!|\[)",
        # Lua
        r"#stdout",
        # Swift
        r"#available",
        # Lua `#` operator
        r"(?<!r)#([^\s\-#]{1,}$|.{1,}do\n?$|[^\s]*,.*\)|[^\s]{1,}\s==)",
        r"\(#.*\)"
    ],
    "--": [
        # Perl `... --;`
        r".*\s--((@|\$|%).*)?;"
    ]
}
FILE_TERMINATORS = [
    r"^1;$"
]
