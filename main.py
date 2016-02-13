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
        ret = ''
        data = 0b00 # 0b10 = escaped, 0b01 = commented
        for char in rawt:
            if char in control.escape  and not data & 0b10:
                data ^= 0b10
            elif char in control.comment and not data & 0b10:
                data ^= 0b01
            elif char in control.endline:
                if not data & 0b10 and ret[-1] not in control.endline: #so no duplicate \ns
                    ret += char
                data &= 0b10
            else:
                data &= 0b01
                if not data & 0b01:
                    ret += char
        return ret
    
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

























