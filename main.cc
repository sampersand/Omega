#include "File.cc"
#include "Object.cc"
#include <vector>
typedef std::vector<Object<void*> > objv;
int main()
{
    File file("/Users/westerhack/code/python/Omega/testcode.om");
    std::cout << file.tostr() << std::endl;
    objv v;
    v.push_back(new Object<double>(123.4));
    Object<double> o(99.23, v);
    o.parens[1] = '1';
    std::cout << o.tostr() << std::endl;
    return 0;
}









