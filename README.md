# CyberSeq — AI-Assisted C/C++ Static Security Analyzer

> **Compiler-Based Static Analysis + Cybersecurity + AI-Assisted Security Explanation**

CyberSeq is a compiler-based static security analyzer for a practical subset of C/C++ source code. It combines **Compiler Design, Cybersecurity, Static Analysis, and AI-assisted vulnerability explanation** into a single desktop application.

The system processes source code through a compiler-style pipeline consisting of:

- Lexical Analysis
- Syntax Analysis
- Abstract Syntax Tree (AST) Generation
- Semantic Analysis
- Symbol Table Management
- AST-based Security Analysis
- AI-assisted Vulnerability Explanation
- Security Scoring
- PDF Security Report Generation

CyberSeq is intentionally designed as a **practical C/C++ subset analyzer rather than a complete C/C++ compiler**. The goal is to demonstrate the concepts clearly while maintaining a complete, functional, and understandable implementation suitable for an academic project.

---

## Authors

- **Chinmay Chauhan**
- **Swapnil Singh**
- **Himanshu Nepaliya**

---

# Table of Contents

- [Project Overview](#project-overview)
- [Why CyberSeq?](#why-cyberseq)
- [Core Workflow](#core-workflow)
- [Architecture](#architecture)
- [Key Features](#key-features)
  - [Lexical Analysis](#1-lexical-analysis)
  - [Syntax Analysis](#2-syntax-analysis)
  - [Abstract Syntax Tree](#3-abstract-syntax-tree)
  - [Semantic Analysis](#4-semantic-analysis)
  - [Symbol Table](#5-symbol-table)
  - [Static Security Analysis](#6-static-security-analysis)
  - [AI Explanation Engine](#7-ai-explanation-engine)
  - [Security Scoring](#8-security-scoring)
  - [PDF Reporting](#9-pdf-security-reporting)
  - [Desktop GUI](#10-desktop-gui)
- [Security Rules](#security-rules)
- [AI Architecture](#ai-architecture)
- [C/C++ Subset](#cc-subset)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Running an Analysis](#running-an-analysis)
- [Testing](#testing)
- [Example](#example)
- [Error Handling](#error-handling)
- [Design Philosophy](#design-philosophy)
- [Advantages](#advantages)
- [Limitations](#limitations)
- [Industry Relevance](#industry-relevance)
- [Academic Relevance](#academic-relevance)
- [Future Scope](#future-scope)
- [Project Status](#project-status)
- [License](#license)

---

# Project Overview

Modern software can be syntactically correct and still contain serious security vulnerabilities.

For example, a program may successfully pass:
```text
Lexical Analysis
       ↓
Syntax Analysis
       ↓
AST Generation
       ↓
Semantic Analysis
````

while still containing:

```text
Hardcoded Credentials
SQL Injection
Command Injection
Unsafe Buffer Operations
Weak Randomness
Resource Leaks
```

CyberSeq addresses this problem by extending the compiler pipeline with a static security-analysis layer.

The project combines three primary domains:

### Compiler Design

The compiler pipeline performs:

* Lexical analysis
* Parsing
* AST generation
* Semantic analysis
* Symbol-table management

### Cybersecurity

The generated AST is analyzed using deterministic security rules to identify common insecure coding patterns.

### Artificial Intelligence

AI is **not responsible for detecting vulnerabilities**.

Instead:

> **The security engine detects the vulnerability → the AI explains the vulnerability.**

This separation makes the security analysis deterministic, reproducible, testable, and easier to explain during an academic demonstration.

---

# Why CyberSeq?

Traditional compiler analysis answers questions such as:

> "Is this program syntactically and semantically valid?"

Security analysis asks a different question:

> "Is this valid program also safe to execute or maintain?"

CyberSeq connects these two areas:

```text
Compiler Design
      +
Abstract Syntax Tree
      +
Static Security Rules
      +
AI-Assisted Explanation
      =
CyberSeq
```

The AST produced by the compiler becomes the foundation for security analysis.

---

# Core Workflow

```text
                  ┌─────────────────────┐
                  │    C/C++ Source     │
                  │        Code         │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Lexical Analyzer  │
                  │       PLY/Lex       │
                  └──────────┬──────────┘
                             │
                           Tokens
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Syntax Analyzer   │
                  │      PLY/Yacc       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │         AST         │
                  │ Abstract Syntax Tree│
                  └──────────┬──────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
   ┌─────────────────────┐       ┌─────────────────────┐
   │ Semantic Analyzer   │       │ Security Analyzer   │
   │                     │       │                     │
   │ • Types             │       │ • Security Rules    │
   │ • Declarations      │       │ • AST Traversal     │
   │ • Scope             │       │ • CWE Mapping       │
   │ • Assignments       │       │ • Severity          │
   └──────────┬──────────┘       └──────────┬──────────┘
              │                             │
              │                             ▼
              │                  ┌─────────────────────┐
              │                  │ Security Findings   │
              │                  └──────────┬──────────┘
              │                             │
              │                             ▼
              │                  ┌─────────────────────┐
              │                  │   AI Explanation    │
              │                  │       Engine        │
              │                  └──────────┬──────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                  ┌─────────────────────┐
                  │   GUI / PDF Report  │
                  │                     │
                  │ • Tokens            │
                  │ • AST               │
                  │ • Semantic Errors   │
                  │ • Security Findings │
                  │ • AI Explanations   │
                  │ • Security Score    │
                  └─────────────────────┘
```

---

# Architecture

CyberSeq follows a modular layered architecture.

```text
CyberSeq
│
├── Input Layer
│      └── C/C++ Source Code
│
├── Compiler Layer
│      ├── Lexer
│      ├── Parser
│      ├── AST
│      ├── Semantic Analyzer
│      └── Symbol Table
│
├── Security Layer
│      ├── Security Rules
│      ├── AST Traversal
│      ├── Severity Classification
│      └── Security Score
│
├── AI Layer
│      ├── AI Helper
│      ├── OpenAI Provider
│      ├── Ollama Provider
│      └── Offline Fallback
│
├── Presentation Layer
│      ├── Desktop GUI
│      └── Analysis Dashboard
│
└── Reporting Layer
       └── PDF Report Generator
```

---

## Compiler Layer

```text
Source Code
     ↓
Lexer
     ↓
Tokens
     ↓
Parser
     ↓
AST
     ↓
Semantic Analyzer
     ↓
Symbol Table + Semantic Diagnostics
```

---

## Security Layer

```text
AST
 ↓
Security Rule Engine
 ↓
AST Traversal
 ↓
Security Findings
 ↓
Severity Classification
 ↓
Security Score
```

---

## AI Layer

```text
Security Finding
       ↓
   AI Helper
       ↓
Provider Selection
       │
       ├───────────────┐
       ▼               ▼
    OpenAI           Ollama
       │               │
       └───────┬───────┘
               │
               ▼
       AI Explanation
               │
               ▼
       GUI / PDF Report
```

If the configured LLM provider is unavailable, CyberSeq can use a deterministic offline fallback.

---

# Key Features

## 1. Lexical Analysis

CyberSeq uses **PLY Lex** to convert source code into a stream of tokens.

The lexer handles:

* Keywords
* Identifiers
* Integer literals
* Floating-point literals
* String literals
* Character literals
* Boolean literals
* Operators
* Parentheses
* Brackets
* Braces
* Semicolons
* Comments
* Lexical errors

Example:

```cpp
int age = 20;
```

can produce:

```text
INT
ID(age)
ASSIGN
INT_LITERAL(20)
SEMI
```

Source locations are tracked so that later compiler and security stages can associate findings with the relevant source line.

---

# 2. Syntax Analysis

CyberSeq uses **PLY Yacc** to validate the grammatical structure of the supported language.

The parser supports constructs such as:

* Variable declarations
* Assignments
* Expressions
* Arithmetic operators
* Relational operators
* Logical operators
* `if`
* `else`
* `while`
* `for`
* `return`
* `print`
* Supported function-style calls

Syntax errors are reported with source locations where available.

---

# 3. Abstract Syntax Tree

After successful parsing, CyberSeq constructs an **Abstract Syntax Tree (AST)**.

The AST represents the logical structure of the source program while removing unnecessary syntactic details.

Example:

```cpp
int age = 20;
```

Conceptual AST:

```text
Program
└── VarDecl
    ├── Type: int
    ├── Name: age
    └── Initializer
        └── Literal
            └── 20
```

For:

```cpp
age = age + 5;
```

the AST can be represented as:

```text
Assignment
├── Identifier(age)
└── BinaryExpression(+)
    ├── Identifier(age)
    └── Literal(5)
```

The AST is subsequently consumed by semantic analysis and security analysis.

---

# 4. Semantic Analysis

Syntax correctness does not guarantee semantic correctness.

CyberSeq performs semantic analysis using the AST and Symbol Table.

It checks:

* Undeclared variables
* Duplicate declarations
* Type compatibility
* Invalid assignments
* Scope-related errors
* Function argument-count mismatches where applicable

Example:

```cpp
int age;
age = 20;
```

is semantically valid.

However:

```cpp
age = 20;
```

without a valid declaration can produce a semantic error.

---

# 5. Symbol Table

The Symbol Table maintains information about identifiers encountered during compilation.

Typical information includes:

| Property             | Description                      |
| -------------------- | -------------------------------- |
| Name                 | Identifier name                  |
| Type                 | Data type                        |
| Scope                | Scope in which identifier exists |
| Declaration Location | Source location                  |
| Metadata             | Additional semantic information  |

The Symbol Table enables semantic analysis to determine:

* Whether an identifier exists
* Whether it has already been declared
* What type it represents
* Which scope it belongs to

---

# 6. Static Security Analysis

After AST construction, CyberSeq performs static security analysis.

The security engine traverses AST nodes and applies modular security rules.

The current implementation includes **10 security rules: SEC001–SEC010**.

Each finding can contain:

* Rule ID
* Vulnerability
* Severity
* Source line
* Recommendation
* Security references

The security engine performs detection independently of the AI layer.

---

# Security Rules

| Rule ID | Vulnerability                 | Typical Severity |
| ------- | ----------------------------- | ---------------- |
| SEC001  | Hardcoded Password            | High             |
| SEC002  | Hardcoded API Key             | High             |
| SEC003  | Weak Password                 | Medium           |
| SEC004  | Potential SQL Injection       | High             |
| SEC005  | Potential Command Injection   | Critical         |
| SEC006  | Unsafe `gets()`               | High             |
| SEC007  | Unsafe `strcpy()`             | Medium           |
| SEC008  | Unsafe `sprintf()`            | Medium           |
| SEC009  | Weak Random Number Generator  | Low              |
| SEC010  | Resource Leak / Unclosed File | Medium           |

---

## SEC001 — Hardcoded Password

Example:

```cpp
string password = "secret_password_123";
```

CyberSeq identifies credential-like variables containing hardcoded values.

### Risk

Hardcoded credentials can be exposed through:

* Source repositories
* Logs
* Backups
* Code sharing
* Compiled artifacts

### Recommended Practice

Use secure configuration or secret-management mechanisms instead of embedding credentials directly in source code.

---

## SEC002 — Hardcoded API Key

Example:

```cpp
string api_key = "AIzaSyD123456789abcdef";
```

The analyzer detects API-key-like patterns and sensitive identifier names.

### Recommended Practice

Store secrets outside source code using appropriate secret-management mechanisms.

---

## SEC003 — Weak Password

Example:

```cpp
string password = "admin123";
```

The analyzer can identify weak or predictable password values.

### Recommended Practice

Use strong credential policies and secure credential management.

---

## SEC004 — Potential SQL Injection

Example:

```cpp
string query =
    "SELECT * FROM users WHERE name=" + input;

db_query(query);
```

The analyzer identifies patterns involving dynamic SQL construction.

### Recommended Practice

Use:

* Parameterized queries
* Prepared statements
* Appropriate input validation

---

## SEC005 — Potential Command Injection

Example:

```cpp
string command = "ls -la " + input;

system(command);
```

The analyzer identifies dynamic values reaching command execution.

### Recommended Practice

Avoid constructing shell commands from untrusted input and prefer safer APIs.

---

## SEC006 — Unsafe `gets()`

Example:

```cpp
gets(buffer);
```

`gets()` does not provide a safe mechanism for restricting input size.

CyberSeq flags calls to this unsafe function.

---

## SEC007 — Unsafe `strcpy()`

Example:

```cpp
strcpy(destination, source);
```

The analyzer flags potentially unsafe unbounded string-copy operations.

Safer implementations should explicitly account for destination capacity.

---

## SEC008 — Unsafe `sprintf()`

Example:

```cpp
sprintf(buffer, format);
```

The analyzer identifies potentially unsafe formatted output into buffers.

A bounded alternative such as `snprintf()` may be appropriate depending on the use case.

---

## SEC009 — Weak Random Number Generator

Example:

```cpp
int token = rand();
```

The analyzer flags conventional pseudo-random generation where security-sensitive randomness may be required.

Security-sensitive applications should use an appropriate cryptographically secure random-number generator.

---

## SEC010 — Resource Leak

Example pattern:

```cpp
int fd = open("audit.log", 1);
read(fd, buffer, 100);
```

without appropriate resource cleanup.

The analyzer can report the potential resource leak.

Recommended pattern:

```text
Open Resource
     ↓
Use Resource
     ↓
Close / Release Resource
```

---

# AST-Based Security Detection

A key design feature of CyberSeq is that security analysis is performed using the **compiler-generated AST**.

For example:

```cpp
system(command);
```

can be represented conceptually as:

```text
FunctionCall("system")
└── Identifier("command")
```

A security rule can inspect this AST structure and determine that a potentially dangerous function is being called.

This creates the important relationship:

```text
Compiler Design
      ↓
AST
      ↓
Static Security Analysis
```

Security analysis therefore becomes an extension of the compiler pipeline rather than a separate text-search utility.

---

# 7. AI Explanation Engine

CyberSeq provides an AI-assisted explanation layer.

The AI does **not independently detect vulnerabilities**.

Instead:

```text
AST
 ↓
Security Rules
 ↓
Security Finding
 ↓
Rule ID + Metadata
 ↓
AI Explanation Engine
 ↓
Human-Readable Explanation
```

For each detected finding, the explanation can contain:

1. Vulnerability Name
2. Simple Explanation
3. Technical Explanation
4. Why It Is Dangerous
5. Possible Attack Scenario
6. Severity
7. Secure Coding Recommendation
8. Corrected Code Example
9. CWE / Security References

This converts a technical security finding into a developer-friendly explanation.

---

# AI Architecture

CyberSeq uses a provider-based AI architecture.

```text
                 Security Finding
                        │
                        ▼
                ┌───────────────┐
                │   AI Helper   │
                └───────┬───────┘
                        │
                 Provider Selection
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
       ┌────────────┐      ┌────────────┐
       │   OpenAI   │      │   Ollama   │
       └────────────┘      └────────────┘
              │                   │
              └─────────┬─────────┘
                        │
                        ▼
                Explanation Output
                        │
                        ▼
                 GUI / PDF Report
```

The AI provider can be changed through configuration without redesigning the compiler or security engine.

---

# OpenAI Support

The architecture supports an OpenAI API provider.

Example configuration:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=your_model
```

The API key should be stored in environment configuration and should **never be committed to GitHub**.

---

# Ollama Support

CyberSeq also supports local LLM inference through Ollama.

Example:

```env
AI_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
```

This allows AI explanations to be generated locally.

Advantages include:

* Local processing
* No external API dependency
* Reduced privacy concerns
* No per-request API cost
* Useful for offline demonstrations

---

# Offline AI Fallback

If the configured AI provider is unavailable, CyberSeq can use a deterministic, rule-specific fallback explanation system.

Fallback output is explicitly labeled:

```text
[Offline Fallback Explanation]
```

This prevents the application from implying that an unavailable LLM generated the explanation.

The fallback system contains vulnerability-specific explanations rather than using one generic explanation for every finding.

---

# 8. Security Scoring

CyberSeq calculates an overall security score based on the severity of detected findings.

The current scoring model uses:

```text
Initial Score = 100

Critical = -20
High     = -10
Medium   = -5
Low      = -2
```

Conceptually:

```text
Initial Score
      │
      ▼
Analyze Findings
      │
      ▼
Classify Severity
      │
      ├── Critical → Deduction
      ├── High     → Deduction
      ├── Medium   → Deduction
      └── Low      → Deduction
      │
      ▼
Final Security Score
```

The report includes a scoring breakdown so that the final score can be understood rather than treated as a black-box number.

The score is an **educational project-level risk indicator**, not an industry-standard security rating.

---

# 9. PDF Security Reporting

CyberSeq can generate a structured PDF security audit report using **ReportLab**.

The report can include:

### Project Summary

* Source file
* Language mode
* Lines of code
* Token count
* Semantic errors
* Security findings
* Security score

### Compiler Results

* Lexical Analysis
* Syntax Analysis
* AST Generation
* Semantic Analysis

### Token Information

Representative tokens and source locations.

### Symbol Table

Identifiers and their semantic information.

### Semantic Diagnostics

Semantic errors and their source locations.

### Security Findings

* Rule ID
* Vulnerability
* Severity
* Source line
* Recommendation

### AI Explanations

Structured vulnerability explanations and secure coding guidance.

### Security Score

Severity-based scoring and deduction breakdown.

---

# 10. Desktop GUI

CyberSeq provides an IDE-style desktop interface.

The GUI includes:

* Source-code editor
* Open File
* Save File
* Clear
* Analyze Code
* Generate Report
* Token Viewer
* AST Viewer
* Semantic Errors
* Security Findings
* AI Explanations
* Scrollable analysis panels
* Severity indicators
* Analysis status information

The interface is designed for easy demonstration of the complete compiler and security-analysis pipeline.

---

# C/C++ Subset

CyberSeq is **not a complete C++ compiler**.

It supports a practical subset of C/C++ suitable for demonstrating compiler design and static security analysis.

The supported subset focuses on constructs required by the project's analysis pipeline.

Typical constructs include:

```text
int
float
char
bool
string

if
else
while
for
return

+
-
*
/
%
==
!=
<
>
<=
>=
&&
||

=
;
{}
()
```

The project intentionally does not attempt to fully implement advanced C++ features such as:

* Classes
* Templates
* Complex inheritance
* Operator overloading
* Pointer-heavy programs
* Advanced STL semantics
* Full preprocessor semantics
* Complete C++ standard-library semantics

This keeps the compiler understandable and maintainable at the project's intended academic scope.

---

# Function Signatures

The semantic analyzer contains project-specific built-in function signatures.

For example:

```text
open(string, int)
read(int, string, int)
```

These signatures are used during semantic analysis to validate function calls.

They are part of the analyzer's supported language specification and should not be confused with complete C/C++ standard-library semantics.

---

# Technology Stack

| Category          | Technology                     |
| ----------------- | ------------------------------ |
| Primary Language  | Python                         |
| Input Language    | Practical C/C++ Subset         |
| Lexical Analysis  | PLY Lex                        |
| Parsing           | PLY Yacc                       |
| AST               | Custom Python AST              |
| Semantic Analysis | Custom Python Implementation   |
| Symbol Table      | Custom Python Implementation   |
| Security Analysis | AST-Based Static Analysis      |
| AI                | OpenAI / Ollama                |
| GUI               | Tkinter / CustomTkinter        |
| PDF Reporting     | ReportLab                      |
| Testing           | pytest                         |
| Configuration     | `.env` / Environment Variables |
| Version Control   | Git / GitHub                   |

---

# Project Structure

A typical project structure is:

```text
CyberSeq/
│
├── ai/
│   ├── __init__.py
│   ├── ai_helper.py
│   └── providers.py
│
├── compiler/
│   ├── __init__.py
│   ├── lexer.py
│   ├── parser.py
│   ├── ast.py
│   ├── semantic.py
│   └── symbol_table.py
│
├── security/
│   ├── __init__.py
│   └── security_rules.py
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   └── controller.py
│
├── reports/
│   ├── __init__.py
│   ├── report_generator.py
│   └── report_utils.py
│
├── examples/
│   ├── sample_cpp.cpp
│   └── comprehensive_vulnerable.cpp
│
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic.py
│   ├── test_security.py
│   ├── test_ai.py
│   └── test_report.py
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The exact file structure may vary slightly depending on the current implementation.

---

# Main Components

## `compiler/lexer.py`

Responsible for:

* Token definitions
* Regular expressions
* Keywords
* Identifiers
* Literals
* Operators
* Delimiters
* Comments
* Lexical errors

---

## `compiler/parser.py`

Responsible for:

* Grammar rules
* Syntax validation
* Parse structure
* AST construction
* Syntax error handling

---

## `compiler/ast.py`

Contains AST node representations such as:

```text
Program
VarDecl
Assignment
BinaryExpression
UnaryExpression
Literal
Identifier
IfStatement
WhileLoop
ForLoop
FunctionCall
Print
Block
Return
```

---

## `compiler/semantic.py`

Responsible for:

* Declaration checking
* Duplicate declaration detection
* Type checking
* Scope validation
* Assignment validation
* Function argument validation
* Semantic diagnostics

Compiler state is reset between independent analysis operations to prevent stale analysis results.

---

## `compiler/symbol_table.py`

Maintains identifier information used during semantic analysis.

---

## `security/security_rules.py`

Contains the modular security-rule engine.

Each security rule is separated so additional rules can be added without redesigning the compiler pipeline.

---

## `ai/ai_helper.py`

Connects security findings to the configured AI provider.

---

## `ai/providers.py`

Contains AI provider implementations, including:

```text
OpenAI
Ollama
Offline / Mock Fallback
```

---

## `gui/main_window.py`

Responsible for the desktop user interface.

---

## `gui/controller.py`

Coordinates the GUI with:

* Compiler
* Semantic Analyzer
* Security Engine
* AI Engine
* Report Generator

---

## `reports/report_generator.py`

Generates structured PDF security reports.

---

## `reports/report_utils.py`

Provides report and security-scoring helper functionality.

---

# Installation

## Requirements

Recommended environment:

* Python 3.10+
* Windows / Linux / macOS
* Tkinter
* Dependencies listed in `requirements.txt`

Optional:

* Ollama
* A supported local Ollama model

---

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd cyberseq-cpp-security-analyzer
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root.

Example:

```env
AI_PROVIDER=ollama

OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3

ENABLE_MOCK_FALLBACK=true
```

### Important

Do not commit your real `.env` file or API keys to GitHub.

Use `.env.example` for public configuration documentation.

---

# Running the Project

Activate the virtual environment.

### Windows

```powershell
.venv\Scripts\activate
```

Then run:

```powershell
python main.py
```

The CyberSeq desktop application should open.

---

# Running an Analysis

1. Start CyberSeq.
2. Open a supported C/C++ source file or enter code in the editor.
3. Click **Analyze Code** or press `F5`.
4. Review the **Tokens** tab.
5. Review the **AST** tab.
6. Check **Semantic Errors**.
7. Open **Security Findings**.
8. Review **AI Explanations**.
9. Generate the PDF report.

---

# Example

Consider a deliberately vulnerable program:

```cpp
int main()
{
    string password = "admin123";

    string api_key = "AIzaSyD123456789abcdef";

    string input = "user_data";

    string query =
        "SELECT * FROM users WHERE name=" + input;

    db_query(query);

    system(input);

    gets(input);

    int token = rand();

    return 0;
}
```

Depending on the supported grammar and active security rules, CyberSeq can identify findings such as:

```text
Hardcoded Password
Weak Password
Hardcoded API Key
Potential SQL Injection
Potential Command Injection
Unsafe gets()
Weak Random Number Generator
```

---

# Example Analysis Pipeline

```text
Source Code
     │
     ▼
Lexer
     │
     ▼
Tokens
     │
     ▼
Parser
     │
     ▼
AST
     │
     ├───────────────┐
     ▼               ▼
Semantic          Security
Analysis          Analysis
     │               │
     ▼               ▼
Semantic          Security
Errors            Findings
                     │
                     ▼
              AI Explanation
                     │
                     ▼
              Security Report
```

---

# Example Successful Vulnerability Analysis

A comprehensive vulnerable test program is expected to demonstrate:

```text
Lexical Analysis:    PASS
Syntax Analysis:     PASS
AST Generation:      PASS
Semantic Errors:      0
Security Analysis:   COMPLETED
Security Findings:   Multiple
```

This demonstrates an important security-analysis concept:

> **A program can be syntactically and semantically valid while still containing security vulnerabilities.**

---

# Error Handling

CyberSeq distinguishes between compiler errors and security findings.

## Lexical Error

```text
Source Code
     ↓
Lexer
     ↓
Lexical Error
```

Occurs when invalid characters or unsupported lexical constructs are encountered.

---

## Syntax Error

```text
Tokens
     ↓
Parser
     ↓
Syntax Error
```

Occurs when the token sequence does not match the supported grammar.

---

## Semantic Error

```text
AST
 ↓
Semantic Analyzer
 ↓
Semantic Error
```

Occurs when the program structure is syntactically valid but semantically invalid.

Examples:

* Undeclared variable
* Duplicate declaration
* Type mismatch
* Invalid assignment
* Invalid function arguments

---

## Security Finding

```text
Valid AST
     ↓
Security Analyzer
     ↓
Security Finding
```

A security finding does not necessarily mean the program has a compiler error.

For example:

```cpp
string password = "admin123";
```

may be completely valid from a compiler perspective while still triggering a security finding.

---

# Testing

CyberSeq uses **pytest** for automated testing.

Run:

```bash
python -m pytest tests/
```

The test suite covers areas such as:

### Lexer

* Valid tokens
* Keywords
* Identifiers
* Literals
* Operators
* Invalid characters

### Parser

* Valid syntax
* Invalid syntax
* Expressions
* Conditional statements
* Loops

### Semantic Analyzer

* Valid declarations
* Duplicate declarations
* Undeclared variables
* Type mismatches
* Scope errors
* Function argument validation

### Security Engine

* Hardcoded passwords
* Hardcoded API keys
* Weak passwords
* SQL injection
* Command injection
* Unsafe functions
* Weak randomness
* Resource leaks
* Safe code

### AI

* Provider selection
* Ollama integration
* OpenAI integration
* Offline fallback
* Rule-specific explanations

### Reports

* PDF generation
* Security findings
* Semantic error formatting
* Score calculation
* Text wrapping

---

# Recommended End-to-End Test Cases

CyberSeq should be tested with four major categories.

## 1. Safe Program

Expected:

```text
Lexical Analysis:    PASS
Syntax Analysis:     PASS
AST Generation:      PASS
Semantic Analysis:   PASS
Security Findings:   0
```

---

## 2. Syntax Error Program

Expected:

```text
Lexical Analysis:    PASS
Syntax Analysis:     FAIL
Syntax Error:        Reported
```

---

## 3. Semantic Error Program

Expected:

```text
Lexical Analysis:    PASS
Syntax Analysis:     PASS
Semantic Analysis:   FAIL
Semantic Errors:     Reported
```

---

## 4. Comprehensive Vulnerable Program

Expected:

```text
Lexical Analysis:    PASS
Syntax Analysis:     PASS
AST Generation:      PASS
Semantic Errors:     0
Security Analysis:   COMPLETED
Security Findings:   Multiple
AI Explanations:     Generated
PDF Report:          Generated
```

---

# Design Philosophy

CyberSeq follows the principle:

> **Detect deterministically, explain intelligently.**

The compiler and security engine are responsible for detection.

The AI engine is responsible for explanation.

This separation provides:

* Reproducibility
* Explainability
* Easier testing
* Easier debugging
* Clear architectural boundaries
* Better academic defensibility

---

# Why AI Is Not Used for Detection

A purely AI-based security system could look like:

```text
Source Code
     ↓
AI
     ↓
"Potential vulnerability"
```

CyberSeq instead uses:

```text
Source Code
     ↓
Compiler
     ↓
AST
     ↓
Deterministic Security Rules
     ↓
Security Finding
     ↓
AI Explanation
```

This means the security engine remains predictable while AI improves the usability and educational value of the results.

---

# Advantages

## 1. Multi-Domain Project

CyberSeq combines:

* Compiler Design
* Cybersecurity
* Static Analysis
* AI
* Software Engineering
* GUI Development
* Automated Reporting

---

## 2. AST-Based Analysis

The security engine operates on the compiler-generated AST, demonstrating how compiler intermediate representations can be reused for security analysis.

---

## 3. Modular Architecture

Compiler, security, AI, GUI, and reporting components are separated.

This makes the project easier to:

* Understand
* Debug
* Test
* Extend

---

## 4. Explainable Findings

Security findings are accompanied by explanations and recommendations instead of only displaying a rule name.

---

## 5. Local AI Support

Ollama enables local LLM inference for explanations.

---

## 6. Offline Operation

The deterministic fallback allows the application to continue providing explanations even when the configured LLM provider is unavailable.

---

## 7. Automated Reporting

The PDF generator creates a structured security audit report suitable for demonstrations and documentation.

---

# Limitations

Current limitations include:

* Supports a practical C/C++ subset rather than the complete language.
* Does not implement complete C++ semantics.
* Security rules are primarily AST/pattern based.
* Static analysis may produce false positives or false negatives.
* Full data-flow analysis is not implemented.
* Full interprocedural analysis is not implemented.
* Advanced pointer and memory analysis are outside the current scope.
* The analyzer does not execute the submitted program.
* AI-generated explanations may require human verification.
* Security scoring is an educational risk indicator rather than an industry-standard rating.
* Full C/C++ preprocessor and toolchain behavior is outside the project's scope.

---

# Industry Relevance

CyberSeq demonstrates concepts used in modern software-development and application-security tooling.

Relevant areas include:

* Static Application Security Testing (SAST)
* Secure Software Development
* Developer Security Tools
* Code Quality Analysis
* Compiler Infrastructure
* DevSecOps
* Automated Code Review
* AI-Assisted Development

The project demonstrates how compiler-generated representations such as ASTs can support security analysis.

---

# Academic Relevance

CyberSeq maps directly to several areas of computer science education.

| Academic Area        | Project Component       |
| -------------------- | ----------------------- |
| Compiler Design      | Lexer                   |
| Compiler Design      | Parser                  |
| Compiler Design      | Grammar                 |
| Compiler Design      | AST                     |
| Compiler Design      | Semantic Analysis       |
| Compiler Design      | Symbol Table            |
| Cybersecurity        | Static Analysis         |
| Cybersecurity        | Vulnerability Detection |
| Cybersecurity        | CWE Mapping             |
| AI                   | LLM-Based Explanation   |
| Software Engineering | Modular Architecture    |
| Testing              | pytest                  |
| GUI Development      | Desktop Application     |
| Reporting            | PDF Generation          |

---

# Project Objectives

The main objectives are:

1. Implement a practical compiler pipeline for a C/C++ subset.
2. Demonstrate lexical analysis using PLY.
3. Implement syntax analysis using PLY Yacc.
4. Construct an Abstract Syntax Tree.
5. Implement semantic analysis.
6. Build and use a Symbol Table.
7. Extend AST analysis into static security analysis.
8. Detect common security vulnerabilities.
9. Assign severity to detected vulnerabilities.
10. Provide AI-assisted vulnerability explanations.
11. Support local LLM inference through Ollama.
12. Provide an offline explanation fallback.
13. Calculate an overall security score.
14. Generate a structured PDF security report.
15. Provide a desktop interface for demonstrating the complete pipeline.

---

# Future Scope

CyberSeq can be extended in several directions.

## Compiler

* Larger C/C++ grammar
* Improved error recovery
* More complete type system
* Function definitions
* Arrays
* Pointers
* Structures
* Classes

## Static Analysis

* Control-flow graph generation
* Data-flow analysis
* Taint analysis
* Interprocedural analysis
* Path-sensitive analysis
* Advanced AST pattern analysis

## Cybersecurity

Additional rules could cover:

* Buffer overflows
* Format-string vulnerabilities
* Integer overflows
* Use-after-free
* Null-pointer dereferences
* Path traversal
* Weak cryptography
* Insecure deserialization

## AI

* Context-aware explanations
* Automated fix generation
* Finding prioritization
* Secure-code rewriting
* Developer Q&A
* Explanation confidence indicators

## GUI

* Inline vulnerability markers
* Code navigation
* Finding highlighting
* Multi-file analysis
* Project workspaces
* Interactive AST visualization

## Reporting

* HTML reports
* JSON reports
* CSV exports
* Historical scan comparison
* Security trend analysis
* CI/CD integration
* SARIF output

---

# Project Status

**Status: Functional Academic Prototype**

CyberSeq currently provides an end-to-end workflow:

```text
C/C++ Source
     ↓
Lexical Analysis
     ↓
Syntax Analysis
     ↓
AST Generation
     ↓
Semantic Analysis
     ↓
AST-Based Security Analysis
     ↓
Security Findings
     ↓
AI-Assisted Explanation
     ↓
Security Scoring
     ↓
PDF Security Report
```

The project is intentionally positioned for demonstrating the integration of compiler design, cybersecurity, and AI.

---

# Project Identity

## CyberSeq

### AI-Assisted C/C++ Static Security Analyzer

**Repository:**

```text
cyberseq-cpp-security-analyzer
```

**Short Description:**

> Compiler-based C/C++ static security analyzer with AST-driven vulnerability detection, severity scoring, AI-assisted explanations, and automated security reports.

---

# License

This project was developed for academic and educational purposes.

If the repository is distributed publicly, an appropriate open-source license can be added based on the authors' requirements.
