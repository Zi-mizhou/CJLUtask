from typing import Optional
from pydantic import BaseModel


class CreateFolderRequest(BaseModel):
    folder_name: str
    parent_id: Optional[int] = None


class DeleteFileListRequest(BaseModel):
    file_ids: list[int]
    parent_id: Optional[int] = None


class DownloadFileListRequest(BaseModel):
    file_ids: list[int]


class RenameFileRequest(BaseModel):
    file_id: int
    new_name: str
