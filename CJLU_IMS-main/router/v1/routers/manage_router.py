from fastapi import APIRouter


router = APIRouter()


@router.post("/add")
async def add_user():
    return {"message": "User added"}


@router.delete("/remove")
async def remove_user():
    return {"message": "User removed"}


@router.put("/update")
async def update_user():
    return {"message": "User updated"}


@router.get("/list")
async def list_users():
    return {"message": "List of users"}


@router.get("/details")
async def user_details():
    return {"message": "User details"}


@router.put("/update_role")
async def update_user_role():
    return {"message": "User role updated"}
