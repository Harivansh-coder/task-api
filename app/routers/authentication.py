from fastapi import HTTPException, status, Depends, APIRouter
from app.schemas.user import UserLogin
from ..database import models
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..utils.hash import verify_hash


router = APIRouter(
    tags=['authentication']
)


@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invalid credentials")

    if not verify_hash(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invalid credentials")

    return {"token": "jnsfvkjndsfvnjndsfkjvsdfvnjfkjdjkfdjjjsjsdfbnvdfnbvsjfdkvksafknvbaks"}
