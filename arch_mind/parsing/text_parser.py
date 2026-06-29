from arch_mind.core.schemas import ParsedRequirement
from typing import Optional
from pydantic import BaseModel, Field
import json
import openai
from arch_mind.core.config import settings

class LLMProvider:
    def __init__(self):
        self.client = openai.AsyncClient(api_key=settings.openai_api_key)
        self.model = settings.model_name
        
    async def extract_structured(self, prompt: str, schema_class: type[BaseModel]) -> BaseModel:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a senior software architect parsing product requirements. Extract information into the provided JSON schema perfectly. ONLY return valid JSON without any markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("No content returned from LLM")
        return schema_class.model_validate_json(content)

class TextRequirementParser:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
    
    async def parse_text(self, requirement_text: str) -> ParsedRequirement:
        prompt = f"""
        Extract from this product requirement: actors, use cases, functional requirements, non-functional requirements (latency, throughput, availability), constraints, implicit assumptions.

        Return a JSON object that matches this schema:
        {{
            "actors": ["user", "admin"],
            "use_cases": [{{"name": "...", "description": "...", "actors": ["..."]}}],
            "functional_requirements": ["..."],
            "non_functional_requirements": {{"latency": "...", "throughput": "..."}},
            "constraints": ["..."],
            "assumptions": ["..."]
        }}

        Requirement text:
        {requirement_text}
        """
        
        # We need a strict schema model that matches the structure. ParsedRequirement already matches it.
        return await self.llm.extract_structured(prompt, ParsedRequirement)
