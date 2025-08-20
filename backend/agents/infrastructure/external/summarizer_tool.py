from .base_tool import BaseTool, ToolInput, ToolOutput
from pydantic import Field
import os
from openai import OpenAI
from typing import Optional, List


class SummarizerInput(ToolInput):
    text: str = Field(..., description="The text to summarize.")
    max_length: int = Field(default=200, description="Maximum length of the summary in words (target around 200).")
    query: Optional[str] = Field(default=None, description="User query to tailor the summary (optional).")


class SummarizerTool(BaseTool):
    name = "summarizer"
    description = "Summarizes text content."
    args_schema = SummarizerInput

    def _run(self, text: str, max_length: int = 200, query: Optional[str] = None) -> ToolOutput:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return ToolOutput(content="OpenAI API key not configured. Set OPENAI_API_KEY.")

        try:
            client = OpenAI(api_key=api_key)
            # Normalize
            normalized = (text or "").strip()
            if not normalized:
                return ToolOutput(content="")

            # If very short input, request a single-paragraph abstract per constraints
            short_mode = len(normalized.split()) < 150

            # Compose ProSummarizer-GPT system prompt
            sys_prompt = (
                "You are “ProSummarizer-GPT”, a senior technical writer.\n"
                "TASK\n"
                "  • Produce a concise, executive-style summary of the material delimited by triple back-ticks.\n"
                "  • Capture ONLY the core arguments, facts and conclusions; omit anecdotes, filler, marketing fluff.\n"
                "  • Length target: ≈12 % of original tokens, hard cap 200 words.\n"
                "  • Tone: neutral, professional, third-person.\n"
                "  • Format: "
                + ("Single-paragraph abstract." if short_mode else "\n        1. One-sentence headline.\n        2. 3-to-5 key-point bullets, each ≤25 words.\n        3. “TL;DR:” one-sentence wrap-up.")
                + "\n\nCONSTRAINTS\n"
                "  • Do not add external knowledge.\n"
                "  • Preserve all critical numbers, names, and dates.\n"
                "  • Rewrite; never quote verbatim ≥20 words.\n"
                "  • If source text is <150 words, return a single-paragraph abstract instead of bullets.\n"
            )
            if query:
                sys_prompt += f"\nAdditional Context: The user's query to address is: '{query}'.\n"

            user_content = f"TEXT\n```\n{normalized}\n```"

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.2,
            )
            content = (resp.choices[0].message.content or "").strip()

            # Enforce ~200-word cap conservatively
            def cap_words(s: str, cap: int = 200) -> str:
                words = s.split()
                if len(words) <= cap:
                    return s
                return " ".join(words[:cap]) + "…"

            content = cap_words(content, max_length)
            return ToolOutput(content=content)
        except Exception as e:
            return ToolOutput(content=f"Summarizer error: {str(e)}")
