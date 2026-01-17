from fastapi import APIRouter, Depends, Request

from model.schema.schemas.base import BaseResponse
from service.index_service import get_index_service

router = APIRouter()


@router.get("/tabs")
async def get_tabs(request: Request, service=Depends(get_index_service)):
    res = await service.get_tabs(request.state.role)
    return BaseResponse.success(data=res)
