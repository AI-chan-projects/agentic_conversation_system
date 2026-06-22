# app/routers/coupling.py
from fastapi import APIRouter
from app.db.database import get_connection
from app.models.user import UserNPCLink
import uuid

router = APIRouter()

@router.post("/couple")
def couple_user_npc(link: UserNPCLink):
    conn = get_connection()
    cursor = conn.cursor()

    # 이미 커플링 됐는지 확인
    cursor.execute("""
        SELECT * FROM relationships
        WHERE entity_a = ? AND entity_b = ? AND world_id = ?
    """, (link.user_id, link.npc_id, link.world_id))

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {"status": "already_linked", "world_id": link.world_id}

    # 새 커플링 생성
    cursor.execute("""
        INSERT INTO relationships (entity_a, entity_b, relation_type, strength, world_id)
        VALUES (?, ?, 'user_npc', 0.0, ?)
    """, (link.user_id, link.npc_id, link.world_id))

    conn.commit()
    conn.close()
    return {"status": "linked", "world_id": link.world_id}