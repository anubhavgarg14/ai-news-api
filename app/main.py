from fastapi import FastAPI

from app.api.routes import ask, health, news, search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI News API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)
app.include_router(search.router)
app.include_router(ask.router)
app.include_router(health.router)
