class locls(dict):
    from group import group
    DEFAULT_GRP = {'$':group(), '$ret':group()}
    def __init__(self):
        import copy
        super().__init__(copy.deepcopy(locls.DEFAULT_GRP))
    @property
    def lv(self):
        "I am the 'lv' property."
        if __debug__:
            from group import group
            assert isinstance(self['$'],group), self['$']
        return self['$']
    @lv.setter
    def lv(self, value):
        if __debug__:
            from group import group
            assert isinstance(self['$'],group), self['$']#
        self['$'] = value
    @lv.deleter
    def lv(self):
        if __debug__:
            from group import group
            assert isinstance(self['$'],group), self['$']#
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
    def __str__(self):
        return '{' + ', '.join(str(k) + ':' + str(self[k]) for k in self) + '}'