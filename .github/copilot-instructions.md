# Azure App Service Demo - Python FastAPI - Copilot Instructions

## Repository Overview

This repository contains a demonstration FastAPI application designed for deployment to Azure App Service. It is a small, production-ready Python web service built with the FastAPI framework.

**Repository Type:** Python Web Application (FastAPI)  
**Target Runtime:** Python 3.9+ (Docker uses Python 3.9, CI uses Python 3.9)  
**Framework:** FastAPI 0.113.0+  
**Deployment Target:** Azure App Service (containerized)  
**Repository Size:** Small (~10 files)

## Project Structure

```
.
├── .github/
│   ├── agents/              # Custom agent configurations (DO NOT MODIFY)
│   ├── workflows/
│   │   └── ci.yml          # GitHub Actions CI pipeline
│   └── copilot-instructions.md
├── app/
│   ├── __init__.py         # Package initializer
│   ├── Dockerfile          # Docker configuration for app directory
│   └── main.py             # Main FastAPI application entry point
├── Dockerfile              # Root-level Docker configuration
├── requirements.txt        # Python dependencies
└── .gitignore             # Standard Python gitignore
```

### Key Files

- **app/main.py**: Contains the FastAPI application instance and all API endpoints
- **requirements.txt**: Two main dependencies - `fastapi[standard]>=0.113.0,<0.114.0` and `pydantic>=2.7.0,<3.0.0`
- **Dockerfile**: Multi-stage Docker build using Python 3.9 base image
- **.github/workflows/ci.yml**: CI pipeline that runs on push/PR to main branch

### Current API Endpoints

The application defines the following endpoints in `app/main.py`:
- `GET /` - Returns `{"Hello": "World"}`
- `GET /status}` - Returns `{"Status": "Success"}` (Note: There's a typo with closing brace)
- `GET /items/{item_id}` - Async endpoint with path and query parameters

## Build and Development Instructions

### Prerequisites

- Python 3.9 or higher (Python 3.12+ also works)
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Environment Setup

**ALWAYS follow these steps in order:**

1. **Install dependencies** (required before any other operation):
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs FastAPI with standard extras (includes uvicorn, pydantic, and all necessary dependencies). Installation typically takes 20-30 seconds.

2. **No additional setup required** - The application has no database, no environment variables, and no complex configuration.

### Running the Application

You have three options to run the application:

#### Option 1: Development Mode with Auto-Reload (Recommended for Development)
```bash
fastapi dev app/main.py
```
- Runs on http://127.0.0.1:8000
- Auto-reloads on code changes
- Interactive API docs at http://127.0.0.1:8000/docs
- Starts in 1-2 seconds

#### Option 2: Production Mode
```bash
fastapi run app/main.py --port 8000
```
- Runs on http://0.0.0.0:8000
- No auto-reload (optimized for production)
- This is the command used in Docker containers

#### Option 3: Direct Uvicorn
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
- Alternative method using uvicorn directly
- More control over server configuration

### Testing

**Current State**: No test framework is configured in this repository.

The CI workflow (`.github/workflows/ci.yml`) has a "Run tests" step that currently only echoes "No tests specified". If you need to add tests:
- Install pytest: `pip install pytest`
- Create tests in a `tests/` directory
- Update the CI workflow to run `pytest`

### Linting and Code Quality

**Current State**: No linters or formatters are configured in this repository.

Common tools you might want to use (not currently installed):
- `black` - Code formatter
- `flake8` or `ruff` - Linter
- `mypy` - Type checker
- `isort` - Import sorter

To add these, update `requirements.txt` or create a separate `requirements-dev.txt`.

### Docker Build

**Important**: Docker builds may fail in environments with SSL certificate issues (e.g., corporate proxies).

**Standard Docker Build**:
```bash
docker build -t fastapi-app .
```

**Running the Docker Container**:
```bash
docker run -p 8000:80 fastapi-app
```
The container exposes port 80 internally and runs the production command: `fastapi run app/main.py --port 80`

**Known Issue**: In some environments, pip within Docker may encounter SSL certificate verification errors. This is environment-specific and not a code issue. The application works correctly outside Docker.

## Continuous Integration

### CI Workflow (.github/workflows/ci.yml)

The CI pipeline runs on:
- Push to `main` branch
- Pull requests to `main` branch

**CI Steps**:
1. Checkout code
2. Set up Python 3.9
3. Install dependencies with `pip install -r requirements.txt`
4. Run tests (currently just echoes "No tests specified")

**Expected Behavior**: The CI should pass as long as dependencies install correctly. There are no tests to fail.

## Development Workflow

### Making Changes

1. **Always install dependencies first** if you haven't already:
   ```bash
   pip install -r requirements.txt
   ```

2. **Make your code changes** in the appropriate files (typically `app/main.py` for API changes)

3. **Test locally** using development mode:
   ```bash
   fastapi dev app/main.py
   ```

4. **Verify the changes** by accessing:
   - API endpoints directly (e.g., http://127.0.0.1:8000/)
   - Interactive docs at http://127.0.0.1:8000/docs
   - OpenAPI schema at http://127.0.0.1:8000/openapi.json

5. **Check Python syntax** (optional but recommended):
   ```bash
   python -m py_compile app/main.py
   ```

### Common Pitfalls

- **Don't forget to install dependencies**: Many commands will fail if you skip `pip install -r requirements.txt`
- **Port conflicts**: If port 8000 is in use, specify a different port with `--port <PORT>`
- **Import errors**: The app expects to be run from the repository root with the import string `app.main:app`

## Adding New API Endpoints

When adding new endpoints to `app/main.py`:

1. Follow the existing pattern using FastAPI decorators (`@app.get()`, `@app.post()`, etc.)
2. Use type hints for all parameters (FastAPI uses these for validation and documentation)
3. Use Pydantic models for request/response bodies
4. The OpenAPI documentation updates automatically
5. Test new endpoints at http://127.0.0.1:8000/docs

Example endpoint pattern:
```python
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

@app.get("/your-endpoint")
async def your_endpoint(param: str, optional: Union[str, None] = None):
    return {"param": param, "optional": optional}
```

## Important Notes

- **No database**: This is a stateless API demo with no persistence layer
- **No authentication**: There is no authentication or authorization configured
- **No external dependencies**: The app doesn't connect to external services
- **Simple structure**: All API logic is in a single file (`app/main.py`)
- **Container-ready**: Designed for Azure App Service container deployment

## Validation Checklist

Before submitting changes, verify:

- [ ] Dependencies install successfully: `pip install -r requirements.txt`
- [ ] Application starts without errors: `fastapi dev app/main.py`
- [ ] All endpoints respond correctly (test via /docs or curl)
- [ ] Python syntax is valid: `python -m py_compile app/main.py`
- [ ] CI requirements are met (dependencies must install cleanly)
- [ ] No sensitive data or credentials are added to the code
- [ ] Changes follow the existing code style and patterns

## Trust These Instructions

These instructions have been validated by running all commands and testing the application. Only search for additional information if:
- You encounter an error not documented here
- You need to add functionality not covered in these instructions
- The instructions appear to be outdated or incorrect

When in doubt, start with `pip install -r requirements.txt` and `fastapi dev app/main.py`.
