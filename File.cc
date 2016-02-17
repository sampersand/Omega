
#include "Constants.cc"
#include <iostream> 
#include <stack>
#include <queue>
#include <vector>
#include <fstream>
#include <string>

typedef std::string str;

class File
{
    std::vector<str> pv; //processed vector
    str filename;
    std::queue<char> readfile();
    std::queue<str> parsefile(const std::queue<char> rawdat);
    std::vector<str> proccessfile(const std::queue<str> rawdat);
    public:
        File() {};
        File(str pfile): filename(pfile){
            pv = proccessfile(parsefile(readfile()));
        };
        str tostr();
};
str File::tostr(){
    return "File '" + filename + "':\n==[start]==\n\n" + Constants::getvs(&pv) +"\n\n==[ end ]==";
}
std::vector<str> File::proccessfile(std::queue<str> dat){
    std::vector<str> ret;

    return ret;
}
std::queue<str> File::parsefile(std::queue<char> rawdat) {
    //break function 
    std::queue<str> ret;
    str last = "";
    char c;
    while(!rawdat.empty()){
        c = rawdat.front();
        last += c;
        if(Constants::in(c, Constants::ENDL)){
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
        using namespace Constants;
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
