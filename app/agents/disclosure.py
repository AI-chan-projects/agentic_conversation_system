# app/agents/disclosure.py
import random

def should_disclose(npc_persona: dict, relationship_strength: float, 
                    user_action: str) -> bool:
    """
    NPC가 정보를 공개할지 결정
    - info_disclosure: open / selective / hidden
    - relationship_strength: -1.0 ~ 1.0
    - user_action: ask / persuade / threaten
    """
    disclosure_type = npc_persona.get("info_disclosure", "selective")

    if disclosure_type == "open":
        return True

    if disclosure_type == "hidden":
        # 협박이면 50% 확률로 공개
        if user_action == "threaten":
            return random.random() < 0.5
        return False

    # selective — 관계 강도 + 행동 기반
    if user_action == "threaten":
        return random.random() < 0.3
    elif user_action == "persuade":
        threshold = 0.3 - (relationship_strength * 0.3)
        return random.random() < threshold
    else:  # ask
        threshold = 0.5 + (relationship_strength * 0.5)
        return random.random() < threshold

def get_disclosure_response(disclosed: bool, secret: str) -> str:
    if disclosed:
        return f"[공개] {secret}"
    return "[거절] 그 정보는 알려줄 수 없어."