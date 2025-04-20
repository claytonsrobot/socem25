# src/socem25/api/main.py

from fastapi import FastAPI
from socem25.startup import Startup

app = FastAPI()
startup = Startup()
startup.startup()

@app.get("/projects")
def get_projects():
    return [p.name for p in startup.services.project_manager.projects]

@app.on_event("shutdown")
def shutdown_event():
    startup.shutdown()