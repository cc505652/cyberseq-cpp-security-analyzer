// Unsupported C++ Syntax Example
// Note: This file demonstrates features OUTSIDE the educational compiler subset.
#include <iostream>
#include <vector>

// UNSUPPORTED: Class definitions and object-oriented programming
class SecurityVault {
private:
    int secret_key;
public:
    SecurityVault(int key) : secret_key(key) {}
};

// UNSUPPORTED: Template functions
template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    // UNSUPPORTED: STL Container vectors
    std::vector<int> numbers = {1, 2, 3};

    // UNSUPPORTED: Exception handling
    try {
        throw 404;
    } catch (int err) {
        std::cout << "Error: " << err;
    }

    return 0;
}
