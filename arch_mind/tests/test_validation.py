import pytest
from arch_mind.core.schemas import ArchitectureDesign, Microservice, GeneratedCode
from arch_mind.validation.consistency_checker import ConsistencyChecker, SecurityScanner

def test_security_scanner():
    code = GeneratedCode()
    code.service_code["config.py"] = "api_key = '12345'"
    scanner = SecurityScanner()
    report = scanner.scan(code)
    assert not report.is_secure
    assert "Possible hardcoded secret found in config.py" in report.warnings
    
    code.service_code["config.py"] = "api_key = os.getenv('API_KEY')"
    report = scanner.scan(code)
    assert report.is_secure
