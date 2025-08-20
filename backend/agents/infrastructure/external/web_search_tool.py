from .base_tool import BaseTool, ToolInput, ToolOutput
from pydantic import Field
from typing import Optional
import os
import httpx
from urllib.parse import quote


class WebSearchInput(ToolInput):
    query: str = Field(..., description="The search query to execute.")


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Searches the web (Mock API: DuckDuckGo Instant Answer)."
    args_schema = WebSearchInput

    def _run(self, query: str) -> ToolOutput:
        # Use DuckDuckGo Instant Answer API (no key needed)
        # https://api.duckduckgo.com/?q=your+query&format=json&no_redirect=1&no_html=1
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_redirect": "1",
            "no_html": "1",
        }
        try:
            with httpx.Client(timeout=10, headers={"User-Agent": "AgentSystem/1.0"}) as client:
                resp = client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()

            results: list[str] = ["[Mock API] Using DuckDuckGo Instant Answer free endpoint."]
            # Prefer direct answers
            answer = (data or {}).get("Answer") or (data or {}).get("Definition")
            answer_url = (data or {}).get("AbstractURL") or (data or {}).get("DefinitionURL")
            if answer:
                results.append(f"Answer: {answer}{' (' + answer_url + ')' if answer_url else ''}")
            # Abstract text if present
            abstract = (data or {}).get("AbstractText")
            if abstract:
                results.append(f"Abstract: {abstract}")

            # Primary results
            for r in (data or {}).get("Results", [])[:3]:
                text = r.get("Text")
                first_url = r.get("FirstURL")
                if text:
                    results.append(f"{text} ({first_url})" if first_url else text)

            # Related topics (flatten a bit)
            related = (data or {}).get("RelatedTopics", [])
            for item in related:
                if "Text" in item:
                    results.append(item["Text"])
                elif "Topics" in item and isinstance(item["Topics"], list):
                    for t in item["Topics"][:2]:
                        if t.get("Text"):
                            results.append(t["Text"])
                if len(results) >= 5:
                    break

            # Note: Wikipedia fallback removed per requirement to use DuckDuckGo only.

            if not results:
                results = ["No results found."]

            return ToolOutput(content="\n".join(results))
        except Exception as e:
            return ToolOutput(content=f"Web search error: {str(e)}")
