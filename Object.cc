
#include <iostream> 
#include <vector>
#include <string>
typedef std::string str;

template<class T>
struct Object
{
    typedef std::vector<Object> objv;

    char parens[2]; //parens around the expression. set to ['\0', '\0'] by default
    objv args; //the arugments that are passed to the function, not usually utilized
    T base;

    Object(T pBase,
           objv args = *new objv,
           char parens0 = '\0',
           char parens1 = '\0'):
                base(pBase),
                args(args){
        parens[0] = '\0';
        parens[1] = '\0';
    }


    str tostr(){
        str ret = "";
        ret += base;
        ret += "@";
        if(parens[0])
            ret += parens[0];
        std::vector<Object<int> >::iterator i = args.begin(); //position shoudl never go above 127 arguments
        while(i != args.end()){
            ret += i++->tostr() + ", ";
        }
        // for (std::vector<Object<int> >::iterator i = args.begin(); i != args.end(); ++i){
        //     ret += (*i);
        //     ret += ", ";
        // }
        if(parens[1])
            ret += parens[1];

        return ret;

    }
};

class Executable
{
    // int (*minus)(int,int) = subtraction;  
    public:
        Executable();
        // virtual Object x();
};