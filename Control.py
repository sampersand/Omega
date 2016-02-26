class control():
    def __init__(self):

        self.linebreak = '\n\r' #linebreak is used for comments
        self.comment = '#'
        self.escape = '\\'
        self.datadef = '@'
        self.nbwhitespace = ' \t\x0b\x0c'
        self.whitespace = self.nbwhitespace + self.linebreak
        self._allquotes = '\'\"`'

        from Obj import operobj, nullobj, boolobj


        self.delims = {
            'arraysep': (',',   operobj(',', 14)),
            'etc'     : ('|',   operobj('|', 14)),
            'endline' : (';\n', operobj(';', 14))}

        self.parens = {
            'l' : '([{',
            'r' : ')]}'}

        self.consts = {
            'null' : nullobj(),
            't' : boolobj(True),  'True'  : boolobj(True),  'T' : boolobj(True),  'true'  : boolobj(True),  
            'f' : boolobj(False), 'False' : boolobj(False), 'F' : boolobj(False), 'false' : boolobj(False), 
        }
        self.opers = {
            'binary':{
            
            },
            'unary':{
                'l':{},
            }
        }
        self.funcs = { }

        for d in self.delims.values():
            for val in d[0]:
                self.opers['unary']['l'][val] = d[1]
    @property
    def alldelims(self):
        """ string of all the delims available """
        return ''.join(v[0] for v in self.delims.values())

    @property
    def allparens(self):
        """ string of all the parens available """
        return ''.join(list(self.parens.values()))# + self.allquotes #yes, quotes are parens lol :P <-- are they?

    @property
    def allquotes(self):
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
        return control._updateDict(dict(), self.opers)

    @property
    def allconsts(self):
        return control._updateDict(dict(), self.consts)

    @property
    def allfuncs(self):
        return control._updateDict(dict(), {'funcs' : self.funcs, 'opers' : self.opers})
    
    @property
    def allkws(self):
        return control._updateDict(dict(), {'funcs' : self.allfuncs, 'consts' : self.allconsts})

        # #crap i need a better way than this D:
        # allfuncs = copy.copy(allopers); allfuncs.update(funcs)
        # allkws = copy.copy(allfuncs); allkws.update(consts)
        # del copy



















