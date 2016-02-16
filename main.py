if __name__ == '__main__':
    import sys
    from omfile import omfile
    if len(sys.argv) == 1:
        filepath = 'testcode.om'
    else:
        filepath = sys.argv[1] #0 is 'main.py'
        if __debug__:
            if '.py' in sys.argv[1]:
                filepath = '/Users/westerhack/code/python/Omega/testcode.om'
    f = omfile(filepath)
    if __debug__:
        print(f)
    print('--')
    evald = f.eval()
    print('--\n\nDone.')
    if __debug__:
        print('locals:',evald)


"""
@f1(arg)
   @f2
   def func(): pass

"""




















