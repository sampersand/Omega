def evalfunc(base, eles, locls):
    name = str(base)
    if name == 'disp':
        from obj import strobj
        args, sep, end = ('', ), ', ', '\n'
        if len(eles) > 0:
            from obj import nullobj
            if not isinstance(eles[0].base, nullobj):
                if not eles[0]:
                    args = (eles[0], )
                else:
                    def gen(eles, locls):
                        for ele in eles:
                            ele.eval(locls)
                            yield locls['$']
                    args = gen(eles, locls)
            if len(eles) > 1:
                if not isinstance(eles[1].base, nullobj):
                    if __debug__:
                        assert isinstance(eles[1].base, strobj)
                    sep = eles[1].base.scrub()
                if len(eles) > 2:
                    if not isinstance(eles[2].base, nullobj):
                        if __debug__:
                            assert isinstance(eles[2].base, strobj)
                        end = eles[2].base.scrub()
        print(*args, sep = sep, end = end)
    elif name == 'if':
        from group import group
        cond, iftrue, iffalse = group(), group(), group()
        if len(eles) > 0:
            cond = eles[0]
            if len(eles) > 1:
                iftrue = eles[1]
                if len(eles) > 2:
                    iffalse = eles[2]
                    if __debug__:
                        if len(eles) > 3:
                            raise SyntaxError('Not allowed to have more than 3 arguments for if statements!')
        cond.eval(locls)
        print('@', cond, iftrue, iffalse, locls,sep='\t|\t')
        (iftrue if cond else iffalse).eval(locls)
    else:
        raise SyntaxError("Unknown function '{}'!".format(name))
def evaloper(base, eles, locls):
    name = str(base)
    import control
    if __debug__:
        assert base is eles.base #shouldn't be any other way...
        assert name in control.allopers #how would it get passed here??
    if name in control.alldelims:
        if name in control.delims['endline'][0]:
            for ele in eles:
                ele.eval(locls) # _should_ set locls['$'] by itself
        elif name in control.delims['applier'][0]:
            eles[0].base.eval(eles[1:], locls)
        elif name in control.delims['arraysep'][0]:
            from group import group
            from obj import arrayobj
            ret = arrayobj()
            for ele in eles:
                ele.eval(locls)
                ret.base.append(locls['$'])
            locls['$'] = group(base = ret)
        else:
            raise SyntaxError("Special Operator '{}' isn't defined yet!".format(name))
    elif '<' == name[0] and name[-1] == '-' or name[0] == '-' and name[-1] == '>': #aka assignment
        d = name[0] == '-'
        name = name[1:-1]
        eles[1 - d].eval(locls)
        for ele in eles[slice(d or None, 1 - d or None, None)]:
            _ioperfunc(name, ele, locls)
    elif name in {'<', '>', '<=', '>=', '==', '=', '<>', '!='}:
        eles[0].eval(locls)
        for ele in eles[1:]:
            last = locls['$']
            ele.eval(locls)
            locls['$'] = locls['$'] if locls['$'].base.comparebase(name, last) else last
    else:
        eles[0].eval(locls)
        for ele in eles[1:]:
            last = locls['$']
            ele.eval(locls)
            locls['$'].base.updatebase(name, last.base)

def _ioperfunc(sname, ele, locls): #sname == stripped name
    """

        !!! DO NOT USE STR IN THE FUTURE. IT WILL MESS EVERYTHING UP !!!

        aka, remove locls[str(eles)]


        hm... take the following code:

                a <- 4;
                b <- 2;
                1 + 2 -+> a -+> b 

        regardless of how '-+>' is percieved,

                a == 7

        However, should:

                b == 5 #(aka the '$' from 1 + 2 and b's old value)#

        or should:

                b == 9 #(aka the '$' right before it's evaluated and b's old value)#

        I think i'll go wtih the second option.
    """

    if sname == '':
        locls[str(ele)] = locls['$']
    else:
        if str(ele) not in locls:
            assert 0, 'what happens here??'
            locls[str(ele)] = locls['$']
            return
        else:
            import control
            from group import group
            g = group(base = control.allopers[sname], args = [locls[str(ele)], locls['$']])
            g.eval(locls)
            import copy
            locls[str(ele)] = copy.deepcopy(locls['$'])





















