"""
LLM Provider Integration Interfaces for C/C++ Secure Code Analyzer Engine.

Abstracts API communication with OpenAI and local Ollama models, complete with
graceful network error handling and offline rule-specific fallback capabilities.
"""

from abc import ABC, abstractmethod
import json
import re
import urllib.request
import urllib.error
from typing import Optional, Dict
import ai.config as config


class AIProvider(ABC):
    """Abstract base interface for LLM explanation providers."""

    @abstractmethod
    def generate_explanation(self, system_prompt: str, user_prompt: str, rule_id: str = "") -> str:
        """Generates text explanation from LLM provider."""
        pass


class MockAIProvider(AIProvider):
    """Offline mock provider used for local testing and offline execution."""

    RULE_FALLBACKS: Dict[str, Dict[str, str]] = {
        "SEC001": {
            "name": "Hardcoded Password",
            "simple": "Sensitive password credentials are written directly into the source code as plain text.",
            "technical": "Static analysis detected hardcoded credential string literals assigned to variables or constants during AST inspection.",
            "why_dangerous": "Anyone with access to the codebase or compiled binary strings can extract credentials and gain unauthorized access.",
            "attack_scenario": "An attacker reviews committed code repositories or binary string dumps to retrieve the hardcoded password and log in as admin.",
            "severity": "HIGH (Loss of Confidentiality & Authentication Bypass)",
            "recommendation": "Store passwords in encrypted environment variables or external secret vaults (e.g., AWS Secrets Manager).",
            "code": "// Secure Alternative:\nstring password = getenv(\"DB_PASSWORD\");",
            "ref": "CWE-259: Use of Hardcoded Password / OWASP A07:2021-Identification and Authentication Failures",
        },
        "SEC002": {
            "name": "Hardcoded API Key",
            "simple": "API keys or authentication tokens are written explicitly into the source code.",
            "technical": "The static analyzer detected string literals containing API token patterns or key identifiers assigned to variables.",
            "why_dangerous": "Leaked API keys allow unauthorized third parties to access cloud services, consume API quotas, or alter infrastructure.",
            "attack_scenario": "Automated secret scanners harvest public code commits within seconds and execute API requests using the stolen credential.",
            "severity": "HIGH (Unauthorized Cloud API Access)",
            "recommendation": "Load API keys dynamically from secure environment variables or a secret management vault at runtime.",
            "code": "// Secure Alternative:\nstring api_key = getenv(\"API_KEY\");",
            "ref": "CWE-798: Use of Hardcoded Credentials / OWASP A07:2021",
        },
        "SEC003": {
            "name": "Weak Password",
            "simple": "Trivial or predictable default passwords (e.g. 'admin123', 'password') are used in source code.",
            "technical": "AST literal inspection matched low-entropy password strings against a known dictionary of default passwords.",
            "why_dangerous": "Trivial passwords are easily guessed using automated dictionary or brute-force attacks.",
            "attack_scenario": "An attacker uses standard default password lists to gain instant administrative control of the application.",
            "severity": "MEDIUM (Weak Authentication Security)",
            "recommendation": "Enforce high-entropy password requirements, password salting, and secure hash functions.",
            "code": "// Secure Alternative:\nstring user_pass = prompt_secure_password();",
            "ref": "CWE-521: Weak Password Requirements / OWASP A07:2021",
        },
        "SEC004": {
            "name": "Potential SQL Injection",
            "simple": "Dynamic string concatenation is used to construct database queries with untrusted input.",
            "technical": "db_query() received dynamically concatenated string expressions or unvalidated identifiers in its AST parameters.",
            "why_dangerous": "Attackers can manipulate query logic to access, modify, or delete database tables beyond intended access limits.",
            "attack_scenario": "Passing \"' OR '1'='1\" in input parameters bypasses authentication checks and dumps customer database tables.",
            "severity": "HIGH (Data Exfiltration & Database Compromise)",
            "recommendation": "Use parameterized prepared statements or ORM query builders to bind parameters safely.",
            "code": "// Secure Alternative:\ndb_query_prepared(\"SELECT * FROM users WHERE id = ?\", user_id);",
            "ref": "CWE-89: Improper Neutralization of Special Elements used in an SQL Command / OWASP A03:2021",
        },
        "SEC005": {
            "name": "Potential Command Injection",
            "simple": "User-controlled input is passed directly to operating system command execution functions.",
            "technical": "system() function invocation received dynamic non-literal variables that may carry unsanitized shell metacharacters.",
            "why_dangerous": "Attackers append command separators (e.g. ';', '&&') to execute arbitrary operating system commands with host privileges.",
            "attack_scenario": "Passing \"file.txt; rm -rf /\" executes the intended command followed by destructive system deletion commands.",
            "severity": "CRITICAL (Arbitrary Operating System Command Execution)",
            "recommendation": "Avoid system(). Use specific library APIs (e.g., execve()) with array-passed arguments without invoking a subshell.",
            "code": "// Secure Alternative:\nexec_safe_command(\"ls\", \"-la\");",
            "ref": "CWE-78: Improper Neutralization of Special Elements used in an OS Command / OWASP A03:2021",
        },
        "SEC006": {
            "name": "Unsafe Function Call (gets)",
            "simple": "The gets() function reads input into a buffer without enforcing buffer size limits.",
            "technical": "gets() reads stdin until a newline is encountered, completely ignoring destination buffer capacity.",
            "why_dangerous": "Overflowing buffer capacity corrupts adjacent stack frame memory, enabling arbitrary remote code execution.",
            "attack_scenario": "An attacker inputs text exceeding buffer capacity to overwrite function return addresses with shellcode.",
            "severity": "HIGH (Stack Buffer Overflow & Code Execution)",
            "recommendation": "Completely eliminate gets(). Use bounded input alternatives like fgets().",
            "code": "// Secure Alternative:\nfgets(buffer, sizeof(buffer), stdin);",
            "ref": "CWE-242: Use of Inherently Dangerous Function / OWASP A06:2021",
        },
        "SEC007": {
            "name": "Unsafe Function Call (strcpy)",
            "simple": "strcpy() copies source strings into destination buffers without verifying buffer capacity limits.",
            "technical": "Unbounded string copying allows source strings longer than destination buffer allocations to trigger buffer overflows.",
            "why_dangerous": "Overwriting buffer boundaries leads to application crashes, memory corruption, and potential code execution.",
            "attack_scenario": "An attacker inputs long strings that overflow destination buffers on the stack.",
            "severity": "MEDIUM (Memory Corruption / Buffer Overflow)",
            "recommendation": "Replace strcpy() with bounded functions such as strncpy() or snprintf().",
            "code": "// Secure Alternative:\nstrncpy(dest, src, sizeof(dest) - 1);\ndest[sizeof(dest) - 1] = '\\0';",
            "ref": "CWE-120: Buffer Copy without Checking Size of Input / OWASP A06:2021",
        },
        "SEC008": {
            "name": "Unsafe Function Call (sprintf)",
            "simple": "sprintf() writes formatted output strings into target buffers without checking output size boundaries.",
            "technical": "Unbounded format expansion can produce string lengths exceeding destination buffer allocation.",
            "why_dangerous": "Buffer overflow corrupts adjacent heap/stack structures and risks stability or arbitrary code execution.",
            "attack_scenario": "Crafting expanded string formats overflows target output buffers during runtime string assembly.",
            "severity": "MEDIUM (Format String / Buffer Overflow)",
            "recommendation": "Replace sprintf() with snprintf() to specify destination buffer capacity limits.",
            "code": "// Secure Alternative:\nsnprintf(buffer, sizeof(buffer), \"%s\", src);",
            "ref": "CWE-134: Use of Externally-Controlled Format String / OWASP A06:2021",
        },
        "SEC009": {
            "name": "Weak Random Number Generator",
            "simple": "Standard rand() produces deterministic, predictable pseudo-random sequence values.",
            "technical": "rand() relies on simple linear congruential algorithms whose internal states are easily reconstructed from short sample outputs.",
            "why_dangerous": "Predictable random numbers fail security guarantees when used for session IDs, tokens, or encryption keys.",
            "attack_scenario": "An attacker predicts subsequent session tokens generated by rand() and hijacks user accounts.",
            "severity": "LOW (Predictable Random Sequence Generation)",
            "recommendation": "Use cryptographically secure random number generators (secure_rand(), /dev/urandom, or OS CSPRNG APIs).",
            "code": "// Secure Alternative:\nint safe_rnd = secure_rand();",
            "ref": "CWE-338: Use of Cryptographically Weak Pseudo-Random Number Generator / OWASP A02:2021",
        },
        "SEC010": {
            "name": "Resource Leak (Unclosed File)",
            "simple": "System resources allocated via open() are not released with matching close() calls.",
            "technical": "Static analysis identified open() file descriptor handles lacking explicit close() cleanup in execution paths.",
            "why_dangerous": "Accumulating unclosed file descriptors exhausts operating system handle limits, causing application denial of service.",
            "attack_scenario": "Repeatedly calling file opening workflows without closing handles consumes all available system file descriptors.",
            "severity": "MEDIUM (Resource Exhaustion / Denial of Service)",
            "recommendation": "Ensure every opened handle is released using close() or managed with RAII resource guards.",
            "code": "// Secure Alternative:\nint fd = open(\"file.txt\", 0);\n// ... process file ...\nclose(fd);",
            "ref": "CWE-775: Missing Release of File Descriptor or Resource / OWASP A08:2021",
        },
    }

    def generate_explanation(self, system_prompt: str, user_prompt: str, rule_id: str = "") -> str:
        # Determine rule_id from parameter or extract from prompt text
        rid = rule_id
        if not rid:
            match = re.search(r"SEC\d{3}", user_prompt)
            if match:
                rid = match.group(0)

        data = self.RULE_FALLBACKS.get(rid)
        if not data:
            return (
                "[Offline Fallback Explanation]\n\n"
                "### 1. Vulnerability Name\nGeneric Static Security Finding\n\n"
                "### 2. Simple Explanation\nThe program performs an unvalidated action on user input or system resources.\n\n"
                "### 3. Technical Explanation\nStatic AST inspection detected an unverified function parameter or handle reference.\n\n"
                "### 4. Why it is Dangerous\nUnvalidated parameters risk buffer overflows, injection vectors, or memory leaks.\n\n"
                "### 5. Possible Attack Scenario\nAn attacker supplies crafted inputs to exploit boundary or resource management flaws.\n\n"
                "### 6. Severity Rating\nMedium Impact\n\n"
                "### 7. Secure Coding Recommendation\nValidate all inputs and manage resource handles explicitly.\n\n"
                "### 8. Corrected Code Example\n```cpp\n// Verify inputs and release resources\n```\n\n"
                "### 9. Security Best Practices\nAdopt defense-in-depth, input validation, and secure memory API standards.\n\n"
                "### 10. Standard References\nCWE / OWASP Top 10 Security Guidelines"
            )

        return (
            "[Offline Fallback Explanation]\n\n"
            f"### 1. Vulnerability Name\n{data['name']}\n\n"
            f"### 2. Simple Explanation\n{data['simple']}\n\n"
            f"### 3. Technical Explanation\n{data['technical']}\n\n"
            f"### 4. Why it is Dangerous\n{data['why_dangerous']}\n\n"
            f"### 5. Possible Attack Scenario\n{data['attack_scenario']}\n\n"
            f"### 6. Severity Rating\n{data['severity']}\n\n"
            f"### 7. Secure Coding Recommendation\n{data['recommendation']}\n\n"
            f"### 8. Corrected Code Example\n```cpp\n{data['code']}\n```\n\n"
            f"### 9. Security Best Practices\nEnforce strict input sanitization, safe API alternatives, and resource cleanup.\n\n"
            f"### 10. Standard References\n{data['ref']}"
        )


