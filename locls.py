class locls(dict):
    def __new__(self):
        from group import group
        return super().__new__(self, ('$',group()))
    @property
    def lv(self):
        return self['$']
    
        