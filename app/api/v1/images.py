from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_images():
    return [{"image": "fakeimage.jpg"}]
