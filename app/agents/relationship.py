# app/agents/relationship.py
from app.db.database import get_connection
from datetime import datetime

def update_relationship(entity_a: str, entity_b: str, world_id: str, 
                         relation_type: str, strength_delta: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM relationships
        WHERE entity_a = ? AND entity_b = ? AND world_id = ?
    """, (entity_a, entity_b, world_id))

    existing = cursor.fetchone()

    if existing:
        new_strength = min(1.0, max(-1.0, existing["strength"] + strength_delta))
        cursor.execute("""
            UPDATE relationships
            SET strength = ?, relation_type = ?, updated_at = ?
            WHERE entity_a = ? AND entity_b = ? AND world_id = ?
        """, (new_strength, relation_type, datetime.now().isoformat(),
              entity_a, entity_b, world_id))
    else:
        cursor.execute("""
            INSERT INTO relationships 
            (entity_a, entity_b, relation_type, strength, world_id, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (entity_a, entity_b, relation_type, strength_delta, 
              world_id, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def get_relationships(entity_id: str, world_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM relationships
        WHERE (entity_a = ? OR entity_b = ?) AND world_id = ?
        ORDER BY strength DESC
    """, (entity_id, entity_id, world_id))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_relationships(world_id: str): # 모든 관계를 가져오는 함수 따로 생성
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relationships WHERE world_id = ?", (world_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_relationship_graph(world_id: str):
    relationships = get_all_relationships(world_id) # 필터링 없는 함수 사용
    nodes_set = set()
    edges = []
    
    for rel in relationships:
        nodes_set.add(rel["entity_a"])
        nodes_set.add(rel["entity_b"])
        edges.append({
            "source": rel["entity_a"], 
            "target": rel["entity_b"], 
            "strength": rel["strength"] # 대시보드와 이름 맞춤
        })
    
    nodes = [{"id": n, "label": n} for n in nodes_set]
    return {"nodes": nodes, "edges": edges}