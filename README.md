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
  - `###.###[j/i]` is a complex number (TODO).
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
- The complete list: Note that all of these have an inverse (`->`'s inverse is `<-`)
  - `A -> B ::= B = A`
  - `A -?> B ::= B = if A, then A, else B`
  - `A -+> B ::= B = B <plus> A`
  - `A --> B ::= B = B <minus> A`
  - `A -*> B ::= B = B <times> A`
  - `A -/> B ::= B = B <divided by> A`
  - `A -%> B ::= B = B <modulo> A`
  - `A -**> B ::= B = B <to the power of> A`
  - `A -&> B ::= B = B <bitwise AND> A`
  - `A -|> B ::= B = B <bitwise OR> A`
  - `A -^> B ::= B = B <bitwise XOR> A`
  - `A -<> B ::= B = B <bitwise left shift> A`
  - `A ->> B ::= B = B <bitwise right shift> A`

###Logic
- All of these but `&&` and `||` will return a boolean value.
- The complete list:
  - `A < B ::= A <less than>  B`
  - `A > B ::= A <greater than>  B`
  - `A <= B ::= A <less than or equal to> B`
  - `A >= B ::= A <greater than or equal to> B`
  - `A == B` and `A = B ::= A <is equal to> B`
  - `A != B` and `A <> B ::= A <is not equal to> B`
  - `A && B ::= if not A, then A, else B`
  - `A || B ::= if A, then A, else B`

###Math
- Normal arithmetic operations.
- The complete list:
  - `A + B ::= A <plus> B`
  - `A - B ::= A <minus> B`
  - `A * B ::= A <times> B`
  - `A / B ::= A <divided by>  B`
  - `A % B ::= A <modulo> B`
  - `A ** B ::= A to the power of  B`

###Bitwise
-Note that these all start with a 'b' to denote bitwise.
- The complete list:  
  - `A b<< B ::= A <bitwise shift left> B`
  - `A b>> B ::= A <bitwise shift right> B`
  - `A b& B ::= A <bitwise AND> B`
  - `A b| B ::= A <bitwise OR>  B`
  - `A b^ B ::= A <bitwise XOR>  B`

###Misc
- The complete list:
  - `A, B, C, ... ::= Array of [A, B, C, ...]`
  - `A; B; ... ::= execute A, then execute B, then execute ...`
  - `A : B : C : ... ::= pass B, C, ... to A`

##Unary

###Left
- The complete list:
  - `b~ A ::= <bitwise negate> A`
  - `pos A ::= +A`. Deprecated.
  - `neg A ::= -A`. Deprecated.
  - `>+ A ::= <increment> A <then set $ to> A`
  - `>- A ::= <decrement> A <then set $ to> A`

###Right
- The complete list:
  - `A ! ::= <factorial of> A`
  - `A +< ::= <set $ to> A <then increment A>`
  - `A -< ::= <set $ to> A <then decrement A>`

#In Built Functions
- `if_statement ::= "if" ":" <expression> ":" <statement(s) if true> [":" <statement(s) if false>]`
  - if `<expression>` evaluates to true, then `<statement(s) if true>` are executed. otherwise, if `<statement(s) if false>` is defined, then they are executed instead.
- `for_statement ::= "for" ":"( <initilization> ";" <condition> ";" <increment> ) ":" <statement(s)>`
  - First, `<initilization>` is executed. Then, `<condition>` is checked. If it is true, then `<statement(s)>` are executed, and `<increment>` is executed. 
- `whilst_statement ::= "whilst" ":" <condition> ":" <statement(s)>`
  - First, `<condition>` is checked. If it is true, then `<statement(s)>` are executed, and the loop is repeated.
- `disp_statement ::= "disp" [":" [<element(s) to display>] [":" [<seperator>] [":" [<endline>]]]]`
  - `<element to display>` defaults to ` `.
  - `<seperator>` defaults to `, `.
  - `<endline>` defaults to `\n'.
- `skip_statement ::= "skip"`
  - A null statement - when evaluated, nothing happens ('$' isn't even updated). eg, `if:(true):skip:(disp:'a')`.
- `abort_statement ::= "abort" [":" <quit message>]`
  - Stops the running of the program, and prints out `<quit message>` if it is supplied (or nothing if it isn't).
- `rm_statement ::= "rm" [":" <variable(s)>]`
  - If `<variable(s)>` is defined, then all variables are deleted. If `<variable(s)>` wasn't passed, then all variables are deleted.






























