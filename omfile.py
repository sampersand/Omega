import control
from group import group
class omfile:
    def __init__(self, filepath, encoding = 'utf-8'):
        self.filepath = filepath
        import codecs
        with codecs.open(filepath, 'r', encoding) as f:
            self.striptext = omfile._striptext(f.read())
        self.tokens = omfile._tokenize(self.striptext)
        import copy
        self.lines = omfile._compresstokens(copy.deepcopy(self.tokens))
    
    def __str__(self):
        def getl(linep, l):
            if not l:
                if __debug__:
                    assert str(l) == ';' or str(l) == '', str(l) #no other known case atm
                return linep, ''
            ret = ''
            if len(l) > 0:
                for ele in l:
                    if ele.basestr not in control.delims['endline'][0]:
                        ret += '\n{}:  \t{}'.format(linep, ele)
                        linep += 1
                    else:
                        e = getl(linep, ele)
                        ret += e[1]
                        linep += e[0]
            return linep, ret
        return "file '{}':\n==[start]==\n{}\n\n==[ end ]==".format(self.filepath, getl(0, self.lines)[1])

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
            elif char in control.linebreak:
                if char in control.delims['endline'][0] and not (data & 0b10):
                    ret += control.delims['endline'][0][0]
                # if not data & 0b10 and (not ret or ret[-1] not in control.linebreak): #so no duplicate \ns
                    # ret += char
                # data &= 0b10 #remove comments
            else:
                # if data & 0b10:
                #     ret += control.escape
                data &= 0b01
                if not data & 0b01:
                    ret += char
        if '@eof' in ret:
            ret = ret[0:ret.find('@eof')]
        return ret + control.delims['endline'][0]
    
    @staticmethod
    def _tokenize(rawt):
        """ goes thru, and splits them up first based upon control.sortedopers and then by control.punctuation. """
        def tokenize(rawt):
            for oper in control.sortedopers:
                if oper in rawt:
                    par = rawt.partition(oper)
                    if rawt[rawt.index(oper) - 1] in control.escape:
                        return [par[0] + par[1]] + tokenize(par[2])
                    return tokenize(par[0]) + [par[1]] + tokenize(par[2])
            for punc in control.punctuation + control.delims['endline'][0]:
                if punc in rawt:
                    par = rawt.partition(punc)
                    if rawt[rawt.index(punc) - 1] in control.escape:
                        return [par[0] + par[1]] + tokenize(par[2])
                    return tokenize(par[0]) + [par[1]] + tokenize(par[2])
            return [rawt]
        tokens = [token for token in (token.strip(control.nbwhitespace) for token in tokenize(rawt)) if token]
            
        ret = []
        currentquote = None
        for token in tokens:
            if token in control.allquotes:
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
            if ret[linep] and ret[linep] in control.datadef:
                control.applyrules(ret.pop(0))
            linep+=1
        from obj import obj
        return [obj.frombase(v) for v in ret]

    @staticmethod
    def _compresstokens(linetokens):
        def compresstokens(linegrp): #this is non-stable
            ret = group(parens = linegrp.parens) #universe
            while linegrp:
                ele = linegrp.pop(0) #pop(0) is inefficient for list. update this in the future
                if str(ele) not in control.allparens:
                    ret.append(group(base = ele))
                else:
                    toappend = group()
                    parens = {str(ele):1}
                    while sum(parens.values()) > 0 and linegrp:
                        toappend.append(linegrp.pop(0))
                        if str(toappend[-1]) in control.allparens:
                            last = str(toappend[-1])
                            if last in control.parens['l']:
                                if last not in parens:
                                    parens[last] = 0
                                parens[last] += 1
                            if last in control.parens['r']:
                                if __debug__:
                                    assert control._invertparen(last) in parens, "unmatched paren '{}'!".format(last)
                                parens[control._invertparen(last)] -= 1
                    if __debug__:
                        assert str(toappend[-1]) in control.allparens, toappend #the last element should be in allparens
                    toappend.parens = (str(ele), str(toappend.pop()))
                    toappend = compresstokens(toappend)
                    ret.append(toappend)
            return ret
        def findhighest(linegrp):
            if __debug__:
                assert linegrp or linegrp.base, linegrp
                #change this in the future when boolean for linegrp changes
            highest = None
            for elep in range(len(linegrp)):
                ele = linegrp[elep].basestr
                assert 'displ' not in control.allopers, control.allopers.keys()
                if ele in control.allopers and (highest == None or
                        control.allopers[ele] > control.allopers[linegrp[highest].basestr]):
                    highest = elep
            if __debug__:
                if not highest:
                    raise SyntaxError("no operator for string '{}'!".format(linegrp))
            return highest
        def fixtkns(line):
            #combine tokens using order of operations
            if not line: return line
            if len(line) == 1: #if the line is literally a single element
                if len(line[0]) == 0: #if the line is literally a single constant
                    return line[0]
                else:
                    return fixtkns(line[0])
            fhp = findhighest(line)
            
            if __debug__:
                assert isinstance(line[fhp], group), 'expected a group for fhp! (not %s)' % line[fhp]
            ret = group(base = line[fhp].base, parens = line.parens)
            current = group()
            while line:
                e = line.pop(0) #was formerly .pop(0)
                if e.base == ret.base:
                    if current:
                        ret.append(fixtkns(current))
                    current = group()
                else:
                    current.append(e)
            if current:
                ret.append(fixtkns(current))
            return ret
        return fixtkns(compresstokens(group(args = linetokens)))
    
    def eval(self):
        import control
        locls = {'$': control.consts['null']}
        self.lines.eval(locls)
        if '$' in locls and not __debug__:
            del locls['$']
        return locls
