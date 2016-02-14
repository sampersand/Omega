class oper:
    def __init__(self, value, priority, func):
        self.value = value
        self.priority = priority
        self.func = func
    def __repr__(self):
        return 'oper({},{},{})'.format(self.value, self.priority, self.func)
    def __str__(self):
        return self.value
    def __lt__(self, other):
        return self.priority < other.priority

class group(list):
    def __new__(self, val = '', args = [], parens = ('','')):
        return super().__new__(self, args)

    def __init__(self, val = '', args = [], parens = ('','')):
        super().__init__(args)
        if __debug__:
            assert type(val) == str, val
            assert type(args) == list, str(args) + str(type(args))
            assert type(parens) == tuple, str(parens) + str(type(parens))
            assert len(parens) == 2, parens
        self.val = val
        self.parens = parens
    def hasparens(self):
        return bool(self.parens[0] or self.parens[1])

    def __repr__(self):
        ret = 'group('
        if self.val:
            ret += 'val = ' + repr(self.val) + ', '
        if self:
            ret += 'args = ' + super().__repr__() + ', '
        if self.hasparens():
            ret += 'parens = ' + repr(self.parens)
        if not self.hasparens() and (self.val or self):
            ret = ret[:-2]
        return ret + ')'

    def __str__(self):
        if not self:
            return ''.join((str(self.parens[0]), str(self.val), str(self.parens[1])))
        if self.val in control.opers['binary']:
            if __debug__:
                assert len(self) == 2, repr(self)
                assert len(self.parens) == 2, repr(self)
            return ''.join((str(self.parens[0]), str(self[0]), str(self.val), str(self[1]), str(self.parens[1])))
        return ''.join((str(self.val), str(self.parens[0]), ', '.join(str(x) for x in self), str(self.parens[1])))
    def eval(self, locls):
        # print(self.val, self.val in control.funcs)
        if self.val in control.allopers:
            control.allopers[self.val].func(self, locls)
        elif self.val in control.funcs:
            control.funcs[self.val](self, locls)
        else:
            if self.val == '':
                if __debug__:
                    assert len(self) == 1 #expects 1 element (in parens)
                self[0].eval(locls)
            elif self.val in locls:
                locls['$'] = locls[self.val]
            else:
                if self.val in control.consts:
                    locls['$'] = control.consts[self.val]
                else:
                    try:
                        locls['$'] = int(self.val)
                    except ValueError:
                        try:
                            locls['$'] = float(self.val)
                        except ValueError:
                            try:
                                locls['$'] = complex(self.val)
                            except ValueError:
                                raise SyntaxError('No known way to deal with \'{}\''.format(self.val))
