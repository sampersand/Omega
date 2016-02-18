// #include <queue>
// #include <fstream>
// #include <iostream> 
#include <vector>
#include "Constants.cc"
#include "Object.cc"
#include "ObjectConstants.cc"
#include "File.cc"

#ifndef str
#define str Constants::str
#endif
int main(){
    File file("/Users/westerhack/code/python/Omega/testcode.om");

    std::cout << file.tostr() << std::endl;

    std::vector<Object<str> > v;
    v.push_back(*new Object<> ("argument 1"));
    v.push_back(*new Object<> ("argument 2"));
    Object<str> o("function", v);
    o.setpar('(', ')');

    std::cout << o.tostr() << std::endl;
    return 0;
}









