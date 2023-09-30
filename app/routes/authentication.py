import bcrypt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt

import app.crud.player_accounts as crud
from app.database import get_db
from app.models.player_accounts import PlayerAccounts
from app.schemas.player_accounts import (
    PlayerAccountCreate,
    PlayerAccountLogin,
    PlayerAccountWithToken
)

router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/login", response_model=PlayerAccountWithToken, status_code=status.HTTP_200_OK)
def login(player_account: PlayerAccountLogin, db: Session = Depends(get_db)):
    #check player account in db

    result = crud.get_player_by_name(db=db, player_name=player_account.name)
    if not result or not bcrypt.checkpw(player_account.password.encode("utf-8"), result.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 정확하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    #make some token
    payload = {
        "player_id": result.player_id,
        "name": result.name,
        "nickname": result.nickname,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    #return PlayerAccountWithToken
    return {
        "player_id": result.player_id,
        "name": result.name,
        "nickname": result.nickname,
        "token": token
    }

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_account(player_create: PlayerAccountCreate, db: Session = Depends(get_db)):
    #check existing player
    result = crud.get_existing_player(db=db, player_create=player_create)
    if result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result)

    #create player account
    crud.create_player_account(db=db, player_create=player_create)
