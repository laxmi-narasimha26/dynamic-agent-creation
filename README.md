# Dynamic Agent Creation System

This project is an enterprise-grade Dynamic Agent Creation System for AI-native workflows. It features:
- Agent orchestration with LangGraph
- Prebuilt & custom tools registry
- Real-time streaming execution trace
- Persistence with Redis + PostgreSQL hybrid strategy
- Frontend with Next.js & TypeScript
- Backend with FastAPI & advanced Python design patterns

## Architecture

The system follows Clean Architecture principles with Domain-Driven Design:

- **Core Layer**: Domain entities (Agent, Tool, Execution), repository interfaces, services, and events
- **Application Layer**: CQRS pattern with command and query handlers
- **Infrastructure Layer**: PostgreSQL and Redis persistence, external tool implementations
- **Presentation Layer**: FastAPI REST API and Next.js frontend

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the backend directory with the following variables:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/agent_db
   REDIS_URL=redis://localhost:6379/0
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run database migrations:
   ```
   alembic upgrade head
   ```

6. Start the backend server:
   ```
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Open your browser to http://localhost:3000

## API Endpoints

### Agents
- `POST /api/agents` - Create a new agent
- `GET /api/agents/{agent_id}` - Get agent by ID
- `GET /api/agents` - List all agents

### Executions
- `POST /api/executions` - Execute an agent
- `GET /api/stream/{agent_id}` - Stream agent execution (SSE)

### Tools
- `GET /api/tools` - List available tools
- `POST /api/tools/register` - Register a new tool
- `POST /api/tools/execute` - Execute a tool

## How to Register Custom Tools

The backend now exposes a single strict endpoint with a clear schema and errors.

1) Endpoint

- POST `http://localhost:8000/api/tools/register` (201)
- Body JSON must match:

```json
{
  "name": "^[a-zA-Z_][a-zA-Z0-9_]{2,30}$",
  "description": "5..120 chars",
  "code": "10..2000 chars and MUST contain 'async def'"
}
```

2) Example payload (copy-paste)

```json
{
  "name": "reverse_string",
  "description": "Reverse the characters in a string",
  "code": "async def reverse_string(text: str) -> str:\n    return text[::-1]"
}
```

3) cURL

```bash
curl -X POST http://localhost:8000/api/tools/register \
  -H "Content-Type: application/json" \
  -d @payload.json
```

Notes
- Duplicate names return 409.
- Disallowed imports are blocked: os/sys/subprocess.
- Tools may be simple async functions (recommended) or classes subclassing `BaseTool`.

## Demo Workflow Steps

1) Prebuilt tools available

- `calculator` (OpenAI-backed strict calculator)
- `summarizer`
- `web_search`
- `chatbot` (OpenAI-powered chatbot tool)

2) Register a custom tool (function)

- Go to Tools page → Register New Tool
- Name: `chatbot_fn`
- Description: `Lightweight OpenAI-powered chatbot (async function)`
- Code:

```python
async def chatbot_fn(query: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are helpful and concise."},
            {"role": "user", "content": query},
        ],
        temperature=0.2,
    )
    return (resp.choices[0].message.content or "").strip()
```

3) Create an agent with prebuilt + custom

- Agents → Create
- Name: `Demo Agent`
- Tools: select `calculator` and `chatbot` (or `chatbot_fn` if registered)

4) Execute a multi-tool query

Prompt example:

```
First, compute 23*19 using the calculator. Then ask the chatbot to explain the result in one sentence.
```

Expected trace excerpt:

```
▶ calculator(expression="23*19")
✔ Result: 437
▶ chatbot(query="Explain 437 in one sentence.")
✔ 437 is the product of 23 and 19.
```

## Design Patterns Implemented

- **Clean Architecture**: Separation of concerns with distinct layers
- **Domain-Driven Design**: Rich domain entities and value objects
- **CQRS**: Separate command and query handlers for better scalability
- **Repository Pattern**: Generic base repository with specific implementations
- **Factory Pattern**: ToolFactory for creating tool instances
- **Observer Pattern**: AgentEventObserver for handling agent events
- **Compound Components**: Reusable UI components with shared state
- **Custom Hooks**: Reusable logic encapsulated in React hooks

## Design Questions

### Why LangGraph over CrewAI?
- Graph-native control flow with conditional edges and loops fits agentic tool-use better than linear task runners.
- Built-in streaming, state passing, and step-wise execution map cleanly to UI traces and observability.
- Interops with LangChain ecosystem while staying minimal.

