import pytest
from arch_mind.core.schemas import ArchitectureDesign, Microservice
from arch_mind.diagrams.mermaid_generator import MermaidGenerator, D2Generator, DiagramValidator

def test_mermaid_syntax():
    design = ArchitectureDesign(
        primary_pattern="microservices",
        services=[Microservice(name="test_svc", responsibility="Test")],
        rationale=""
    )
    m_gen = MermaidGenerator()
    diagram = m_gen.generate_architecture(design)
    
    validator = DiagramValidator()
    assert validator.validate_mermaid(diagram)
    
def test_d2_syntax():
    design = ArchitectureDesign(
        primary_pattern="microservices",
        services=[Microservice(name="test_svc", responsibility="Test")],
        rationale=""
    )
    d_gen = D2Generator()
    diagram = d_gen.generate_architecture(design)
    assert "direction: right" in diagram
    assert "test_svc" in diagram
