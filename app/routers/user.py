# app/routers/user.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.database import get_connection
import uuid

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    user_id: str = None  # 생략 시 서버에서 자동 생성

@router.post("/users")
def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    
    # user_id가 없으면 uuid 생성
    user_id = user.user_id or str(uuid.uuid4())[:8]
    
    try:
        cursor.execute(
            "INSERT INTO users (user_id, username) VALUES (?, ?)",
            (user_id, user.username)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"유저 생성 실패: {str(e)}")
    
    conn.close()
    return {"message": "유저가 성공적으로 생성되었습니다.", "user_id": user_id, "username": user.username}