from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    name: str
    email: EmailStr


class User(UserOut):
    name: str
    email: EmailStr
    password: str
