import io
from PIL import Image
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
import pandas as pd

from schemas.geojson import GeoJSONPoint
from services.ml import MlService

router = APIRouter(prefix="/api/v1/ml", tags=["ml"])


@router.post(
    "/fire_points",
    summary="получение точек возникновение пожаров",
    response_model=list[GeoJSONPoint],
)
async def create_fire_points(
        csv_file: UploadFile = File(...),
        tiff_file: UploadFile = File(...),
        ml_service: MlService = Depends(),
):
    csv_info, tiff_image = await validate_request(csv_file, tiff_file)

    return ml_service.generate_fire_points(csv_info, tiff_image)


@router.post(
    "/heat_map",
    summary="получение heatmap пожаров",
    response_model=dict,
)
async def create_heat_map(
        csv_file: UploadFile = File(...),
        tiff_file: UploadFile = File(...),
        ml_service: MlService = Depends(),
):

    csv_info, tiff_image = await validate_request(csv_file, tiff_file)

    return ml_service.generate_fire_heat_map(csv_info, tiff_image)


async def validate_request(csv_file: UploadFile, tiff_file: UploadFile) -> (pd.DataFrame, Image):
    if csv_file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    if tiff_file.content_type != 'image/tiff':
        raise HTTPException(status_code=400, detail="Invalid TIFF file type. Please upload a TIFF file.")

    try:
        contents = await csv_file.read()
        csv_info = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the CSV file: {str(e)}")

    try:
        tiff_contents = await tiff_file.read()
        tiff_image = Image.open(io.BytesIO(tiff_contents))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the TIFF file: {str(e)}")

    return csv_info, tiff_image
