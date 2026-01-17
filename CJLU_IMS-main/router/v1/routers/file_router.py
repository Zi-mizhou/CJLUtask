from typing import Optional
from fastapi import APIRouter, Depends, Form, UploadFile

from database.database import get_db
from model.schema.schemas.base import BaseResponse
from model.schema.schemas.file import (
    CreateFolderRequest,
    DeleteFileListRequest,
    DownloadFileListRequest,
    RenameFileRequest,
)
from service.file_service import FileService, get_file_service
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/list")
async def get_file_list(
    parent_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    service: FileService = Depends(get_file_service),
):
    res = await service.get_file_list(db=db, parent_id=parent_id)
    return BaseResponse.success(data=res)


@router.post("/folder")
async def create_folder(
    create_folder_request: CreateFolderRequest,
    db: AsyncSession = Depends(get_db),
    service: FileService = Depends(get_file_service),
):
    res = await service.create_folder(
        db=db,
        folder_name=create_folder_request.folder_name,
        parent_id=create_folder_request.parent_id,
    )
    return BaseResponse.success(data=res)


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    parent_id: Optional[int] = Form(None),
    db: AsyncSession = Depends(get_db),
    service: FileService = Depends(get_file_service),
):
    res = await service.upload_file(db=db, file=file, parent_id=parent_id)
    return BaseResponse.success(data=res)


@router.delete("/delete")
async def delete_file(
    delete_file_list_request: DeleteFileListRequest,
    db: AsyncSession = Depends(get_db),
    service: FileService = Depends(get_file_service),
):
    res = await service.delete_file_list(
        db=db,
        file_ids=delete_file_list_request.file_ids,
        parent_id=delete_file_list_request.parent_id,
    )
    return BaseResponse.success(data={})


@router.post("/download")
async def download_file_list(
    download_file_list_request: DownloadFileListRequest,
    db: AsyncSession = Depends(get_db),
    service: FileService = Depends(get_file_service),
):
    res = await service.get_download_url_list(
        db=db, file_ids=download_file_list_request.file_ids
    )
    return BaseResponse.success(data=res)


@router.put("/rename")
async def rename_file(
    rename_file_request: RenameFileRequest,
    db: AsyncSession = Depends(get_db),
    service: FileService = Depends(get_file_service),
):
    res = await service.rename_file(
        db=db,
        file_id=rename_file_request.file_id,
        new_name=rename_file_request.new_name,
    )
    return BaseResponse.success(data=res)


@router.get("/preview/{file_id}")
async def preview_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    service: FileService = Depends(get_file_service),
):
    res = await service.preview_file(db=db, file_id=file_id)
    return BaseResponse.success(data=res)
