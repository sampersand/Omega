assignment:
    a -> b
    b <- a
    a -+> b
    b <+- a
    ect, etc...
if statements:
    <if_statement> ::= if <expression> <b>:</b>
                            [<left_paren>] <statement(s) if true> [<right_paren>]
                        [:  [<left_paren>] <statement(s) if false> [<right_paren>]]
    whitespace doesn't matter
