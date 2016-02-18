#include <vector>
namespace FileConstants
{
    static const Constants::str TEST;
    static const Constants::str ESCP = "\\";
    static const Constants::str ENDL = "\n;";
    static const Constants::str CMMNT = "#";
    static const Constants::str LNBRK = "\n\r";
    static const Constants::str DATADEF = "@";
    static const Constants::str NONBRWHTSPC = " \t\x0b\x0c";
    static const Constants::str WHTSPC = NONBRWHTSPC + LNBRK;
    static const Constants::str QUOTES = "'\"`";
    template<class T>
    static const Constants::str getvs(const std::vector<T> * v, bool commas = false){
        Constants::str ret = "";
        for (typename std::vector<T>::const_iterator i = v->begin(); i != v->end(); ++i)
            ret += *i + (commas ? ", " : "");
        return ret;
    }
    static const inline bool in(char c, Constants::str s){
        return s.find(c) != Constants::str::npos;
    }
}

class File
{
    std::vector<Constants::str> pv; //processed vector
    Constants::str filename;
    std::queue<char> readfile();
    std::queue<Constants::str> parsefile(const std::queue<char> rawdat);
    std::vector<Constants::str> proccessfile(const std::queue<Constants::str> rawdat);
    public:
        File() {};
        File(Constants::str pfile): filename(pfile){
            pv = proccessfile(parsefile(readfile()));
        };
        Constants::str tostr();
};
Constants::str File::tostr(){
    return "File '" + filename + "':\n==[start]==\n\n" + FileConstants::getvs(&pv) +"\n\n==[ end ]==";
}
std::vector<Constants::str> File::proccessfile(std::queue<Constants::str> dat){
    std::vector<Constants::str> ret;
    return ret;
}
std::queue<Constants::str> File::parsefile(std::queue<char> rawdat) {
    //break function 
    std::queue<Constants::str> ret;
    Constants::str last = "";
    char c;
    while(!rawdat.empty()){
        c = rawdat.front();
        last += c;
        if(FileConstants::in(c, FileConstants::ENDL)){
            ret.push(last);
            last.clear();
        }
        rawdat.pop();
    }
    if(not last.empty()){
        ret.push(last);
    }
    return ret;
}
std::queue<char> File::readfile() {
        using namespace FileConstants;
        std::queue<char> q;
        std::ifstream myfile;
        myfile.open(filename);
        if(not myfile.is_open()){
            std::cerr << "Invalid file! '" << filename << '\'' << std::endl;
            return q;
        }
        char c, data = 0b00; //0b10 is escaped, 0b01 is commented
        while(myfile >> std::noskipws >> c){
            //ik, ik, you can use switch statements...
            if(in(c, ESCP) and not (data & 0b10)){
                data ^= 0b10;
            } else if(in(c, CMMNT) and not (data & 0b10)){
                data ^= 0b01;
            } else if(in(c, LNBRK) or in(c, ENDL)){
                if(in(c, ENDL) and not (data & 0b10) and
                   c != q.back())  {
                    q.push(c);
                    // q.push(ENDL[0]);
                }
                //data &= 0b10 //remove comments
            } else {
                data &= 0b01;
                if(not (data & 0b01)){
                    q.push(c);
                }
            }
        }
        myfile.close();
        return q;    
}
