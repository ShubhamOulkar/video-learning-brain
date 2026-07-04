# Self video learning brain

> NOTE: This project is built from copy of fork https://github.com/topoteretes/cognee

## Development Setup

### Prerequisites

- **Python**: 3.12+
- **uv**: Python package manager
- **pnpm**: Node package manager

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install pnpm

```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

### 3. Clone and Setup Cognee

```bash
# Navigate to project directory
cd video-learning-brain

# Install Python dependencies with uv
uv sync

# Create environment file
cp .env.template .env
```

### 5. Start Development Cognee Servers

**Cognee (FastAPI on port 8000):**
```bash
uvicorn cognee.api.client:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the Application

- **Cognee API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

> Note: The current video ingestion implementation now sends video content as
**Base64** data URIs instead of using LiteLLM's create_file API. This
matches the existing audio/image infrastructure, works across more
providers, and provides a simpler baseline for validating multimodal
video ingestion before introducing provider-specific file upload APIs.
