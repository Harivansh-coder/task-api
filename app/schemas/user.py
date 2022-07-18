from pydantic import BaseModel, EmailStr

# model for response


class UserOut(BaseModel):
    name: str
    email: EmailStr

# model for signup


class User(UserOut):
    password: str

# model for login


class UserLogin(BaseModel):
    email: EmailStr
    password: str
