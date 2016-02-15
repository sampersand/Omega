class omobj:
    def __init__(self, base, evalfunc = None):
        self.base = omobj._getbase(base)
        self.evalfunc = evalfunc

    @staticmethod
    def _getbase(base):
        import control
        if base == '':
            return base
        if base[0] in control.allquotes:
            if __debug__:
                assert base[-1] in control.allquotes
            return base
        else:
            try:
                return int(base)
            except ValueError:
                try:
                    return float(base)
                except ValueError:
                    try:
                        return complex(base)
                    except ValueError:
                        return str(base)

    def __str__(self):
        return str(self.base)

    def __repr__(self):
        return 'omobj({},evalfunc={})'.format(repr(self.base), repr(self.evalfunc))

    def __bool__(self):
        return bool(str(self))

    def eval(self, eles, locls):
        # print('attempting to eval eles \'{}\' with locls \'{}\' in omobj \'{}\''.format(eles, locls, self))
        if self.evalfunc != None:
            self.evalfunc(eles, locls)
        else:
            # print('evalfunc is none, returning self.base ({})'.format(self.base))
            locls['$'] = self.base

class oper(omobj):

    def __init__(self, base, priority, evalfunc):
        super().__init__(base, evalfunc)
        self.priority = priority

    def __repr__(self):
        return 'oper({},{},{})'.format(self.base, self.priority, self.evalfunc)

    def __str__(self):
        return self.base
    def __lt__(self, other):
        return self.priority < other.priority

    def eval(self, eles, locls):
        print('attempting to eval eles \'{}\' with locls \'{}\' in oper \'{}\''.format(eles, locls, self))
        # if __debug__:
        #     if eles.basestr not in control.allopers:
        #         raise SyntaxError('operator \'{}\' isn\'t defined'.format(eles.basestr))
        if self.evalfunc == None:
            self._specialoper(eles, locls)
        elif eles:
            eles[0].eval(locls)
            ret = locls['$']
            name = eles.basestr
            for ele in eles[1:]:
                ele.eval(locls)
                ret = self.evalfunc(ret, locls['$'])
            locls['$'] = ret# x = y
        print("evaluated '{}' with locals {}, and getting {}".format(eles, locls, locls['$']))

    def _specialoper(self, eles, locls):
        from group import group
        import control
        print('todo: uncomment things in _specialoper')
        name = eles.basestr
        if name in control.alldelims:
            if name in control.delims['arraysep']:
                eles[0].eval(locls)
                ret = []
                name = eles.basestr
                for ele in eles:
                    ele.eval(locls)
                    ret.append(locls['$'])
                locls['$'] = group(val = ret)# x = y
                return
            else:
                raise SyntaxError('Special Operator \'{}\' isn\'t defined yet!'.format(name))
        elif name == ':':
            if eles[0].basestr in locls:
                assert 0, 'when does this ever happen?'
                locls[eles[0].basestr].eval(eles[1])
            else:
                eles[0].base.eval(eles[1],locls)
        elif name == '||' or name == '&&':
            eles[0].eval(locls)
            element = locls['$']
            if name == '&&' and not element or name == '||' and element:
                return element
            eles[1].eval(locls)
        else:
            direc = name in ['<-', '<?-', '<+-', '<--', '<*-', '</-', '<**-', '<%-', '<&-', '<|-', '<^-', '<<-', '<>-']
            if direc == 1:
                eles[1].eval(locls)
                value =locls['$']
                key = eles[0].basestr
            else:
                eles[0].eval(locls)
                value =locls['$']
                key = eles[1].basestr
                name = '<' + name[1:-1] + '-'
            if __debug__:
                assert name == '<-'  or\
                       name == '->'  or\
                       name == '<?-' or\
                       name == '-?>' or\
                       key in locls, '\'{}\' needs to be defined to perform \'{}\' on it!'.format(key, name)
            if   name == '<-'  : locls[key] = value
            elif name == '<?-' : locls[key] = value if value else (locls[key] if key in locls else None)
            elif name == '<+-' : locls[key] += value
            elif name == '<--' : locls[key] -= value
            elif name == '<*-' : locls[key] *= value
            elif name == '</-' : locls[key] /= value
            elif name == '<**-': locls[key] **= value
            elif name == '<%-' : locls[key] %= value
            elif name == '<&-' : locls[key] &= value
            elif name == '<|-' : locls[key] |= value
            elif name == '<^-' : locls[key] ^= value
            elif name == '<<-' : locls[key] <<= value
            elif name == '<>-' : locls[key] >>= value
            if direc == 0: #swap the return value
                locls['$'] = locls[key]

class func(omobj):
    def __init__(self, base):
        super().__init__(base, None)
    def eval(self, eles, locls):
        print('attempting to eval eles \'{}\' with locls \'{}\' in func \'{}\''.format(eles, locls, self))
        if self.evalfunc == None:
            print('evalfunc is none, returning self.base ({})'.format(self.base))
            return self.base
        return None