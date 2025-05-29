from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserAuthCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)


class UserAuthRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class UserAuthVerify(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)
