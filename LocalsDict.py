class localsdict(dict):
    lastval = '$'
    def __init__(self):
        import Group
        super().__init__({localsdict.lastval: Group.group()})
