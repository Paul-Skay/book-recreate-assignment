from fastapi import APIRouter, HTTPException, status
from database import users
from schemas.user import Response, UserCreate, UserUpdate
from services.user import user_service


user_router = APIRouter()


@user_router.get("")
def get_users():
    return users


@user_router.get("/{id}")
def get_user_by_id(id: str):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found.")
    return {
        "message": "user retrieved successfully",
        "data": user
    }


@user_router.post("", status_code=status.HTTP_201_CREATED)
def add_user(user_in: UserCreate):
    user = user_service.create_user(user_in)
    return Response(message="user added successfully", data=user)


@user_router.put("/{id}")
def update_user(id: str, user_in: UserUpdate):
    user = user_service.update_user(id, user_in)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"user with id: {id} not found"
        )
    return Response(message="user updated successfully", data=user)

@user_router.delete("/{id}")
def delete_user(id: str):
    is_deleted = user_service.delete_user(id)
    if not is_deleted:
        raise HTTPException(
            status_code=404,
            detail=f"user with id: {id} not found"
        )
    return Response(message="user deleted successfully")
