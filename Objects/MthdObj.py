from Objects import obj
class mthdobj(obj):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return super().__repr__().replace(')', '%r)' % self.name)
class funcobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)
class operobj(mthdobj):
    def __init__(self, name, priority, attrstr):
        """ name is used to print, attrstr is used to actually execute the function. """
        super().__init__(name)
        self.priority = priority
        self.attrstr = attrstr
    def __repr__(self):
        return super().__repr__().replace(')', ', %r, %r)' % (self.priority, self.attrstr))
class ufuncobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)