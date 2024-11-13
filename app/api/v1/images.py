from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def read_images():
    return [{"image": "fakeimage.jpg"}]
