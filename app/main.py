from fastapi import FastAPI
from app.routers import interview

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


app.include_router(interview.router)

@app.get("/", tags=['Common'])
async def root():
    return {"message": "Welcome to the Devterview AI Server!"}