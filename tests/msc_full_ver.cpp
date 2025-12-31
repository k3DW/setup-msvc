// Copyright 2025 Braden Ganetsky
// Distributed under the Boost Software License, Version 1.0.
// https://www.boost.org/LICENSE_1_0.txt

#include <cstdlib>
#include <iostream>
#include <string>

#define STR_(x) #x
#define STR(x) STR_(x)

int main(int argc, const char* argv[]) {
    if (argc != 2) {
        std::cout << "Requires an argument\n";
        return EXIT_FAILURE;
    }

    const std::string expected = argv[1];
    const std::string actual = STR(_MSC_FULL_VER);

    std::cout << "Expected: " << expected << "\n";
    std::cout << "Actual:   " << actual << "\n";
    if (expected == actual) {
        std::cout << "Success\n";
        return EXIT_SUCCESS;
    } else {
        std::cout << "Failure\n";
        return EXIT_FAILURE;
    }
}
