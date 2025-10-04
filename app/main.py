from fastapi import FastAPI
from app.routes import text_analysis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Text Analysis API")


# origins = [
#     "http://localhost:3000",  # local frontend
#     "https://kai-developer-test.web.app/"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow all origins
    allow_credentials=False,   # must be False when using "*"
    allow_methods=["*"],       # allow all HTTP methods
    allow_headers=["*"],       # allow all headers
)

app.include_router(text_analysis.router, prefix="/api")
