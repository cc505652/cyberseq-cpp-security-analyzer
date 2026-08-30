<<<<<<< HEAD
# cyberseq-cpp-security-analyzer
Compiler-based C/C++ static security analyzer with AST-driven vulnerability detection, security scoring, and AI-assisted explanations.
=======
# AI-Powered Secure Code Analyzer

> **Educational C/C++ Subset Compiler & Static Security Audit Platform**

This compiler supports a well-defined procedural subset of the C/C++ language intended for educational purposes and academic project demonstrations. It integrates classical compilation theory (Lexing, Parsing, AST Generation, Symbol Table Management, Semantic Validation) with deterministic Static Application Security Testing (SAST) and Large Language Model (LLM) educational explanations.

---

## 1. Supported C/C++ Language Features

* **Program Entry**: `int main() { ... return 0; }` or `int main(void)`
* **Data Types**: `int`, `float`, `char`, `bool`, `string`, `const`
* **Declarations & Assignments**: Variable initialization, reassignment, and array declarations (`char buf[256];`)
* **Arithmetic Operators**: `+`, `-`, `*`, `/`, `%`
* **Comparison Operators**: `==`, `!=`, `<`, `>`, `<=`, `>=`
* **Logical Operators**: `&&`, `||`, `!`
* **Stream Operators**: `<<` (LSHIFT), `>>` (RSHIFT)
* **Control Statements**: `if`, `else`, `while`, `for`, `break`, `continue`
* **Input / Output Statements**: `printf()`, `scanf()`, `std::cout <<`, `std::cin >>`, `print()`
* **Security & System Built-ins**: `gets()`, `strcpy()`, `sprintf()`, `strcat()`, `system()`, `db_query()`, `rand()`, `secure_rand()`, `open()`, `read()`, `write()`, `close()`
* **Preprocessor Directives**: Skips `#include <header>` and `#include "header"` directives transparently
* **Comments**: Single-line (`//`) and multi-line (`/* ... */`) comments

---

## 2. Unsupported Features & Known Limitations

The following advanced C++ features are **intentionally unsupported** to maintain simplicity for an academic final-year project:

* **Object-Oriented Programming**: `class`, `struct`, inheritance, polymorphism, access modifiers (`public`, `private`).
* **Templates & Generics**: Function templates, class templates.
* **STL Containers & Iterators**: `std::vector`, `std::map`, `std::string` class methods, `std::unique_ptr`.
* **Pointers & References**: `*ptr`, `&ref`, pointer arithmetic, `delete`, `new`.
* **Advanced C++ Constructs**: Lambda expressions, exception handling (`try`/`catch`), operator overloading, namespaces (`using namespace std;` line is skipped).

---

## 3. Quick Start

### Launch Desktop GUI IDE
```bash
python main.py
```

### Run Automated Unit Tests
```bash
pytest tests/
```
>>>>>>> 01e9159 (Initial commit: C/C++ Secure Code Analyzer with static audit engine, rule-specific AI fallbacks, ReportLab generator, and unit tests)
