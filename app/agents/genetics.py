# app/agents/genetics.py
import random
import uuid

def merge_seeds(parent_a: dict, parent_b: dict) -> dict:
    """
    두 NPC의 유전 시드를 합성해서 자식 시드 생성
    """
    def blend(a: str, b: str) -> str:
        # 각 부모에서 절반씩 가져와 합성
        a_words = a.split()
        b_words = b.split()
        half_a = a_words[:len(a_words)//2]
        half_b = b_words[len(b_words)//2:]
        return " ".join(half_a + half_b)

    def mutate(text: str, chance: float = 0.1) -> str:
        # 돌연변이 — 랜덤 형질 추가
        mutations = [
            "with an unusual birthmark",
            "bearing a rare gift",
            "marked by fate",
            "touched by misfortune",
            "gifted with sharp instincts"
        ]
        if random.random() < chance:
            return text + f", {random.choice(mutations)}"
        return text

    child_seed = {
        "appearance": mutate(blend(
            parent_a.get("appearance", "unknown appearance"),
            parent_b.get("appearance", "unknown appearance")
        )),
        "personality": mutate(blend(
            parent_a.get("personality", "neutral"),
            parent_b.get("personality", "neutral")
        )),
        "ability": blend(
            parent_a.get("ability", "average"),
            parent_b.get("ability", "average")
        ),
        "story": f"Born from {parent_a.get('name', 'unknown')} and {parent_b.get('name', 'unknown')}.",
        "mutation_chance": round(
            (parent_a.get("mutation_chance", 0.1) + 
             parent_b.get("mutation_chance", 0.1)) / 2, 2
        )
    }

    return child_seed

def create_child_npc(parent_a_meta: dict, parent_b_meta: dict) -> dict:
    child_id = f"npc_{uuid.uuid4().hex[:6]}"
    child_seed = merge_seeds(
        parent_a_meta.get("genetic_seed", {}),
        parent_b_meta.get("genetic_seed", {})
    )

    return {
        "npc_id": child_id,
        "name": f"Child of {parent_a_meta.get('name', '?')} & {parent_b_meta.get('name', '?')}",
        "persona": {
            "background": child_seed["story"],
            "info_disclosure": "selective"
        },
        "genetic_seed": child_seed
    }