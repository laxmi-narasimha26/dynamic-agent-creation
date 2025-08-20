from .base_tool import BaseTool, ToolInput, ToolOutput
from pydantic import Field
from typing import Optional
from openai import OpenAI
import os


class ChatbotInput(ToolInput):
    query: str = Field(..., description="The user's message to the chatbot")
    system: Optional[str] = Field(
        default="You are a helpful, concise assistant.",
        description="Optional system prompt to steer behavior.",
    )
    model: Optional[str] = Field(
        default="gpt-4o-mini",
        description="OpenAI model to use.",
    )


class ChatbotTool(BaseTool):
    name = "chatbot"
    description = "A simple OpenAI-powered chatbot that answers user queries."
    args_schema = ChatbotInput

    def _run(self, query: str, system: Optional[str] = None, model: Optional[str] = None) -> ToolOutput:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return ToolOutput(content="OpenAI API key not configured. Set OPENAI_API_KEY.")

        try:
            client = OpenAI(api_key=api_key)
            sys_prompt = system or "You are a helpful, concise assistant."
            mdl = model or "gpt-4o-mini"

            resp = client.chat.completions.create(
                model=mdl,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": query},
                ],
                temperature=0.2,
            )
            content = (resp.choices[0].message.content or "").strip()
            return ToolOutput(content=content)
        except Exception as e:
            return ToolOutput(content=f"Chatbot error: {str(e)}")
