from jinja2 import Environment, FileSystemLoader
from arch_mind.core.config import settings
from arch_mind.core.schemas import ArchitectureDesign, Microservice, GeneratedCode
import os

class TemplateEngine:
    def __init__(self, template_dir: str = settings.templates_dir):
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        self.env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
        
    def get_template(self, name: str):
        return self.env.get_template(name)

class PythonGenerator:
    def __init__(self, env: Environment):
        self.env = env
        
    def generate_service(self, service: Microservice) -> str:
        template = self.env.get_template("fastapi_service.py.j2")
        return template.render(
            service_name=service.name,
            endpoints=service.endpoints,
            models=service.data_models,
            events_published=service.events_published,
            dependencies=service.dependencies
        )
    
    def generate_dockerfile(self, service: Microservice) -> str:
        template = self.env.get_template("python_dockerfile.j2")
        return template.render(service_name=service.name)
        
    def generate_requirements(self) -> str:
        template = self.env.get_template("requirements.txt.j2")
        return template.render()

class TerraformGenerator:
    def __init__(self, env: Environment):
        self.env = env
        
    def generate_iac(self, design: ArchitectureDesign) -> str:
        template = self.env.get_template("main.tf.j2")
        return template.render(design=design)

class DBSchemaGenerator:
    def __init__(self, env: Environment):
        self.env = env
        
    def generate_alembic(self, service: Microservice) -> str:
        # Simplification: returning generic models.py content for sqlalchemy
        template = self.env.get_template("sqlalchemy_models.py.j2")
        return template.render(models=service.data_models)

class CodeGenerator:
    def __init__(self):
        self.engine = TemplateEngine()
        self.python_gen = PythonGenerator(self.engine.env)
        self.tf_gen = TerraformGenerator(self.engine.env)
        self.db_gen = DBSchemaGenerator(self.engine.env)
        
    async def generate(self, design: ArchitectureDesign, language: str = "python") -> GeneratedCode:
        generated = GeneratedCode()
        
        # Generate services
        for service in design.services:
            if language == "python":
                code = self.python_gen.generate_service(service)
                generated.service_code[f"{service.name}/main.py"] = code
                
                reqs = self.python_gen.generate_requirements()
                generated.service_code[f"{service.name}/requirements.txt"] = reqs
                
                dockerfile = self.python_gen.generate_dockerfile(service)
                generated.dockerfiles[service.name] = dockerfile
                
                models = self.db_gen.generate_alembic(service)
                generated.service_code[f"{service.name}/models.py"] = models
                
        # Generate docker-compose
        dc_template = self.engine.env.get_template("docker_compose.yml.j2")
        generated.docker_compose = dc_template.render(services=design.services)
        
        # Generate IAC
        generated.iac = self.tf_gen.generate_iac(design)
        
        return generated