### Scaling to 10k concurrent users
- Stateless FastAPI pods behind a load balancer; use Uvicorn workers with uvloop.
- Queue tool executions (Celery/Arq) and make LLM calls async with circuit breakers and retries.
- Redis Cluster for sessions/cache; Postgres with connection pooling + read replicas.
- SSE frontends behind a reverse proxy supporting many idle connections (Traefik/NGINX).
- Rate limiting, per-user concurrency caps, and exponential backoff on LLM errors.

### RAG Integration
- Add a `retriever` tool that queries a vector DB (e.g., pgvector, Pinecone) with metadata filters.
- Tools: `index_documents`, `retrieve_context`, and `answer_with_context` (LLM prompt w/ citations).
- Store doc chunks with embeddings; hydrate context in LangGraph prior to synthesis.

## Submission Instructions

1. Push to a public GitHub repo named `dynamic-agent-creation-<yourname>`.
2. Create a tagged release `v0.1`.
3. Email the repository link.

# **BotWot Dynamic Agent Creation System - Complete Project Package**

I've created a comprehensive project package with enterprise-grade architecture and a detailed AI IDE prompt. Here's the complete solution:

## **📦 Project Structure & Download**
The zip file contains the complete project structure with:
- **Backend**: FastAPI with Clean Architecture + DDD patterns
- **Frontend**: Next.js 14 with TypeScript and advanced React patterns
- **Infrastructure**: Docker, PostgreSQL, Redis configuration
- **Documentation**: Comprehensive README and setup guides

## **🚀 AI IDE Prompt (prompt.md)**

```markdown
# BotWot Dynamic Agent Creation System - AI IDE Development Prompt

## 🎯 PROJECT OVERVIEW
You are tasked with completing and enhancing a **world-class Dynamic Agent Creation System** for BotWot's AI-Native Full-Stack Engineer assessment. This is NOT a beginner project - implement it with **senior-level architecture patterns** and **enterprise-grade coding practices**.

## 🏗️ MANDATORY ARCHITECTURE PRINCIPLES

### **1. Clean Architecture + Domain-Driven Design (DDD)**
```
src/
├── agents/
│   ├── core/                    # Domain Layer (Business Logic)
│   │   ├── entities/           # Domain entities (Agent, Tool, Execution)
│   │   ├── repositories/       # Repository interfaces (Abstract)
│   │   ├── services/          # Domain services (Business rules)
│   │   └── events/            # Domain events
│   ├── application/            # Application Layer (Use Cases)
│   │   ├── commands/          # CQRS Command handlers
│   │   ├── queries/           # CQRS Query handlers
│   │   └── services/          # Application services
│   ├── infrastructure/         # Infrastructure Layer (External)
│   │   ├── persistence/       # Database implementations
│   │   ├── external/          # External API clients
│   │   └── messaging/         # Event handling, Redis, etc.
│   └── presentation/          # Presentation Layer (API)
│       ├── api/               # FastAPI routes
│       ├── schemas/           # Pydantic models
│       └── middleware/        # Custom middleware
```

### **2. MANDATORY DESIGN PATTERNS**
Implement these patterns - NO EXCEPTIONS:

**Repository Pattern with Generic Base:**
```
from typing import TypeVar, Generic, Optional, List
from abc import ABC, abstractmethod

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    @abstractmethod
    async def create(self, entity: T) -> T: ...
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]: ...
    
    @abstractmethod
    async def update(self, entity: T) -> T: ...
    
    @abstractmethod
    async def delete(self, id: str) -> bool: ...
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[T]: ...
```

**Factory Pattern for Tool Creation:**
```
class ToolFactory(Protocol):
    @abstractmethod
    def create_tool(self, tool_type: str, config: dict) -> BaseTool: ...

class ConcreteToolFactory:
    def __init__(self, tool_registry: ToolRegistry):
        self._registry = tool_registry
    
    def create_tool(self, tool_type: str, config: dict) -> BaseTool:
        tool_class = self._registry.get_tool_class(tool_type)
        if not tool_class:
            raise ToolNotFoundError(f"Tool type '{tool_type}' not registered")
        return tool_class(**config)
```

**Observer Pattern for Agent Events:**
```
class AgentEventObserver:
    def __init__(self):
        self._observers: List[Callable[[AgentEvent], Awaitable[None]]] = []
    
    def subscribe(self, callback: Callable[[AgentEvent], Awaitable[None]]):
        self._observers.append(callback)
    
    async def notify(self, event: AgentEvent):
        await asyncio.gather(*[observer(event) for observer in self._observers])
