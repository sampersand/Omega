class group(list):
    def __new__(self, base = '', args = [], parens = ('','')):
        return super().__new__(self, args)

    def __init__(self, base = '', args = [], parens = ('','')):
        import control
        import omobj
        self.base = omobj.omobj.genobj(base)
        super().__init__(args)
        self.parens = parens