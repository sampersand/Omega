class oper:
    def __init__(self, value, priority, func):
        self.value = value
        self.priority = priority
        self.func = func
    def __repr__(self):
        return 'oper({}, {}, {})'.format(self.value, self.priority, self.func)
    def __str__(self):
        return self.value
    def __lt__(self, other):
        return self.priority < other.priority
class group:
    def __init__(self, val, *args):
        self.val = val
        self.args = args
class control:
    endline = '\n\r;'
    comment = '#'
    escape = '\\'
    nbwhitespace = ' \t\x0b\x0c'
    whitespace = nbwhitespace + endline
    punctuation = '!"#$%&\'()*+-,/:;<=>?@[\\]^`{|}~' #stuff used to break apart things, ignoring ._
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
                0   b~x         -x          +x          ++x         --x
                1   x!          x++         x--
                2   x ** y
                3   x * y       x / y       x %  y
                4   x + y       x - y
                5   x b<< y     x b>> y
                6   x b& y
                7   x b^ y
                8   x b| y
                9   x < y       x > y       x <= y      x >= y      ==     !=
                10  x && y
                11  x || y
                12  x <-   y     x <?- y
                    x <+-  y     x <-- y     x <*- y     x </- y     x <**- y
                    x <%-  y     x <&- y     x <|- y     x <^- y     x <<<- y    x <>>- y
                    And their inverses
            """
        
    opers = {
        'binary':{
            '**'  : oper('**',     2, lambda eles: None), # power of
            '*'   : oper('*',      3, lambda eles: None), # mult
            '/'   : oper('/',      3, lambda eles: None), # div
            '%'   : oper('%',      3, lambda eles: None), # mod
            '+'   : oper('+',      4, lambda eles: None), # plus
            '-'   : oper('-',      4, lambda eles: None), # minus
            'b<<' : oper('b<<',    5, lambda eles: None), # bitwise <<
            'b>>' : oper('b<<',    5, lambda eles: None), # bitwise >>
            'b&'  : oper('b&',     6, lambda eles: None), # bitwise &
            'b^'  : oper('b^',     7, lambda eles: None), # bitwise ^
            'b|'  : oper('b|',     8, lambda eles: None), # bitwise |
            '<'   : oper('<',      9, lambda eles: None), # less than
            '>'   : oper('>',      9, lambda eles: None), # greater than
            '<='  : oper('<=',     9, lambda eles: None), # less than or equal
            '>='  : oper('>=',     9, lambda eles: None), # greater than or equal
            '=='  : oper('==',     9, lambda eles: None), # equal to
            '!='  : oper('!=',     9, lambda eles: None), # not equal to
            '&&'  : oper('&&',    10, lambda eles: None), # boolean and
            '||'  : oper('||',    11, lambda eles: None), # booleon or
            #assignment operators
            # all notes are in form of "x OPERATOR y" like 'x <- y'
            '<-'   : oper('<-',   12, lambda eles: None), # x = y
            '<?-'  : oper('<?-',  12, lambda eles: None), # x = bool(y) ? y : None
            '<+-'  : oper('<+-',  12, lambda eles: None), # x += y
            '<--'  : oper('<--',  12, lambda eles: None), # x -= y
            '<*-'  : oper('<*-',  12, lambda eles: None), # x *= y
            '</-'  : oper('</-',  12, lambda eles: None), # x /= y
            '<**-' : oper('<**-', 12, lambda eles: None), # x **= y
            '<%-'  : oper('<%-',  12, lambda eles: None), # x %= y
            '<&-'  : oper('<&-',  12, lambda eles: None), # x &= y
            '<|-'  : oper('<|-',  12, lambda eles: None), # x |= y
            '<^-'  : oper('<^-',  12, lambda eles: None), # x ^= y
            '<<-'  : oper('<<-',  12, lambda eles: None), # x <<= y
            '<>-'  : oper('<>-',  12, lambda eles: None), # x >>= y
            #inverted assignment operators
            # all notes are in form of "x OPERATOR y" like 'x -> y'
            '->'   : oper('->',   12, lambda eles: None), # y = x
            '-?>'  : oper('-?>',  12, lambda eles: None), # y = bool(x) ? x : None
            '-+>'  : oper('-+>',  12, lambda eles: None), # y += x
            '-->'  : oper('-->',  12, lambda eles: None), # y -= x 
            '-*>'  : oper('-*>',  12, lambda eles: None), # y *= x 
            '-/>'  : oper('-/>',  12, lambda eles: None), # y /= x 
            '-**>' : oper('-**>', 12, lambda eles: None), # y **= x 
            '-%>'  : oper('-%>',  12, lambda eles: None), # y %= x 
            '-&>'  : oper('-&>',  12, lambda eles: None), # y &= x 
            '-|>'  : oper('-|>',  12, lambda eles: None), # y |= x 
            '-^>'  : oper('-^>',  12, lambda eles: None), # y ^= x 
            '-<>'  : oper('-<>',  12, lambda eles: None), # y <<= x 
            '->>'  : oper('->>',  12, lambda eles: None)  # y >>= x 
             },\
        'unary':{
            'l':{'~':oper('~', 0, lambda x: None)},
            'r':{'!':oper('!', 1, lambda x: None)}
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
        self.compressedtokens = wfile._compresstokens(self.tokens)

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
                if not data & 0b10 and ret[-1] not in control.endline: #so no duplicate \ns
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
        def findhighest(linetokens):
            if __debug__:
                assert linetokens
            highest = None
            for elep in range(len(linetokens)):
                ele = linetokens[elep]
                if ele in control.allopers and (highest == None or
                                                control.allopers[ele] > control.allopers[linetokens[highest]]):
                    highest = elep
            if __debug__:
                assert highest != None
            return highest

        def fixtokens(line):
            if len(line) <= 1:
                return line
            highest = findhighest(line)
            oper = line[highest]
            if oper in control.opers['binary']:
                if __debug__:
                    assert len(line) > 2, 'binary operator \'{}\' in {} needs to have 3+ elements!'.format(oper, line)
                return group(oper, fixtokens(line[0:highest]), fixtokens(line[0:highest]), 
            return None
            
        ['a', '<-', '(', '1', '+', '2', ')']
        return [fixtokens(line) for line in linetokens]
    def __str__(self):
        return str(self.compressedtokens)
        return str(vars(self))


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
"""

























