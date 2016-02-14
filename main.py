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
    def __repr__(self):
        return 'group(val = {}, args = {}, parens = {})'.format(repr(self.val), super().__repr__(), repr(self.parens))
    def __str__(self):
        if not self and not self.parens[0] and not self.parens[1]:
            return str(self.val)
        if self.val in control.opers['binary']:
            if __debug__:
                assert len(self) == 2, repr(self)
                assert len(self.parens) == 2, repr(self)
            return ' '.join((str(self.parens[0]), str(self[0]), str(self.val), str(self[1]), str(self.parens[1])))
        return ''.join((str(self.val), str(self.parens[0]), ', '.join(str(x) for x in self), str(self.parens[1])))
class control:
    endline = '\n\r;'
    comment = '#'
    escape = '\\'
    nbwhitespace = ' \t\x0b\x0c'
    whitespace = nbwhitespace + endline
    parens = {'l':'([{','r':')]}'}
    allparens = ''.join(list(parens.values()))
    alldelims = ',:'
    punctuation = '!"#$%&\'*+-/;<=>?@\\^`|~' + allparens + alldelims#stuff used to break apart things, ignoring ._
    """
                1   ()   []   ->   .   ::
                2   !   ~   -   +   *   &   sizeof   type cast   ++   --  
                3   *   /   %
                4   +   -
                5   <<   >>
                6   <   <=   >   >=
                7   ==   !=
                8   &
                9   ^
                10  |
                11  &&
                12  ||
                13   ? :
                14  =   +=   -=   *=   /=   %=   &=   |=   ^=   <<=   >>=
                15  ,
                --
                mine:
                0   :
                1   b~x         -x          +x          ++x         --x
                2   x!          x++         x--
                3   x ** y
                4   x * y       x / y       x %  y
                5   x + y       x - y
                6   x b<< y     x b>> y
                7   x b& y
                8   x b^ y
                9   x b| y
                10   x < y       x > y       x <= y      x >= y      ==     !=
                11  x && y
                12  x || y
                13  x <-   y     x <?- y
                    x <+-  y     x <-- y     x <*- y     x </- y     x <**- y
                    x <%-  y     x <&- y     x <|- y     x <^- y     x <<<- y    x <>>- y
                    And their inverses
            """
    opers = {
        'binary':{
            ':'   : oper(':',      0, lambda eles: None), # association
            '**'  : oper('**',     3, lambda eles: None), # power of
            '*'   : oper('*',      4, lambda eles: None), # mult
            '/'   : oper('/',      4, lambda eles: None), # div
            '%'   : oper('%',      4, lambda eles: None), # mod
            '+'   : oper('+',      5, lambda eles: None), # plus
            '-'   : oper('-',      5, lambda eles: None), # minus
            'b<<' : oper('b<<',    6, lambda eles: None), # bitwise <<
            'b>>' : oper('b<<',    6, lambda eles: None), # bitwise >>
            'b&'  : oper('b&',     7, lambda eles: None), # bitwise &
            'b^'  : oper('b^',     8, lambda eles: None), # bitwise ^
            'b|'  : oper('b|',     9, lambda eles: None), # bitwise |
            '<'   : oper('<',     10, lambda eles: None), # less than
            '>'   : oper('>',     10, lambda eles: None), # greater than
            '<='  : oper('<=',    10, lambda eles: None), # less than or equal
            '>='  : oper('>=',    10, lambda eles: None), # greater than or equal
            '=='  : oper('==',    10, lambda eles: None), # equal to
            '!='  : oper('!=',    10, lambda eles: None), # not equal to
            '&&'  : oper('&&',    11, lambda eles: None), # boolean and
            '||'  : oper('||',    12, lambda eles: None), # booleon or
            #assignment operators
            # all notes are in form of "x OPERATOR y" like 'x <- y'
            '<-'   : oper('<-',   13, lambda eles: None), # x = y
            '<?-'  : oper('<?-',  13, lambda eles: None), # x = bool(y) ? y : None
            '<+-'  : oper('<+-',  13, lambda eles: None), # x += y
            '<--'  : oper('<--',  13, lambda eles: None), # x -= y
            '<*-'  : oper('<*-',  13, lambda eles: None), # x *= y
            '</-'  : oper('</-',  13, lambda eles: None), # x /= y
            '<**-' : oper('<**-', 13, lambda eles: None), # x **= y
            '<%-'  : oper('<%-',  13, lambda eles: None), # x %= y
            '<&-'  : oper('<&-',  13, lambda eles: None), # x &= y
            '<|-'  : oper('<|-',  13, lambda eles: None), # x |= y
            '<^-'  : oper('<^-',  13, lambda eles: None), # x ^= y
            '<<-'  : oper('<<-',  13, lambda eles: None), # x <<= y
            '<>-'  : oper('<>-',  13, lambda eles: None), # x >>= y
            #inverted assignment operators
            # all notes are in form of "x OPERATOR y" like 'x -> y'
            '->'   : oper('->',   13, lambda eles: None), # y = x
            '-?>'  : oper('-?>',  13, lambda eles: None), # y = bool(x) ? x : None
            '-+>'  : oper('-+>',  13, lambda eles: None), # y += x
            '-->'  : oper('-->',  13, lambda eles: None), # y -= x 
            '-*>'  : oper('-*>',  13, lambda eles: None), # y *= x 
            '-/>'  : oper('-/>',  13, lambda eles: None), # y /= x 
            '-**>' : oper('-**>', 13, lambda eles: None), # y **= x 
            '-%>'  : oper('-%>',  13, lambda eles: None), # y %= x 
            '-&>'  : oper('-&>',  13, lambda eles: None), # y &= x 
            '-|>'  : oper('-|>',  13, lambda eles: None), # y |= x 
            '-^>'  : oper('-^>',  13, lambda eles: None), # y ^= x 
            '-<>'  : oper('-<>',  13, lambda eles: None), # y <<= x 
            '->>'  : oper('->>',  13, lambda eles: None)  # y >>= x 
             },\
        'unary':{
            'l':{'~':oper('~', 1, lambda x: None)},
            'r':{'!':oper('!', 2, lambda x: None)}
        }
    }

    allopers = opers['binary']; allopers.update(opers['unary']['l']); allopers.update(opers['unary']['r'])
    sortedopers = tuple(x for x in reversed(sorted(allopers.keys(), key = lambda l: len(l)))) #sorted by length

