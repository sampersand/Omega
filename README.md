# Omega
This was my very original programming language. It's a bit rough around the edges, as I didn't really know what I was doing.

## Why so many colons
Because I didn't know what an AST was, I devised a special way to parse things: the colon, or as it's called internally, `applier`.
Each sequential `:` indicates that more arguments should be passed to the first value. So for `if:(foo):{bar}:{baz}`, this is running the 
internal `if` function with the arguments `(foo)`, `{bar}`, and `{baz}`. Not great, but it's a workaround.
