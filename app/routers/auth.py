from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.schemas.user import UserLogin
from ..database import models
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..utils import hash, oauth2

router = APIRouter(
    tags=['authentication']
)


@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # for oauth2passwordform username = useremail

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"invalid credentials")

    if not hash.verify_hash(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"invalid credentials")

    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {"access_token": access_token, "token_type": "bearer"}
