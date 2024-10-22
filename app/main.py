from fastapi import FastAPI
from app.routers import interview
import os
import yaml
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager

app = FastAPI(
    title="Devterview AI API",
    description="This is the AI API for the Interview King application.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Common",
        },
        {
            "name": "Interview",
        }
    ]
)

def generate_openapi_yaml():
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Description of your API",
        routes=app.routes,
    )
    
    os.makedirs("lib", exist_ok=True)
    
    with open("lib/api-spec.yaml", "w") as file:
        yaml.dump(openapi_schema, file, default_flow_style=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Server starts
    yield
    # Server is shutting down
    generate_openapi_yaml()


app = FastAPI(lifespan=lifespan)

app.include_router(interview.router)

@app.get("/", tags=['Common'])
async def root():
    return {"message": "Welcome to the Devterview AI Server!"}