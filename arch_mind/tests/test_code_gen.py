import pytest
from arch_mind.core.schemas import ArchitectureDesign, Microservice, DBTable, DBColumn, DBSchema
from arch_mind.code_generation.template_engine import CodeGenerator
import ast

@pytest.mark.asyncio
async def test_code_generation():
    design = ArchitectureDesign(
        primary_pattern="microservices",
        services=[
            Microservice(
                name="auth", 
                responsibility="Auth",
                data_models=DBSchema(tables=[
                    DBTable(name="users", columns=[DBColumn(name="id", type="Integer", is_primary_key=True)])
                ])
            )
        ],
        rationale=""
    )
    generator = CodeGenerator()
    code = await generator.generate(design, "python")
    
    assert "auth/main.py" in code.service_code
    assert "auth/models.py" in code.service_code
    assert "auth" in code.dockerfiles
    assert code.docker_compose
    assert code.iac
    
    # Check syntax of generated python code
    ast.parse(code.service_code["auth/main.py"])
    ast.parse(code.service_code["auth/models.py"])
