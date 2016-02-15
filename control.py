from omobj import oper, omobj, func
import math
from random import random
delims = {'arraysep':(',', oper(',', 14, None)),
          'etc':('|', oper('|', 14, None)),
          'endline':(';', oper(';', 14, lambda x, y: y))
          }
parens = {'l':'([{', 'r':')]}'}
consts = {
    'True': True,   'False': False,     'None' : None, 'Null' : None, 'Nil' : None,
    'true': True,   'false': False,     'none' : None, 'null' : None, 'nil' : None,
    'T': True, 'F': False, 'N':None, #these can be overriden
    't': True, 'f': False, 'n':None, #these can be overriden
    'pi': math.pi,  'PI': math.pi,      'π': math.pi,   'Π': math.pi,
    'e': math.e,    'E':  math.e,
    'k': 8.9875517873681764E9, 'K': 8.9875517873681764E9,
    'i': complex(0, 1), 'j':complex(0,1),
    'nan':float('nan'), 'NAN': float('nan'),
    'inf':float('inf'), '∞': float('inf'),
    'rand':random(),
    '½': 1 / 2,
    '⅓': 1 / 3,
    '⅔': 2 / 3,
    '¼': 1 / 4,
    '¾': 3 / 4,
    '⅕': 1 / 5,
    '⅖': 2 / 5,
    '⅗': 3 / 5,
    '⅘': 4 / 5,
    '⅙': 1 / 6,
    '⅚': 5 / 6,
    '⅐': 1 / 7,
    '⅛': 1 / 8,
    '⅜': 3 / 8,
    '⅝': 5 / 8,
    '⅞': 7 / 8,
    '⅑': 1 / 9,
    '⅒': 1/ 10,
}
opers = {
    'binary':{
        ':'   : oper(':',      0, None), # association
        '??'  : oper(':',      0, None), # association todo: remove
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
         },\
    'unary':{
        'l':{'~':oper('~', 1, lambda x, y: ~y),
             'pos':oper('pos', 1, lambda x, y: +y),
             'neg':oper('neg', 1, lambda x, y: -y)},
        'r':{'!':oper('!', 2, lambda x, y: not x)}
    }
}
for d in delims.values():
    for val in d[0]:
        opers['unary']['l'][val] = d[1]
funcs = {
    #reason this is a dict not a tuple is because later on some of these might be 1-line lambdas
    'if': func('if'),
    'for': func('for'),
    'disp': func('disp'),
    'abort': func('abort'),
    'displ': func('displ'),
    'dispc': func('dispc'), #commas bxn elements
}

linebreak = '\n\r' #linebreak is used for comments
comment = '#'
escape = '\\'
datadef = '@'
nbwhitespace = ' \t\x0b\x0c'
whitespace = nbwhitespace + linebreak

allquotes = '\'\"`'
alldelims = ''.join(v[0] for v in delims.values())
allparens = ''.join(list(parens.values())) + allquotes #yes, quotes are parens lol :P
import copy
#crap i need a better way than this D:
allopers = copy.copy(opers['binary']); allopers.update(opers['unary']['l']); allopers.update(opers['unary']['r'])
allfuncs = copy.copy(allopers); allfuncs.update(funcs)
del copy

sortedopers = tuple(x for x in reversed(sorted(allopers.keys(), key = lambda l: len(l)))) #sorted by length

punctuation = '!#$%&*+-/;<=>?@^|~' + allparens + alldelims + allquotes#stuff used to break apart things, ignoring ._

def _invertparen(paren):
    return {'(':')', ')':'(',
            '[':']', ']':'[',
            '{':'}', '}':'{'}[paren]

def _doFunc(eles, locls, funcname):
    if 'disp' in funcname:
        if __debug__:
            if len(eles) != 0:
                assert eles[0].basestr == funcname, 'this shouldn\'t break'
        if len(eles) == 0:
            print(end = '' if funcname == 'disp' else '\n')
        elif len(eles[1]) == 0:
            eles[1].eval(locls)
            print(locls['$'],end = '' if funcname == 'disp' else '\n')
        elif funcname == 'disp':
            for ele in eles[1]:
                ele.eval(locls)
                print(locls['$'], end = '')
        elif funcname == 'displ':
            for ele in eles[1]:
                ele.eval(locls)
                print(locls['$'], end = '\n')
        elif funcname == 'dispc':
            for ele in eles[1]:
                ele.eval(locls)
                print(locls['$'], end = ', ' if ele is not eles[1][-1] else '\n')
    elif funcname == 'abort':
        if len(eles) == 0:
            locls['$'] = ''
        else:
            if __debug__:
                assert eles[0].basestr == funcname, 'this shouldn\'t break'
            eles[1].eval(locls)
        if __debug__:
            assert '$' in locls
        quit('Aborting!' + ('' if locls['$'] == '' else ' Message: \'{}\''.format(str(locls['$']))))
    elif funcname == 'if':
        if __debug__:
            assert eles[0].basestr == funcname, 'this shouldn\'t break'
            assert len(eles) in (3, 4), 'can only have if:(cond):(if true)[:(if false)];'
        eles[1].eval(locls) # evaluates the condition
        if locls['$']:
            eles[2].eval(locls)
        elif len(eles) == 4:
            eles[3].eval(locls)
    elif funcname == 'for':
        if __debug__:
            assert eles[0].basestr == funcname, 'this shouldn\'t break'
            assert len(eles) == 3, 'can only have for:(...):{ expression };'
            assert len(eles[1]) == 3, 'can only have (initialize; condition; increment)'
        eles[1][0].eval(locls) # initializes the for loop the condition
        while True:
            eles[1][1].eval(locls) #check the conditoin
            if not locls['$']:
                break
            eles[2].eval(locls)
            eles[1][2].eval(locls) #increment
    else:
        raise SyntaxError('function \'{}\' isn\'t defined yet!'.format(funcname))

