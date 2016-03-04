from Objects import obj
class mthdobj(obj):
    def __init__(self, name):
        self.name = name
assert 0, repr(mthdobj(1))
class funcobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)
class operobj(mthdobj):
    def __init__(self, name, priority, attrstr):
        """ name is used to print, attrstr is used to actually execute the function. """
        super().__init__(name)
        self.priority = priority
        self.attrstr = attrstr
class ufuncobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)
