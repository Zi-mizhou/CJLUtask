from fastapi import APIRouter
from .routers import (
    auth_router,
    user_router,
    index_router,
    file_router,
    department_router,
)


router = APIRouter()

router.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
router.include_router(user_router.router, prefix="/user", tags=["User"])
router.include_router(index_router.router, prefix="/index", tags=["Index"])
router.include_router(file_router.router, prefix="/file", tags=["File"])
router.include_router(
    department_router.router, prefix="/department", tags=["Department"]
)
