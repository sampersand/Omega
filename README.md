#General Notes
<ul> Comments are multi-line. That is, when an unescaped '#' is found, no text will be registered until another unescaped '#' is found</ul>
<ul> ```$``` is the last value parsed.</ul>
<ul> Arrays are defined like ```[a, b, c, ...]```.</ul>
<ul> ```@eof``` will end the file at that position</ul>
##Assignment
<ul>a -> b</ul>
<ul>b <- a</ul>
<ul>a -+> b</ul>
<ul>b <+- a</ul>
<ul>...</ul>
##If statements
```<if_statement> ::= if <expression> ":" <statement(s) if true> [":" <statement(s) if false>] ";"```<br>
#####Notes:
<ul>The statements and expressions can be surrounded by parenthesis if needed.</ul>
##for statements
```<for_statement> ::= for <expression> ":" <statement(s) if true> [":" <statement(s) if false>] ";"```<br>
#####Notes:
<ul>The statements and expressions can be surrounded by parenthesis if needed.</ul>
<ul>Watch out! stuff like ```>1``` are interpreted as ```null>1```!.</ul>

#Operators
##Binary
###Assignment
<ul>```->```, ```<-```</ul>
<ul>```-+>```, ```<+-```</ul>
<ul>```-->```, ```<--```</ul>
<ul>```-*>```, ```<*-```</ul>
<ul>```-/>```, ```</-```</ul>