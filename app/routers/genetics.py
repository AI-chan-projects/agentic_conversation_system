# app/routers/genetics.py
from fastapi import APIRouter
from app.agents.genetics import create_child_npc
from app.db.database import get_connection
from pydantic import BaseModel
import json

router = APIRouter()

class BreedRequest(BaseModel):
    parent_a_id: str
    parent_b_id: str

@router.post("/breed")
def breed(request: BreedRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM npcs WHERE npc_id = ?", (request.parent_a_id,))
    parent_a = dict(cursor.fetchone())
    parent_a["genetic_seed"] = json.loads(parent_a["genetic_seed"] or "{}")

    cursor.execute("SELECT * FROM npcs WHERE npc_id = ?", (request.parent_b_id,))
    parent_b = dict(cursor.fetchone())
    parent_b["genetic_seed"] = json.loads(parent_b["genetic_seed"] or "{}")

    conn.close()

    child = create_child_npc(parent_a, parent_b)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO npcs (npc_id, name, persona, genetic_seed)
        VALUES (?, ?, ?, ?)
    """, (
        child["npc_id"],
        child["name"],
        json.dumps(child["persona"], ensure_ascii=False),
        json.dumps(child["genetic_seed"], ensure_ascii=False)
    ))
    conn.commit()
    conn.close()

    return {"child": child}