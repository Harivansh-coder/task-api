from fastapi import HTTPException, status, Response, Depends, APIRouter
from app.schemas.response import UserResponse
from app.schemas.user import User
from ..database import models
from sqlalchemy.orm import Session
from ..database.connection import get_db
from typing import List
from ..utils.hash import password_hash


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/",  response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: User, db: Session = Depends(get_db)):

    user.password = password_hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}",  response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {user_id} not found")

    return user


# @router.patch("/{id}", response_model=UserResponse)
# def update_user(id: int, user: User,  db: Session = Depends(get_db)):

#     update_query = db.query(models.User).filter(models.User.id == id)

#     # if user does not exits
#     if not update_query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"user with id {id} not found")
#     # if user do exits
#     update_query.update(user.dict(), synchronize_session=False)
#     db.commit()
#     return update_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int,  db: Session = Depends(get_db)):

    deleted_user = db.query(models.User).filter(models.User.id == id)
    if not deleted_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    deleted_user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
