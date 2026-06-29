from arch_mind.core.schemas import ParsedRequirement, UnifiedRequirement, ClarifyingQuestion
from arch_mind.parsing.text_parser import LLMProvider
import openai
from pydantic import BaseModel
from typing import List

class MergedResponse(BaseModel):
    actors: List[str]
    use_cases: List[dict]
    functional_requirements: List[str]
    non_functional_requirements: dict
    constraints: List[str]
    assumptions: List[str]
    visual_elements: List[dict]

class RequirementMerger:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        
    async def merge_requirements(self, text_req: ParsedRequirement, image_req: ParsedRequirement) -> UnifiedRequirement:
        prompt = f"""
        Merge the following requirements extracted from text and image.
        Resolve conflicts, combine lists, and create a unified view.
        
        Text Requirements:
        {text_req.model_dump_json()}
        
        Image Requirements:
        {image_req.model_dump_json()}
        
        Return a merged JSON matching this schema:
        {{
            "actors": [],
            "use_cases": [{{"name": "", "description": "", "actors": []}}],
            "functional_requirements": [],
            "non_functional_requirements": {{}},
            "constraints": [],
            "assumptions": [],
            "visual_elements": [{{"type": "", "label": "", "connections": []}}]
        }}
        """
        
        merged_data = await self.llm.extract_structured(prompt, MergedResponse)
        return UnifiedRequirement(
            actors=merged_data.actors,
            use_cases=merged_data.use_cases,
            functional_requirements=merged_data.functional_requirements,
            non_functional_requirements=merged_data.non_functional_requirements,
            constraints=merged_data.constraints,
            assumptions=merged_data.assumptions,
            visual_elements=merged_data.visual_elements,
            clarifying_questions=[]
        )

class AmbiguityDetector:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        
    async def detect(self, req: UnifiedRequirement) -> List[ClarifyingQuestion]:
        class QuestionsList(BaseModel):
            questions: List[ClarifyingQuestion]
            
        prompt = f"""
        Analyze the following unified system requirements for missing critical information.
        Check for missing: scale expectations, data volume, latency requirements, security needs, compliance (e.g. GDPR).
        Identify ambiguous terms or contradictory requirements.
        
        Requirements:
        {req.model_dump_json()}
        
        Return a JSON object with a list of clarifying questions:
        {{
            "questions": [
                {{"question": "What is the expected peak QPS?", "context": "Needed to determine DB scaling strategy"}},
                {{"question": "Do you need GDPR compliance?", "context": "User data is mentioned but no compliance specified"}}
            ]
        }}
        """
        
        response = await self.llm.extract_structured(prompt, QuestionsList)
        return response.questions
