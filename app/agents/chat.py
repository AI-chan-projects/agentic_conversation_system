# app/agents/chat.py
import httpx
import json
from app.agents.memory import save_memory, load_memory
from app.agents.disclosure import should_disclose, get_disclosure_response
from app.agents.relationship import get_relationships
from app.db.database import get_connection

OLLAMA_URL = "http://localhost:11434/api/chat"
NPC_MODEL = "gemma2:2b"

async def chat_with_npc(npc_id: str, user_id: str, user_message: str,
                         user_action: str = "ask", world_id: str = "world_001"):
    
    # 1. DB에서 NPC 페르소나 데이터 조회
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, persona FROM npcs WHERE npc_id = ?", (npc_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return "NPC 정보를 찾을 수 없습니다."

    npc_name = row["name"]
    persona = json.loads(row["persona"] or "{}")

    # 2. 관계 강도 가져오기
    relationships = get_relationships(npc_id, world_id)
    strength = relationships[0]["strength"] if relationships else 0.0

    # 3. 비밀 정보 공개 여부 확인
    secret = persona.get("secret", None)
    if secret:
        disclosed = should_disclose(persona, strength, user_action)
        if not disclosed:
            return get_disclosure_response(False, secret)

    # 4. 이전 메모리 불러오기
    memories = load_memory(npc_id, user_id)
    memory_context = "\n".join([m["summary"] for m in memories if m["summary"]])

    # 5. NPC 시스템 프롬프트 구성
    system_prompt = f"""
    You are {npc_name}.
    {persona.get('background', '')}
    info_disclosure: {persona.get('info_disclosure', 'selective')}
    
    Past interactions with this user:
    {memory_context}
    """

    payload = {
        "model": NPC_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json=payload, timeout=30)
        result = response.json()

    npc_response = result["message"]["content"]

    # 6. 메모리 저장
    save_memory(
        npc_id=npc_id,
        user_id=user_id,
        raw_log=f"user: {user_message}\nnpc: {npc_response}",
        summary={"last_topic": user_message[:50]}
    )

    return npc_response