class control:
    import math
    from random import random
    linebreak = '\n\r' #linebreak is used for comments
    endline = ';' #used to seperate lines
    # endline = '\n\r;'
    comment = '#'
    escape = '\\'
    nbwhitespace = ' \t\x0b\x0c'
    whitespace = nbwhitespace + linebreak
    parens = {'l':'([{',
              'r':')]}'}
    allparens = ''.join(list(parens.values()))
    alldelims = ',|'
    punctuation = '!"#$%&\'*+-/;<=>?@\\^`|~' + allparens + alldelims#stuff used to break apart things, ignoring ._
    consts = {
        'true': True,   'false': False,     'none' : None, 'null' : None, 'nil' : None,
        'T': True, 'F': False, 'N':None, #these can be overriden
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
            ':'  : oper(':',     0, lambda eles, locls: control._doOper(eles, locls, '@:')), # association
            '**'  : oper('**',     3, lambda eles, locls: control._doOper(eles, locls, '**' )), # power of
            '*'   : oper('*',      4, lambda eles, locls: control._doOper(eles, locls, '*'  )), # mult
            '/'   : oper('/',      4, lambda eles, locls: control._doOper(eles, locls, '/'  )), # div
            '%'   : oper('%',      4, lambda eles, locls: control._doOper(eles, locls, '%'  )), # mod
            '+'   : oper('+',      5, lambda eles, locls: control._doOper(eles, locls, '+'  )), # plus
            '-'   : oper('-',      5, lambda eles, locls: control._doOper(eles, locls, '-'  )), # minus
            'b<<' : oper('b<<',    6, lambda eles, locls: control._doOper(eles, locls, 'b<<')), # bitwise <<
            'b>>' : oper('b<<',    6, lambda eles, locls: control._doOper(eles, locls, 'b>>')), # bitwise >>
            'b&'  : oper('b&',     7, lambda eles, locls: control._doOper(eles, locls, 'b&' )), # bitwise &
            'b^'  : oper('b^',     8, lambda eles, locls: control._doOper(eles, locls, 'b^' )), # bitwise ^
            'b|'  : oper('b|',     9, lambda eles, locls: control._doOper(eles, locls, 'b|' )), # bitwise |
            '<'   : oper('<',     10, lambda eles, locls: control._doOper(eles, locls, '<'  )), # less than
            '>'   : oper('>',     10, lambda eles, locls: control._doOper(eles, locls, '>'  )), # greater than
            '<='  : oper('<=',    10, lambda eles, locls: control._doOper(eles, locls, '<=' )), # less than or equal
            '>='  : oper('>=',    10, lambda eles, locls: control._doOper(eles, locls, '>=' )), # greater than or equal
            '=='  : oper('==',    10, lambda eles, locls: control._doOper(eles, locls, '==' )), # equal to
            '='   : oper('=',     10, lambda eles, locls: control._doOper(eles, locls, '='  )), # equal to
            '!='  : oper('!=',    10, lambda eles, locls: control._doOper(eles, locls, '!=' )), # not equal to
            '&&'  : oper('&&',    11, lambda eles, locls: control._doOper(eles, locls, '@and')), # boolean and
            '||'  : oper('||',    12, lambda eles, locls: control._doOper(eles, locls, '@or')), # booleon or
            #assignment operators
            # all notes are in form of "x OPERATOR y" like 'x <- y'
            '<-'   : oper('<-',   13, lambda eles, locls: control._doOper(eles, locls, '@<-')), # x = y
            '<?-'  : oper('<?-',  13, lambda eles, locls: control._doOper(eles, locls, '@<?-')), # x = bool(y) ? y : None
            '<+-'  : oper('<+-',  13, lambda eles, locls: control._doOper(eles, locls, '@<+-')), # x += y
            '<--'  : oper('<--',  13, lambda eles, locls: control._doOper(eles, locls, '@<--')), # x -= y
            '<*-'  : oper('<*-',  13, lambda eles, locls: control._doOper(eles, locls, '@<*-')), # x *= y
            '</-'  : oper('</-',  13, lambda eles, locls: control._doOper(eles, locls, '@</-')), # x /= y
            '<**-' : oper('<**-', 13, lambda eles, locls: control._doOper(eles, locls, '@<**-')), # x **= y
            '<%-'  : oper('<%-',  13, lambda eles, locls: control._doOper(eles, locls, '@<%-')), # x %= y
            '<&-'  : oper('<&-',  13, lambda eles, locls: control._doOper(eles, locls, '@<&-')), # x &= y
            '<|-'  : oper('<|-',  13, lambda eles, locls: control._doOper(eles, locls, '@<|-')), # x |= y
            '<^-'  : oper('<^-',  13, lambda eles, locls: control._doOper(eles, locls, '@<^-')), # x ^= y
            '<<-'  : oper('<<-',  13, lambda eles, locls: control._doOper(eles, locls, '@<<-')), # x <<= y
            '<>-'  : oper('<>-',  13, lambda eles, locls: control._doOper(eles, locls, '@<>-')), # x >>= y
            #inverted assignment operators
            # all notes are in form of "x OPERATOR y" like 'x -> y'
            '->'   : oper('->',   13, lambda eles, locls: control._doOper(eles, locls, '@->' )), # y = x
            '-?>'  : oper('-?>',  13, lambda eles, locls: control._doOper(eles, locls, '@-?>')), # y = bool(x) ? x : None
            '-+>'  : oper('-+>',  13, lambda eles, locls: control._doOper(eles, locls, '@-+>')), # y += x
            '-->'  : oper('-->',  13, lambda eles, locls: control._doOper(eles, locls, '@-->')), # y -= x 
            '-*>'  : oper('-*>',  13, lambda eles, locls: control._doOper(eles, locls, '@-*>')), # y *= x 
            '-/>'  : oper('-/>',  13, lambda eles, locls: control._doOper(eles, locls, '@-/>')), # y /= x 
            '-**>' : oper('-**>', 13, lambda eles, locls: control._doOper(eles, locls, '@-**>')), # y **= x 
            '-%>'  : oper('-%>',  13, lambda eles, locls: control._doOper(eles, locls, '@-%>')), # y %= x 
            '-&>'  : oper('-&>',  13, lambda eles, locls: control._doOper(eles, locls, '@-&>')), # y &= x 
            '-|>'  : oper('-|>',  13, lambda eles, locls: control._doOper(eles, locls, '@-|>')), # y |= x 
            '-^>'  : oper('-^>',  13, lambda eles, locls: control._doOper(eles, locls, '@-^>')), # y ^= x 
            '-<>'  : oper('-<>',  13, lambda eles, locls: control._doOper(eles, locls, '@-<>')), # y <<= x 
            '->>'  : oper('->>',  13, lambda eles, locls: control._doOper(eles, locls, '@->>'))  # y >>= x 
             },\
        'unary':{
            'l':{'~':oper('~', 1, lambda x: None)},
            'r':{'!':oper('!', 2, lambda x: None)}
        }
    }
    funcs = {
        'if': lambda eles, locls: control._doFunc(eles, locls, 'if'),
        'for': lambda eles, locls: control._doFunc(eles, locls, 'for'),
        'disp': lambda eles, locls: control._doFunc(eles, locls, 'disp'),
    }
    allopers = opers['binary']; allopers.update(opers['unary']['l']); allopers.update(opers['unary']['r'])
    sortedopers = tuple(x for x in reversed(sorted(allopers.keys(), key = lambda l: len(l)))) #sorted by length

    @staticmethod
    def _doFunc(eles, locls, funcname):
        if __debug__:
            assert eles[0].val == funcname, 'this shouldn\'t break'
            assert eles.val == ':', 'this shouldn\'t break!'
        if funcname == 'disp':
            eles[1].eval(locls)
            print(locls['$'])
        elif funcname == 'if':
            if __debug__:
                assert len(eles[1]) == 2, 'this shouldn\'t break!' #should be CONDITION, VALUE
                assert eles[1].val == ':', 'this shouldn\'t break!'
            eles[1][0].eval(locls) # evaluates the condition
            if locls['$']:
                eles[1][1][0].eval(locls)
            elif len(eles[1][1]) == 2:
                eles[1][1][1].eval(locls)
        elif funcname == 'for':
            if __debug__:
                assert len(eles[1]) == 2, 'this shouldn\'t break!' #should be CONDITION, VALUE
                assert eles[1].val == ':', 'this shouldn\'t break!'
            eles[1][0].eval(locls) # evaluates the condition
            if locls['$']:
                eles[1][1][0].eval(locls)
            elif len(eles[1][1]) == 2:
                eles[1][1][1].eval(locls)

        else:
            raise SyntaxError('function \'{}\' isn\'t defined yet!'.format(funcname))
    @staticmethod
    def _doOper(eles, locls, funcname):
        if funcname[0] == '@':
            funcname = funcname[1:]
            if funcname == ':':
                if __debug__:
                    assert eles[0].val in control.funcs, 'no way to proccess function \'{}\''.format(eles[0].val)
                control.funcs[eles[0].val](eles, locls)
            elif funcname == 'or' or funcname == 'and':
                eles[0].eval(locls)
                element = locls['$']
                eles[1].eval(locls)
                locls['$'] = (element or locls['$']) if funcname == 'or' else (element and locls['$'])
            else:
                # if funcname in ['<-', '->', '<?-', '->':
                if funcname in ['<-', '<?-', '<+-', '<--', '<*-', '</-', '<**-', '<%-', '<&-', '<|-', '<^-', '<<-', '<>-']:
                    eles[1].eval(locls)
                    value =locls['$']
                    key = eles[0].val
                else:
                    eles[0].eval(locls)
                    value =locls['$']
                    key = eles[1].val

                if __debug__:
                    assert funcname == '<-'  or\
                           funcname == '->'  or\
                           funcname == '<?-' or\
                           funcname == '-?>' or\
                           key in locls, '\'{}\' needs to be defined to perform \'{}\' on it!'.format(key, funcname)
                    if   funcname == '<-'   or funcname == '->'  : locls[key] = value
                    elif funcname == '<?-'  or funcname == '-?>' :
                        locls[key] = value if value else (locls[key] if key in locls else None)
                    elif funcname == '<+-'  or funcname == '-+>' : locls[key] += value
                    elif funcname == '<--'  or funcname == '-->' : locls[key] = value
                    elif funcname == '<*-'  or funcname == '-*>' : locls[key] = value
                    elif funcname == '</-'  or funcname == '-/>' : locls[key] = value
                    elif funcname == '<**-' or funcname == '-**>': locls[key] = value
                    elif funcname == '<%-'  or funcname == '-%>' : locls[key] = value
                    elif funcname == '<&-'  or funcname == '-&>' : locls[key] = value
                    elif funcname == '<|-'  or funcname == '-|>' : locls[key] = value
                    elif funcname == '<^-'  or funcname == '-^>' : locls[key] = value
                    elif funcname == '<<-'  or funcname == '-<>' : locls[key] = value
                    elif funcname == '<>-'  or funcname == '->>' : locls[key] = value
        else:
            funcs = {
                '**'  : lambda a, b: a ** b,
                '*'   : lambda a, b: a * b,
                '/'   : lambda a, b: a /  b,
                '%'   : lambda a, b: a %  b,
                '+'   : lambda a, b: a + b,
                '-'   : lambda a, b: a -  b,
                'b<<' : lambda a, b: a << b,
                'b>>' : lambda a, b: a >> b,
                'b&'  : lambda a, b: a & b,
                'b^'  : lambda a, b: a ^ b,
                'b|'  : lambda a, b: a | b,
                '<'   : lambda a, b: a <  b,
                '>'   : lambda a, b: a >  b,
                '<='  : lambda a, b: a <= b,
                '>='  : lambda a, b: a >= b,
                '=='  : lambda a, b: a == b,
                '='   : lambda a, b: a == b,
                '!='  : lambda a, b: a != b,
            }
            eles[0].eval(locls)
            ret = locls['$']
            for ele in eles[1:]:
                ele.eval(locls)
                ret = funcs[funcname](ret, locls['$'])
            locls['$'] = ret# x = y

