#include <iostream>
#include <vector>
#include "ObjectTypes.cc"
#include "Object.cc"
#include "File.cc"
int main(){
    File file("/Users/westerhack/code/python/Omega/testcode.om");

    #ifndef str
    #define str std::string
    #endif
    std::cout << file.tostr() << std::endl;

    std::vector<Object> v;
    v.push_back(*new Object(new ObjectTypes::String("argument 1")));
    v.push_back(*new Object(new ObjectTypes::String("argument 2")));
    Object o(new ObjectTypes::String("function name"), v);
    o.setpar('(', ')');

    std::cout << o.tostr() << std::endl;
    return 0;
}









