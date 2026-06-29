import pytest
from arch_mind.parsing.text_parser import ParsedRequirement

def test_parsing_schemas():
    req = ParsedRequirement(
        actors=["admin"],
        use_cases=[{"name": "login", "description": "admin logs in", "actors": ["admin"]}]
    )
    assert req.actors == ["admin"]
    assert req.use_cases[0].name == "login"
