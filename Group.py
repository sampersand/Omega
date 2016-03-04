class group(list):
    def __init__(self, data = None, obj = None, control = None, args = [], parens = ('', '')):
        super().__init__(args)
        self.data = data
        self.obj = obj
        self.control = control
        self.args = args
        self.parens = parens