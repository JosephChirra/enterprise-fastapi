from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import user

from app.routers import users

app = FastAPI(
    title="Enterprise EMS",
    version="1.0.0",
)



# Base.metadata.create_all(bind=engine)



app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"],
)


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "FastAPI is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}