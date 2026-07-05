# Persistent video ingestion pipeline

## Architecture

```
                    VIDEO INGESTION PIPELINE

┌───────────────────┐
│   Video (.mp4)    │
└─────────┬─────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ GenericAPIAdapter.transcribe_video()│
│                                     │
│ • load video                        │
│ • Base64 encode                     |
|   (matching infrastructure)         |
|   (file api for large files)        │
│ • Send to Vision LLM                │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ Vision LLM (Gemini/OpenAI/Claude)   │
│                                     │
│ Produces chronological document     │
│                                     │
│ • Audio                             │
│ • Visual events                     │
│ • OCR text                          │
│ • Summary                           │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ Unified Text Representation         │
│                                     │
│ Video: meeting.mp4                  │
│ 00:00 Audio...                      │
│ 00:00 Visual...                     │
│ 00:00 OCR...                        │
│ ...                                 │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ Existing Cognee Pipeline            │
│                                     │
│ Chunking                            │
│ ↓                                   │
│ Entity Extraction                   │
│ ↓                                   │
│ Relationship Discovery              │
│ ↓                                   │
│ Knowledge Graph                     │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ Persistent Improving Memory         │
│                                     │
│ New videos update the graph         │
│                                     │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ Natural Language Queries            │
│                                     │
│ "What decisions were made?"         │
│ "What changed this week?"           │
│ "Who owns this task?"               │
└─────────────────────────────────────┘
```

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
