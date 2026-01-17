from fastapi import APIRouter, Depends, Request

from database.database import get_db
from model.schema.schemas.base import BaseResponse
from model.schema.schemas.department import (
    CreateDepartmentRequest,
    UpdateDepartmentRequest,
)
from service.department_service import DepartmentService, get_department_service
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/department/{department_id}")
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    service: DepartmentService = Depends(get_department_service),
) -> BaseResponse:
    res = await service.get_department_details(db=db, department_id=department_id)
    return BaseResponse.success(data=res)


@router.get("/department")
async def get_all_departments(
    db: AsyncSession = Depends(get_db),
    service: DepartmentService = Depends(get_department_service),
) -> BaseResponse:
    res = await service.get_all_departments(db=db)
    return BaseResponse.success(data=res)


@router.post("/department")
async def create_department(
    create_department_request: CreateDepartmentRequest,
    db: AsyncSession = Depends(get_db),
    service: DepartmentService = Depends(get_department_service),
) -> BaseResponse:
    res = await service.create_department(
        db=db, create_department_request=create_department_request
    )
    return BaseResponse.success(data=res)


@router.delete("/department/{department_id}")
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    service: DepartmentService = Depends(get_department_service),
) -> BaseResponse:
    await service.delete_department(db=db, department_id=department_id)
    return BaseResponse.success(message="Department deleted successfully")


@router.put("/department/{department_id}")
async def update_department(
    department_id: int,
    update_department_request: UpdateDepartmentRequest,
    db: AsyncSession = Depends(get_db),
    service: DepartmentService = Depends(get_department_service),
) -> BaseResponse:
    res = await service.update_department(
        db=db,
        department_id=department_id,
        update_department_request=update_department_request,
    )
    return BaseResponse.success(data=res)
