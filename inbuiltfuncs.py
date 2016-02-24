def evalfunc(base, eles, locls):
    name = str(base)
    if name == 'disp':
        from obj import strobj
        args, sep, end = ('', ), ', ', '\n'
        if len(eles) > 0:
            from obj import nullobj
            if not eles[0].base.isnull():
                if not eles[0]:
                    eles[0].eval(locls)
                    args = (locls['$'], )
                else:
                    def gen(eles, locls):
                        for ele in eles:
                            ele.eval(locls)
                            yield locls['$'].base.strobj.scrub()
                    args = gen(eles, locls)
            if len(eles) > 1:
                if not eles[1].base.isnull():
                    if __debug__:
                        assert isinstance(eles[1].base, strobj)
                    sep = eles[1].base.scrub()
                if len(eles) > 2:
                    if not eles[2].base.isnull():
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
        (iftrue if locls['$'].base else iffalse).eval(locls)
    elif name == 'skip':
        pass #keep this here.
    elif name == 'del':
        if not eles:
            locls.reset()
        else:
            if __debug__:
                assert len(eles) == 1, "only 1 thing after the semicolon..."
            if not eles[0]:
                del locls[str(eles[0])]
            else:
                for ele in eles[0]:
                    del locls[str(ele)]
        if '$' not in locls:
            from group import group
            locls['$'] = group()
    elif name == 'for':
        if __debug__:
            assert len(eles) == 2, 'for:(init;cond;inc):(statements)'
            assert len(eles[0]) == 3, 'for:(init;cond;inc):(statements)'
        eles[0][0].eval(locls) #initialization
        while True:
            eles[0][1].eval(locls) #evaluate the condition
            if not locls['$'].base:
                break
            eles[1].eval(locls) #execute the statements
            eles[0][2].eval(locls) #increment
    # elif name == 'abort':
    #     pass
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
    elif name in control.opers['binary']['assignment']: #aka assignment
        d = name[0] == '-'
        name = name[1:-1]
        eles[1 - d].eval(locls)
        for ele in eles[slice(d or None, 1 - d or None, None)]:
            _ioperfunc(name, ele, locls)
    elif name in control.opers['binary']['logic']:
        eles[0].eval(locls)
        for ele in eles[1:]:
            last = locls['$']
            ele.eval(locls)
            locls['$'] = last.base.comparebase(last, name, locls['$'])
    elif name in control.opers['unary']['l'] or name in control.opers['unary']['r']:
        evalunary(base, eles, locls)
    else:
        eles[0].eval(locls)
        for ele in eles[1:]:
            last = locls['$']
            ele.eval(locls)
            if locls['$'] == 9:
                assert locls['$'] is not locls['a']
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
        # locls['$'] = locls[str(ele)]
    else:
        if str(ele) not in locls:
            locls[str(ele)] = locls['$']
            assert 0, 'what happens here?? ' + str(ele)+' ' +str(locls) #oh i know, its when the ele isnt defined
            return
        else:
            import control
            from group import group
            group(base = control.allopers[sname], args = [locls['$'], locls[str(ele)]]).eval(locls)
            import copy
            locls[str(ele)] = copy.deepcopy(locls['$'])


def evalunary(base, eles, locls):
    name = str(base)
    import control
    if __debug__:
        assert base is eles.base #not necessary, just figured.
        if name in control.opers['unary']['l']:
            assert eles[0].base.isnull() #unary l should have null on the left (~X has no left term)
        else:
            assert len(eles) == 1
    if name == '>+' or name == '>-':
        from group import group
        from obj import numobj
        group(base = control.allopers['-%s>'%name[1]], args = [ group(base = numobj(1)), eles[1]]).eval(locls)
    elif name == '+<' or name == '-<':
        from group import group
        from obj import numobj
        import copy;
        ret = copy.deepcopy(locls[str(eles[0])]);
        group(base = control.allopers['-%s>'%name[0]], args = [ group(base = numobj(1)), eles[0]]).eval(locls)
        locls['$'] = ret
    elif name == '!':
        import math
        eles[0].eval(locls)
        locls['$'].base.base = math.factorial(locls['$'].base.base)
    elif name == 'pos' or name == 'neg':
        eles[1].eval(locls)
        locls['$'].base.base = locls['$'].base.base
    elif name == 'b~':
        eles[1].eval(locls)
        locls['$'].base.base = ~locls['$'].base.base
    else:
        raise SyntaxError("Unknown unary function '{}'!".format(name))
    


















