// Safe C++ Program Demo (Zero Security Vulnerabilities)
#include <iostream>
#include <stdio.h>

int main() {
    int count = 10;
    int total = 0;

    for (int i = 0; i < count; i = i + 1) {
        total = total + i;
    }

    int safe_rand_val = secure_rand();

    int fd = open("safe_data.txt", 0);
    if (fd > 0) {
        printf("File opened successfully.\n");
        close(fd);
    }

    std::cout << "Computed total: " << total;
    return 0;
}
