from Objects import nullobj, boolobj, funcobj, operobj, omfuncobj
from Group import group
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

    class _specdelimsdict(_specdict):
        def __contains__(self, i):
            return any(i in e for e in self.values())

    class _spectuple(tuple):
        """ when using 'in' it uses the first element. """
        def __contains__(self, item):
            if __debug__:
                assert len(self) == 2, 'can only be used in this case!'
            return item in self[0]
            
    def __init__(self):
        self.linebreak = '\n\r' #linebreak is used for comments
        self.comment = '#'
        self.escape = '\\'
        self.datadef = '@'
        self.nbwhitespace = ' \t\x0b\x0c'
        self.whitespace = self.nbwhitespace + self.linebreak
        self._allquotes = '\'\"`' #just for continuity

        self.escapechars = {'\\n': '\n',
                       '\\t': '\t',
                       '\\r': '\r',
                       "\\'": '\'',
                       '\\`': '`',
                       '\\"': '\"',
                       '\\\\':'\\',
                       '\\#':'#',
                       }

        self.parens = control._specdict({
            'l' : control._specdict({'(' : ')', '[' : ']', '{' : '}'}),
            'r' : control._specdict({')' : '(', ']' : '[', '}' : '{'}),
        })

        self.consts = control._specdict({
            # 'null'  : group(data = None,  baseobj = nullobj(True)),
            # 'True'  : group(data = True,  baseobj = boolobj()),  'true'  : group(data = True,  baseobj = boolobj()),  
            # 'False' : group(data = False, baseobj = boolobj()), 'false' : group(data = False, baseobj = boolobj()), 
            # '$'     :  group(data = None, baseobj = funcobj('$'))
        })
        self.opers = control._specdict({
            'binary':control._specdict({
                'math':control._specdict({
                    '**'  : operobj('**',     3, '_func_pow'), # power of
                    '*'   : operobj('*',      4, '_func_mul'), # mult
                    '/'   : operobj('/',      4, '_func_div'), # div
                    '%'   : operobj('%',      4, '_func_mod'), # mod
                    '+'   : operobj('+',      5, '_func_add'), # plus
                    '-'   : operobj('-',      5, '_func_sub'), # minus
                    }),

                'bitwise':control._specdict({
                    'b<<' : operobj('b<<',    6, '_func_rshift'), # bitwise <<
                    'b>>' : operobj('b<<',    6, '_func_lshift'), # bitwise >>
                    'b&'  : operobj('b&',     7, '_func_and'), # bitwise &
                    'b^'  : operobj('b^',     8, '_func_xor'), # bitwise ^
                    'b|'  : operobj('b|',     9, '_func_or'), # bitwise |
                    }),
                'logic':control._specdict({
                    '<'   : operobj('<',     10, '_func_lt'), # less than
                    '>'   : operobj('>',     10, '_func_gt'), # greater than
                    '<='  : operobj('<=',    10, '_func_le'), # less than or equal
                    '>='  : operobj('>=',    10, '_func_ge'), # greater than or equal
                    '=='  : operobj('==',    10, '_func_eq'), # equal to
                    '='   : operobj('=',     10, '_func_eq'), # equal to
                    '<>'  : operobj('<>',    10, '_func_ne'), # equal to
                    '!='  : operobj('!=',    10, '_func_ne'), # not equal to
                    '&&'  : operobj('&&',    11, None    ), # boolean and
                    '||'  : operobj('||',    12, None    ), # booleon or
                    }),
                
                'assignment':control._specdict({
                    # all notes are in form of "x OPERATOR y" like 'x <- y' for reversed operators
                    'l':control._specdict({
                        # a -> b is 'r'
                        '<-'   : operobj('<-',   14, None), # x = y
                        '<?-'  : operobj('<?-',  14, None), # x = bool(y) ? y : None
                        '<+-'  : operobj('<+-',  14, None), # x += y
                        '<--'  : operobj('<--',  14, None), # x -= y
                        '<*-'  : operobj('<*-',  14, None), # x *= y
                        '</-'  : operobj('</-',  14, None), # x /= y
                        '<**-' : operobj('<**-', 14, None), # x **= y
                        '<%-'  : operobj('<%-',  14, None), # x %= y
                        '<&-'  : operobj('<&-',  14, None), # x &= y
                        '<|-'  : operobj('<|-',  14, None), # x |= y
                        '<^-'  : operobj('<^-',  14, None), # x ^= y
                        '<<-'  : operobj('<<-',  14, None), # x <<= y
                        '<>-'  : operobj('<>-',  14, None), # x >>= y
                        }),
                    'r':control._specdict({
                        # b <- a is 'l'
                        '->'   : operobj('->',   14, None), # y = x
                        '-?>'  : operobj('-?>',  14, None), # y = bool(x) ? x : None
                        '-+>'  : operobj('-+>',  14, None), # y += x
                        '-->'  : operobj('-->',  14, None), # y -= x 
                        '-*>'  : operobj('-*>',  14, None), # y *= x 
                        '-/>'  : operobj('-/>',  14, None), # y /= x 
                        '-**>' : operobj('-**>', 14, None), # y **= x 
                        '-%>'  : operobj('-%>',  14, None), # y %= x 
                        '-&>'  : operobj('-&>',  14, None), # y &= x 
                        '-|>'  : operobj('-|>',  14, None), # y |= x 
                        '-^>'  : operobj('-^>',  14, None), # y ^= x 
                        '-<>'  : operobj('-<>',  14, None), # y <<= x 
                        '->>'  : operobj('->>',  14, None), # y >>= x 
                        }),
                    }),
                'delims':control._specdict({

                    }),
                }),
            'unary' : control._specdict({
                'l' : control._specdict({
                    # '~'   : operobj('~',    1, '_func_not'),
                    # 'pos' : operobj('pos',  1, '_func_pos'),
                    # 'neg' : operobj('neg',  1, '_func_neg'),
                    # '>+'  : operobj('>+',   1, None),
                    # '>-'  : operobj('>-',   1, None),
                    }),
                'r' : control._specdict({
                    # '!'   : operobj('!',    2, None),
                    # '+<'  : operobj('+<',   2, None),
                    # '-<'  : operobj('-<',   2, None),
                    })
                })
            })
        self.funcs = control._specdict({
            'if'     : funcobj('if'),
            'rm'     : funcobj('rm'),
            'om'     : omfuncobj('om'),
            'for'    : funcobj('for'),
            'disp'   : funcobj('disp'),
            'skip'   : funcobj('skip'),
            'func'   : funcobj('func'),
            'class'  : funcobj('class'),
            'abort'  : funcobj('abort'),
            'input'  : funcobj('input'),
            'whilst' : funcobj('whilst'),
            'return' : funcobj('return'),#Watch out! return:a+b is {return:a} + b
            'escape' : funcobj('escape'),
        })
        self.delims = control._specdelimsdict({
            'arraysep': control._spectuple((',',   operobj(',', 15, None))),
            'etc'     : control._spectuple(('|',   operobj('|', 15, None))),
            'endline' : control._spectuple((';\n', operobj(';', 16, None))),
            'applier' : control._spectuple((':',   operobj(':',  0, None))),
        })
        for d in self.delims.values():
            for val in d[0]:
                self.opers['binary']['delims'][val] = d[1]
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
        for k, v in d.items():
            v
            if isinstance(v, dict):
                control._updateDict(mdict, v)
            else:
                mdict[k] = v
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
    def _invertparen(self, paren):
        """ invert parens - used in file parsing. eg, '(' -> ')'. """
        return self.parens[paren in self.parens['l'] and 'l' or 'r'][paren]














