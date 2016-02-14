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
    def isempty(self):
        return self.isnull() or not self and not self.hasparens() and self.val in control.endline
    def isnull(self):
        return not self and not self.hasparens() and not self.val
    def eval(self, locls):
        if self.isnull():
            locls['$'] = None
        # print(self.val, self.val in control.funcs)
        elif self.val in control.allopers:
            control.evaloper(self, locls)
        elif self.val in control.funcs:
            control.funcs[self.val](self, locls)
        else:
            if self.val == '':
                if __debug__:
                    assert len(self) == 1, self #expects 1 element (in parens)
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
    datadef = '@'
    nbwhitespace = ' \t\x0b\x0c'
    whitespace = nbwhitespace + linebreak
    alldelims = ',|' + endline
    allquotes = '\'\"`'
    parens = {'l':'([{',
              'r':')]}'}
    allparens = ''.join(list(parens.values())) + allquotes #yes, quotes are parens lol :P
    punctuation = '!#$%&*+-/;<=>?@^|~' + allparens + alldelims + allquotes#stuff used to break apart things, ignoring ._
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
            ':'   : oper(':',      0, None), # association
            '??'   : oper(':',      0, None), # association
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
    for delim in alldelims:
        opers['unary']['l'][str(delim)] = oper(str(delim), 14, lambda x, y: y)
    funcs = {
        'if': lambda eles, locls: control._doFunc(eles, locls, 'if'),
        'for': lambda eles, locls: control._doFunc(eles, locls, 'for'),
        'disp': lambda eles, locls: control._doFunc(eles, locls, 'disp'),
        'displ': lambda eles, locls: control._doFunc(eles, locls, 'displ'),
    }
    allopers = opers['binary']; allopers.update(opers['unary']['l']); allopers.update(opers['unary']['r'])
    sortedopers = tuple(x for x in reversed(sorted(allopers.keys(), key = lambda l: len(l)))) #sorted by length

    @staticmethod
    def _doFunc(eles, locls, funcname):
        if __debug__:
            assert eles[0].val == funcname, 'this shouldn\'t break'
        if funcname == 'disp' or funcname == 'displ':
            eles[1].eval(locls)
            print(locls['$'], end = '\n' if funcname == 'displ' else '') #keep this here!
        elif funcname == 'if':
            if __debug__:
                assert len(eles[1]) == 2, 'this shouldn\'t break!' #should be CONDITION, VALUE
            eles[1][0].eval(locls) # evaluates the condition
            # if len(eles[1])
            if locls['$']:
                if len(eles[1][1]) == 2:
                    eles[1][1].eval(locls)
                else:
                    eles[1][1][0].eval(locls)
            elif len(eles[1][1]) == 2:
                eles[1][1][1].eval(locls)
        elif funcname == 'for':
            if __debug__:
                assert len(eles[1]) == 2, 'this shouldn\'t break!' #should be CONDITION, VALUE
            eles[1][0][0].eval(locls) # evaluates the condition
            while True:
                eles[1][0][1][0].eval(locls) #checks the statement
                if not locls['$']:
                    break
                eles[1][1].eval(locls)
                eles[1][0][1][1].eval(locls)
            if locls['$']:
                eles[1][1][0].eval(locls)
            elif len(eles[1][1]) == 2:
                eles[1][1][1].eval(locls)

        else:
            raise SyntaxError('function \'{}\' isn\'t defined yet!'.format(funcname))
    
    @staticmethod
    def _specialoper(eles, locls):
        name = eles.val
        if name == ':':
            if __debug__:
                assert eles[0].val in control.funcs, 'no way to proccess function \'{}\''.format(eles[0].val)
            control.funcs[eles[0].val](eles, locls)
        elif name == '||' or name == '&&':
            eles[0].eval(locls)
            element = locls['$']
            if name == '&&' and not element or name == '||' and element:
                return element
            eles[1].eval(locls)
            locls['$'] = (element or locls['$']) if name == '&&' else (element and locls['$'])
        # elif name in control.opers['unary']['l']:
        #     if __debug__:
        #         assert eles[0].isnull(),eles #should be (nothing, item)
        #     eles[1].eval(locls)
        #     locls['$'] = ~locls['$']
        else:
            direc = name in ['<-', '<?-', '<+-', '<--', '<*-', '</-', '<**-', '<%-', '<&-', '<|-', '<^-', '<<-', '<>-']
            if direc == 1:
                eles[1].eval(locls)
                value =locls['$']
                key = eles[0].val
            else:
                eles[0].eval(locls)
                value =locls['$']
                key = eles[1].val
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

    @staticmethod
    def evaloper(eles, locls):
        if eles.val not in control.allopers:
            raise SyntaxError('operator \'{}\' isn\'t defined'.format(eles.val))
        oper = control.allopers[eles.val]
        if oper.func == None:
            control._specialoper(eles, locls)
        elif eles:
            eles[0].eval(locls)
            ret = locls['$']
            name = eles.val
            for ele in eles[1:]:
                ele.eval(locls)
                ret = control.allopers[name].func(ret, locls['$'])
            locls['$'] = ret# x = y

    @staticmethod
    def applyrules(tokens):
        print(tokens)
        if __debug__:
            assert tokens[0] == '@'
            assert tokens[1] == 'define', tokens[1] #currently, only 'define' is defined.
        assert 0, 'not implemented yet! todo: this'
        # fixedtokens = 

