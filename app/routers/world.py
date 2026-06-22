# app/routers/world.py
from fastapi import APIRouter
from app.db.database import get_connection
import json

router = APIRouter()

@router.get("/npcs")
def get_npcs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT npc_id, name, persona, genetic_seed FROM npcs")
    rows = cursor.fetchall()
    conn.close()
    return {"npcs": [
        {
            "npc_id": row["npc_id"],
            "name": row["name"],
            "persona": json.loads(row["persona"] or "{}"),
            "genetic_seed": json.loads(row["genetic_seed"] or "{}")
        }
        for row in rows
    ]}

@router.post("/worlds")
def create_world(owner_id: str, world_name: str):
    # UUID를 활용해 고유한 world_id 생성
    import uuid
    world_id = f"world_{uuid.uuid4().hex[:8]}"
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO worlds (world_id, owner_id, world_name) VALUES (?, ?, ?)",
                   (world_id, owner_id, world_name))
    conn.commit()
    conn.close()
    return {"world_id": world_id, "message": "월드가 생성되었습니다."}

@router.get("/worlds/{owner_id}")
def get_user_worlds(owner_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM worlds WHERE owner_id = ?", (owner_id,))
    rows = cursor.fetchall()
    conn.close()
    return {"worlds": [dict(row) for row in rows]}