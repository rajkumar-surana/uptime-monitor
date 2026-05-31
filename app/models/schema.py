from pydantic import BaseModel

class authRequest(BaseModel):
    email: str
    password:str

class monitorCreate(BaseModel):
    url: str
    interval_seconds: int = 60
    webhook_url: str | None = None

class monitorUpdate(BaseModel):
    interval_seconds: int | None= None
    webhook_url: str | None = None
    is_active:bool | None = None