def _specialoper(eles, locls):
    from group import group
    name = eles.basestr
    if name in alldelims:
        if name in delims['arraysep']:
            eles[0].eval(locls)
            ret = []
            name = eles.basestr
            for ele in eles:
                ele.eval(locls)
                ret.append(locls['$'])
            locls['$'] = group(val = ret)# x = y
            return
        else:
            raise SyntaxError('Special Operator \'{}\' isn\'t defined yet!'.format(name))
    elif name == ':':
        if eles[0].base in alldelims:
            assert 0, str(eles) + " | " + eles[0]
        if eles[0].base in locls:
            locls[eles[0].base].eval(eles[1])
        else:
            if __debug__:
                assert eles[0].base in funcs, 'no way to proccess function \'{}\''.format(eles[0].base)
            funcs[eles[0].base](eles, locls)
    elif name == '||' or name == '&&':
        eles[0].eval(locls)
        element = locls['$']
        if name == '&&' and not element or name == '||' and element:
            return element
        eles[1].eval(locls)
        locls['$'] = (element or locls['$']) if name == '&&' else (element and locls['$'])
    else:
        direc = name in ['<-', '<?-', '<+-', '<--', '<*-', '</-', '<**-', '<%-', '<&-', '<|-', '<^-', '<<-', '<>-']
        if direc == 1:
            eles[1].eval(locls)
            value =locls['$']
            key = eles[0].base
        else:
            eles[0].eval(locls)
            value =locls['$']
            key = eles[1].base
        if __debug__:
            assert name == '<-'  or\
                   name == '->'  or\
                   name == '<?-' or\
                   name == '-?>' or\
                   key in locls, '\'{}\' needs to be defined to perform \'{}\' on it!'.format(key, name)
            if   name == '<-'   or name == '->'  : locls[key] = value
            elif name == '<?-'  or name == '-?>' :
                locls[key] = value if value else (locls[key] if key in locls else None)
            elif name == '<+-'  or name == '-+>' : locls[key] += value
            elif name == '<--'  or name == '-->' : locls[key] = value
            elif name == '<*-'  or name == '-*>' : locls[key] = value
            elif name == '</-'  or name == '-/>' : locls[key] = value
            elif name == '<**-' or name == '-**>': locls[key] = value
            elif name == '<%-'  or name == '-%>' : locls[key] = value
            elif name == '<&-'  or name == '-&>' : locls[key] = value
            elif name == '<|-'  or name == '-|>' : locls[key] = value
            elif name == '<^-'  or name == '-^>' : locls[key] = value
            elif name == '<<-'  or name == '-<>' : locls[key] = value
            elif name == '<>-'  or name == '->>' : locls[key] = value
        if direc == 0: #swap the return value
            locls['$'] = locls[key]

def evaloper(eles, locls):
    if eles.base not in allopers:
        raise SyntaxError('operator \'{}\' isn\'t defined'.format(eles.base))
    oper = allopers[eles.base]
    if oper.func == None:
        _specialoper(eles, locls)
    elif eles:
        eles[0].eval(locls)
        ret = locls['$']
        name = eles.base
        for ele in eles[1:]:
            ele.eval(locls)
            ret = allopers[name].func(ret, locls['$'])
        locls['$'] = ret# x = y

def applyrules(tokens):
    print(tokens)
    if __debug__:
        assert tokens[0] == '@'
        assert tokens[1] == 'define', tokens[1] #currently, only 'define' is defined.
    assert 0, 'not implemented yet! todo: this'
    # fixedtokens = 

def _getomobj(base):
    if __debug__:
        if not isinstance(base, str):
            print('warning: \'{}\' isnt not a string'.format(repr(base)))
    # print("_getomobj: '{} ({})' ({})".format(\
    #         allfuncs[base] if base in allfuncs else omobj(base),
    #         type(allfuncs[base] if base in allfuncs else omobj(base)),
    #         base in allfuncs), type(allfuncs[';']))
    return allfuncs[base] if base in allfuncs else omobj(base)
