#include <iostream> 
// #include <stack>
#include <stack>
#include <fstream>
#include <string>
namespace consts
{
    static const char TAB =  '\t';
    static const char ESCP = '\\';
    static const char ENDL = '\n';
    static const char CMMNT = '#';

};

// static const inline void printv(std::stack<char> * v){
//     for (std::stack<char>::const_iterator i = v->begin(); i != v->end(); ++i)
//         std::cout << *i;
//     std::cout << std::endl;
// }
static const inline void prints(std::stack<char> * s){
    std::stack<char> dcopy = *s;
    while(!dcopy.empty()){
        std::cout << dcopy.top() << ", ";
        dcopy.pop();
    }
    std::cout << std::endl;
}
static const inline void prints(std::stack<std::string> * s){
    std::stack<std::string> dcopy = *s;
    while(!dcopy.empty()){
        std::cout << dcopy.top() << ", ";
        dcopy.pop();
    }
    std::cout << std::endl;
}
static const inline void prerr(std::string errmsg){ std::cerr << std::endl << "Error: " << errmsg << '.' << std::endl; }
static const inline void abort(std:: string errmsg){ prerr(errmsg); std::abort(); }
static const inline void abortexp(std:: string s){ prerr("'" + s + "' Expected"); std::abort(); }
static const inline bool isalph(char c){ return false;}
static const std::stack<char> readfile(std::string inpf) {
    std::stack<char> v;
    std::ifstream myfile;
    char c;
    bool escaped, commented;
    myfile.open(inpf);
    while(myfile >> std::noskipws >> c){
        switch(c){
            case consts::ESCP:
                if(!escaped){
                    escaped = true;
                    break;
                }
            case consts::ENDL:
                if(!escaped)
                    commented = true;
                else
                    continue;
            case consts::CMMNT:
                if(!escaped){
                    commented = !commented;
                }
                if(v.size() == 0 || v.top() == consts::ENDL) //ignore multiple empty lines
                    continue;    
            default:
                escaped = false;
                if(!commented)
                    v.push(c);
        }
    }
    myfile.close();
    return v;    
}
static const std::stack<std::string> getstack(std::stack<char> * data){
    std::stack<std::string> dstack;
    std::string prev = "";
    while(data->size() != 0){
        prev = prev + data->top();
        data->pop();
        std::cout << prev << std::endl;
    }
    return dstack;
}
static const void exec(std::stack<char>* v){ }
int main(int argc, char const *argv[])
{
    std::stack<char> data = readfile("testcode.wc");
    std::stack<std::string> dstack = getstack(&data);
    prints(&data);
    prints(&dstack);
    std::cout << "executing" << std::endl;
    exec(&data);
    return 0;
}
/*
{--------------------------------------------------------------}
program Cradle;

{--------------------------------------------------------------}
{ Constant Declarations }

const TAB = ^I;

{--------------------------------------------------------------}
{ Variable Declarations }

var Look: char;              { Lookahead Character }
                              
{--------------------------------------------------------------}
{ Read New Character From Input Stream }

procedure GetChar;
begin
   Read(Look);
end;

{--------------------------------------------------------------}
{ Report an Error }

procedure Error(s: string);
begin
   WriteLn;
   WriteLn(^G, 'Error: ', s, '.');
end;


{--------------------------------------------------------------}
{ Report Error and Halt }

procedure Abort(s: string);
begin
   Error(s);
   Halt;
end;


{--------------------------------------------------------------}
{ Report What Was Expected }

procedure Expected(s: string);
begin
   Abort(s + ' Expected');
end;

{--------------------------------------------------------------}
{ Match a Specific Input Character }

procedure Match(x: char);
begin
   if Look = x then GetChar
   else Expected('''' + x + '''');
end;


{--------------------------------------------------------------}
{ Recognize an Alpha Character }

function IsAlpha(c: char): boolean;
begin
   IsAlpha := upcase(c) in ['A'..'Z'];
end;
                              

{--------------------------------------------------------------}

{ Recognize a Decimal Digit }

function IsDigit(c: char): boolean;
begin
   IsDigit := c in ['0'..'9'];
end;


{--------------------------------------------------------------}
{ Get an Identifier }

function GetName: char;
begin
   if not IsAlpha(Look) then Expected('Name');
   GetName := UpCase(Look);
   GetChar;
end;


{--------------------------------------------------------------}
{ Get a Number }

function GetNum: char;
begin
   if not IsDigit(Look) then Expected('Integer');
   GetNum := Look;
   GetChar;
end;


{--------------------------------------------------------------}
{ Output a String with Tab }

procedure Emit(s: string);
begin
   Write(TAB, s);
end;




{--------------------------------------------------------------}
{ Output a String with Tab and CRLF }

procedure EmitLn(s: string);
begin
   Emit(s);
   WriteLn;
end;

{--------------------------------------------------------------}
{ Initialize }

procedure Init;
begin
   GetChar;
end;


{--------------------------------------------------------------}
{ Main Program }

begin
   Init;
end.
{--------------------------------------------------------------}
*/