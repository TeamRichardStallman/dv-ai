from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Config


def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[Config.BACK_API_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
