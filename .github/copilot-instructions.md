# Azure App Service FastAPI Demo - Copilot Instructions

## Repository Overview

This is a minimal FastAPI demo application designed for deployment to Azure App Service. It's a small Python web service repository (~10 files) using FastAPI framework with Pydantic for data validation.

**Languages & Frameworks:**
- Python 3.9+ (CI uses 3.9, local development tested with 3.12)
- FastAPI 0.113.0 with standard extensions
- Pydantic 2.7.0+ for data validation
- Uvicorn as ASGI server

## Project Structure

```
/
├── .github/
│   ├── copilot-instructions.md  # This file
│   └── workflows/
│       └── ci.yml               # CI workflow (install deps only, no tests)
├── app/
│   ├── __init__.py             # Empty module marker
│   ├── main.py                 # Main FastAPI application
│   └── Dockerfile              # Alternative Dockerfile (in app dir)
├── Dockerfile                   # Main Dockerfile (root level)
├── requirements.txt             # Python dependencies
└── .gitignore                  # Standard Python gitignore
```

**Main Application:** `app/main.py` contains:
- FastAPI app instance
- Three endpoints: `/` (Hello World), `/status}` (status check - note the `}` is part of the path), `/items/{item_id}` (parameterized endpoint)
- Direct uvicorn runner for local development

## Build, Run, and Test Instructions

### Environment Setup

**ALWAYS** run these commands in order when starting fresh:

```bash
# 1. Install/upgrade pip (required)
python -m pip install --upgrade pip

# 2. Install dependencies (required before any other step)
pip install -r requirements.txt
```

**Dependencies install time:** ~30-60 seconds depending on network

### Running the Application

**Development Mode** (with auto-reload):
```bash
fastapi dev app/main.py --port 8000
```
- Access at: http://127.0.0.1:8000
- Docs at: http://127.0.0.1:8000/docs
- Auto-reloads on file changes

**Production Mode:**
```bash
fastapi run app/main.py --port 8000
```

**Direct Python execution:**
```bash
python app/main.py
# Runs on http://127.0.0.1:8000
```

### Testing the Application

**No formal test suite exists.** To validate changes, use manual testing:

```bash
# Using FastAPI TestClient (recommended):
python -c "
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
print('Root:', client.get('/').json())
print('Status:', client.get('/status}').json())
print('Items:', client.get('/items/42?q=test').json())
"
```

Expected output:
```
Root: {'Hello': 'World'}
Status: {'Status': 'Success'}
Items: {'item_id': 42, 'q': 'test'}
```

### Docker Build

**IMPORTANT:** Docker build **WILL FAIL** in this environment due to SSL certificate verification issues with PyPI. The Dockerfile is valid but cannot be tested here.

```bash
# This command will fail with SSL errors:
docker build -t fastapi-demo .
# Error: SSL: CERTIFICATE_VERIFY_FAILED
```

The Dockerfile at root level is the primary one and uses:
- Base image: `python:3.9`
- Runs: `fastapi run app/main.py --port 80`

### Linting and Code Quality

**No linters or formatters are configured.** No `pyproject.toml`, `.flake8`, `.pylintrc`, or similar files exist. If adding linting, follow Python community standards (black, flake8, mypy, etc.).

### Syntax Validation

```bash
# Validate Python syntax:
python -m py_compile app/main.py

# Import test:
python -c "import app.main; print('Import successful')"
```

## CI/CD Pipeline

**GitHub Actions CI:** `.github/workflows/ci.yml`
- Triggers: Push/PR to `main` branch
- Uses: Python 3.9, ubuntu-latest
- Steps:
  1. Checkout code
  2. Setup Python 3.9
  3. Upgrade pip
  4. Install dependencies from requirements.txt
  5. Echo "No tests specified" (no actual tests run)

**To replicate CI locally:**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
# Note: CI doesn't run tests, only validates dependency installation
```

## Key Facts and Gotchas

1. **Endpoint Path:** The `/status}` endpoint includes a `}` character in the path - this is intentional, not a typo
2. **No Tests:** There is no test infrastructure (no pytest, unittest, etc.)
3. **No README:** No README.md or other documentation exists
4. **Duplicate Dockerfiles:** Both root and `app/Dockerfile` exist - root Dockerfile is primary
5. **Python Version:** CI uses 3.9, but code works with 3.12+ (tested)
6. **SSL Issues:** Docker builds fail in sandboxed environments due to SSL certificate issues with PyPI
7. **Dependencies:** Always install dependencies before any build/run/test operations

## File Contents Reference

**requirements.txt:**
```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

**app/main.py endpoints:**
- `GET /` → `{"Hello": "World"}`
- `GET /status}` → `{"Status": "Success"}`  
- `GET /items/{item_id}?q={query}` → `{"item_id": int, "q": str|None}`

## Instructions for Agents

**Trust these instructions.** Only search/explore if:
- Information here is incomplete for your specific task
- You encounter an error not documented here
- You need to understand implementation details beyond what's documented

**For code changes:**
- Install dependencies first (always)
- Validate with TestClient or manual runs
- No formal tests to run, but ensure endpoints still work
- Follow FastAPI and Pydantic conventions
- CI only checks dependency installation, not functionality

