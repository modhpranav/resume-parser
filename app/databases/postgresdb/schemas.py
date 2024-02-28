from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserSignUp(BaseModel):
    username: str
    password: Optional[str]
    fullname: Optional[str] = None
    picture: Optional[str] = None


class User(BaseModel):
    username: str
    fullname: Optional[str]
    provider: Optional[str]
    register_date: Optional[datetime]
    skills: Optional[str]
    resume: Optional[str]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserStat(BaseModel):
    provider: str
    count: int