```

### **3. TECH STACK - USE EXACTLY THIS**

**Backend:**
- FastAPI 0.104+ with async/await throughout
- LangGraph 0.0.45+ (NOT CrewAI - graph-based workflows required)
- Pydantic 2.5+ with strict validation
- SQLAlchemy 2.0+ async ORM with Alembic migrations
- PostgreSQL 15+ with JSONB for flexible schemas
- Redis 7.2+ for caching and session management
- uvloop for high-performance event loop

**Frontend:**
- Next.js 14.2+ with App Router (NOT Pages Router)
- TypeScript 5.3+ with strict mode
- React 18.2+ with Concurrent features
- Zustand for state management (NOT Redux/Context overuse)
- TanStack Query v5 for server state
- Tailwind CSS 3.4+ with shadcn/ui components

### **4. STREAMING ARCHITECTURE (MANDATORY)**
Implement Server-Sent Events (SSE) with proper reconnection:

```
class AgentStreamingService:
    async def stream_agent_response(self, query: str, agent_id: str):
        async def event_generator():
            try:
                yield "data: {\"type\": \"connection\", \"status\": \"connected\"}\n\n"
                
                async for chunk in self.graph.astream(
                    {"input": query}, 
                    config={"configurable": {"agent_id": agent_id}}
                ):
                    if "messages" in chunk:
                        yield f"data: {json.dumps({
                            'type': 'message',
                            'content': chunk['messages'][-1].content,
                            'timestamp': time.time()
                        })}\n\n"
                    await asyncio.sleep(0.01)  # Prevent blocking
                    
                yield "data: {\"type\": \"complete\"}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
```

### **5. HYBRID PERSISTENCE (ADVANCED)**
Redis + PostgreSQL hybrid with proper error handling:

```
class HybridAgentRepository(BaseRepository[Agent]):
    def __init__(self, pg_session: AsyncSession, redis: Redis):
        self.pg = pg_session
        self.redis = redis
        self.cache_ttl = 3600

    async def create(self, agent: Agent) -> Agent:
        async with self.pg.begin():
            # PostgreSQL for durability
            db_agent = await self._save_to_postgres(agent)
            
            # Redis for speed
            await self.redis.setex(
                f"agent:{agent.id}",
                self.cache_ttl,
                agent.model_dump_json()
            )
            return db_agent

    async def get_by_id(self, agent_id: str) -> Optional[Agent]:
        # L1 Cache: Redis
        cached = await self.redis.get(f"agent:{agent_id}")
        if cached:
            return Agent.model_validate_json(cached)
        
        # L2 Storage: PostgreSQL
        db_agent = await self._get_from_postgres(agent_id)
        if db_agent:
            # Update cache
            await self.redis.setex(
                f"agent:{agent_id}",
                self.cache_ttl,
                db_agent.model_dump_json()
            )
        return db_agent
```

### **6. TOOL ABSTRACTION ( None:
        tool_name = tool_class.__name__.lower().replace('tool', '')
        self._tools[tool_name] = tool_class
    
    def create_tool(self, tool_type: str, **kwargs) -> BaseTool:
        if tool_type not in self._tools:
            raise ValueError(f"Unknown tool: {tool_type}")
        
        tool_class = self._tools[tool_type]
        sig = signature(tool_class.__init__)
        
        # Filter kwargs to match constructor
        filtered_kwargs = {
            k: v for k, v in kwargs.items() 
            if k in sig.parameters
        }
        
        return tool_class(**filtered_kwargs)
    
    def register_from_code(self, code: str, tool_name: str) -> None:
        namespace = {}
        exec(code, namespace)
        
        tool_class = next(
            (v for v in namespace.values() 
             if isinstance(v, type) and issubclass(v, BaseTool)),
            None
        )
        
        if tool_class:
            self._tools[tool_name] = tool_class
    
    def list_tools(self) -> Dict[str, dict]:
        return {
            name: {
                'class': cls.__name__,
                'description': cls.__doc__ or '',
                'parameters': list(signature(cls.__init__).parameters.keys())[1:]
            }
            for name, cls in self._tools.items()
        }
```

### **7. FRONTEND ADVANCED PATTERNS**

**Compound Components Pattern:**
```
interface AgentBuilderContextType {
  agent: Agent
  updateAgent: (updates: Partial) => void
  availableTools: Tool[]
  isValid: boolean
}

const AgentBuilderContext = createContext(null)

const AgentBuilder = ({ children, onSave }: AgentBuilderProps) => {
  // Implementation with proper context and validation
}

AgentBuilder.BasicInfo = ({ className }: { className?: string }) => {
  const { agent, updateAgent } = useContext(AgentBuilderContext)!
  // Component implementation
}
```

