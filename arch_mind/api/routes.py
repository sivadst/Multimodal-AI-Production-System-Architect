import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from arch_mind.core.schemas import DesignRequest, ArchitectureDesign, GeneratedCode, ValidationReport, TrafficEstimate
from arch_mind.parsing.text_parser import TextRequirementParser, LLMProvider
from arch_mind.parsing.image_parser import ImageRequirementParser, CLIPEmbedder
from arch_mind.parsing.requirement_merger import RequirementMerger, AmbiguityDetector
from arch_mind.architecture.pattern_selector import ArchitectureDesigner
from arch_mind.code_generation.template_engine import CodeGenerator
from arch_mind.validation.consistency_checker import ConsistencyChecker, SecurityScanner
from arch_mind.diagrams.mermaid_generator import MermaidGenerator, D2Generator
from arch_mind.api.websocket import manager
from arch_mind.core.schemas import ParsedRequirement
import uuid

router = APIRouter()

# In-memory store for demo
designs_db = {}
code_db = {}

llm = LLMProvider()
text_parser = TextRequirementParser(llm)
clip = CLIPEmbedder()
image_parser = ImageRequirementParser(clip)
merger = RequirementMerger(llm)
designer = ArchitectureDesigner(llm)
code_gen = CodeGenerator()
consistency = ConsistencyChecker()
security = SecurityScanner()
mermaid_gen = MermaidGenerator()
d2_gen = D2Generator()

@router.post("/architect/design", response_model=ArchitectureDesign)
async def design_architecture(req: DesignRequest):
    text_req = await text_parser.parse_text(req.requirements_text)
    
    if req.whiteboard_image:
        import base64
        import io
        from PIL import Image
        
        img_data = base64.b64decode(req.whiteboard_image.split(",")[1] if "," in req.whiteboard_image else req.whiteboard_image)
        img = Image.open(io.BytesIO(img_data))
        image_req = await image_parser.parse_image(img)
    else:
        image_req = ParsedRequirement()
        
    unified_req = await merger.merge_requirements(text_req, image_req)
    
    design = await designer.design(unified_req)
    
    design_id = str(uuid.uuid4())
    designs_db[design_id] = design
    return design

@router.post("/architect/generate", response_model=GeneratedCode)
async def generate_code(design_id: str, language: str = "python"):
    if design_id not in designs_db:
        raise HTTPException(status_code=404, detail="Design not found")
        
    design = designs_db[design_id]
    code = await code_gen.generate(design, language)
    code_db[design_id] = code
    return code

@router.post("/architect/validate", response_model=ValidationReport)
async def validate_design(design_id: str):
    if design_id not in designs_db or design_id not in code_db:
        raise HTTPException(status_code=404, detail="Design or code not found")
        
    design = designs_db[design_id]
    code = code_db[design_id]
    
    c_report = consistency.check(design, code)
    s_report = security.scan(code)
    
    return ValidationReport(
        is_valid=c_report.is_consistent and s_report.is_secure,
        consistency_errors=c_report.errors,
        security_warnings=s_report.warnings
    )

@router.get("/architect/diagram/{design_id}")
async def get_diagram(design_id: str, format: str = "mermaid"):
    if design_id not in designs_db:
        raise HTTPException(status_code=404, detail="Design not found")
        
    design = designs_db[design_id]
    if format == "mermaid":
        return {"diagram": mermaid_gen.generate_architecture(design)}
    elif format == "d2":
        return {"diagram": d2_gen.generate_architecture(design)}
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

@router.websocket("/ws/design/{design_id}")
async def design_stream(websocket: WebSocket, design_id: str):
    await manager.connect(websocket)
    try:
        await manager.send_message({"step": "parsing", "detail": "Extracting requirements..."}, websocket)
        await asyncio.sleep(1)
        await manager.send_message({"step": "designing", "detail": "Selecting microservices pattern..."}, websocket)
        await asyncio.sleep(1)
        await manager.send_message({"step": "generating", "detail": "Writing FastAPI service..."}, websocket)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
