import jwt
import bcrypt
import os
from fastapi import HTTPException, Request
from datetime import datetime, timedelta, timezone

def hash_pwd(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def verify_pwd(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_token(user_id, email):
    expires = datetime.now(timezone.utc) + timedelta(hours=24)
    expires_at=int(expires.timestamp())
    secret=os.getenv("SECRET_KEY")
    token=jwt.encode({"sub":user_id, "email":email, "aud":"uptime-monitor4000", "exp":expires_at },secret , algorithm="HS256")
    return token

def decode_token(token):
    #verify sign and expiry
    secret=os.getenv("SECRET_KEY")
    try:
        hey= jwt.decode(token,secret, algorithms=["HS256"], audience="uptime-monitor4000")
    except:
        raise HTTPException(400, "Not a valid token")
    if(hey["sub"]):
        return hey["sub"]
    else :
        raise HTTPException(404,"Not a valid user")


async def get_current_user(request:Request):
    try:
        auth_header = request.headers.get("Authorization")  # "Bearer eyJhbG..."
        if(auth_header==None or auth_header=="" or not auth_header.startswith("Bearer ")):
            raise HTTPException(401,"Invalid auth header")
        token = auth_header.split(" ")[1] 
        return decode_token(token)                   # "eyJhbG..."
    except:
        raise HTTPException(401, "Invalid token or token does not exist")
    