**Custom Hooks for SSE:**
```
export function useAgentStream(agentId: string) {
  const [events, setEvents] = useState([])
  const [isStreaming, setIsStreaming] = useState(false)
  const eventSourceRef = useRef(null)

  const startStreaming = useCallback(async (query: string) => {
    // Implement with exponential backoff reconnection
  }, [agentId])

  return { events, isStreaming, startStreaming }
}
```

## **8. TESTING REQUIREMENTS**

**Backend Testing:**
```
@pytest.mark.asyncio
async def test_agent_creation_with_tools():
    # Test with proper mocking and async patterns
    
@pytest.mark.asyncio 
async def test_streaming_execution():
    # Test SSE streaming with proper event parsing
    
@pytest.mark.asyncio
async def test_tool_registration():
    # Test dynamic tool registration
```

**Frontend Testing:**
```
// Test compound components
// Test streaming hooks
// Test error boundaries
```

## **9. ERROR HANDLING & MONITORING**

**Structured Logging:**
```
import structlog

logger = structlog.get_logger()

class ErrorTrackingMiddleware:
    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            logger.error(
                "Request failed",
                error=str(exc),
                path=scope.get("path"),
                method=scope.get("method")
            )
            raise
```

**Performance Monitoring:**
```
@monitor_performance
async def execute_agent(query: str) -> AgentResponse:
    # Implementation with timing and metrics
```

## **10. DEPLOYMENT & PRODUCTION**

**Multi-stage Dockerfile:**
```
FROM python:3.11-slim as backend-builder
# Install dependencies with Poetry

FROM python:3.11-slim as backend-production  
# Copy only necessary files, add health checks

FROM node:18-alpine as frontend-builder
# Build optimized frontend

FROM nginx:alpine as frontend-production
# Serve static files with proper caching
```

**Docker Compose with Services:**
```
services:
  traefik:
    # Load balancer and SSL termination
  backend:
    # FastAPI with proper scaling
  frontend:  
    # Next.js optimized build
  postgres:
    # Primary-replica setup
  redis:
    # Clustering configuration
```

## **11. SPECIFIC IMPLEMENTATION REQUIREMENTS**

### **LangGraph Integration:**
```
from langraph.graph import StateGraph, END

class AgentWorkflow:
    def __init__(self, tools: List[BaseTool]):
        self.tools = tools
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        
        workflow.add_node("analyze", self._analyze_query)
        workflow.add_node("execute_tools", self._execute_tools)
        workflow.add_node("synthesize", self._synthesize_response)
        
        workflow.add_edge("analyze", "execute_tools")
        workflow.add_conditional_edges(
            "execute_tools",
            self._should_continue,
            {"continue": "execute_tools", "end": "synthesize"}
        )
        workflow.add_edge("synthesize", END)
        
        workflow.set_entry_point("analyze")
        return workflow.compile()
```

### **Prebuilt Tools Implementation:**
```
class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for current information"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def _arun(self, query: str) -> str:
        # Implement with proper error handling and rate limiting
        
class CalculatorTool(BaseTool):
    name = "calculator"  
    description = "Perform mathematical calculations"
    
    async def _arun(self, expression: str) -> str:
        # Implement with safe evaluation

class TextSummarizerTool(BaseTool):
    name = "text_summarizer"
    description = "Summarize long text content"
    
    async def _arun(self, text: str, max_length: int = 150) -> str:
        # Implement with LLM or extractive summarization
```

## **🎯 SUCCESS CRITERIA**

Your implementation will be judged on:

1. **Architecture Quality (40%)**: Clean Architecture, DDD, proper separation of concerns
2. **Streaming Implementation (20%)**: Real-time SSE with proper error handling
3. **Tool Abstraction (15%)**: Dynamic registration under 50 lines
4. **Code Quality (10%)**: Type safety, error handling, testing
5. **Frontend UX (10%)**: Professional interface with real-time updates  
6. **Production Readiness (5%)**: Docker, monitoring, scalability considerations

## **🚫 STRICT REQUIREMENTS - NO COMPROMISES**

