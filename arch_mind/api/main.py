from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from arch_mind.api.routes import router
from arch_mind.core.telemetry import logger

app = FastAPI(title="ArchMind API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("ArchMind API started")

@app.get("/health")
async def health():
    return {"status": "ok"}
