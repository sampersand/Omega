import math
linebreak = '\n\r' #linebreak is used for comments
comment = '#'
allkeywords = {}
escape = '\\'
datadef = '@'
nbwhitespace = ' \t\x0b\x0c'
whitespace = nbwhitespace + linebreak
allquotes = '\'\"`'

# import re
# numre = re.compile(r'^(0[oxbOXB])?[\d.]+([eE]?[-+]?[\d.]+)?[ij]?$')
# strre = re.compile(r'(?s)\A([{}]).*\1\Z'.format(allquotes))
from obj import *#operobj, obj, methodobj,'',  numobj

escapechars = {'\\n': '\n',
               '\\t': '\t',
               '\\r': '\r',
               "\\'": '\'',
               '\\`': '`',
               '\\"': '\"',
               '\\\\':'\\',
               }
delims = {'arraysep':(',', operobj(',', 14)),
          'etc':('|', operobj('|', 14)),
          'endline':(';\n', operobj(';', 16)),
          'applier':(':', operobj(':', 0)),
          }

parens = {'l':'([{', 'r':')]}'}
allconsts = {
    'true' : boolobj(True),
    'false': boolobj(False),
    'null' : nullobj(True),
    'pi'   : floatobj(math.pi), 'π': floatobj(math.pi),
    'e'    : floatobj(math.e),
    'k'    : floatobj(8.987551787368e9),
    'imag' : complexobj(complex(0,1)),
    'nan'  : floatobj(float('nan')), 'NaN': floatobj(float('nan')),
    'inf'  : floatobj(float('inf')), '∞': floatobj(float('inf')),

    '½' : floatobj(1 / 2), '⅓' : floatobj(1 / 3), '⅔' : floatobj(2 / 3), '¼' : floatobj(1 / 4), '¾' : floatobj(3 / 4),
    '⅕' : floatobj(1 / 5), '⅖' : floatobj(2 / 5), '⅗' : floatobj(3 / 5), '⅘' : floatobj(4 / 5), '⅙' : floatobj(1 / 6),
    '⅚' : floatobj(5 / 6), '⅛' : floatobj(1 / 8), '⅜' : floatobj(3 / 8), '⅝' : floatobj(5 / 8), '⅞' : floatobj(7 / 8),
}
opers = {
    'binary':{
    #TODO: make assignment operators in here
        'math':{
            '**'  : operobj('**',     3), # power of
            '*'   : operobj('*',      4), # mult
            '/'   : operobj('/',      4), # div
            '%'   : operobj('%',      4), # mod
            '+'   : operobj('+',      5), # plus
            '-'   : operobj('-',      5), # minus
        },
        'bitwise':{
            'b<<' : operobj('b<<',    6), # bitwise <<
            'b>>' : operobj('b<<',    6), # bitwise >>
            'b&'  : operobj('b&',     7), # bitwise &
            'b^'  : operobj('b^',     8), # bitwise ^
            'b|'  : operobj('b|',     9), # bitwise |
        },
        'logic':{
            '<'   : operobj('<',     10), # less than
            '>'   : operobj('>',     10), # greater than
            '<='  : operobj('<=',    10), # less than or equal
            '>='  : operobj('>=',    10), # greater than or equal
            '=='  : operobj('==',    10), # equal to
            '='   : operobj('=',     10), # equal to
            '<>'  : operobj('<>',    10), # equal to
            '!='  : operobj('!=',    10), # not equal to
            '&&'  : operobj('&&',    11), # boolean and
            '||'  : operobj('||',    12), # booleon or
            },
        'assignment':{
            # all notes are in form of "x OPERATOR y" like 'x <- y'
            '<-'   : operobj('<-',   15), # x = y
            '<?-'  : operobj('<?-',  15), # x = bool(y) ? y : None
            '<+-'  : operobj('<+-',  15), # x += y
            '<--'  : operobj('<--',  15), # x -= y
            '<*-'  : operobj('<*-',  15), # x *= y
            '</-'  : operobj('</-',  15), # x /= y
            '<**-' : operobj('<**-', 15), # x **= y
            '<%-'  : operobj('<%-',  15), # x %= y
            '<&-'  : operobj('<&-',  15), # x &= y
            '<|-'  : operobj('<|-',  15), # x |= y
            '<^-'  : operobj('<^-',  15), # x ^= y
            '<<-'  : operobj('<<-',  15), # x <<= y
            '<>-'  : operobj('<>-',  15), # x >>= y
            #inverted assignment operators
            # all notes are in form of "x OPERATOR y" like 'x -> y'
            '->'   : operobj('->',   15), # y = x
            '-?>'  : operobj('-?>',  15), # y = bool(x) ? x : None
            '-+>'  : operobj('-+>',  15), # y += x
            '-->'  : operobj('-->',  15), # y -= x 
            '-*>'  : operobj('-*>',  15), # y *= x 
            '-/>'  : operobj('-/>',  15), # y /= x 
            '-**>' : operobj('-**>', 15), # y **= x 
            '-%>'  : operobj('-%>',  15), # y %= x 
            '-&>'  : operobj('-&>',  15), # y &= x 
            '-|>'  : operobj('-|>',  15), # y |= x 
            '-^>'  : operobj('-^>',  15), # y ^= x 
            '-<>'  : operobj('-<>',  15), # y <<= x 
            '->>'  : operobj('->>',  15)  # y >>= x 
            },
         },
    'unary':{
        'l':{
            '~'  :operobj('~',    1),
            'pos':operobj('pos',  1),
            'neg':operobj('neg',  1),
            '>+' :operobj('>+',   1),
            '>-' :operobj('>-',   1),
            },
        'r':{
            '!'  :operobj('!',    2),
            '+<' :operobj('+<',   2),
            '-<' :operobj('-<',   2),
            }
    }
}
funcs = {
    #reason this is a dict not a tuple is because later on some of these might be 1-line lambdas
    'if': methodobj('if'),
    'rm': methodobj('rm'),
    'om': methodobj('om'),
    'for': methodobj('for'),
    'disp': methodobj('disp'),
    'skip': methodobj('skip'), #ignore that line
    'func': methodobj('func'),
    'abort': methodobj('abort'),
    'whilst': methodobj('whilst'),
    'return': methodobj('return'),
}
for d in delims.values():
    for val in d[0]:
        opers['unary']['l'][val] = d[1]

alldelims = ''.join(v[0] for v in delims.values())
allparens = ''.join(list(parens.values())) + allquotes #yes, quotes are parens lol :P
import copy
#crap i need a better way than this D:
binopers = copy.copy(opers['binary']['math'])
binopers.update(opers['binary']['bitwise'])
binopers.update(opers['binary']['assignment'])
binopers.update(opers['binary']['logic'])
allopers = copy.copy(binopers)
allopers.update(opers['unary']['l'])
allopers.update(opers['unary']['r'])

allfuncs = copy.copy(allopers); allfuncs.update(funcs)
allkeywords = copy.copy(allfuncs); allkeywords.update(allconsts)
del copy

sortedopers = tuple(x for x in reversed(sorted(allopers.keys(), key = lambda l: len(l)))) #sorted by length

punctuation = '!#%&*+-/;<=>?@^|~' + allparens + alldelims + allquotes#stuff used to break apart things, ignoring ._$

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