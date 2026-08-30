// Supported C/C++ Subset Sample Program
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Declarations & Assignments
    int count = 10;
    string password = "secret_password_123";
    char buffer[256];

    // C++ Stream Output
    std::cout << "Starting Security Audit Demo..." << count;

    // Unsafe Function Calls (Vulnerabilities Detected by Static Security Analyzer)
    gets(buffer);

    string command = "rm -rf /tmp/data";
    system(command);

    if (count > 0) {
        printf("Audit Complete.\n");
    } else {
        printf("Audit Error.\n");
    }

    return 0;
}
