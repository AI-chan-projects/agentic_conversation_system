#app/routers/relationship.py
from fastapi import APIRouter
from app.agents.relationship import get_relationship_graph

router = APIRouter()

@router.get("/graph/{world_id}")
def get_world_graph(world_id: str):
    return get_relationship_graph(world_id)