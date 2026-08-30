// Comprehensive Vulnerable C++ Program for Security Audit Demo
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

int main() {
    // SEC001 & SEC003: Hardcoded sensitive credentials & weak password
    string password = "secret_password_123";
    string default_pwd = "admin123";

    // SEC002: Hardcoded API Key
    string api_key = "AIzaSyD1234567890abcdef";

    // Variables for memory buffer operations
    string input_buffer = "user_data";
    string dest_buffer = "destination_memory";
    string format_spec = "format_string";

    // SEC006: Unsafe gets() call
    gets(input_buffer);

    // SEC007: Unsafe strcpy() call (signature: string, string)
    strcpy(dest_buffer, input_buffer);

    // SEC008: Unsafe sprintf() call (signature: string, string)
    sprintf(dest_buffer, format_spec);

    // SEC004: Dynamic SQL Injection vector
    string query = "SELECT * FROM users WHERE name=" + input_buffer;
    db_query(query);

    // SEC005: Command Injection vector
    string sys_cmd = "ls -la " + input_buffer;
    system(sys_cmd);

    // SEC009: Weak pseudo-random number generator
    int rand_val = rand();

    // SEC010: Resource Leak (open without matching close)
    int file_fd = open("audit_log.txt", 1);
    read(file_fd, input_buffer, 100);

    std::cout << "Security audit scan sequence completed." << rand_val;
    return 0;
}
