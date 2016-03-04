class objgrp():
    def __init__(self, data = None, objtype = None, args = list(), control = None, parens = ('', '')):
        if __debug__:
            assert control != None, 'Cannot pass an empty control!'
            assert isinstance(data, (str, type(None))), repr(data)
        self.data = data
        self.objtype = objtype
        self.args = args
        self.control = control
        self.parens = parens
    def __repr__(self):
        ret = 'objgrp('
        if self.data != None: ret += 'data=%r,' % self.data
        if self.objtype != None: ret += 'objtype=%r,' % self.objtype
        if self.args != []: ret += 'args=%r,' % self.args
        # if self.control != None: ret += 'control=%r,' % self.control
        if self.parens != ('', ''): ret += 'parens=%r,' % self.parens
        return (ret != 'objgrp(' and ret[:-1] or objgrp) + ')'
    def onlydata(self):
        return bool(self.args == list() and  self.parens == ('', ''))