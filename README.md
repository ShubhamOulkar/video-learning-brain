# Self video learning brain

> NOTE: This project is built upon fork from https://github.com/topoteretes/cognee

## Development Setup

### Prerequisites

- **Python**: 3.12+
- **Node.js**: 24.0+ [Download](https://nodejs.org/en/download)
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

### 3. Clone and Setup Backend

```bash
# Navigate to project directory
cd video-learning-brain

# Install Python dependencies with uv
uv sync

# Create environment file
cp .env.template .env
```

### 4. Setup Frontend

```bash
cd cognee-frontend

# Install Node dependencies with pnpm
pnpm install
```

### 5. Start Development Servers

**Terminal 1 - Backend (FastAPI on port 8000):**
```bash
uvicorn cognee.api.client:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend (Next.js on port 3000):**
```bash
pnpm dev
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
