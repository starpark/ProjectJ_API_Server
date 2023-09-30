import datetime
from sqlalchemy import Column, NVARCHAR, DATETIME, INT, BINARY
from sqlalchemy.orm import validates
from fastapi import HTTPException
from starlette import status
from app.database import Base

class PlayerAccounts(Base):
    __tablename__ = "PlayerAccounts"

    player_id = Column(INT, primary_key=True, nullable=False, autoincrement=True)
    name = Column("name", NVARCHAR(20), nullable=False)
    nickname = Column("nickname", NVARCHAR(12), nullable=False)
    password = Column("password", BINARY(60), nullable=False)
    registration_date = Column(DATETIME, nullable=False, default=datetime.datetime.now)

    @validates("name")
    def validate_name(self, key, name) -> str:
        if len(name) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="아이디가 너무 짧습니다."
            )
        elif len(name) > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="아이디가 너무 깁니다."
            )
        return name

    @validates("nickname")
    def validate_nickname(self, key, nickname) -> str:
        if len(nickname) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="닉네임이 너무 짧습니다."
            )
        elif len(nickname) > 12:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="닉네임이 너무 깁니다."
            )
        return nickname