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
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

@router.post("/login", response_model=PlayerAccountWithToken)
def login(player_account: PlayerAccountLogin, db: Session = Depends(get_db)):
    #check player account in db
    player = crud.get_player_by_name(db=db, player_name=player_account.name)
    if not player or not bcrypt.checkpw(player_account.password.encode("utf-8"), player.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    #make some token
    payload = {
        "player_id": player.player_id,
        "name": player.name,
        "nickname": player.nickname,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    #return PlayerAccountWithToken
    return {
        "player_id": player.player_id,
        "name": player.name,
        "nickname": player.nickname,
        "token": token
    }

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_player(player_create: PlayerAccountCreate, db: Session = Depends(get_db)):
    #check existing player
    player = crud.get_existing_player(db=db, player_create=player_create)
    if player:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already existing player")

    #insert player
    try:
        crud.create_player_account(db=db, player_create=player_create)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_414_REQUEST_URI_TOO_LONG, detail="Parameter too long")
