import pytest
from arch_mind.core.schemas import ArchitectureDesign, Microservice, DBTable, DBColumn, DBSchema
from arch_mind.diagrams.mermaid_generator import MermaidGenerator
from arch_mind.validation.consistency_checker import ConsistencyChecker
from arch_mind.core.schemas import GeneratedCode

def test_mermaid_generator():
    design = ArchitectureDesign(
        primary_pattern="microservices",
        services=[
            Microservice(name="auth", responsibility="Auth")
        ],
        rationale=""
    )
    gen = MermaidGenerator()
    out = gen.generate_architecture(design)
    assert "graph TB" in out
    assert "auth" in out

def test_consistency_checker():
    design = ArchitectureDesign(
        primary_pattern="microservices",
        services=[Microservice(name="auth", responsibility="Auth")],
        rationale=""
    )
    code = GeneratedCode()
    # auth/main.py is missing
    checker = ConsistencyChecker()
    report = checker.check(design, code)
    assert not report.is_consistent
    assert "Missing generated code for service: auth" in report.errors

    # Fix error
    code.service_code["auth/main.py"] = ""
    report = checker.check(design, code)
    assert report.is_consistent
