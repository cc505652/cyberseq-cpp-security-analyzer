# Setup & Deployment Guide: AI-Powered Secure Code Analyzer

This guide provides step-by-step instructions for setting up and running the **AI-Powered Secure Code Analyzer** project on any fresh machine.

---

## 1. Prerequisites

Before installing, ensure the following software is installed on your machine:
* **Python**: Version 3.12 or higher (Python 3.13 recommended)
* **Git**: Version control client (optional, for cloning repository)
* **Tcl/Tk**: Included by default with standard Python installers on Windows and macOS. On Linux, ensure `python3-tk` is installed.

---

## 2. Setting Up Virtual Environment

### Windows (PowerShell or Command Prompt)
```powershell
# Navigate to project directory
cd path\to\Compiler Design

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### Linux / macOS (Bash or Zsh)
```bash
# Navigate to project directory
cd path/to/Compiler\ Design

# Ensure python3-tk is installed (Debian/Ubuntu)
sudo apt update && sudo apt install -y python3-tk python3-venv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

---

## 3. Installing Dependencies

Once the virtual environment is activated, install all required dependencies from `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Required Packages:
* `ply>=3.11` (Python Lex & Yacc for Lexer/Parser)
* `customtkinter>=6.0.0` (Modern Dark Theme Desktop GUI Framework)
* `darkdetect>=0.8.0` (OS Theme Detection Utility)
* `reportlab>=4.0.0` (PDF Audit Report Generation Engine)
* `python-dotenv>=1.0.0` (Environment Variables & `.env` File Loader)
* `pytest>=8.0.0` (Automated Test Suite Runner)

---

## 4. Environment Configuration (`.env`)

The project supports environment variable configuration via a `.env` file in the root directory.

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` to configure your AI provider and API keys:

```env
# AI Provider Selection ("openai", "ollama", or "mock")
AI_PROVIDER=ollama

# OpenAI Settings (If using OpenAI Cloud)
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Ollama Settings (If using local Ollama instance)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3

# Fallback Settings
ENABLE_MOCK_FALLBACK=true
```

---

## 5. Running the Application

### Launching GUI Desktop IDE (Default Entry Point)
Run the root single entry point script:

```bash
python main.py
```

Alternatively, launch directly via the GUI launcher:

```bash
python gui/app.py
```

### Headless / CLI Fallback Mode
If a graphical window manager is not detected (e.g. running inside SSH, Docker, or headless Linux CI/CD environments), `main.py` automatically falls back to interactive/batch CLI analysis mode without crashing.

---

## 6. Running the Automated Test Suite

To run the complete automated test suite covering Lexer, Parser, AST, Symbol Table, Semantic Analysis, Static Security Rules, AI Engine, GUI, and PDF Report Generation:

```bash
pytest tests/
```

---

## 7. Common Troubleshooting

| Issue / Error Message | Root Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'dotenv'` | Dependency not installed in active environment. | Run `pip install python-dotenv` or `pip install -r requirements.txt`. |
| `_tkinter.TclError` / No display name | Missing Tkinter OS bindings or headless Linux. | On Ubuntu/Debian, run `sudo apt install python3-tk`. `main.py` will also automatically switch to CLI fallback mode. |
| OpenAI API Error / Missing Key | `OPENAI_API_KEY` not set in `.env`. | Provide `OPENAI_API_KEY` in `.env` or set `AI_PROVIDER=ollama` / default to offline Mock fallback. |
