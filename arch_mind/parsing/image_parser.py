from PIL import Image
import io
import base64
from typing import Optional
from arch_mind.core.schemas import ParsedRequirement, VisualElement
import pytesseract
from transformers import CLIPProcessor, CLIPModel
import torch
import openai
from arch_mind.core.config import settings

class CLIPEmbedder:
    def __init__(self):
        # We'll use a small model for classification of diagram types
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
    def classify_diagram_type(self, image: Image.Image) -> str:
        choices = ["flowchart", "entity relationship diagram", "system architecture diagram", "wireframe", "hand-drawn sketch"]
        inputs = self.processor(text=choices, images=image, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        best_idx = probs.argmax().item()
        return choices[best_idx]

class ImageRequirementParser:
    def __init__(self, clip_embedder: CLIPEmbedder):
        self.clip = clip_embedder
        self.client = openai.AsyncClient(api_key=settings.openai_api_key)
        self.model = settings.model_name
        
    async def parse_image(self, image: Image.Image) -> ParsedRequirement:
        # 1. Use CLIP to classify diagram type
        diagram_type = self.clip.classify_diagram_type(image)
        
        # 2. Use OCR (pytesseract) to extract text labels
        extracted_text = pytesseract.image_to_string(image).strip()
        
        # 3. Use LLM with vision capability (GPT-4o) to describe structure
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        prompt = f"""
        This is an image of a {diagram_type}.
        The following text was extracted via OCR:
        {extracted_text}
        
        Describe the diagram structure as a JSON object matching this schema:
        {{
            "visual_elements": [
                {{"type": "box|line|text|database|actor", "label": "name", "connections": ["list of connected labels"]}}
            ],
            "actors": ["any actors identified"],
            "functional_requirements": ["any functional flows identified"]
        }}
        """
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a software architect analyzing visual diagrams. Output valid JSON matching the schema exactly."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
                ]}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("No content from vision model")
            
        import json
        data = json.loads(content)
        
        req = ParsedRequirement()
        req.visual_elements = [VisualElement(**v) for v in data.get("visual_elements", [])]
        req.actors = data.get("actors", [])
        req.functional_requirements = data.get("functional_requirements", [])
        return req
