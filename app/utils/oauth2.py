from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas.token import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "boom"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        playload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = playload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(sttus_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)
