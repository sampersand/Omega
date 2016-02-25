class locls(dict):
    from group import group
    DEFAULT_GRP = {'$':group(), '$ret':group()}
    def __init__(self):
        import copy
        super().__init__(copy.deepcopy(locls.DEFAULT_GRP))
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
    def clear(self):
        super().clear()
        import copy
        self.update(copy.deepcopy(locls.DEFAULT_GRP))