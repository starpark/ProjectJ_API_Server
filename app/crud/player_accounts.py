import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from app.models.player_accounts import PlayerAccounts
from app.schemas.player_accounts import (
    PlayerAccountWithToken,
    PlayerAccountLogin,
    PlayerAccountCreate,
    PlayerAccountUpdate
)

def get_player_by_name(db: Session, player_name: str):
    return db.query(PlayerAccounts).filter(PlayerAccounts.name == player_name).first()

def get_player_by_nickname(db: Session, player_nickname: str):
    return db.query(PlayerAccounts).filter(PlayerAccounts.nickname == player_nickname).first()

def create_player_account(db: Session, player_create: PlayerAccountCreate):
    if len(player_create.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호가 너무 짧습니다."
        )

    hashed_password = bcrypt.hashpw(player_create.password.encode("utf-8"), bcrypt.gensalt())
    db_player_account = PlayerAccounts(name=player_create.name, nickname=player_create.nickname, password=hashed_password)
    db.add(db_player_account)
    db.commit()
    db.refresh(db_player_account)
    return db_player_account

def get_existing_player(db: Session, player_create: PlayerAccountCreate):
    result = db.query(PlayerAccounts)
    if result.filter(PlayerAccounts.name == player_create.name).first():
        return "이미 존재하는 아이디입니다."

    if result.filter(PlayerAccounts.nickname == player_create.nickname).first():
        return "이미 존재하는 닉네임입니다."