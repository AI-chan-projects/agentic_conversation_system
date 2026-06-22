# app/main.py
from fastapi import FastAPI
from app.db.database import init_db
from app.routers import coupling, chat, genetics, world, user, relationship
from app.agents.background import simulate_background_events

app = FastAPI(title="NPC Agent System")

app.include_router(coupling.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(genetics.router, prefix="/api")
app.include_router(world.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(relationship.router, prefix="/api")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "NPC Agent System Running"}

@app.post("/api/simulate/{world_id}")
def simulate(world_id: str):
    events = simulate_background_events(world_id)
    return {"events": events, "count": len(events)}