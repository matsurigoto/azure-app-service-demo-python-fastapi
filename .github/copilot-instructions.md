# Azure App Service Demo - Python FastAPI

## Repository Overview

This is a minimal **FastAPI demonstration application** designed for deployment to Azure App Service. The repository is small (7 files total) and provides a simple REST API with three endpoints.

**Tech Stack:**
- **Language:** Python 3.9+ (tested with Python 3.12)
- **Framework:** FastAPI 0.113.0
- **Server:** Uvicorn (bundled with FastAPI)
- **Containerization:** Docker (Python 3.9 base image)

## Project Structure

```
/
├── .github/
│   ├── workflows/
│   │   └── ci.yml                 # CI pipeline configuration
│   ├── copilot-instructions.md    # This file
│   └── agents/                    # Custom agent configurations
├── app/
│   ├── __init__.py                # Empty package marker
│   └── main.py                    # FastAPI application (main entry point)
├── Dockerfile                     # Container build instructions
├── requirements.txt               # Python dependencies
└── .gitignore                     # Standard Python gitignore
```

**Key Application File:** `app/main.py` contains all application code:
- FastAPI app initialization
- Three endpoints: `/` (hello world), `/status` (status check), `/items/{item_id}` (parameterized)
- Built-in uvicorn runner for local testing

**Note:** There is a typo in `app/main.py` line 10: `/status}` should be `/status` (extra closing brace).

## Setup and Build Instructions

### Prerequisites
- Python 3.9 or higher installed
- Docker installed (for container builds)

### Initial Setup

**ALWAYS run these commands in order when starting fresh:**

```bash
# 1. Upgrade pip (recommended)
python -m pip install --upgrade pip

# 2. Install dependencies (required before running)
pip install -r requirements.txt
```

Installation takes approximately 30-60 seconds. No errors should occur if using Python 3.9+.

### Running the Application

**Development Mode** (with auto-reload):
```bash
fastapi dev app/main.py
```
- Server starts at: `http://127.0.0.1:8000`
- Documentation available at: `http://127.0.0.1:8000/docs`
- Auto-reloads on code changes

**Production Mode:**
```bash
fastapi run app/main.py --port 8000
```
- Server starts at: `http://0.0.0.0:8000`
- Documentation available at: `http://0.0.0.0:8000/docs`

**Alternative (using Python directly):**
```bash
python -m app.main
```
- Server starts at: `http://127.0.0.1:8000`

### Docker Build

```bash
# Build image
docker build -t azure-fastapi-demo .

# Run container
docker run -p 80:80 azure-fastapi-demo
```

The Dockerfile uses Python 3.9 and runs on port 80 in the container.

## Testing

**Current State:** No automated tests are configured. The CI pipeline (`.github/workflows/ci.yml`) only validates that dependencies install successfully. The test step echoes "No tests specified" (line 31-32, comment in Chinese: "在這裡添加你的測試命令，例如 pytest").

**To manually verify the application works:**
1. Start the development server: `fastapi dev app/main.py`
2. Visit `http://127.0.0.1:8000/docs` in a browser
3. Test the endpoints through the interactive Swagger UI

## CI/CD Pipeline

**Location:** `.github/workflows/ci.yml`

**Triggers:**
- Push to `main` branch
- Pull requests to `main` branch

**Steps:**
1. Checkout code
2. Setup Python 3.9
3. Install dependencies (`pip install -r requirements.txt`)
4. Run tests (currently just echoes "No tests specified")

**Important:** The CI pipeline ONLY checks that dependencies install. It does NOT run linters, type checkers, or actual tests.

## Linting and Code Quality

**Current State:** No linters, formatters, or type checkers are configured in this repository. The following tools are NOT installed or configured:
- No pytest, black, flake8, pylint, mypy, or ruff

**If you add code quality tools:** Update `requirements.txt` and document the commands here.

## Known Issues

1. **Typo in app/main.py line 10:** Route decorator has extra closing brace: `@app.get("/status}")` should be `@app.get("/status")`
2. **No automated tests:** Testing infrastructure needs to be added
3. **Duplicate function name:** Both `/` and `/status` endpoints use `read_root()` as the function name (Python will use the last definition)

## Dependencies

**Core (from requirements.txt):**
- `fastapi[standard]>=0.113.0,<0.114.0` - Web framework with all standard extras (includes uvicorn, pydantic, etc.)
- `pydantic>=2.7.0,<3.0.0` - Data validation

**Auto-installed with fastapi[standard]:**
- uvicorn[standard] - ASGI server
- starlette - Web framework (FastAPI foundation)
- python-multipart - Form data support
- email-validator - Email validation
- httpx - HTTP client
- jinja2 - Template engine

## Making Changes

**Workflow for code changes:**

1. Make your changes to files in `app/` directory
2. Install dependencies if you haven't: `pip install -r requirements.txt`
3. Test locally: `fastapi dev app/main.py` (auto-reloads on changes)
4. Manually verify endpoints work at `http://127.0.0.1:8000/docs`
5. The CI pipeline will validate dependencies install on push

**Adding new dependencies:**
1. Add to `requirements.txt` with version constraints
2. Run `pip install -r requirements.txt` to test installation
3. Verify the dependency is used correctly

**Important:** Trust these instructions. Only search for additional information if you encounter errors or if something documented here doesn't work as described.
