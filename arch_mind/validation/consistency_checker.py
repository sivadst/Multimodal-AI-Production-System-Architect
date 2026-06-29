from arch_mind.core.schemas import ArchitectureDesign, GeneratedCode, ConsistencyReport, SecurityReport, CostProjection, IaCConfig, TrafficEstimate
import re

class ConsistencyChecker:
    def check(self, design: ArchitectureDesign, code: GeneratedCode) -> ConsistencyReport:
        errors = []
        
        for service in design.services:
            # 1. Every service in design has generated code
            main_py_path = f"{service.name}/main.py"
            if main_py_path not in code.service_code:
                errors.append(f"Missing generated code for service: {service.name}")
                continue
                
            code_content = code.service_code[main_py_path]
            
            # 2. Every API endpoint in design has implementation
            for endpoint in service.endpoints:
                if endpoint.path not in code_content:
                    errors.append(f"Missing endpoint {endpoint.path} in {service.name}")
                    
        # 3. Check for published/consumed event mismatches globally
        all_published = set()
        all_consumed = set()
        for svc in design.services:
            for ev in svc.events_published:
                all_published.add(ev.name)
            for ev in svc.events_consumed:
                all_consumed.add(ev.name)
                
        for consumed in all_consumed:
            if consumed not in all_published:
                errors.append(f"Event {consumed} is consumed but never published")
                
        return ConsistencyReport(is_consistent=len(errors) == 0, errors=errors)

class SecurityScanner:
    def scan(self, code: GeneratedCode) -> SecurityReport:
        warnings = []
        secret_pattern = re.compile(r'(api_key|password|secret)\s*=\s*[\'"][^\'"]+[\'"]', re.IGNORECASE)
        
        for filepath, content in code.service_code.items():
            if secret_pattern.search(content):
                warnings.append(f"Possible hardcoded secret found in {filepath}")
                
        # Basic check for JWT/Auth middleware in FastAPI setup (simplified)
        for filepath, content in code.service_code.items():
            if filepath.endswith("main.py"):
                if "Depends" in content and "get_db" in content:
                    pass # At least dependencies are used
                # Real implementation would check for actual Auth Dependency
                
        return SecurityReport(is_secure=len(warnings) == 0, warnings=warnings)

class CostEstimator:
    def estimate(self, iac: str, traffic: TrafficEstimate) -> CostProjection:
        # Dummy estimation logic for demonstration
        compute_cost = 50.0  # Base cost for ECS Fargate
        db_cost = 30.0       # Base cost for RDS
        network_cost = traffic.data_transfer_gb_month * 0.09
        
        total = compute_cost + db_cost + network_cost
        breakdown = {
            "compute": compute_cost,
            "database": db_cost,
            "network": network_cost
        }
        
        return CostProjection(monthly_total=total, breakdown=breakdown)
