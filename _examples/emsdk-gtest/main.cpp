#include <iostream>
#include <zlib.h>
#include <gtest/gtest.h>


static std::string greet(const std::string& name) {
    std::ostringstream s;
    s << "Hello " << name << "!";
    return s.str();
}


int main()
{
    std::cout << "Using zlib version: " << zlibVersion() << std::endl;
    std::cout << "Greet: " << greet(" emsdk!") << std::endl;
    EXPECT_EQ(std::string("Hello World!"), greet("World"));
}
