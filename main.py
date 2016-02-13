class control:
    endline = '\n\r;'
    comment = '#'
    whitespace = ' \t\x0b\x0c' + endline
    # digits = '0123456789abcdefABCDEF.,oOxX'
    # punctuation = '!"#$%&\'()*+-,/:;<=>?@[\\]^`{|}~._'
    # parensr = '[({'
    # parensl = '])}'
    # parenstr = parensl + parensr + '\'\"'

    # delims = '!#$&;@\\`' + parenstr

    # binfuncs = ('-?>', '<?-', '->', '<-', '==', '**', '<=', '>=', '!=', '>>', '<<',\
    #          '+', '*', '-', '/', '%', '~', '|', '&', '^', '<', '>', '=')
    # unarayl = ()
    # unarayr = ()

    funcs = binfuncs + unarayl + unarayr
    @staticmethod
    def allin(totest, tocompareto):
        for s in totest:
            if s not in tocompareto:
                return False
        return True

class wfile:
    def __init__(self, filepath, encoding = 'utf-8'):
        self.filepath = filepath
        import codecs
        with codecs.open(filepath, 'r', encoding) as f:
            self.rawtext = wfile._reducelines(f.read())

    @staticmethod
    def _reducelines(rawt):
        """ remove comments and blank lines"""
        ret = ''
        for char in rawt:
            if char in control.comment:
            if char in control.endline:
        return ret
    def __str__(self):
        return str(vars(self))


if __name__ == '__main__':
    f = wfile('testcode.wc')
    print(f)

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

























