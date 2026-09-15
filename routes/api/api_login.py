import os
from fastapi import APIRouter, Depends, HTTPException
from schema.login_schema import Login
from db.db_engine import Session, get_db, AsyncSession
from db.db_table_schema import User_Info
from sqlalchemy import select
from typing import Annotated
from sqlalchemy.exc import IntegrityError
import bcrypt
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
load_dotenv()
secret_key = os.environ.get("secret_key")
router = APIRouter(prefix="/api", tags=["login and register"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

def create_hashed_password(password:str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password:str, hashedpassword:str):
    return bcrypt.checkpw(password.encode('utf-8'), hashedpassword.encode('utf-8'))

@router.post("/login")
async def router_login(login:Login, db: Annotated[AsyncSession, Depends(get_db)]):
    email = login.email
    password = login.password
    query = select(User_Info.hashedpassword, User_Info.role).where(User_Info.email == email)
    response = await db.execute(query)
    val = response.fetchone()
    if not val or not verify_password(password, val[0]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": email, "role": val[1]})
    return {"message": "Login successful", "access_token": access_token, "role": val[1]}

@router.post("/register")
async def router_register(login:Login, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        email = login.email
        password = login.password
        hashedpassword = create_hashed_password(password)
        new_user = User_Info(email=email, hashedpassword=hashedpassword)
        db.add(new_user)
        await db.commit()
        return {"message": "Account created successfully"}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Account already exists")