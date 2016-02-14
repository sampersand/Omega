#General Notes
<ul> Comments are multi-line. That is, when an unescaped '#' is found, no text will be registered until another unescaped '#' is found</ul>
#Assignment
<ul>a -> b</ul>
<ul>b <- a</ul>
<ul>a -+> b</ul>
<ul>b <+- a</ul>
<ul>...</ul>
#If statements
```<if_statement> ::= if <expression> ":" <statement(s) if true> [":" <statement(s) if false>] ";"```<br>
#####Notes:
<ul>The statements and expressions can be surrounded by parenthesis if needed.</ul>
<ul>To seperate multiple lines in if statements, use ``,``.</ul>