class OpenAIProvider(AIProvider):
    """OpenAI Cloud API Integration Provider."""

    def __init__(self, api_key: str = "", model: str = "") -> None:
        self.api_key: str = api_key or config.OPENAI_API_KEY
        self.model: str = model or config.OPENAI_MODEL

    def generate_explanation(self, system_prompt: str, user_prompt: str, rule_id: str = "") -> str:
        if not self.api_key:
            if config.ENABLE_MOCK_FALLBACK:
                return MockAIProvider().generate_explanation(system_prompt, user_prompt, rule_id=rule_id)
            raise ValueError("OpenAI API Key is missing. Set OPENAI_API_KEY environment variable.")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        }

        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=config.OPENAI_TIMEOUT) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"]
        except urllib.error.URLError as e:
            if config.ENABLE_MOCK_FALLBACK:
                return MockAIProvider().generate_explanation(system_prompt, user_prompt, rule_id=rule_id)
            raise RuntimeError(f"OpenAI API Connection Error: {e}")


class OllamaProvider(AIProvider):
    """Local Ollama LLM Integration Provider."""

    def __init__(self, host: str = "", model: str = "") -> None:
        self.host: str = host or config.OLLAMA_HOST
        self.model: str = model or config.OLLAMA_MODEL

    def generate_explanation(self, system_prompt: str, user_prompt: str, rule_id: str = "") -> str:
        url = f"{self.host.rstrip('/')}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "stream": False,
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=config.OLLAMA_TIMEOUT) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data.get("response", "")
        except urllib.error.URLError as e:
            if config.ENABLE_MOCK_FALLBACK:
                return MockAIProvider().generate_explanation(system_prompt, user_prompt, rule_id=rule_id)
            raise RuntimeError(f"Ollama Local Server Error: {e}")