class wfile:
    def __init__(self, filepath, encoding = 'utf-8'):
        self.filepath = filepath
        import codecs
        with codecs.open(filepath, 'r', encoding) as f:
            self.striptext = wfile._striptext(f.read())
        self.tokens = wfile._tokenize(self.striptext)
        import copy
        self.compressedtokens = wfile._compresstokens(copy.deepcopy(self.tokens))

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
            elif char in control.endline:
                if not data & 0b10 and (not ret or ret[-1] not in control.endline): #so no duplicate \ns
                    ret += char
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
                        control.allopers[ele] > control.allopers[linetokens[highest].val]):
                    highest = elep
            if __debug__:
                assert highest != None, 'no highest for ' + str(linetokens)
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
            if not line:
                return line
            if len(line) == 1: #if the line is literally a single element
                if len(line[0]) == 0: #if the line is literally a single constant
                    return line[0]
                else:
                    return fixtkns(line[0])
            fhp = findhighest(line)
            if __debug__:
                assert isinstance(line[fhp], group), 'expected a group for fhp! (not %s)' % line[fhp]
            ret = group(val = line[fhp].val, parens = line.parens)
            s = fixtkns(line[0:fhp])
            e = fixtkns(line[fhp + 1:])
            if s != None:
                ret.append(s)
            if e != None:
                ret.append(e)
            return ret
            """
                private static TokenNode condense(final Collection<TokenNode> line){
                    if(line.size() == 0)
                        return null;
                    if(line.size() == 1)
                        if(line.get(0).size() == 0)
                            return line.get(0);
                        else
                            return new TokenNode(line.get(0)){{
                                add(condense(new Collection<TokenNode>().addAllE(line.get(0).elements)));
                            }};

                    int fhp = firstHighPriority(line);
                    if(fhp == -1)
                        return new TokenNode(new Token()){{
                            line.forEach(e -> add(condense(new Collection<TokenNode>().addE(e))));
                        }};
                    TokenNode u = condense(new Collection<TokenNode>().addE(line.get(fhp)));
                    TokenNode s = condense(new Collection<TokenNode>().addAllE(line.subList(0, fhp)));
                    TokenNode e = condense(new Collection<TokenNode>().addAllE(line.subList(fhp + 1)));
                    if(s != null)
                        u.add(s);
                    if(e != null)
                        u.add(e);
                    return u;
                }
            """
            #order of operations
            # if len(line) <= 1:
            #     return line
            # highest = findhighest(line)
            # oper = line[highest]
            # if oper.val in control.opers['binary']:
            #     if __debug__:
            #         assert len(line) > 2, 'binary operator \'{}\' in {} needs to have 3+ elements!'.format(oper, line)
            #     # print('fixtknsret:',group(val = oper.val,
            #     #              args = [fixtkns(line[0:highest]), fixtkns(line[highest + 1:])],
            #     #              parens = oper.parens))
            #     return group(val = oper.val,
            #                  args = [fixtkns(line[0:highest]), fixtkns(line[highest + 1:])],
            #                  parens = oper.parens)
            # return None

        return group('',list(fixtkns(compresstokens(group('',line))) for line in linetokens))
    def __str__(self):
        return str(self.compressedtokens)

if __name__ == '__main__':
    f = wfile('testcode.wc')
    print(f)

"""
@f1(arg)
   @f2
   def func(): pass

"""







"""
('1,234.5', '*', '(', '1e4', '-', '2.4', ')', '-?>', 'b')
1,234.5
--
*
1,234.5
--
(
*
1,234.5
--
1e4
(
*
1, 234.5
--
2.4
-
1e4
(
*
1, 234.5


group(val = '',
      args = [
        group(val = 'a',
              args = [],
              parens = ['', '']),
        group(val = '<-',
              args = [],
              parens = ['', '']),
        group(val = 'arary',
              args = [],
              parens = ['', '']),
        group(val = '',
              args = ['position'],
              parens = ('[', ']')),
        group(val = '+',
              args = [],
              parens = ['', '']),
        group(val = '',
              args = ['1', '+', '2'],
              parens = ('(', ')'))
        ],
      parens = ['', ''])


group(  val = '',
        args = [
            group(  val = '<-',
                    args = [
                        [
                            group(  val = 'a',
                                    args = [],
                                    parens = ['', '']
                            )
                        ], 
                        group(  val = '+',
                                args = [
                                    group(  val = ':',
                                            args = [
                                                [
                                                    group(  val = 'array',
                                                            args = [],
                                                            parens = ['', '']
                                                    )
                                                ],
                                                [
                                                    group(  val = '',
                                                            args = ['position'],
                                                            parens = ('[', ']')
                                                    )
                                                ]
                                            ],
                                        parens = ['', '']
                                    ),
                                    [group(val = '',
        args = ['1', '+', '2'],
        parens = ('(', ')'))]],
        parens = ['', ''])],
        parens = ['', ''])],
        parens = ['', ''])
"""






















