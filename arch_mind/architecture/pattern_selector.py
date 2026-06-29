from typing import List
from pydantic import BaseModel
from arch_mind.core.schemas import UnifiedRequirement, TradeoffAnalysis, ArchitectureDesign, Microservice, Event
from arch_mind.parsing.text_parser import LLMProvider
import json

class PatternSelection(BaseModel):
    selected_patterns: List[str]
    justification: str

class TradeoffsList(BaseModel):
    tradeoffs: List[TradeoffAnalysis]

class ServiceList(BaseModel):
    services: List[Microservice]
    global_events: List[Event]

class TradeoffAnalyzer:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        
    async def analyze_tradeoffs(self, req: UnifiedRequirement, patterns: List[str]) -> List[TradeoffAnalysis]:
        prompt = f"""
        Analyze trade-offs for these architectural patterns based on the requirements.
        Patterns: {patterns}
        
        Requirements:
        {req.model_dump_json()}
        
        For each pattern, estimate:
        - Latency (p50, p99)
        - Cost (fixed + variable)
        - Complexity (cognitive load, deployment complexity)
        - Scalability (horizontal scaling ease)
        - Maintainability (testing, debugging, onboarding)
        
        Return a JSON object:
        {{
            "tradeoffs": [
                {{
                    "pattern": "microservices",
                    "latency_estimation": "Higher p99 due to network hops",
                    "cost_estimation": "Higher baseline cost (multiple instances)",
                    "complexity": "High deployment complexity",
                    "scalability": "Excellent per-service scaling",
                    "maintainability": "Requires distributed tracing",
                    "justification": "Good fit for large teams..."
                }}
            ]
        }}
        """
        response = await self.llm.extract_structured(prompt, TradeoffsList)
        return response.tradeoffs

class PatternSelector:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        self.available_patterns = ["microservices", "monolith", "serverless", "event_driven", "cqrs", "saga"]
        
    async def select_patterns(self, req: UnifiedRequirement) -> List[str]:
        prompt = f"""
        Select the most appropriate primary architecture pattern(s) from this list: {self.available_patterns}
        based on these requirements:
        {req.model_dump_json()}
        
        Consider team size (implied), scale, data requirements, and constraints.
        If it's a small team/low traffic, prefer monolith.
        
        Return a JSON object:
        {{
            "selected_patterns": ["microservices", "event_driven"],
            "justification": "High scale and independent teams require microservices..."
        }}
        """
        response = await self.llm.extract_structured(prompt, PatternSelection)
        return response.selected_patterns

class ServiceDesigner:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        
    async def design_services(self, req: UnifiedRequirement, primary_pattern: str) -> tuple[List[Microservice], List[Event]]:
        prompt = f"""
        Design the services, APIs, data models, and events for this system.
        Primary Pattern: {primary_pattern}
        
        Requirements:
        {req.model_dump_json()}
        
        For each bounded context:
        - Define service name, responsibility, owner team
        - Define REST API endpoints
        - Define data ownership (DB schemas)
        - Define events published/consumed
        - Define dependencies
        
        Return JSON object:
        {{
            "services": [
                {{
                    "name": "user_service",
                    "responsibility": "Manage user identities",
                    "owner_team": "identity",
                    "endpoints": [
                        {{"path": "/users", "method": "POST", "summary": "Create user", "response_schema": "User", "is_public": true}}
                    ],
                    "data_models": {{
                        "tables": [
                            {{"name": "users", "columns": [{{"name": "id", "type": "uuid", "is_primary_key": true, "is_nullable": false}}]}}
                        ]
                    }},
                    "events_published": [{{"name": "UserCreated", "payload_schema": "UserCreatedPayload", "producer": "user_service", "consumers": []}}],
                    "events_consumed": [],
                    "dependencies": []
                }}
            ],
            "global_events": [
                {{"name": "UserCreated", "payload_schema": "UserCreatedPayload", "producer": "user_service", "consumers": []}}
            ]
        }}
        """
        response = await self.llm.extract_structured(prompt, ServiceList)
        return response.services, response.global_events

class ArchitectureDesigner:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        self.pattern_selector = PatternSelector(llm_provider)
        self.tradeoff_analyzer = TradeoffAnalyzer(llm_provider)
        self.service_designer = ServiceDesigner(llm_provider)
        
    async def design(self, req: UnifiedRequirement) -> ArchitectureDesign:
        # 1. Select patterns
        selected_patterns = await self.pattern_selector.select_patterns(req)
        primary = selected_patterns[0] if selected_patterns else "monolith"
        
        # 2. Analyze tradeoffs for candidates (top 3 patterns maybe, but let's just analyze the selected ones + monolith for baseline)
        candidates = list(set(selected_patterns + ["monolith"]))
        tradeoffs = await self.tradeoff_analyzer.analyze_tradeoffs(req, candidates)
        
        # 3. Design services
        services, global_events = await self.service_designer.design_services(req, primary)
        
        return ArchitectureDesign(
            primary_pattern=primary,
            tradeoffs=tradeoffs,
            services=services,
            global_events=global_events,
            rationale=f"Selected {primary} based on requirements analysis."
        )
