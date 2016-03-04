class obj(object):
    def __repr__(self):
        return type(self).__qualname__ + '()'
