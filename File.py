import Control
import codecs
import copy
from Group import group
from LocalsDict import localsdict
class file:
    def __init__(self, filepath, control = None, encoding = 'utf-8'):
        if control == None:
            control = Control.control()
        self.control = control
        self.filepath = filepath
        with codecs.open(filepath, 'r', encoding) as f:
            self.lines = self._genlines(f.read())
    def __str__(self):
        ret = "file '%s':\n==[start]==" % self.filepath
        lines = self.lines.linestr()
        ret += lines
        return ret + '\n==[ end ]=='
    def _genlines(self, rawt):
        def striptext(self, rawt):
            """ remove comments and blank lines"""
            ret = ''
            data = 0b00 # 0b10 = escaped, 0b01 = commented
            for char in rawt:
                if data & 0b10:
                    ret += '\\' + char
                    data &= 0b01
                elif char in self.control.escape  and not data & 0b10:
                    data ^= 0b10
                elif char in self.control.comment and not data & 0b10:
                    data ^= 0b01
                elif char in self.control.linebreak:
                    if char in self.control.delims['endline'][0] and\
                         not (data & 0b10) and ret and \
                         ret[-1] not in self.control.delims['endline'][0]:
                        ret += self.control.delims['endline'][0][0]
                    # if not data & 0b10 and (not ret or ret[-1] not in self.control.linebreak): #so no duplicate \ns
                        # ret += char
                    # data &= 0b10 #remove comments
                else:
                    # if data & 0b10:
                    #     ret += self.control.escape
                    data &= 0b01
                    if not data & 0b01:
                        ret += char
            if '@eof' in ret:
                ret = ret[0:ret.find('@eof')]
            return self.control.delims['endline'][0][0] + ret + self.control.delims['endline'][0][0]
        def tokenize(self, rawt):
            """ goes thru, and splits them up first based upon control.sortedopers and then by control.punctuation. """
            def createtokens(rawt):
                for oper in self.control.sortedopers:
                    if oper in rawt:
                        par = rawt.partition(oper)
                        if rawt[rawt.index(oper) - 1] in self.control.escape:
                            return [par[0] + par[1]] + createtokens(par[2])
                        return createtokens(par[0]) + [par[1]] + createtokens(par[2])
                for punc in self.control.punctuation:
                    if punc in rawt:
                        par = rawt.partition(punc)
                        if rawt[rawt.index(punc) - 1] in self.control.escape:
                            return [par[0] + par[1]] + createtokens(par[2])
                        return createtokens(par[0]) + [par[1]] + createtokens(par[2])
                return [rawt]
            tokens = [token for token in createtokens(rawt) if token]
            ret = []
            currentquote = None
            for token in tokens:
                if token in self.control.allquotes and token:
                    if currentquote == None:
                        ret.append(token)
                        currentquote = token
                    else:
                        if token == currentquote:
                            currentquote = None
                        ret[-1] += token
                elif currentquote:
                    ret[-1] += token
                else:
                    ret.append(token)
            #@define stuff
            linep = 0
            while linep < len(ret): 
                if ret[linep] and ret[linep] in self.control.datadef:
                    self.control.applyrules(ret.args.pop(0))
                linep+=1
            ret2 = []
            for token in ret:
                if token:
                    if token[0] not in self.control.allquotes:
                        if token.strip(self.control.nbwhitespace):
                            if __debug__:
                                assert token[-1] not in self.control.allquotes, token
                            ret2.append(token.strip(self.control.nbwhitespace))
                    else:
                        ret2.append(token)

            ret = []
            for e in (e.strip(self.control.nbwhitespace) for e in ret2):
                if not ret or not e or e not in self.control.delims['endline']\
                    or str(ret[-1].data) not in self.control.delims['endline']:
                    ret.append(group(e, control = self.control))
            return ret
            return [group(e, control = self.control) for e in (e.strip(self.control.nbwhitespace) for e in ret2) if e]
        def compresstokens(self, linetokens):
            def compresstokens(linegrp): #this is non-stable
                ret = group(control = self.control, parens = linegrp.parens) #universe
                while len(linegrp) != 0:
                    ele = linegrp.pop(0) #pop(0) is inefficient for list. update this in the future
                    if str(ele) not in self.control.allparens:
                        ret.append(ele)
                    else:
                        toappend = group(control = self.control)
                        parens = {str(ele):1}
                        while sum(parens.values()) > 0 and len(linegrp) != 0:
                            toappend.append(linegrp.pop(0))
                            if str(toappend[-1]) in self.control.allparens:
                                last = str(toappend[-1])
                                if last in self.control.parens['l']:
                                    if last not in parens:
                                        parens[last] = 0
                                    parens[last] += 1
                                if last in self.control.parens['r']:
                                    if __debug__:
                                        assert self.control._invertparen(last) in parens, "unmatched paren '{}'!".format(last)
                                    parens[self.control._invertparen(last)] -= 1
                        if __debug__:
                            assert str(toappend[-1]) in self.control.allparens, toappend #the last element should be in allparens
                        toappend.parens = (str(ele), str(toappend.pop()))
                        toappend = compresstokens(toappend)
                        ret.append(toappend)
                return ret
            def findhighest(linegrp):
                if __debug__:
                    assert linegrp or linegrp.data, linegrp
                    #change this in the future when boolean for linegrp changes
                highest = None
                for elep in range(len(linegrp)):
                    ele = str(linegrp[elep])
                    if ele in self.control.allopers and (highest == None or
                            self.control.allopers[ele].priority >=\
                            self.control.allopers[str(linegrp[highest].data)].priority):
                        highest = elep
                if __debug__:
                    if highest == None:
                    #     linegrp.data = self.control.delims['applier'][1]
                    #     return linegrp
                        raise SyntaxError("no operator for string '{}'!".format(repr(linegrp))) # ':' was still required
                return linegrp[highest]
            def fixtkns(line):
                #combine tokens using order of operations
                if not line:
                    # if __debug__:
                        # assert 0, "when does this ever happen??"
                    return line
                if len(line) == 1: #if the line is literally a single element, usually: ([blah, blah])
                    if len(line[0]) == 0: #if the line[0] is literally a single constant, aka: blah
                        return line[0]
                    else:
                        return fixtkns(line[0])
                fhp = findhighest(line)
                if __debug__:
                    assert isinstance(fhp, group), 'expected a group for fhp! (not %s)' % fhp
                    assert not fhp and fhp.data, fhp
                ret = group(data = fhp.data, control = self.control, parens = line.parens)
                current = group(control = self.control)
                while line:
                    e = line.pop(0) #was formerly .pop(0)
                    if e.data == ret.data:
                        # if current: #these used to strip out null values, but is ignored now
                        #     ret.append(fixtkns(current))
                        ret.append(fixtkns(current))
                        current = group(control = self.control)
                    else:
                        current.append(e)
                if current:
                    ret.append(fixtkns(current))

                return ret
            return fixtkns(compresstokens(group(args = linetokens, control = self.control)))
        return compresstokens(self, tokenize(self, striptext(self, rawt)))
    def eval(self):
        ldict = localsdict(self.control)
        self.lines.evaluate(ldict)
        return ldict
