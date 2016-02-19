namespace ObjectTypes{
    class Base {
    protected:
        void* base;
    public:
        Base();
        Base(void* base): base(base){};
        std::string tostr(){
            std::cout << "TODO: this" << std::endl;
            return "";
        }
    };

    class String: public Base {
    public:
        String(std::string base): Base() {};
        // String(std::string base): Base(base){};
        
    };
}