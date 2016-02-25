class locls(dict):
    def __init__(self):
        from group import group
        super().__init__({'$':group(), '$ret':group()})
    @property
    def lv(self):
        "I am the 'lv' property."
        return self['$']
    @lv.setter
    def lv(self, value):
        self['$'] = value
    @lv.deleter
    def lv(self):
        del self['$']
    @property
    def ret(self):
        "I am the 'ret' property."
        return self['$ret']
    @ret.setter
    def ret(self, value):
        self['$ret'] = value
    @ret.deleter
    def ret(self):
        del self['$']