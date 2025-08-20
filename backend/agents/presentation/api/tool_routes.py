from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, constr, validator
from typing import Dict, Any, Optional, List
from ...core.services.tool_registry import get_global_registry

router = APIRouter()

tool_registry = get_global_registry()

class ToolRegistrationIn(BaseModel):
    """Schema aligned with API spec: accepts tool_name and code"""
    tool_name: constr(strip_whitespace=True, pattern=r"^[a-zA-Z_][a-zA-Z0-9_]{2,30}$")  # type: ignore
    description: Optional[constr(min_length=5, max_length=120)] = None  # type: ignore
    code: str = Field(..., min_length=10, max_length=2000)

    @validator("code")
    def must_define_async_fn(cls, v: str) -> str:
        if "async def" not in v:
            raise ValueError("Function must be async")
        # lightweight safety: block a few risky imports
        banned = ("import os", "import sys", "import subprocess", "from os ", "from sys ", "from subprocess ")
        if any(b in v for b in banned):
            raise ValueError("Disallowed imports detected (os/sys/subprocess)")
        return v

class ToolRegistrationOut(BaseModel):
    name: str
    description: str

class ToolExecutionRequest(BaseModel):
    tool_type: str
    parameters: Dict[str, Any]

class LLMToolRegistrationIn(BaseModel):
    """Schema for code-free LLM-proxy tool registration.
    Only name and description are required. Parameters always default to ["input"].
    """
    name: constr(strip_whitespace=True, pattern=r"^[a-zA-Z_][a-zA-Z0-9_]{2,30}$")  # type: ignore
    description: constr(min_length=5, max_length=120)  # type: ignore

@router.get("/tools", summary="List available tools")
async def list_tools():
    """List all available tools and their specifications."""
    tools = tool_registry.list_tools()
    # Debug: log current tool keys
    try:
        print(f"[tools] list -> {list(tools.keys())}")
    except Exception:
        pass
    return tools

@router.post("/tools/register", status_code=200, summary="Register a new tool (async function or BaseTool)")
async def register_tool(payload: ToolRegistrationIn) -> str:
    """Register a new tool from Python code with strict validation.
    Returns tool name string on success.
    """
    try:
        name = payload.tool_name.strip()
        # Ensure unique name
        if name in tool_registry.list_tools().keys():
            raise HTTPException(status_code=409, detail="Tool name already exists")

        # Basic line limit safety (approx ~60 lines)
        if payload.code.count("\n") > 120:
            raise HTTPException(status_code=400, detail="Code too long; limit to ~120 lines for safety")

        # Use description if provided, otherwise default
        description = payload.description or "No description provided"
        
        # Register the tool
        tool_registry.register_llm_code_tool(name, description, payload.code)
        return name  # Return tool name string as per API spec
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to register tool: {str(e)}")

@router.post("/tools/register_llm", status_code=201, summary="Register a new LLM-proxy tool (no code)")
@router.post("/tools/register_llm/", status_code=201, include_in_schema=False)
@router.post("/tools/register-llm", status_code=201, include_in_schema=False)
async def register_llm_tool(payload: LLMToolRegistrationIn) -> ToolRegistrationOut:
    """Register an LLM-backed tool using only name/description/parameters.
    The tool forwards input to OpenAI Chat Completions with a system prompt built from description.
    """
    try:
        name = payload.name.strip()
        if name in tool_registry.list_tools().keys():
            raise HTTPException(status_code=409, detail="Tool name already exists")

        # Parameters are fixed as ["input"] for all LLM tools
        tool_registry.register_llm_tool(name, payload.description, ["input"])
        return ToolRegistrationOut(name=name, description=payload.description)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to register LLM tool: {str(e)}")

@router.post("/tools/execute", summary="Execute a tool")
async def execute_tool(request: ToolExecutionRequest):
    """Execute a tool with the provided parameters."""
    try:
        tool = tool_registry.create_tool(request.tool_type, **request.parameters)
        result = tool.run(**request.parameters)
        return {"result": result.content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Execution failed: {str(e)}")
