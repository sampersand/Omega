from omobj import oper, omobj, func
import math
from random import random
linebreak = '\n\r' #linebreak is used for comments
comment = '#'
allkeywords = {}
escape = '\\'
datadef = '@'
nbwhitespace = ' \t\x0b\x0c'
whitespace = nbwhitespace + linebreak
allquotes = '\'\"`'

delims = {'arraysep':(',', oper(',', 14)),
          'etc':('|', oper('|', 14)),
          'endline':(';', oper(';', 14))
          }
parens = {'l':'([{', 'r':')]}'}
consts = {
    'True'  : omobj(True),          'False' : omobj(False),     'None'  : omobj(None),
    'true'  : omobj(True),          'false' : omobj(False),     'none'  : omobj(None),
#    'T'     : omobj(True),          'F'     : omobj(False),     'N'     : omobj(None), #can be overode
#    't'     : omobj(True),          'f'     : omobj(False),     'n'     : omobj(None), #can be overode
    'pi'    : omobj(math.pi),       'π'     : omobj(math.pi),   'e'     : omobj(math.e),
    'k'     : omobj(8.987551787368e9),'imag': omobj(complex(0, 1)),
    'rand'  : omobj(None, random()), 'nan'  : omobj(float('nan')), 'NaN': omobj(float('nan')),
    'inf'   : omobj(float('inf')),  '∞'     : omobj(float('inf')),

    '½' : omobj(1 / 2), '⅓' : omobj(1 / 3), '⅔' : omobj(2 / 3), '¼' : omobj(1 / 4), '¾' : omobj(3 / 4),
    '⅕' : omobj(1 / 5), '⅖' : omobj(2 / 5), '⅗' : omobj(3 / 5), '⅘' : omobj(4 / 5), '⅙' : omobj(1 / 6),
    '⅚' : omobj(5 / 6), '⅛' : omobj(1 / 8), '⅜' : omobj(3 / 8), '⅝' : omobj(5 / 8), '⅞' : omobj(7 / 8),
}
opers = {
    'binary':{
        ':'   : oper(':',      0, None), # association
        '**'  : oper('**',     3, lambda x, y: x ** y), # power of
        '*'   : oper('*',      4, lambda x, y: x *  y), # mult
        '/'   : oper('/',      4, lambda x, y: x /  y), # div
        '%'   : oper('%',      4, lambda x, y: x %  y), # mod
        '+'   : oper('+',      5, lambda x, y: x +  y), # plus
        '-'   : oper('-',      5, lambda x, y: x -  y), # minus
        'b<<' : oper('b<<',    6, lambda x, y: x << y), # bitwise <<
        'b>>' : oper('b<<',    6, lambda x, y: x >> y), # bitwise >>
        'b&'  : oper('b&',     7, lambda x, y: x &  y), # bitwise &
        'b^'  : oper('b^',     8, lambda x, y: x ^  y), # bitwise ^
        'b|'  : oper('b|',     9, lambda x, y: x |  y), # bitwise |
        '<'   : oper('<',     10, lambda x, y: x <  y), # less than
        '>'   : oper('>',     10, lambda x, y: x >  y), # greater than
        '<='  : oper('<=',    10, lambda x, y: x <= y), # less than or equal
        '>='  : oper('>=',    10, lambda x, y: x >= y), # greater than or equal
        '=='  : oper('==',    10, lambda x, y: x == y), # equal to
        '='   : oper('=',     10, lambda x, y: x == y), # equal to
        '<>'  : oper('<>',    10, lambda x, y: x != y), # equal to
        '!='  : oper('!=',    10, lambda x, y: x != y), # not equal to
        '&&'  : oper('&&',    11, None), # boolean and
        '||'  : oper('||',    12, None), # booleon or
        #assignment operators
        # all notes are in form of "x OPERATOR y" like 'x <- y'
        '<-'   : oper('<-',   13, None), # x = y
        '<?-'  : oper('<?-',  13, None), # x = bool(y) ? y : None
        '<+-'  : oper('<+-',  13, None), # x += y
        '<--'  : oper('<--',  13, None), # x -= y
        '<*-'  : oper('<*-',  13, None), # x *= y
        '</-'  : oper('</-',  13, None), # x /= y
        '<**-' : oper('<**-', 13, None), # x **= y
        '<%-'  : oper('<%-',  13, None), # x %= y
        '<&-'  : oper('<&-',  13, None), # x &= y
        '<|-'  : oper('<|-',  13, None), # x |= y
        '<^-'  : oper('<^-',  13, None), # x ^= y
        '<<-'  : oper('<<-',  13, None), # x <<= y
        '<>-'  : oper('<>-',  13, None), # x >>= y
        #inverted assignment operators
        # all notes are in form of "x OPERATOR y" like 'x -> y'
        '->'   : oper('->',   13, None), # y = x
        '-?>'  : oper('-?>',  13, None), # y = bool(x) ? x : None
        '-+>'  : oper('-+>',  13, None), # y += x
        '-->'  : oper('-->',  13, None), # y -= x 
        '-*>'  : oper('-*>',  13, None), # y *= x 
        '-/>'  : oper('-/>',  13, None), # y /= x 
        '-**>' : oper('-**>', 13, None), # y **= x 
        '-%>'  : oper('-%>',  13, None), # y %= x 
        '-&>'  : oper('-&>',  13, None), # y &= x 
        '-|>'  : oper('-|>',  13, None), # y |= x 
        '-^>'  : oper('-^>',  13, None), # y ^= x 
        '-<>'  : oper('-<>',  13, None), # y <<= x 
        '->>'  : oper('->>',  13, None)  # y >>= x 
         },
    'unary':{
        'l':{'~':oper('~', 1, lambda x, y: ~y),
             'pos':oper('pos', 1, lambda x, y: +y),
             'neg':oper('neg', 1, lambda x, y: -y)},
        'r':{'!':oper('!', 2, lambda x, y: not x)}
    }
}
funcs = {
    #reason this is a dict not a tuple is because later on some of these might be 1-line lambdas
    'if': func('if'),
    'for': func('for'),
    'disp': func('disp'),
    'abort': func('abort'),
    'displ': func('displ'),
    'dispc': func('dispc'), #commas bxn elements
    'skip': func('skip'), #commas bxn elements
}

for d in delims.values():
    for val in d[0]:
        opers['unary']['l'][val] = d[1]

alldelims = ''.join(v[0] for v in delims.values())
allparens = ''.join(list(parens.values())) + allquotes #yes, quotes are parens lol :P
import copy
#crap i need a better way than this D:
allopers = copy.copy(opers['binary']); allopers.update(opers['unary']['l']); allopers.update(opers['unary']['r'])
allfuncs = copy.copy(allopers); allfuncs.update(funcs)
allkeywords = copy.copy(allfuncs); allkeywords.update(consts)
del copy

sortedopers = tuple(x for x in reversed(sorted(allopers.keys(), key = lambda l: len(l)))) #sorted by length

punctuation = '!#$%&*+-/;<=>?@^|~' + allparens + alldelims + allquotes#stuff used to break apart things, ignoring ._

def _invertparen(paren):
    return {'(':')', ')':'(',
            '[':']', ']':'[',
            '{':'}', '}':'{'}[paren]


def applyrules(tokens):
    print(tokens)
    if __debug__:
        assert tokens[0] == '@'
        assert tokens[1] == 'define', tokens[1] #currently, only 'define' is defined.
    assert 0, 'not implemented yet! todo: this'
    # fixedtokens = 