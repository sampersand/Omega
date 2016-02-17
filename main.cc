#include "File.cc"
#include "Object.cc"

int main()
{
    File file("/Users/westerhack/code/python/Omega/testcode.om");
    std::cout << file.tostr() << std::endl;
    Object o;
    return 0;
}









