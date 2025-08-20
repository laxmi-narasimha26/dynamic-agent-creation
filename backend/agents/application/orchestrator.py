from typing import TypedDict, List, Generator, Dict, Any
from langgraph.graph import StateGraph, END
from agents.core.services.tool_registry import ToolRegistry, get_global_registry


class AgentState(TypedDict):
    query: str
    tools: List[str]
    index: int
    context: str
    last_output: str


def _make_graph(tool_registry: ToolRegistry):
    graph = StateGraph(AgentState)

    def run_next_tool(state: AgentState) -> AgentState:
        tools = state["tools"]
        idx = state["index"]
        q = state["query"]
        context = state["context"]
        if idx >= len(tools):
            return state
        name = tools[idx]
        # Create tool instance (supports class-based and function-based). If missing, skip.
        try:
            tool = tool_registry.create_tool(name)
        except Exception:
            return {
                **state,
                "index": idx + 1,
                "last_output": f"Skipping unknown tool: {name}",
            }
        try:
            if name == "web_search":
                out = tool.run(query=q)
                content = str(out.content)
                context += f"\n[web_search]\n{content}\n"
            elif name == "calculator":
                out = tool.run(expression=q)
                content = str(out.content)
                context += f"\n[calculator]\n{content}\n"
            elif name == "summarizer":
                text_to_summarize = (context or q).strip()
                out = tool.run(text=text_to_summarize, max_length=240, query=q)
                content = str(out.content)
                context += f"\n[summarizer]\n{content}\n"
            else:
                # Attempt generic pass-through using kwargs
                out = tool.run(query=q, text=context or q)
                content = str(out.content)
                context += f"\n[{name}]\n{content}\n"
            return {
                **state,
                "index": idx + 1,
                "context": context,
                "last_output": content,
            }
        except Exception as e:
            return {
                **state,
                "index": idx + 1,
                "last_output": f"Tool {name} error: {e}",
            }

    graph.add_node("step", run_next_tool)

    def should_continue(state: AgentState) -> str:
        return "step" if state["index"] < len(state["tools"]) else END

    graph.set_entry_point("step")
    graph.add_conditional_edges("step", should_continue)

    return graph.compile()


def stream_agent_events(agent: Any, query: str) -> Generator[Dict[str, Any], None, None]:
    registry = get_global_registry()
    app = _make_graph(registry)

    init: AgentState = {
        "query": (query or "").strip(),
        "tools": agent.tools or [],
        "index": 0,
        "context": "",
        "last_output": "",
    }

    yield {"type": "message", "content": f"Processing query: {init['query']}"}
    yield {"type": "message", "content": f"Loaded agent '{agent.name}' with tools: {', '.join(init['tools']) or 'none'}"}

    # Ensure summarizer is included when using web_search to produce a concise final answer
    tools = list(init["tools"]) if init["tools"] else []
    if ("web_search" in tools) and ("summarizer" not in tools):
        tools.append("summarizer")
        yield {"type": "message", "content": "Auto-attached 'summarizer' to refine web search results."}
    init["tools"] = tools

    for state in app.stream(init, stream_mode="values"):
        # Emit last step output if any
        last = state.get("last_output")
        if last:
            yield {"type": "message", "content": last}

    # Final result is the aggregated context
    final_context = state.get("context", "") if 'state' in locals() else ""
    yield {"type": "result", "content": final_context.strip()}
    yield {"type": "complete"}
