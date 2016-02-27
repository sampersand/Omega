class localsdict(dict):
    lastval = '$'
    def __init__(self):
        import Group
        super().__init__({localsdict.lastval: Group.group()})
    def __str__(self):
        return '{' + ', '.join(str(v) + ' : ' + str(self[v]) for v in self) + '}'