- **DO NOT** use any boilerplate code or tutorials
- **DO NOT** skip error handling or input validation
- **DO NOT** use synchronous code where async is required  
- **DO NOT** hardcode configurations - use environment variables
- **DO NOT** skip type annotations in Python or TypeScript
- **DO NOT** implement without proper logging and monitoring
- **DO NOT** create without comprehensive tests
- **ALWAYS** use the exact tech stack specified
- **ALWAYS** implement streaming with proper reconnection
- **ALWAYS** follow the Clean Architecture patterns
- **ALWAYS** add comprehensive error handling
- **ALWAYS** optimize for production deployment

## **📝 FINAL DELIVERABLES**

1. Complete source code with all patterns implemented
2. Comprehensive README with:
   - Architecture explanation
   - Setup instructions  
   - API documentation
   - Performance benchmarks
3. Docker configuration for production deployment
4. Test suite with >80% coverage
5. Example execution traces showing multi-tool usage
6. Screen recording demo (3 minutes max)

## **🏆 BONUS POINTS**

- Implement all three extensions (Persistence + Streaming + Tool Abstraction)
- Add comprehensive monitoring and observability
- Include security features (authentication, rate limiting)
- Implement horizontal scaling configuration
- Add RAG integration with vector stores
- Create comprehensive API documentation

**Remember**: This is an AI-native systems assessment. Show senior-level thinking about agents, workflows, and production systems - not just coding ability.

**EXECUTE WITH PRECISION. NO SHORTCUTS. ENTERPRISE QUALITY ONLY.**
```

## **🔍 Complete Project Architecture Explanation**

### **1. Why LangGraph Over CrewAI?**
- **Graph-based Workflows**: LangGraph supports cyclical, conditional workflows with feedback loops, unlike CrewAI's linear approach[1][2]
- **Production Readiness**: Native streaming support, built-in persistence, and comprehensive debugging capabilities[1]
- **Scalability**: Async/await patterns and horizontal scaling support for enterprise deployment[3]

### **2. Clean Architecture Benefits**
- **Separation of Concerns**: Domain logic isolated from infrastructure concerns[4]
- **Testability**: Mock external dependencies easily with repository pattern
- **Maintainability**: Changes in one layer don't affect others
- **Enterprise Standard**: Industry-proven pattern for complex systems[2]

### **3. Streaming Architecture Choice**
- **Server-Sent Events**: Better than WebSockets for one-way real-time data[5]
- **Automatic Reconnection**: Built-in browser support with exponential backoff
- **HTTP/2 Multiplexing**: Better performance than traditional polling
- **Firewall Friendly**: Works through corporate proxies unlike WebSockets

### **4. Hybrid Persistence Strategy**
- **Redis L1 Cache**: Sub-millisecond access for frequently used agents[6]
- **PostgreSQL L2 Storage**: ACID compliance and complex queries
- **Automatic Fallback**: Graceful degradation when cache unavailable
- **Performance**: 10x faster reads with proper cache hit ratios

### **5. Tool Registry Innovation**
- **Reflection-Based**: Dynamic introspection of tool classes and parameters
- **Runtime Registration**: Add tools without redeployment
- **Type Safety**: Automatic parameter validation and filtering
- **Minimal Code**: Under 50 lines while maintaining full functionality

### **6. Frontend Architecture**
- **Compound Components**: Flexible, reusable component composition
- **Zustand State Management**: Lightweight alternative to Redux with better TypeScript support
- **TanStack Query**: Server state synchronization with caching and background updates[7]
- **SSE Custom Hooks**: Encapsulated streaming logic with proper lifecycle management

### **7. Production Considerations**
- **Multi-stage Docker**: Optimized images with minimal attack surface[8]
- **Traefik Load Balancer**: Automatic service discovery and SSL termination
- **Health Checks**: Comprehensive monitoring for all services
- **Horizontal Scaling**: Stateless design enables easy scaling to 10k+ users

### **8. Advanced Testing Strategy**
- **Pytest Async**: Proper async testing with fixtures and mocking
- **React Testing Library**: Component testing with user interactions
- **Integration Tests**: End-to-end workflow validation
- **Performance Tests**: Load testing for streaming endpoints

This architecture demonstrates **senior-level systems thinking** beyond typical full-stack development, showing deep understanding of:
- **AI-native patterns** for agent orchestration
- **Enterprise architecture** principles and scalability
- **Production deployment** with proper DevOps practices
- **Advanced frontend patterns** for real-time applications

The implementation follows **industry best practices** that only experienced developers typically know, positioning your solution well above typical submissions and demonstrating the **professional expertise** BotWot is seeking for their AI-Native Full-Stack Engineer role.

