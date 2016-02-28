#include <iostream>
#include <vector>
#include <fstream>
#include <queue>
namespace FileConstants
{
    static const std::string TEST;
    static const std::string ESCP = "\\";
    static const std::string ENDL = "\n;";
    static const std::string CMMNT = "#";
    static const std::string LNBRK = "\n\r";
    static const std::string DATADEF = "@";
    static const std::string NONBRWHTSPC = " \t\x0b\x0c";
    static const std::string WHTSPC = NONBRWHTSPC + LNBRK;
    static const std::string QUOTES = "'\"`";
    template<class T>
    static const std::string getvs(const std::vector<T> * v, bool commas = false){
        std::string ret = "";
        for (typename std::vector<T>::const_iterator i = v->begin(); i != v->end(); ++i)
            ret += *i + (commas ? ", " : "");
        return ret;
    }
    static const inline bool in(char c, std::string s){
        return s.find(c) != std::string::npos;
    }
}

class File
{
    std::vector<std::string> pv; //processed vector
    std::string filename;
    std::queue<char> readfile();
    std::queue<std::string> parsefile(const std::queue<char> rawdat);
    std::vector<std::string> proccessfile(const std::queue<std::string> rawdat);
    public:
        File() {};
        File(std::string pfile): filename(pfile){
            pv = proccessfile(parsefile(readfile()));
        };
        std::string tostr();
};
std::string File::tostr(){
    return "File '" + filename + "':\n==[start]==\n\n" + FileConstants::getvs(&pv) +"\n\n==[ end ]==";
}
std::vector<std::string> File::proccessfile(std::queue<std::string> dat){
    std::vector<std::string> ret;
    return ret;
}
std::queue<std::string> File::parsefile(std::queue<char> rawdat) {
    //break function 
    std::queue<std::string> ret;
    std::string last = "";
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
