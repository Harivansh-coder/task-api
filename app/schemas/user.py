from pydantic import BaseModel, EmailStr, constr

# model for response


class UserOut(BaseModel):
    name: str
    email: EmailStr

# model for signup


class User(UserOut):
    password: constr(min_length=8)

# model for login


class UserLogin(BaseModel):
    email: EmailStr
    password: str
