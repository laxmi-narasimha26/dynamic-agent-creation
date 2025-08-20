# FastAPI main backend app entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# CORS: allow local frontend dev server
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from api.agent import router as agent_router
from agents.presentation.api.streaming_routes import router as streaming_router
from agents.presentation.api.tool_routes import router as tool_router

app.include_router(agent_router, prefix="/api", tags=["Agents"])
app.include_router(streaming_router, prefix="/api", tags=["Streaming"])
app.include_router(tool_router, prefix="/api", tags=["Tools"])

@app.get("/", tags=["Root"])
async def root():
    return {
        "status": "ok",
        "service": "Dynamic Agent Backend",
        "health": "/health",
        "docs": "/docs",
    }

@app.get('/health')
async def health_check():
    return {'status': 'ok'}
