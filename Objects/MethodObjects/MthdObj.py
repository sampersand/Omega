from Objects import obj
class mthdobj(obj):
    def __init__(self, name = ''):
        self.name = name

    def __repr__(self):
        return super().__repr__().replace(')', '%r)' % self.name)

















