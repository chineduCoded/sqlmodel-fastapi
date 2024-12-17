from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import heroes, teams
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "ok"}

app.include_router(heroes.router, tags=["Heroes"])
app.include_router(teams.router, tags=["Teams"])