from Objects import obj
class nullobj(obj):
    """
    The class that represents a null object.
    In reality, it is representing a 'None' object type, but there is no way to access 'None'.
    """
    def __init__(self, isuser = False):
        super().__init__(None)
        self.isuser = isuser

    def __repr__(self):
        return 'nullobj()'

    def isnull(self):
        return not self.isuser

    def __str__(self):
        return 'null'