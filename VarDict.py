class vardict(dict):
    lastval = '$'
    def __init__(self):
        import Group
        super().__init__({vardict.lastval: Group.group()})
