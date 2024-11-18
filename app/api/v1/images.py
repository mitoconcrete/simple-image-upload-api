from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import UUID4

from app.api.depedencies import get_image_service
from app.schema.dto.image import (
    GetImageResponse,
    GetImagesResponse,
    ImageServiceOutput,
    SaveLogInput,
    UploadImageResponse,
)
from app.schema.enum.image import ImageProcessingType
from app.service.image import ImageService
from app.tasks.image import process_image_task
from app.util.image_util import create_save_path, get_image_format

router = APIRouter()


@router.get('/{image_id}', response_model=GetImageResponse)
async def get_image(
    image_id: UUID4,
    service: ImageService = Depends(get_image_service),
):
    return GetImageResponse(**service.get(image_id).model_dump())


@router.get('/', response_model=GetImagesResponse)
async def get_images(
    limit: int = 10,
    page: int = 0,
    service: ImageService = Depends(get_image_service),
) -> dict:
    return GetImagesResponse(**service.get_all(limit, page).model_dump())


def preprocess(service: ImageService, image_bytes: bytes) -> tuple[UUID4, bytes, ImageServiceOutput]:
    preprocessed_image = service.preprocess(image_bytes)
    preprocessed_filename = create_save_path(get_image_format(preprocessed_image))
    original_url = service.upload(preprocessed_filename, preprocessed_image)
    original_image_model = service.save(original_url)
    original_id = original_image_model.id
    service.save_log(SaveLogInput(original_id=original_id, status=ImageProcessingType.READY))
    refresh_image_model = service.get(original_id)
    return (original_id, preprocessed_image, refresh_image_model)


@router.post('/', response_model=List[UploadImageResponse])
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    service: ImageService = Depends(get_image_service),
):
    images = [file.file.read() for file in files]
    # 1. validate images
    service.validate(images)

    response: list[ImageServiceOutput] = []

    for image in images:
        # 2. image preprocessing
        original_id, preprocessed_image, original_image_model = preprocess(service, image)
        # 3. image processing send to task queue
        process_image_task.apply_async(args=[original_id, preprocessed_image], ignore_result=True)
        # 4. append response
        response.append(original_image_model)

    return [UploadImageResponse(**item.model_dump()) for item in response]
