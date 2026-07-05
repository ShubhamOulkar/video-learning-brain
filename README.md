# Cognee Video Ingestion Pipeline

## Overview

This project adds native video understanding to Cognee's memory pipeline. Instead of building a separate computer vision system, it uses existing multimodal models to convert videos into structured chronological knowledge that is stored in Cognee's knowledge graph. The implementation demonstrates a practical AI employee memory system that can continuously learn from meeting recordings, project discussions, training sessions, and other video-based knowledge sources.

Demo:

[Watch Sober AI Employee Demo](https://www.youtube.com/watch?v=iI3C5pXqNf8)

## Architecture

```text
                    VIDEO INGESTION PIPELINE

┌───────────────────┐
│   Video (.mp4)    │
└─────────┬─────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ GenericAPIAdapter.transcribe_video()│
│                                     │
│ • Load video                        │
│ • Base64 encode                     │
│ • Send to multimodal model          │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ Vision LLM                          │
│ (Gemini/OpenAI/Claude)              │
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
│ Self-Improving Memory               │
│                                     │
│ New videos update the graph         │
│ automatically                       │
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

## Results

This project includes:

- [multimedia_processing](/multimedia_processing) for evaluation
- [sober_ai_employee](/sober_ai_employee/) for a practical business use case demonstration

Additional resources:

- Evaluation metrics: [evaluation_results.json](/multimedia_processing/evaluation/evaluation_results.json)
- Generated video transcript example: [news video](/multimedia_processing/artifacts/video.txt)
- Meeting memory example: [meeting transcript](/sober_ai_employee/artifacts/text_bf8c58a82724f080e770e57d7f0988c6.txt)

## Current Limitations & Future Work

The current implementation uses Base64-encoded video data to validate Cognee's multimodal memory pipeline and works well for small videos.

This approach was intentionally chosen because it:

- Matches the existing audio and image ingestion infrastructure.
- Requires minimal architectural changes.
- Allows rapid validation of video memory creation.
- Works across providers that support multimodal video inputs.

However, Base64 transport is not ideal for large-scale production workloads because:

- Request payload size increases by approximately 33%.
- Large videos can exceed provider token limits.
- Entire videos must be loaded into memory before transmission.
- Upload latency increases as video size grows.

### Next Step: Provider File APIs

The first production-ready improvement will be replacing Base64 transport with provider-native file upload APIs.

```text
Video
   │
   ▼
Provider File API
(OpenAI Files / Gemini Files / Claude Files)
   │
   ▼
Provider Multimodal Model
   │
   ▼
Chronological Text
   │
   ▼
Cognee Knowledge Graph
```

This approach preserves Cognee's existing memory architecture while enabling support for significantly larger videos.

### Provider Compatibility

Not all providers currently support video understanding.

For providers that do not natively support video inputs, a compatibility pipeline may be introduced in future iterations to extract audio and visual content before ingestion.

### Long-Term Direction

A longer-term direction is integrating dedicated video embedding models such as Marengo or similar multimodal video encoders.

```text
Video
   │
   ▼
Video Embedding Model
   │
   ▼
Video Embeddings
   │
   ▼
Cognee Context Manager
   │
   ▼
Knowledge Graph + Retrieval
```

This would allow scalable retrieval over large video collections while continuing to leverage Cognee's persistent memory and knowledge graph infrastructure.

---

## Development Setup

### Prerequisites

- Python 3.12+
- uv
- pnpm

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install pnpm

```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

### 3. Clone and Setup

```bash
git clone <repository-url>

cd video-learning-brain

uv sync

cp .env.template .env
```

Configure your API keys inside `.env`.

### 4. Start Local Cognee Server

```bash
uvicorn cognee.api.client:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the Application

- Cognee API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
