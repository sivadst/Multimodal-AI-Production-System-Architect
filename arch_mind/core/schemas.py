from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field

# --- Requirements ---

class VisualElement(BaseModel):
    type: str # e.g., "box", "line", "text"
    label: str
    connections: List[str] = []

class ClarifyingQuestion(BaseModel):
    question: str
    context: str

class UseCase(BaseModel):
    name: str
    description: str
    actors: List[str] = []

class ParsedRequirement(BaseModel):
    actors: List[str] = []
    use_cases: List[UseCase] = []
    functional_requirements: List[str] = []
    non_functional_requirements: Dict[str, str] = {}
    constraints: List[str] = []
    assumptions: List[str] = []
    visual_elements: List[VisualElement] = []

class UnifiedRequirement(ParsedRequirement):
    clarifying_questions: List[ClarifyingQuestion] = []


# --- Architecture Design ---

class TradeoffAnalysis(BaseModel):
    pattern: str
    latency_estimation: str
    cost_estimation: str
    complexity: str
    scalability: str
    maintainability: str
    justification: str

class APIEndpoint(BaseModel):
    path: str
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    summary: str
    request_schema: Optional[str] = None
    response_schema: str
    is_public: bool = True

class DBColumn(BaseModel):
    name: str
    type: str
    is_primary_key: bool = False
    is_nullable: bool = False

class DBTable(BaseModel):
    name: str
    columns: List[DBColumn]
    relations: List[str] = []

class DBSchema(BaseModel):
    tables: List[DBTable]

class Event(BaseModel):
    name: str
    payload_schema: str
    producer: str
    consumers: List[str] = []

class Microservice(BaseModel):
    name: str
    responsibility: str
    owner_team: str = "backend"
    endpoints: List[APIEndpoint] = []
    data_models: DBSchema = Field(default_factory=lambda: DBSchema(tables=[]))
    events_published: List[Event] = []
    events_consumed: List[Event] = []
    dependencies: List[str] = [] # other service names

class ArchitectureDesign(BaseModel):
    primary_pattern: str
    tradeoffs: List[TradeoffAnalysis] = []
    services: List[Microservice] = []
    global_events: List[Event] = []
    rationale: str

# --- API Layer (FastAPI endpoints) ---

class DesignRequest(BaseModel):
    requirements_text: str
    whiteboard_image: Optional[str] = None # base64
    constraints: Dict[str, Any] = {}
    preferred_patterns: List[str] = []

class GeneratedCode(BaseModel):
    service_code: Dict[str, str] = {} # filename -> content
    dockerfiles: Dict[str, str] = {}
    docker_compose: str = ""
    iac: str = ""
    db_migrations: Dict[str, str] = {}

class ValidationReport(BaseModel):
    is_valid: bool
    consistency_errors: List[str] = []
    security_warnings: List[str] = []
    cost_estimate: str = ""

class TrafficEstimate(BaseModel):
    requests_per_second: int
    data_transfer_gb_month: int

class IaCConfig(BaseModel):
    provider: str = "aws"
    resources: List[Dict[str, Any]] = []

class CostProjection(BaseModel):
    monthly_total: float
    breakdown: Dict[str, float]

class ConsistencyReport(BaseModel):
    is_consistent: bool
    errors: List[str] = []

class SecurityReport(BaseModel):
    is_secure: bool
    warnings: List[str] = []
