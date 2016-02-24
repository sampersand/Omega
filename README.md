#General Notes
- Comments are multi-line. That is, when an unescaped `#` is found, no text will be registered until another unescaped `#` is found.
- Escape things with `\\`
- `@eof` will end the file at that position.<br>
- When a statement is needed, eg `if:statement: ...`, the statement can be either a single variable, or surrounded by parenthesis, eg `if:(statement): ...`.
- Watch out! stuff like `>1` is interpreted as `null>1`!.
#Variables
- See Assignment Operators for more information about how to assign variables.
- Define strings by surrounding them in a pair of quotes (`\`'"`), eg `'this is a string!'`.
  - Quotes can be escaped in strings to prevent them from ending.
- Define numbers by writing normal values, or prefixing them with special values.
  - `###` is an integer.
  - `###.###` or `###.###[e/E][-/+]###.###` is a float.
  - `###.###[j/i]` is a compled (TODO).
  - The prefixes in `-#` and `+#` are handled seperately.
  - `0[x/X]###` is for hexadecimal
  - `0[o/O]###` is for octodecimal
  - `0[b/B]###` is for binary
- Define arrays by seperating values with commas, eg `[a, b, c, ...]`.
- `$` is the last value evaluated. Can be helpful in certain circumstances, eg `if:function():$:null`.
#Operators

##Binary

###Assignment
- Use `<-` and `->` to assign values to variables. `A <- 9` and `9 -> A` are the _exact_ same.
- Just like assignment operators, "i" operators can go either direction. `A -+> B` is the same as `A + B -> B`.
- The complete list. Note that all of these have an inverse (`->`'s inverse is `<-`)
    - `A -> B`  ::= `B = A`.
    - `A -?> B` ::= `B = A ? A : B`.
    - `A -+> B` ::= `B = B +  A`.
    - `A --> B` ::= `B = B -  A`.
    - `A -*> B` ::= `B = B *  A`.
    - `A -/> B` ::= `B = B /  A`.
    - `A -** B` ::= `B = B ** A`.
    - `A -%> B` ::= `B = B %  A`.
    - `A -&> B` ::= `B = B &  A`.
    - `A -|> B` ::= `B = B |  A`.
    - `A -^> B` ::= `B = B ^  A`.
    - `A -<> B` ::= `B = B << A`.
    - `A ->> B` ::= `B = B >> A`.

###Logic
  - All of these but `&&` and `||` will return a boolean value.
  - The complete list.
    - `A <  B` ::= `A <  B`
    - `A >  B` ::= `A >  B`
    - `A <= B` ::= `A <= B`
    - `A >= B` ::= `A >= B`
    - `A == B` and `A = B` ::= `A == B`
    - `A != B` and `A <> B` ::= `A != B`
    - `A && B` ::= `If not A then A, else B`
    - `A || B` ::= `If A then A, else B`

###Math
  -  

    - `A  +  B` ::= `A  +  B`
    - `A  -  B` ::= `A  -  B`
    - `A  *  B` ::= `A  *  B`
    - `A  /  B` ::= `A  /  B`
    - `A  %  B` ::= `A  %  B`
    - `A **  B` ::= `A to the power of  B`
    - `A b<< B` ::= `A <bitwise shift left> B`
    - `A b>> B` ::= `A b>> B`
    - `A b&  B` ::= `A b&  B`
    - `A b^  B` ::= `A b^  B`
    - `A b|  B` ::= `A b|  B`
#In Built Functions
- `<if_statement> ::= if ":" <expression> ":" <statement(s) if true> [":" <statement(s) if false>]`
- `<for_statement> ::= for ":" <initilization> ":" <condition> ":" <increment condition> ":" <statement(s)>`
- `<disp_statement> ::= disp ":" [<element(s) to display>] [":" [<seperator>] [":" [<endline>]]]]`
  - `<element to display>` defaults to ` `.
  - `<seperator>` defaults to `, `.
  - `<endline>` defaults to `\n'.
- `skip`
  - When a statement is needed, this just skips it. eg, `if:(true):skip:(disp:'a')`.






























