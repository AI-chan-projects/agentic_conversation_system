# app/models/user.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    user_id: str
    username: str

class UserNPCLink(BaseModel):
    user_id: str
    npc_id: str
    world_id: str