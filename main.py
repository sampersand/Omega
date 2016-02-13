class control:
    __all__ = []
    #these are borrowed from "import string"
    digits = '0123456789abcdefABCDEF.,oOxX'
    punctuation = '!"#$%&\'()*+-,/:;<=>?@[\\]^`{|}~._'
    parensr = '[({'
    parensl = '])}'
    parenstr = parensl + parensr + '\'\"'

    delims = '!#$&;@\\`' + parenstr
    whitespace = ' \t\n\r\x0b\x0c'
    endline = '\n\r;'
    comment = '#'

    binfuncs = ('-?>', '<?-', '->', '<-', '==', '**', '<=', '>=', '!=', '>>', '<<',\
             '+', '*', '-', '/', '%', '~', '|', '&', '^', '<', '>', '=')
    unarayl = ()
    unarayr = ()

    funcs = binfuncs + unarayl + unarayr
    @staticmethod
    def allin(totest, tocompareto):
        for s in totest:
            if s not in tocompareto:
                return False
        return True

class file:
    def __init__(self, filepath, rawtext, values = None, stack = None):
        self.filepath = filepath
        self.rawtext = rawtext
        self.tokens = file.parsetokens(self.rawtext)
        self.values = values or {}
        self.stack = stack or []

    @staticmethod
    def parsetokens(rawt):
        #generator
        def tokenize(rawt):
            ctokens = []
            prev = ''
            for c in rawt:
                if c not in control.delims and c not in control.whitespace:
                    prev += c
                else:
                    if prev:
                        yield prev
                    prev = ''
                    yield c
            if prev:
                yield prev
        def condensewhitespace(tokengen):
            genline = []
            commented = False
            for t in tokengen:
                if t in control.comment:
                    commented = not commented
                    continue
                if t in control.endline:
                    yield genline
                    genline.clear()
                    commented = False
                elif not commented and t.strip(control.whitespace):
                    genline.append(t)
            yield genline

        def condensetokens(linegen):
            for line in linegen:
                if not line:
                    continue
                yield line
        return tuple(tuple(x) for x in condensetokens(condensewhitespace(tokenize(rawt))))

    @staticmethod
    def fromfile(filepath, encoding = 'utf-8'):
        import codecs
        with codecs.open(filepath, 'r', encoding) as f:
            rawtext = f.read()
        return file(filepath, rawtext)

    def __str__(self):
        return str(self.tokens)

    def evalexpr(self, fname, *args):
        if __debug__:
            assert len(args) == 2, args
        args = (self.values[args[0]] if args[0] in self.values else args[0], \
                self.values[args[1]] if args[1] in self.values else args[1])

        if fname == '+':
            self.values['_'] = float(args[0]) + float(args[1])

        elif fname == '*':
            self.values['_'] = float(args[0]) * float(args[1])

        elif fname == '->' or fname == '<-':
            fn = fname == '->'
            self.values[args[not fn]] = args[fn]
            if '_' in self.values:
                del self.values['_']
        else:
            raise SyntaxError("Expression value of '{}' with args '{}'' isn't implemented yet!".format(fname, args))
    def eval(self):
        for line in self.tokens:
            lineiter = iter(line)
            for ele in lineiter:
                if ele in control.binfuncs:
                    if __debug__:
                        assert len(self.stack) != 0 or '_' in self.values,\
                            'cannot ' + ele + ' with an empty stack (values: ' + str(self.values) + ')'
                        if len(self.stack) > 0 and isinstance(self.stack[-1], str):
                            assert self.stack[-1] not in control.parensr, 'cannot ' + ele + ' with a paren on the left'
                    assert 0, help(memoryview)
                    n = next(lineiter)
                    l = self.values['_'] if '_' in self.values else self.stack.pop()
                    self.evalexpr(ele, n, l)
                    print(self.values)
                else:
                    self.stack.append(ele)
        return self.values


if __name__ == '__main__':
    f = file.fromfile('testcode.wc')
    print(f)
    print(f.eval())

"""
@f1(arg)
   @f2
   def func(): pass

"""







"""
('1,234.5', '*', '(', '1e4', '-', '2.4', ')', '-?>', 'b')
1,234.5
--
*
1,234.5
--
(
*
1,234.5
--
1e4
(
*
1, 234.5
--
2.4
-
1e4
(
*
1, 234.5
"""

























