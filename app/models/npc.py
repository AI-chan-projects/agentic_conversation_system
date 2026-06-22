# app/models/npc.py
from pydantic import BaseModel
from typing import Optional

class GeneticSeed(BaseModel):
    appearance: str        # 외형 시드
    personality: str       # 성격 시드
    ability: str           # 능력치 시드
    story: str             # 스토리 시드
    mutation_chance: float # 돌연변이 확률 0.0~1.0

class NPCMeta(BaseModel):
    npc_id: str
    name: str
    persona: dict          # 세계관 내 기본 정보
    genetic_seed: GeneticSeed
    info_disclosure: str   # "open" | "selective" | "hidden"