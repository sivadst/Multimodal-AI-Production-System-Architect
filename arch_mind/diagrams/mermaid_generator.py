from arch_mind.core.schemas import ArchitectureDesign, DBSchema, UseCase
import re

class MermaidGenerator:
    def generate_architecture(self, design: ArchitectureDesign) -> str:
        lines = ["graph TB", "  Client[Client]"]
        
        for service in design.services:
            lines.append(f"  {service.name}[{service.name.replace('_', ' ').title()}]")
            lines.append(f"  Client -->|API Call| {service.name}")
            
            # DB for service
            if service.data_models.tables:
                db_name = f"db_{service.name}"
                lines.append(f"  {db_name}[({db_name})]")
                lines.append(f"  {service.name} --> {db_name}")
                
            # Events published
            for event in service.events_published:
                lines.append(f"  EventBus[((Event Bus))]")
                lines.append(f"  {service.name} -->|Publishes {event.name}| EventBus")
                
            # Events consumed
            for event in service.events_consumed:
                lines.append(f"  EventBus -->|Consumes {event.name}| {service.name}")
                
            # Dependencies
            for dep in service.dependencies:
                lines.append(f"  {service.name} -->|Depends On| {dep}")
                
        # Deduplicate and return
        unique_lines = list(dict.fromkeys(lines))
        return "\n".join(unique_lines)
    
    def generate_sequence(self, use_case: UseCase) -> str:
        lines = ["sequenceDiagram"]
        for actor in use_case.actors:
            lines.append(f"  participant {actor}")
        lines.append(f"  Note over {', '.join(use_case.actors)}: {use_case.name}")
        return "\n".join(lines)
    
    def generate_er(self, db_schema: DBSchema) -> str:
        lines = ["erDiagram"]
        for table in db_schema.tables:
            lines.append(f"  {table.name} {{")
            for col in table.columns:
                pk_mark = " PK" if col.is_primary_key else ""
                lines.append(f"    {col.type} {col.name}{pk_mark}")
            lines.append("  }")
        return "\n".join(lines)

class D2Generator:
    def generate_architecture(self, design: ArchitectureDesign) -> str:
        lines = ["direction: right", "Client: {shape: person}"]
        
        for service in design.services:
            svc = service.name
            lines.append(f"{svc}: {{shape: rectangle}}")
            lines.append(f"Client -> {svc}: API")
            
            if service.data_models.tables:
                db_name = f"db_{svc}"
                lines.append(f"{db_name}: {{shape: cylinder}}")
                lines.append(f"{svc} -> {db_name}")
                
            for dep in service.dependencies:
                lines.append(f"{svc} -> {dep}")
                
            for event in service.events_published:
                lines.append("Event Bus: {shape: queue}")
                lines.append(f"{svc} -> Event Bus: {event.name}")
                
            for event in service.events_consumed:
                lines.append(f"Event Bus -> {svc}: {event.name}")
                
        return "\n".join(dict.fromkeys(lines))

class DiagramValidator:
    def validate_mermaid(self, diagram: str) -> bool:
        # Simple syntactic checks (unclosed brackets, valid start)
        if not (diagram.startswith("graph ") or diagram.startswith("sequenceDiagram") or diagram.startswith("erDiagram")):
            return False
        if diagram.count("[") != diagram.count("]"):
            return False
        if diagram.count("(") != diagram.count(")"):
            return False
        if diagram.count("{") != diagram.count("}"):
            return False
        return True
