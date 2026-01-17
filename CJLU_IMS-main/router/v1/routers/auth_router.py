from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from database.database import get_db
from model.schema.schemas.base import BaseResponse
from service.auth_service import AuthService, get_auth_service
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    res = await service.login(db=db, username=username, password=password)
    return BaseResponse.success(msg="Login successful", data=res)


@router.post("/register")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: AsyncSession = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    res = await service.register(db=db, username=username, password=password, role=role)
    return BaseResponse.success(msg="Registration successful", data=res)


@router.put("/reset-password")
async def reset_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    db: AsyncSession = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    user_id = request.state.user_id
    res = await service.reset_password(
        db=db, user_id=user_id, old_password=old_password, new_password=new_password
    )
    return BaseResponse.success(msg="Password reset successful", data=res)


@router.get("/public-key")
async def get_public_key(
    request: Request,
    service: AuthService = Depends(get_auth_service),
) -> PlainTextResponse:
    if request.cookies.get("session_id") and request.cookies.get("timestamp"):
        pas = True
    else:
        pas = False
    key, session_id, timestamp = await service.get_public_key(pas)
    base_resp = BaseResponse.success(data={"public_key": key})
    response = JSONResponse(content=base_resp.model_dump())
    if pas:
        return response
    response.set_cookie(
        key="session_id", value=session_id, httponly=True, samesite="lax", expires=3500
    )
    response.set_cookie(
        key="timestamp", value=timestamp, httponly=True, samesite="lax", expires=3500
    )
    return response


@router.post("/refresh-public-key")
async def refresh_public_key(
    request: Request,
    service: AuthService = Depends(get_auth_service),
):
    user_id = request.state.user_id
    role = request.state.role
    await service.refresh_public_key(user_id, role)
    return BaseResponse.success(msg="Public key refreshed successfully", data={})
