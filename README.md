# Dynamic Agent Creation System

A pragmatic agentic system with:
- FastAPI backend and Next.js (TypeScript) frontend
- Dynamic tool registry (prebuilt + LLM proxy tools; code tools planned for scale-up)
- Graph-based orchestration with LangGraph
- Streaming-friendly design and clean, layered architecture

This README is rebuilt end-to-end to reflect the actual codebase and the final API surface.

---

## 0) Quick Start (recommended)

From the project root, this starts both backend and frontend for you:

```cmd
python start_all.py
```

If you prefer to run services manually, follow the steps below.

## 1) Setup Instructions

Prerequisites:
- Python 3.11+ (3.12 recommended)
- Node.js 18+ and npm
- An OpenAI API key (required for LLM-backed tools)
- Windows, macOS, or Linux (examples here use Windows-friendly commands)

Environment variables (backend/.env):
```
OPENAI_API_KEY=sk-...
```

Start the backend (from project root):
```cmd
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Start the frontend:
```cmd
cd frontend
npm install
npm run dev
```

Notes:
- Frontend is configured to proxy API calls via `frontend/next.config.mjs` to `http://127.0.0.1:8000`.
- Backend enables CORS for `http://localhost:3000` and `http://127.0.0.1:3000` (see `backend/main.py`).
- If port 8000 is stuck on Windows:
```cmd
taskkill /F /IM uvicorn.exe /T & taskkill /F /IM python.exe /T & for /f "tokens=5" %a in ('netstat -ano ^| findstr LISTENING ^| findstr :8000') do taskkill /F /PID %a
```

Health checks:
```cmd
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/tools
```

---

## 2) How to Register Custom Tools

Currently supported custom tool type: LLM proxy tools (no-code). Code snippet-based tools are planned for a future scale-up release and are not available right now.

Backend routes (from `backend/agents/presentation/api/tool_routes.py`):
- List tools: `GET /api/tools`
- Register LLM tool: `POST /api/tools/register_llm` (aliases: `/api/tools/register-llm`, `/api/tools/register_llm/`)

Schema and example (LLM proxy tool)

- Request body:
```json
{
  "name": "summarizer_llm",
  "description": "Summarize input concisely"
}
```
- cURL (primary path):
```cmd
curl -X POST http://127.0.0.1:8000/api/tools/register_llm ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"summarizer_llm\",\"description\":\"Summarize input concisely\"}"
```
- Aliases that also work: `/api/tools/register-llm`, `/api/tools/register_llm/`
- Parameters are fixed to `["input"]` at execution time.

Via UI (frontend):
- Tools page → Create LLM Tool (no code) → fill Name/Description → submit.

Persistence note:
- The in-memory registry resets on backend restart. Re-register tools after a restart.

---

## 3) Demo Workflow Steps

Goal: Show a multi-tool flow with prebuilt + LLM tools and an execution trace.

1) Register an LLM tool (e.g., `summarizer_llm`)
```cmd
curl -X POST http://127.0.0.1:8000/api/tools/register_llm ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"summarizer_llm\",\"description\":\"Summarize input concisely\"}"
```

2) Ensure a prebuilt tool is available (e.g., `chatbot`).

3) Create an agent (via UI if available) and attach tools: `chatbot` + `summarizer_llm`. Alternatively, conceptually run two steps using tools directly.

4) Example multi-step query (conceptual):
- Step 1: Ask chatbot to generate a sentence.
- Step 2: Pass chatbot output to `summarizer_llm` to shorten it.

5) Example trace
```
▶ chatbot(query="Say: BotWot builds reliable AI systems with great UX.")
✔  BotWot builds reliable AI systems with great UX.
▶ summarizer_llm(input="BotWot builds reliable AI systems with great UX.")
✔  BotWot builds reliable AI systems.
```

6) Tools list check
```cmd
curl http://127.0.0.1:8000/api/tools
```

---

## 4) Design Questions (Answers)

A) Why LangGraph over CrewAI?
- Graph-native control flow: LangGraph lets us model conditional branches, loops, and retries naturally, which maps well to tool-chaining and iterative reasoning.
- Fine-grained state and streaming: It supports step-wise execution and streaming, which we surface as traces in the UI.
- Ecosystem fit: Works cleanly with LangChain primitives without imposing heavy orchestration opinions.
- Operational clarity: Deterministic graphs are easier to debug and observe than opaque agent loops.

B) Scaling to 10k concurrent users
- Stateless API pods: Run FastAPI behind a load balancer (e.g., Traefik/NGINX), multiple Uvicorn workers, uvloop.
- Async everywhere: Non-blocking LLM calls, circuit breakers, retries, backoff.
- Work queues: Offload long-running tool work to Celery/Arq/RQ with Redis/RabbitMQ backends.
- Persistence: Redis Cluster for sessions/caching; Postgres with connection pooling, read replicas.
- Streaming at scale: SSE/WebSocket proxy tuned for many idle connections; shard channels; heartbeat and backpressure.
- Cost & limits: Per-user rate limits, token budgets, and batching where possible.
- Observability: Structured logs, metrics, tracing; SLO-based autoscaling.

C) Adding RAG (Retrieval-Augmented Generation)
- Components:
  - Indexer tool: `index_documents(docs, metadata)` → stores chunks + embeddings in a vector DB (pgvector/Pinecone/Weaviate).
  - Retriever tool: `retrieve_context(query, filters)` → returns top-k chunks.
  - Answer tool: `answer_with_context(input, context)` → composes a prompt with citations for the LLM.
- Flow in LangGraph:
  - analyze → maybe_retrieve → execute_tools → synthesize
  - Conditional edges decide when to retrieve; pass context forward as part of the graph state.
- API additions:
  - `/api/rag/index` (POST) and `/api/rag/retrieve` (POST)

---

## 5) Architecture Overview

- `backend/`
  - `main.py`: FastAPI app, CORS, and routers mount.
  - `agents/presentation/api/tool_routes.py`: list/register/execute tool endpoints (LLM tools only).
  - `agents/core/services/tool_registry.py`: global in-memory tool registry and runners.
- `frontend/`
  - Next.js App Router page at `src/app/tools/page.tsx` for managing tools.
  - Proxy rewrites in `next.config.mjs` to `http://127.0.0.1:8000`.

Principles:
- Clean, layered design with clear separation of presentation and core services.
- Minimal, safe dynamic code registration (validation + disallowed imports).
- LLM proxy tool path for no-code tools with a fixed `input` parameter.

---

## 6) Submission Instructions

- Push code to a public GitHub repo named `dynamic-agent-creation.
- Create a tagged release `v0.1`.
- Attach a ≤3 minute screen-capture demo showing:
- 
  

https://github.com/user-attachments/assets/be4e2022-85dc-46d8-80b0-432a5812a4a3



---

## 7) Troubleshooting

- 404 from `/api/...` in the browser: ensure the backend is running on 127.0.0.1:8000 and the Next dev server is up on 3000. Check `frontend/next.config.mjs`.
- CORS errors when calling the backend directly from the browser: ensure backend started with latest code (CORS is enabled in `backend/main.py`).
- Tools disappear after restart: expected with in-memory registry—re-register.
- Port 8000 busy on Windows: use the command at the top of this README to kill lingering processes.

---

