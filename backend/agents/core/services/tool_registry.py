from typing import Dict, Type, Any, Optional, Callable
import inspect
from ...infrastructure.external.base_tool import BaseTool, ToolOutput
from ...infrastructure.external.web_search_tool import WebSearchTool
from ...infrastructure.external.calculator_tool import CalculatorTool
from ...infrastructure.external.summarizer_tool import SummarizerTool
from ...infrastructure.external.chatbot_tool import ChatbotTool
import ast
import os
import json


class ToolRegistry:
    def __init__(self):
        # Store tool metadata supporting both class-based and function-based tools
        # kind: 'class' -> {'class': Type[BaseTool]}
        # kind: 'function' -> {'callable': Callable, 'description': str, 'parameters': [str]}
        self._tools: Dict[str, Dict[str, Any]] = {
            'web_search': {'kind': 'class', 'class': WebSearchTool},
            'calculator': {'kind': 'class', 'class': CalculatorTool},
            'summarizer': {'kind': 'class', 'class': SummarizerTool},
            'chatbot': {'kind': 'class', 'class': ChatbotTool},
        }
        # Load any persisted runtime tools
        try:
            self._load_persisted()
        except Exception as e:
            # Avoid crashing on startup due to persistence problems
            try:
                print(f"[tools] warn: failed to load persisted tools: {e}")
            except Exception:
                pass

    def _save_persisted_llm_code_entry(self, name: str, description: str, code: str) -> None:
        """Persist an llm_code tool entry including code for rehydration."""
        path = self._persist_path()
        payload = []
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    if isinstance(existing, list):
                        payload = existing
        except Exception:
            payload = []
        updated = False
        for item in payload:
            if item.get('name') == name:
                item.update({
                    'name': name,
                    'kind': 'function',
                    'description': description,
                    'parameters': ["input"],
                    'llm_code': True,
                    'code': code,
                })
                updated = True
                break
        if not updated:
            payload.append({
                'name': name,
                'kind': 'function',
                'description': description,
                'parameters': ["input"],
                'llm_code': True,
                'code': code,
            })
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception as e:
            try:
                print(f"[tools] warn: failed to persist llm-code tool '{name}': {e}")
            except Exception:
                pass
    
    def get_tool_class(self, tool_type: str) -> Optional[Type[BaseTool]]:
        meta = self._tools.get(tool_type)
        if not meta:
            return None
        if meta.get('kind') == 'class':
            return meta.get('class')
        return None
    
    def create_tool(self, tool_type: str, **kwargs) -> BaseTool:
        if tool_type not in self._tools:
            raise ValueError(f"Unknown tool: {tool_type}")
        meta = self._tools[tool_type]
        if meta.get('kind') == 'class':
            tool_class: Type[BaseTool] = meta['class']
            # Filter kwargs to match constructor
            filtered_kwargs = {
                k: v for k, v in kwargs.items()
                if k in getattr(tool_class.__init__, '__annotations__', {})
            }
            return tool_class(**filtered_kwargs)
        elif meta.get('kind') == 'function':
            fn: Callable[..., Any] = meta['callable']
            description: str = meta.get('description', '')
            params: list[str] = meta.get('parameters', [])

            # Build a lightweight wrapper tool so the rest of the system can run .run()
            # Define a dynamic args_schema-compatible model for listing is not necessary here;
            # parameters are already tracked in meta for list_tools().
            class FunctionTool(BaseTool):  # type: ignore
                name = tool_type
                description = description
                args_schema = None  # parameters provided by registry list

                def _run(self, **call_kwargs):
                    # Filter provided args to the function signature
                    sig = inspect.signature(fn)
                    # If the function accepts **kwargs, pass everything through to preserve inputs like 'input'
                    if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()):
                        bound = call_kwargs
                    else:
                        bound = {k: v for k, v in call_kwargs.items() if k in sig.parameters}
                    res = fn(**bound)
                    # If async, await in a dedicated event loop for this thread
                    if inspect.isawaitable(res):
                        import asyncio
                        try:
                            # Create a new loop for this worker thread
                            loop = asyncio.new_event_loop()
                            try:
                                asyncio.set_event_loop(loop)
                                res = loop.run_until_complete(res)
                            finally:
                                loop.close()
                                asyncio.set_event_loop(None)
                        except Exception as e:
                            return ToolOutput(content=f"Custom tool async execution error: {e}")
                    return ToolOutput(content=str(res))

            return FunctionTool()
        else:
            raise ValueError(f"Unsupported tool kind for {tool_type}")
    
    def register_from_code(self, code: str, tool_name: str, description: Optional[str] = None) -> None:
        """Register a tool from Python source.
        Accepts either a BaseTool subclass or a plain function (sync/async).
        """
        # Basic safety: refuse very large blobs
        if len(code) > 10000:
            raise ValueError("Code too large; limit ~10KB")

        namespace: Dict[str, Any] = {}
        exec(code, namespace)

        # 1) Prefer a BaseTool subclass if present
        tool_class = next(
            (v for v in namespace.values()
             if isinstance(v, type) and issubclass(v, BaseTool) and v is not BaseTool),
            None
        )
        if tool_class:
            self._tools[tool_name] = {'kind': 'class', 'class': tool_class}
            # Persist class-based tool code as well for reloads
            self._save_persisted_entry(tool_name, 'class', code, description or '', parameters=[])
            return

        # 2) Otherwise accept a top-level callable (function)
        fn = None
        # Prefer an object matching the provided tool_name
        candidate = namespace.get(tool_name)
        if candidate and (inspect.isfunction(candidate) or inspect.iscoroutinefunction(candidate)):
            fn = candidate
        if fn is None:
            # Find first non-dunder function defined in this snippet (avoid builtins and classes)
            for k, v in namespace.items():
                if k.startswith("__"):
                    continue
                if inspect.isfunction(v) or inspect.iscoroutinefunction(v):
                    fn = v
                    break
        if not fn:
            raise ValueError("No callable or BaseTool subclass found in code")

        # Inspect parameters for listing
        try:
            sig = inspect.signature(fn)
            param_names = [p.name for p in sig.parameters.values() if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
        except Exception:
            param_names = []

        self._tools[tool_name] = {
            'kind': 'function',
            'callable': fn,
            'description': description or '',
            'parameters': param_names,
        }
        # Persist function-based tool so it survives reloads
        self._save_persisted_entry(tool_name, 'function', code, description or '', parameters=param_names)
    
    def register_llm_tool(self, tool_name: str, description: str, parameters: Optional[list[str]] = None) -> None:
        """Register an LLM-proxy tool that forwards input to OpenAI Chat Completions.
        Parameters default to ["input"].
        """
        param_names = parameters or ["input"]

        # Capture description in the closure for the system prompt
        system_prompt = (
            f"You are a specialized tool named '{tool_name}'. "
            f"{description}. Respond with the final result only, no preamble."
        )

        def llm_proxy(**kwargs) -> str:
            try:
                # Prefer 'input' as main content; otherwise forward kwargs as JSON
                main = kwargs.get('input')
                if main is None:
                    try:
                        main = json.dumps(kwargs, ensure_ascii=False)
                    except Exception:
                        main = str(kwargs)
                from openai import OpenAI
                client = OpenAI()
                resp = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": str(main)},
                    ],
                    temperature=0.0,
                    max_tokens=128,
                )
                return (resp.choices[0].message.content or "").strip()
            except Exception as e:
                return f"LLM tool error: {e}"

        self._tools[tool_name] = {
            'kind': 'function',
            'callable': llm_proxy,
            'description': description,
            'parameters': param_names,
        }
        # Persist as a special llm_proxy entry
        self._save_persisted_llm_entry(tool_name, description, param_names)

    def register_llm_code_tool(self, tool_name: str, description: str, code: str) -> None:
        """Register a code-backed LLM execution tool.
        The tool never executes code locally; instead, it sends a strict execution prompt to OpenAI with the provided code and input.
        Parameters are fixed to ["input"].
        """
        strict_prompt_prefix = (
            "You are \u201cToolRunner-GPT\u201d, a deterministic Python interpreter that executes one async\n"
            "function in your reasoning space.\n\n"
            "RULES\n"
            "1. Read TOOL NAME, DESCRIPTION, CODE, INPUT exactly as provided\u2014do not modify.\n"
            "2. Mentally evaluate the CODE on the INPUT under Python 3.11 semantics.\n"
            "3. If async, assume one await cycle.\n"
            "4. Return ONLY the function\u2019s return value as plain text\u2014no commentary, no formatting.\n"
            "5. If execution would raise an error, return the error text only.\n\n"
            "TOOL NAME\n[[>]]\n\nTOOL DESCRIPTION\n[[>]]\n\nTOOL SOURCE CODE\n```python\n[[>]]\n```\n\nINPUT TO THE FUNCTION\n[[>]]\n\nBEGIN EXECUTION NOW \u2014 RETURN SINGLE RESULT STRING ONLY"
        )

        def llm_code_runner(**kwargs) -> str:
            try:
                user_input = kwargs.get('input')
                if user_input is None:
                    try:
                        user_input = json.dumps(kwargs, ensure_ascii=False)
                    except Exception:
                        user_input = str(kwargs)
                from openai import OpenAI
                client = OpenAI()
                messages = [
                    {"role": "system", "content": strict_prompt_prefix},
                    {"role": "user", "content": (
                        f"TOOL NAME\n{tool_name}\n\n"
                        f"TOOL DESCRIPTION\n{description}\n\n"
                        f"TOOL SOURCE CODE\n```python\n{code}\n```\n\n"
                        f"INPUT TO THE FUNCTION\n{user_input}"
                    )},
                ]
                resp = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.0,
                    max_tokens=128,
                )
                return (resp.choices[0].message.content or "").strip()
            except Exception as e:
                return f"LLM tool error: {e}"

        self._tools[tool_name] = {
            'kind': 'function',
            'callable': llm_code_runner,
            'description': description,
            'parameters': ["input"],
        }
        self._save_persisted_llm_code_entry(tool_name, description, code)
    
    def list_tools(self) -> Dict[str, dict]:
        info: Dict[str, dict] = {}
        for name, meta in self._tools.items():
            if meta.get('kind') == 'class':
                cls = meta['class']
                description = getattr(cls, 'description', '') or ''
                params = []
                try:
                    schema = getattr(cls, 'args_schema', None)
                    if schema is not None:
                        if hasattr(schema, 'model_fields'):
                            params = list(schema.model_fields.keys())
                        elif hasattr(schema, '__fields__'):
                            params = list(schema.__fields__.keys())
                except Exception:
                    params = []
                info[name] = {
                    'class': cls.__name__,
                    'description': description,
                    'parameters': params,
                }
            elif meta.get('kind') == 'function':
                info[name] = {
                    'class': 'function',
                    'description': meta.get('description', ''),
                    'parameters': meta.get('parameters', []),
                }
        return info

    # ------------------------- Persistence helpers -------------------------
    def _persist_path(self) -> str:
        # Save under backend/config/registered_tools.json relative to this file
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../config'))
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, 'registered_tools.json')

    def _load_persisted(self) -> None:
        path = self._persist_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return
        if not isinstance(data, list):
            return
        for entry in data:
            try:
                name = entry.get('name')
                kind = entry.get('kind')
                desc = entry.get('description', '')
                if not name:
                    continue
                if name in self._tools:
                    continue
                # Rehydrate special llm_proxy entries
                if entry.get('llm_proxy') is True:
                    params = entry.get('parameters') or ["input"]
                    self.register_llm_tool(name, desc, params)
                    continue
                # Rehydrate llm_code entries
                if entry.get('llm_code') is True:
                    code = entry.get('code') or ''
                    if code:
                        self.register_llm_code_tool(name, desc, code)
                    continue
                # Fallback to code-based entries
                code = entry.get('code')
                if not code:
                    continue
                self.register_from_code(code, name, desc)
            except Exception as e:
                try:
                    print(f"[tools] warn: failed to load persisted '{entry}': {e}")
                except Exception:
                    pass

    def _save_persisted_entry(self, name: str, kind: str, code: str, description: str, parameters: list[str]) -> None:
        path = self._persist_path()
        payload = []
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    if isinstance(existing, list):
                        payload = existing
        except Exception:
            payload = []
        # Upsert by name
        updated = False
        for item in payload:
            if item.get('name') == name:
                item.update({
                    'name': name,
                    'kind': kind,
                    'code': code,
                    'description': description,
                    'parameters': parameters,
                })
                updated = True
                break
        if not updated:
            payload.append({
                'name': name,
                'kind': kind,
                'code': code,
                'description': description,
                'parameters': parameters,
            })
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception as e:
            try:
                print(f"[tools] warn: failed to persist tool '{name}': {e}")
            except Exception:
                pass

    def _save_persisted_llm_entry(self, name: str, description: str, parameters: list[str]) -> None:
        """Persist an llm_proxy tool entry without code for rehydration."""
        path = self._persist_path()
        payload = []
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    if isinstance(existing, list):
                        payload = existing
        except Exception:
            payload = []
        # Upsert by name
        updated = False
        for item in payload:
            if item.get('name') == name:
                item.update({
                    'name': name,
                    'kind': 'function',
                    'description': description,
                    'parameters': parameters,
                    'llm_proxy': True,
                })
                updated = True
                break
        if not updated:
            payload.append({
                'name': name,
                'kind': 'function',
                'description': description,
                'parameters': parameters,
                'llm_proxy': True,
            })
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception as e:
            try:
                print(f"[tools] warn: failed to persist llm tool '{name}': {e}")
            except Exception:
                pass

# Module-level singleton so all routers and orchestrator share state
_GLOBAL_REGISTRY: Optional[ToolRegistry] = None

def get_global_registry() -> ToolRegistry:
    global _GLOBAL_REGISTRY
    if _GLOBAL_REGISTRY is None:
        _GLOBAL_REGISTRY = ToolRegistry()
    return _GLOBAL_REGISTRY
