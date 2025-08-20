from .base_tool import BaseTool, ToolInput, ToolOutput
from pydantic import Field
import os
import json
from typing import Optional
from openai import OpenAI


class CalculatorInput(ToolInput):
    expression: str = Field(..., description="The mathematical expression to evaluate.")


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs mathematical calculations."
    args_schema = CalculatorInput

    def _run(self, expression: str) -> ToolOutput:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return ToolOutput(content="OpenAI API key not configured. Set OPENAI_API_KEY.")

        try:
            client = OpenAI(api_key=api_key)
            system = (
                "You are a strict calculator. Evaluate the given mathematical expression "
                "exactly and return a pure JSON object {\"result\": <number>} with no extra text."
            )
            user = f"Expression: {expression}\nReturn JSON only."

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0,
            )
            content = (resp.choices[0].message.content or "").strip()

            value: Optional[str] = None
            try:
                data = json.loads(content)
                if isinstance(data, dict) and "result" in data:
                    value = str(data["result"])
            except Exception:
                # fallback: extract number-like content
                value = content

            if value is None:
                return ToolOutput(content="Error: Unable to parse calculator result.")
            return ToolOutput(content=f"Result: {value}")
        except Exception as e:
            return ToolOutput(content=f"Calculator error: {str(e)}")