class wfile:
    def __init__(self, filepath, encoding = 'utf-8'):
        self.filepath = filepath
        import codecs
        with codecs.open(filepath, 'r', encoding) as f:
            self.striptext = wfile._striptext(f.read())
        self.tokens = wfile._tokenize(self.striptext)
        import copy
        self.lines = wfile._compresstokens(copy.deepcopy(self.tokens))
    
    def __iter__(self):
        return iter(self.lines)
    
    def __str__(self):
        ret = 'file \'{}\':\n==[start]==\n'.format(self.filepath)
        pos = 1
        for line in self.lines:
            ret += '\n{}: \t{}'.format(pos, line)
            pos+=1
        return ret + '\n\n==[ end ]=='
        # return 'file \'{}\':\n>>\t{}'.format(self.filepath, '\n\t'.join(str(line) for line in self.lines))

    @staticmethod
    def _striptext(rawt):
        """ remove comments and blank lines"""
        ret = ''
        data = 0b00 # 0b10 = escaped, 0b01 = commented
        for char in rawt:
            if char in control.escape  and not data & 0b10:
                data ^= 0b10
            elif char in control.comment and not data & 0b10:
                data ^= 0b01
            elif char in control.linebreak:
                # if not data & 0b10 and (not ret or ret[-1] not in control.linebreak): #so no duplicate \ns
                    # ret += char
                data &= 0b10
            else:
                data &= 0b01
                if not data & 0b01:
                    ret += char
        return ret
    
    @staticmethod
    def _tokenize(rawt):
        """ goes thru, and splits them up first based upon control.sortedopers and then by control.punctuation. """
        def tokenize(rawt):
            for oper in control.sortedopers:
                if oper in rawt:
                    par = rawt.partition(oper)
                    return tokenize(par[0]) + [par[1]] + tokenize(par[2])
            for punc in control.punctuation + control.endline:
                if punc in rawt:
                    par = rawt.partition(punc)
                    return tokenize(par[0]) + [par[1]] + tokenize(par[2])
            return [rawt]
        tokens = (token.strip(control.nbwhitespace) for token in tokenize(rawt))
        ret = [[]]
        for token in tokens:
            if not token:
                continue
            if token in control.endline:
                ret.append([])
            else:
                ret[-1].append(token)
        return [l for l in ret if l]

    @staticmethod
    def _compresstokens(linetokens):
        def findhighest(linegrp):
            if __debug__:
                assert linegrp or linegrp.val, linegrp
            highest = None
            for elep in range(len(linegrp)):
                ele = linegrp[elep].val
                if ele in control.allopers and (highest == None or
                        control.allopers[ele] > control.allopers[linegrp[highest].val]):
                    highest = elep
            if __debug__:
                assert highest != None, 'no highest for ' + str(linegrp)
            return highest
        def compresstokens(linegrp): #this is non-stable
            ret = group(parens = linegrp.parens) #universe
            while linegrp:
                ele = linegrp.pop(0) #pop(0) is inefficient for list. update this in the future
                if ele not in control.allparens:
                    ret.append(group(ele))
                else:
                    toappend = group()
                    parens = 1
                    while parens > 0 and linegrp:
                        toappend.append(linegrp.pop(0))
                        if toappend[-1] in control.parens['l']:
                            parens += 1
                        if toappend[-1] in control.parens['r']:
                            parens -= 1
                    if __debug__:
                        assert toappend[-1] in control.allparens, toappend #the last element should be in allparens
                    toappend.parens = (ele, toappend.pop())
                    toappend = compresstokens(toappend)
                    ret.append(toappend)
            return ret
        def fixtkns(line):
            #combine tokens using order of operations
            if not line:
                return line
            if len(line) == 1: #if the line is literally a single element
                if len(line[0]) == 0: #if the line is literally a single constant
                    return line
                else:
                    return fixtkns(line[0])
            fhp = findhighest(line)
            if __debug__:
                assert isinstance(line[fhp], group), 'expected a group for fhp! (not %s)' % line[fhp]
            ret = group(val = line[fhp].val, parens = line.parens)
            s = fixtkns(group(args = line[0:fhp]))
            e = fixtkns(group(args = line[fhp + 1:]))
            if s != None:
                if len(s) == 1 and not s.val and not s.hasparens():
                    ret.append(s[0])
                else:
                    ret.append(s)
            if e != None:
                if len(e) == 1 and not e.val and not e.hasparens():
                    ret.append(e[0])
                else:
                    ret.append(e)
            return ret

        return group(args = [fixtkns(compresstokens(group(args = line))) for line in linetokens])
    

    def eval(self):
        locls = {}
        for line in self:
            line.eval(locls)
        if '$' in locls:
            del locls['$']
        return locls

if __name__ == '__main__':
    """
    assignment:
        a -> b
        b <- a
        a -+> b
        b <+- a
        ect, etc...
    if statements:
        if:(Condition):{Expression if true}:{Expression if false}
        the false part is optional
        The parenthesis used do not matter, so it can be
        if:{a == b}:(a <+- 1):[b <+- 1]
    """
    f = wfile('testcode.wc')
    print(f)
    print('--')
    print(f.eval())

"""
@f1(arg)
   @f2
   def func(): pass

"""
















