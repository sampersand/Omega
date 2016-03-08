class ArgumentError(SyntaxError):
    def __init__(self, reason = None):
        super(ArgumentError, self).__init__()
        self.arg = arg
        