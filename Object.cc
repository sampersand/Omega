#include <vector>
template<typename T = Constants::str>
class Object
{
    typedef std::vector<Object<> > objv;
    char lpar, rpar; //parens around the arguments, set to '\0' usually
    objv args; //the arugments that are passed to the function, not usually utilized
    T base;
public:
    Object(T base, objv args = *new objv, char lpar = '\0', char rpar = '\0'):
        base(base), args(args), lpar(lpar), rpar(rpar){}

    Constants::str tostr(){
        Constants::str ret = "";
        ret += base;
        if(lpar)
            ret += lpar;
        if(args.size() != 0){
            typename std::vector<Object>::iterator i = args.begin(); //position shoudl never go above 127 arguments
            ret += i->tostr();
            while(++i != args.end())
                ret += ", " + i->tostr();
        }
        if(rpar)
            ret += rpar;
        return ret;
    }
    void setpar(char l, char r){lpar = l; rpar = r;}
    void setargs(objv pargs){args = pargs;}
};

class Executable
{
    // int (*minus)(int,int) = subtraction;  
    public:
        Executable();
        // virtual Object x();
};
class Operator: private Object<Constants::str> {
public:
    Operator();
    
};






