#include <string>
#include <queue>
#include <vector>
typedef std::string str;
namespace Constants
{
    static const str ESCP = "\\";
    static const str ENDL = "\n;";
    static const str CMMNT = "#";
    static const str LNBRK = "\n\r";
    static const str DATADEF = "@";
    static const str NONBRWHTSPC = " \t\x0b\x0c";
    static const str WHTSPC = NONBRWHTSPC + LNBRK;
    static const str QUOTES = "'\"`";

    static const str getvs(const std::vector<str> * v, bool commas = false){
        str ret = "";
        for (std::vector<str>::const_iterator i = v->begin(); i != v->end(); ++i)
            ret += *i + (commas ? ", " : "");
        return ret;
    }

    template<class T>
    static const str getqs(const std::queue<T> * q){
        str ret = "";
        std::queue<T> qcopy = *q;
        while(!qcopy.empty()){
            ret += qcopy.front();
            qcopy.pop();
        }
        return ret;
    }

    static const inline bool in(char c, str s){
        return s.find(c) != str::npos;
    }
};
