# src/socem25/api/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from socem25.startup import Startup

@asynccontextmanager
async def lifespan(app: FastAPI):
    startup = Startup()
    startup.startup()
    app.state.startup = startup  # Save to app state for use in routes
    yield
    startup.shutdown()

app = FastAPI(lifespan=lifespan) 
@app.get("/projects")
def get_projects():
    startup = app.state.startup
    return [p.name for p in startup.services.project_manager.projects]
