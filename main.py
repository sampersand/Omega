if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        filepath = 'testcode.om'
    else:
        filepath = sys.argv[1] #0 is 'main.py'
        if __debug__:
            if sys.argv[1] == '/Users/westerhack/code/python/Omega/main.py':
                filepath = 'testcode.om'
    from omfile import omfile
    f = omfile(filepath)
    if __debug__:
        print(f)
        print('--')
    evald = f.eval()
    if __debug__:
        print(evald)

"""
@f1(arg)
   @f2
   def func(): pass

"""














