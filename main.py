class element:
    def __init__(self, val, **kwargs):
        pass
class node:
    def __init__(self, name, args = [], parens = None):
        self.name = name
        self.parens = ['', ''] or parens
        self.args = args
    def __str__(self):
        return self.name + self.parens[0] + ', '.join(self.args) + self.parens[1]
    def __repr__(self):
        # return 'node({}, parens={}, args={})'.format(self.name, self.parens, self.args)
        return '{}{}<{}>{}'.format(self.name, self.parens[0], self.args, self.parens[1])
class control:
    inbuilt_functions = {
        'assign': {
            '->': element('->', func=lambda l, r: None)
        }
    }
            # {'unaryl':_cdict({'~':_oper('~', 13, 1)}),\
             # 'unaryr':_cdict({'!':_oper('!', 14, 2)}),\
             # 'binoper':_cdict(\
                # {'assign': _cdict({                                                                                   \
                #     '->' : _oper('->',  0), '<-' : _oper('<-',  0), '-?>': _oper('-?>', 0), '<?-': _oper('<?-', 0) }),\
                #  'iassaign': _cdict({                                                                                 \
                #     '+=' : _oper('+=',  0), '-=' : _oper('-=',  0), '*=' : _oper('*=',  0), '/=' : _oper('/=',  0),   \
                #     '**=': _oper('**=', 0), '%=' : _oper('%=',  0), '>>=': _oper('>>=', 0), '<<=': _oper('<<=', 0),   \
                #     '|=' : _oper('|=',  0), '&=' : _oper('&=',  0), '^=' : _oper('^=',  0)                         }),\
                #  'math'  : _cdict({                                                                                   \
                #     '+'  : _oper('+',  10), '-'  : _oper('-',  10), '*'  : _oper('*',  11), '/'  : _oper('/',  11),   \
                #     '%'  : _oper('%',  11), '**' : _oper('**', 12)                                                 }),\
                #  'bitwise':_cdict({                                                                                   \
                #     '>>' : _oper('>>',  9), '<<' : _oper('<<',  9), '|'  : _oper('|',   4), '^'  : _oper('^',   5),   \
                #     '&'  : _oper('&',   6)                                                                         }),\
                #  'equality': _cdict({                                                                                 \
                #     '>'  : _oper('>',   8), '<'  : _oper('<',   8), '<=' : _oper('<=',  8), '>=' : _oper('>=',  8),   \
                #     '='  : _oper('=',   7), '!=': _oper('!=',   7)                                                 }),\
                #  })
    parens = {"l":('(','[','{'), "r":(')',']','}')}
    escapechar = '\\'
    quotechar = '\''
    tokensepchar = ' '
    linesepchar = '\n'

class file:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath) as f:
            self.rawlines = ''.join(f.readlines()).split(control.linesepchar)
        self.rawlines = [l.strip('\n') for l in self.rawlines if l.strip()[0] != '#']
        self.lines = file._parseraw(self.rawlines)

    def __str__(self):
        return "file '{}':\n{}".format(self.filepath, '\n'.join([str(e) for e in self.lines]))

    def _parseraw(rawl):
        import re #regex
        def fixline(rawl):
            """ TODO: This. It should do 'a*b' --> 'a * b'. """ 
            # for parentype in control.parens['l'], control.parens['r']:
                # for p in parentype:
                # rawl = re.sub('([^ ]{}[^ ])')
            return rawl

        def tokenize(rawl):
            ret = ['']
            isqouted = False
            rawiter = iter(rawl)
            for char in rawiter:
                if char == control.escapechar:
                    ret[-1] += next(rawiter)
                    continue
                if char == control.quotechar:
                    isqouted = not isqouted
                    if isqouted:
                        ret.append(control.quotechar)
                    continue
                if isqouted:
                    ret[-1] += char
                else:
                    if char != control.tokensepchar:
                        ret[-1] += char
                    else:
                        ret.append('')
            return [v for v in ret if v]
        def join(tokens):
            ret = []
            while tokens:
                t = tokens.pop(0)
                if t not in control.parens['l'] and t not in control.parens['r']:
                    ret.append(node(t))

                elif t in control.parens['l']:
                    ret[-1].parens[0] = t
                    ret[-1].args.append(ret[-1])

                elif t in control.parens['r']:
                    tokens.insert(0, t)
                    print(tokens)
                    break
            return ret
        return tuple(join(tokenize(fixline(line))) for line in rawl)
if __name__ == '__main__':
    f = file('testcode.wc')
    print(f)

"""
@f1(arg)
   @f2
   def func(): pass

"""



















