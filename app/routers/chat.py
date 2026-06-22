# app/routers/chat.py
from fastapi import APIRouter, HTTPException
from app.agents.chat import chat_with_npc
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    npc_id: str
    user_id: str
    message: str
    user_action: str = "ask"
    world_id: str  # 클라이언트가 명시적으로 전달해야 함

@router.post("/chat")
async def chat(request: ChatRequest):
    # world_id가 비어있는지 체크
    if not request.world_id:
        raise HTTPException(status_code=400, detail="world_id는 필수입니다.")
        
    # persona 인자를 제거하고 호출
    response = await chat_with_npc(
        npc_id=request.npc_id,
        user_id=request.user_id,
        user_message=request.message,
        user_action=request.user_action,
        world_id=request.world_id
    )
    return {"npc_response": response}