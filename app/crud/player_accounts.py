import bcrypt
from sqlalchemy.orm import Session

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
    hashed_password = bcrypt.hashpw(player_create.password.encode("utf-8"), bcrypt.gensalt())
    print(hashed_password)
    db_player_account = PlayerAccounts(name=player_create.name, nickname=player_create.nickname, password=hashed_password)
    db.add(db_player_account)
    db.commit()
    db.refresh(db_player_account)
    return db_player_account

def get_existing_player(db: Session, player_create: PlayerAccountCreate):
    return db.query(PlayerAccounts).filter(
        (PlayerAccounts.name == player_create.name) |
        (PlayerAccounts.nickname == player_create.nickname)
    ).first()
