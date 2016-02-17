//name picle / phycle / cycle, but with some weird spelling at the front
#include <iostream> 
// #include <stack>
#include <stack>
#include <vector>
#include <fstream>
#include <string>
typedef char letter;
namespace consts
{
    static const letter TAB =  '\t';
    static const letter ESCP = '\\';
    static const letter ENDL = '\n';
    static const letter CMMNT = '#';

    static const void printv(std::vector<letter> * v){
        for (std::vector<letter>::const_iterator i = v->begin(); i != v->end(); ++i)
            std::cout << *i;
        std::cout << std::endl;
    }

    template<class T>
    static const void prints(const std::stack<T> * s){
        std::stack<T> dcopy = *s;
        while(!dcopy.empty()){
            std::cout << dcopy.top() << ", ";
            dcopy.pop();
        }
        std::cout << std::endl;
    }

    static const void prerr(std::string errmsg){
        std::cerr << std::endl << "Error: " << errmsg << '.' << std::endl;
    }

    static const void abort(std:: string errmsg){
        prerr(errmsg);
        std::abort();
    }

    static const void abortexp(std:: string s){
        prerr("'" + s + "' Expected");
        std::abort();
    }

};
class File
{
    std::stack<letter> rawstack;
    std::string filename;
    std::stack<letter> readfile();
    public:
        File() {};
        File(std::string pfile) {filename = pfile; rawstack = readfile();};
};
std::stack<letter> File::readfile() {
        std::stack<letter> v;
        std::ifstream myfile;
        letter c;
        letter info = 0b000; //0b100 is escaped 0b010 is block comment, 0b001 
        myfile.open(filename);
        if(not myfile.is_open()){
            std::cerr << "Invalid file! '" << filename << '\'' << std::endl;
            return v;
        }
        while(myfile >> std::noskipws >> c){
            switch(c){
                default:
                    info &= 0b011; //remove the escape
                    if(info){
                        std::cout << "A" << std::endl;
                        std::abort();
                    }
                    info ^= 1;
                    std::cout << "@" << std::endl;
            }
            // switch(c){
            //     case consts::ESCP:
            //         if(!escaped){
            //             escaped = true;
            //             break;
            //         }
            //     case consts::ENDL:
            //         if(!escaped)
            //             commented = true;
            //         else
            //             continue;
            //     case consts::CMMNT:
            //         if(!escaped){
            //             commented = !commented;
            //         }
            //         if(v.size() == 0 || v.top() == consts::ENDL) //ignore multiple empty lines
            //             continue;    
            //     default:
            //         escaped = false;
            //         if(!commented)
            //             v.push(c);
            // }
        }
        myfile.close();
        return v;    
    }
/*
static const inline bool isalph(letter c){ return false;}
static const std::stack<std::string> getstack(std::stack<letter> * data){
    std::stack<std::string> dstack;
    std::string prev = "";
    while(data->size() != 0){
        prev = prev + data->top();
        data->pop();
        std::cout << prev << std::endl;
    }
    return dstack;
}
static const void exec(std::stack<letter>* v){ }
*/
int main()
{
    // File file ("~/desktop/pass.txt");
    File file("/Users/westerhack/code/python/Omega/testcode.om");
    // std::stack<letter> data = readfile("testcode.wc");
    // std::stack<std::string> dstack = getstack(&data);
    // prints(&data);
    // prints(&dstack);
    // std::cout << "executing" << std::endl;
    // exec(&data);
    return 0;
}









