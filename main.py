class control:
    endline = '\n\r;'
    comment = '#'
    escape = '\\'
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
    # funcs = binfuncs + unarayl + unarayr

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
            self.striptext = wfile._striptext(f.read())
        self.tokens = wfile.tokenize(self.striptext)

    @staticmethod
    def _striptext(rawt):
        """ remove comments and blank lines"""
        strippedtext = ''
        for char in rawt:
            if not strippedtext:
                strippedtext += char
            elif strippedtext[-1] in control.comment:
                if char in control.endline or char in control.comment:
                    strippedtext = strippedtext[:-1]
            else:
                if char in control.endline and strippedtext[-1] in control.endline:
                    continue
                strippedtext += char
        return strippedtext
    
    @staticmethod
    def tokenize(rawt):
        return rawt
    def __str__(self):
        return str(self.tokens)
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

























