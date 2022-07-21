from fastapi import HTTPException, status, Response, Depends, APIRouter
from app.schemas.response import UserResponse
from app.utils.oauth2 import get_current_user
from ..database import models
from sqlalchemy.orm import Session
from ..database.connection import get_db
from typing import List

router = APIRouter(
    prefix="/admins",
    tags=["admins"]
)


@router.get("/",  response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    admin_user = db.query(models.AdminUser).filter(
        models.AdminUser.id == current_user.id).first()
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")

    users = db.query(models.User).all()
    return users


@router.get("/{user_id}",  response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    admin_user = db.query(models.AdminUser).filter(
        models.AdminUser.id == current_user.id).first()
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {user_id} not found")

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int,  db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    admin_user = db.query(models.AdminUser).filter(
        models.AdminUser.id == current_user.id).first()
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")

    deleted_user = db.query(models.User).filter(models.User.id == id)
    if not deleted_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    deleted_user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
