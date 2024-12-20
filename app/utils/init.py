from contextlib import asynccontextmanager

from app.utils.generate import generate_openapi_yaml


@asynccontextmanager
async def lifespan(app):
    yield
    generate_openapi_yaml(app)
