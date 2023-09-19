from pydantic import BaseModel
from typing import Optional

class PlayerAccountBase(BaseModel):
    name: str
    nickname: str

class PlayerAccountLogin(BaseModel):
    name: str
    password: str

class PlayerAccountCreate(PlayerAccountLogin):
    nickname: str

class PlayerAccountUpdate(BaseModel):
    nickname: Optional[str]
    password: Optional[str]

class PlayerAccountWithToken(PlayerAccountBase):
    player_id: int
    token: str

class PlayerAccount(PlayerAccountBase):
    player_id: int

    class Config:
        from_attributes = True