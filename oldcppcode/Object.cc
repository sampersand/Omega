#include <iostream>
#include <vector>
#include <map>
class Object
{
    protected:
        typedef std::vector<Object> objv;
        char lpar, rpar; //parens around the arguments, set to '\0' usually
        objv args; //the arugments that are passed to the function, not usually utilized
        ObjectTypes::Base base;
    public:
        Object(ObjectTypes::Base base, objv args = *new objv, char lpar = '\0', char rpar = '\0'):
            base(base), args(args), lpar(lpar), rpar(rpar){}

        std::string tostr(){
            std::string ret = "";
            ret += base.tostr();
            if(lpar)
                ret += lpar;
            if(args.size() != 0){
                std::vector<Object>::iterator i = args.begin(); //position shoudl never go above 127 arguments
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
        virtual ~Executable();
        // virtual Object x();
};
namespace ObjectConstants{
    typedef std::map<std::string, Object> localsmap;
}
class Operator: protected Object {
    protected:
        char priority;
        int (*func)(int, int);
    public:
        Operator(ObjectTypes::String base, char priority, int (*func)(int,int)): Object(base), priority(priority){};
    
};
namespace ObjectConstants{

    static const std::map<std::string, Operator> opers;
};












