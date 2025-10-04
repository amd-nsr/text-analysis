from fastapi import FastAPI
from app.routes import text_analysis

app = FastAPI(title="Text Analysis API")

app.include_router(text_analysis.router, prefix="/api")
