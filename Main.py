
if __name__ == '__main__':
    import sys
    from File import file

    if len(sys.argv) != 2:
        quit(f"usage: {sys.argv[0]} <file>")
    if __debug__:
        from time import time_ns
        start = time_ns()
    f = file(sys.argv[1])
    if __debug__:
        print(f)
        print('--')
    ldict = f.eval()
    if __debug__:
        print('--')
        if '$dnd' not in ldict:
            print('Locals Str ::', str(ldict),'\n')
            print('Locals Repr ::', repr(ldict),'\n')
            print('Total Elapsed Time ::', time_ns() - start, 'nanoseconds\n')
 
