from Objects.FuncObj import funcobj
class operobj(funcobj):
    """
    The class that represents operators on objects.
    """
    def __init__(self, base, priority):
        super().__init__(base, None)
        self.priority = priority

    def __repr__(self):
        return 'operobj({},{})'.format(self.base, self.priority)

    def eval(self, args, ldict):
        print('trying to eval:',self,args,ldict)