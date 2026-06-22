# app/agents/memory.py
from app.db.database import get_connection
import json
from datetime import datetime

def save_memory(npc_id: str, user_id: str, raw_log: str, summary: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memories (npc_id, user_id, summary, raw_log, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        npc_id,
        user_id,
        json.dumps(summary, ensure_ascii=False),
        raw_log,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def load_memory(npc_id: str, user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM memories
        WHERE npc_id = ? AND user_id = ?
        ORDER BY updated_at DESC LIMIT 10
    """, (npc_id, user_id))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]