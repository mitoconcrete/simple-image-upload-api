from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import UUID4

from app.api.depedencies import get_image_service
from app.schema.dto.image import GetImageResponse, GetImagesResponse, UploadImageResponse
from app.service.image import ImageService
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


@router.post('/', response_model=List[UploadImageResponse])
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    service: ImageService = Depends(get_image_service),
):
    images = [file.file.read() for file in files]
    # 1. validate images
    service.validate(images)

    # 2. preprocess images
    preprocessed_images = [service.preprocess(image) for image in images]

    # 3. upload and save original images
    create_filenames = [(create_save_path(get_image_format(image)), image) for image in preprocessed_images]
    original_urls = [(service.upload(name, image), image) for name, image in create_filenames]
    original_ids = [(service.save(url).id, image) for url, image in original_urls]

    # 4. process images
    processed_images = [(original_id, service.process(image)) for original_id, image in original_ids]

    # 5. upload and save processed images
    create_filenames = [(original_id, create_save_path('svg'), image) for original_id, image in processed_images]
    svg_urls = [(original_id, service.upload(name, image), image) for original_id, name, image in create_filenames]
    response = [service.update(original_id, url) for original_id, url, _ in svg_urls]

    return [UploadImageResponse(**item.model_dump()) for item in response]
