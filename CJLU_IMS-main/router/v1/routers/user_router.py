from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

from database.database import get_db
from model.schema.schemas.base import BaseResponse
from model.schema.schemas.user import UpdateUserProfileRequest
from service.user_service import UserService, get_user_service
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/profile")
async def get_profile(
    request: Request,
    db: AsyncSession = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    user_id = request.state.user_id
    role = request.state.role
    res = await service.get_user_profile(db, user_id, role)
    return BaseResponse.success(msg="User profile fetched successfully", data=res)


@router.put("/profile")
async def update_profile(
    request: Request,
    data: UpdateUserProfileRequest,
    db: AsyncSession = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    user_id = request.state.user_id
    role = request.state.role
    await service.update_user_profile(db, user_id, role, data)
    return BaseResponse.success(msg="User profile updated successfully")


@router.post("/avatar")
async def upload_avatar(
    request: Request,
    avatar: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    user_id = request.state.user_id
    res = await service.upload_avatar(db, user_id, avatar)
    return BaseResponse.success(msg="User avatar uploaded successfully", data=res)
