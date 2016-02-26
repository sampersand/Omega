class control():
    class _specdict(dict):
        """ when using 'in' it goes thru all the subdicts as well."""
        def __contains__(self, i):
            for item in self:
                if isinstance(self[item], dict) and i in self[item]:
                    return True
                if i == item:
                    return True
            return False
            
    def __init__(self):

        self.linebreak = '\n\r' #linebreak is used for comments
        self.comment = '#'
        self.escape = '\\'
        self.datadef = '@'
        self.nbwhitespace = ' \t\x0b\x0c'
        self.whitespace = self.nbwhitespace + self.linebreak
        self._allquotes = '\'\"`'

        from Obj import operobj, nullobj, boolobj

        self.delims = control._specdict({
            'arraysep': (',',   operobj(',', 14)),
            'etc'     : ('|',   operobj('|', 14)),
            'endline' : (';\n', operobj(';', 16)),
            'applier' : (':',   operobj(':',  0))
            })

        self.parens = control._specdict({
            'l' : control._specdict({'(' : ')', '[' : ']', '{' : '}'}),
            'r' : control._specdict({')' : '(', ']' : '[', '}' : '{'}),
            } )

        self.consts = control._specdict({
            'null' : nullobj(),
            't' : boolobj(True),  'True'  : boolobj(True),  'T' : boolobj(True),  'true'  : boolobj(True),  
            'f' : boolobj(False), 'False' : boolobj(False), 'F' : boolobj(False), 'false' : boolobj(False), 
        })
        self.opers = control._specdict({
            'binary':control._specdict({
                'math':control._specdict({
                    '**'  : operobj('**',     3), # power of
                    '*'   : operobj('*',      4), # mult
                    '/'   : operobj('/',      4), # div
                    '%'   : operobj('%',      4), # mod
                    '+'   : operobj('+',      5), # plus
                    '-'   : operobj('-',      5), # minus
                }),
                # 'bitwise':control._specdict({
                #     'b<<' : operobj('b<<',    6), # bitwise <<
                #     'b>>' : operobj('b<<',    6), # bitwise >>
                #     'b&'  : operobj('b&',     7), # bitwise &
                #     'b^'  : operobj('b^',     8), # bitwise ^
                #     'b|'  : operobj('b|',     9), # bitwise |
                # }),
                # 'logic':control._specdict({
                #     '<'   : operobj('<',     10), # less than
                #     '>'   : operobj('>',     10), # greater than
                #     '<='  : operobj('<=',    10), # less than or equal
                #     '>='  : operobj('>=',    10), # greater than or equal
                #     '=='  : operobj('==',    10), # equal to
                #     '='   : operobj('=',     10), # equal to
                #     '<>'  : operobj('<>',    10), # equal to
                #     '!='  : operobj('!=',    10), # not equal to
                #     '&&'  : operobj('&&',    11), # boolean and
                #     '||'  : operobj('||',    12), # booleon or
                #     }),
                
                'assignment':control._specdict({
                    # all notes are in form of "x OPERATOR y" like 'x <- y' for reversed operators
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
                    }),
                 }),
            'unary':{
                'l':{},
            }
        })
        self.funcs = control._specdict({ })

        for d in self.delims.values():
            for val in d[0]:
                self.opers['unary']['l'][val] = d[1]

        self._punctuation = '!#%&*+-/;<=>?@^|~'

    @property
    def alldelims(self):
        """ string of all the delims available """
        return ''.join(v[0] for v in self.delims.values())
    @property
    def allparens(self):
        """ string of all the parens available """
        return ''.join(list(self.parens['l'].values()) + list(self.parens['r'].values()))# + self.allquotes #yes, quotes are parens lol :P <-- are they?
    @property
    def allquotes(self):
        """ The Complete list of quotes. """
        return self._allquotes
    @staticmethod
    def _updateDict(mdict, d):
        for k in d.keys():
            e = d[k]
            if isinstance(e, dict):
                control._updateDict(mdict, e)
            else:
                mdict[k] = e
        return mdict
    @property
    def allopers(self):
        """ The Complete list of operators. """
        return control._updateDict(dict(), self.opers)
    @property
    def allconsts(self):
        """ The Complete list of constants. """
        return control._updateDict(dict(), self.consts)
    @property
    def allfuncs(self):
        """ The Complete list of functions. """
        return control._updateDict(dict(), {'funcs' : self.funcs, 'opers' : self.opers})
    @property
    def allkws(self):
        """ The Complete list of keywords. """
        return control._updateDict(dict(), {'funcs' : self.allfuncs, 'consts' : self.allconsts})
    @property
    def sortedopers(self):
        """ A sorted list of operators - in descending order of length of the operator (<**- is larger than +)"""
        return tuple(x for x in reversed(\
            sorted(self.allopers.keys(),
                   key = lambda l:
                   len(l)))) #sorted by length
    @property
    def punctuation(self):
        """ stuff used to break apart things, ignoring: ._$ """
        return '!#%&*+-/<=>?@^|~' + self.allparens + self.alldelims + self.allquotes + self.delims['endline'][0]
    def _invertparen(paren):
        """ invert parens - used in file parsing. eg, '(' -> ')'. """
        return self.parens[paren in self.parens['l'] and 'l' or 'r'][paren]

    

















