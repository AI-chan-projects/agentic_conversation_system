# app/agents/background.py
from app.agents.relationship import update_relationship, get_relationships
from app.db.database import get_connection
import random
from datetime import datetime

def simulate_background_events(world_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    # 해당 world의 모든 NPC 가져오기
    cursor.execute("SELECT npc_id FROM npcs")
    npcs = [row["npc_id"] for row in cursor.fetchall()]
    conn.close()

    if len(npcs) < 2:
        return []

    events = []

    # NPC 쌍마다 랜덤 이벤트 발생
    for i in range(len(npcs)):
        for j in range(i+1, len(npcs)):
            npc_a = npcs[i]
            npc_b = npcs[j]

            # 30% 확률로 이벤트 발생
            if random.random() < 0.3:
                event_type = random.choice([
                    "trade",      # 우호 +
                    "conflict",   # 적대 +
                    "rumor",      # 중립 변화
                ])

                strength_delta = {
                    "trade": 0.1,
                    "conflict": -0.15,
                    "rumor": random.uniform(-0.05, 0.05)
                }[event_type]

                update_relationship(
                    entity_a=npc_a,
                    entity_b=npc_b,
                    world_id=world_id,
                    relation_type=event_type,
                    strength_delta=strength_delta
                )

                events.append({
                    "npc_a": npc_a,
                    "npc_b": npc_b,
                    "event": event_type,
                    "delta": strength_delta,
                    "timestamp": datetime.now().isoformat()
                })

    return events

# 백그라운드 이벤트 배치 시뮬레이션 설명
# 핵심 개념은 — 유저가 없는 동안 NPC끼리 자율적으로 상호작용한 것처럼 접속 시점에 시뮬레이션하는 거야.
# 예를 들어 유저가 3일 만에 접속하면, 그 사이 Elena랑 다른 NPC가 사이가 나빠졌을 수도 있는 거지.