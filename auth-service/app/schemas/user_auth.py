from pydantic import BaseModel, EmailStr, Field


class UserAuthCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)

