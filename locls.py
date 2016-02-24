class locls(dict):
    def __init__(self):
        from group import group
        super().__init__({'$':group()})
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