class wfile:
    def __init__(self, filepath, encoding = 'utf-8'):
        self.filepath = filepath
        import codecs
        with codecs.open(filepath, 'r', encoding) as f:
            self.striptext = wfile._striptext(f.read())
        self.tokens = wfile._tokenize(self.striptext)
        import copy
        self.lines = wfile._compresstokens(copy.deepcopy(self.tokens))
    
    def __str__(self):
        def getl(linep, l):
            if not l:
                assert str(l) == ';' or str(l) == '', str(l) #no other known case atm
                return linep, ''
            if __debug__:
                print(l[0])
                assert l[0].val not in control.endline or not l[0].val, l[0].val # node structure should prevent this.
            ret = ''
            if l[0]:
                ret = '\n{}:  \t{}'.format(linep, l[0])
                linep += 1
            if l[1].val not in control.endline:
                ret += '\n{}:  \t{}'.format(linep, l[1])
                linep += 1
            else:
                e = getl(linep, l[1])
                ret += e[1]
                linep += e[0]
            return linep, ret
        return 'file \'{}\':\n==[start]==\n{}\n\n==[ end ]=='.format(self.filepath, getl(0, self.lines)[1])

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
                data &= 0b10 #remove comments
            else:
                if data & 0b10:
                    ret += control.escape
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
                    if rawt[rawt.index(oper) - 1] in control.escape:
                        return [par[0] + par[1]] + tokenize(par[2])
                    return tokenize(par[0]) + [par[1]] + tokenize(par[2])
            for punc in control.punctuation + control.endline:
                if punc in rawt and rawt[rawt.index(punc) - 1] not in control.escape:
                    par = rawt.partition(punc)
                    return tokenize(par[0]) + [par[1]] + tokenize(par[2])
            return [rawt]
        tokens = [token.strip(control.nbwhitespace) for token in tokenize(rawt)]
            

        ret = []

        for token in tokens: #clear empty lines
            if not token:
                continue
            else:
                ret.append(token)

        #@define stuff
        linep = 0
        while linep < len(ret): 
            if ret[linep] and ret[linep] in control.datadef:
                control.applyrules(ret.pop(0))
            linep+=1
        return ret

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
        return fixtkns(compresstokens(group(args = linetokens)))
    

    def eval(self):
        locls = {}
        self.lines.eval(locls)
        if '$' in locls:
            del locls['$']
        return locls

if __name__ == '__main__':
    f = wfile('testcode.om')
    print(f)
    print('--')
    print(f.eval())

"""
@f1(arg)
   @f2
   def func(): pass

"""
















