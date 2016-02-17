#include <vector>
class Object
{
    typedef std::vector<Object> objv;
    char parens[2]; //parens around the expression. set to null by defualt
    objv args;
    public:
        Object();
        Object(objv args): args(args){};
        Object(objv args): args(args){};
};