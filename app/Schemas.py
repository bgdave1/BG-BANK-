from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True


# Auth Schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# Transaction Schemas
class TransactionBase(BaseModel):
    amount: float
    type: str  # deposit, withdraw, transfer


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int
    timestamp: datetime
    user_id: int

    class Config:
        orm_mode = True
