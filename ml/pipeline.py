import catboost as cb
import geojson
import numpy as np
import pandas as pd
import rasterio
from PIL import Image
import io

from ml.constants import THRESHOLD, MODEL_PATH
from ml.processing import load_and_preprocess_tiff, process_csv
from ml.utils import pixel_to_coord

loaded_model = cb.CatBoostClassifier()
loaded_model.load_model(MODEL_PATH)


def generate_fire_points(
    csv_info: pd.DataFrame, tiff_image: Image
) -> list[geojson.Point]:
    """
    generate_fire_points(csv_info: pd.DataFrame, tiff_image: Image) -> list[geojson.Point]

    This function generates a list of GeoJSON `Point` objects representing locations with high fire probability, based on input data from a CSV file and a multi-band TIFF image. The function uses machine learning predictions to identify fire-prone areas from the image and returns the geographical coordinates of those points.

    Parameters:
        csv_info (pd.DataFrame):
            A pandas DataFrame containing tabular data from a CSV file, used to enhance pixel information from the TIFF image.
        tiff_image (Image):
            A multi-band TIFF image containing geospatial data. This image provides pixel data for analysis.

    Returns:
        list[geojson.Point]:
            A list of GeoJSON Point objects representing geographical locations where the probability of fire exceeds a predefined threshold.

    Function Workflow:
        1. The function loads and preprocesses the TIFF image using `load_and_preprocess_tiff()`, extracting pixel data from selected bands (red, green, blue, infrared, and mask).
        2. The original shape and transformation matrix of the TIFF image are obtained using `rasterio`.
        3. The CSV data is processed using `process_csv()` to calculate mean values, which are expanded across all pixel data in the TIFF image.
        4. The pixel data and processed CSV data are combined into a single DataFrame.
        5. The function ensures that all features required by the machine learning model (`loaded_model`) are present in the DataFrame, filling missing features with NaN values.
        6. The pre-trained model is used to predict the fire probabilities for each pixel.
        7. For pixels with fire probability higher than a defined threshold (`THRESHOLD`), the pixel coordinates are converted to geographical coordinates using `pixel_to_coord()`.
        8. A GeoJSON `Point` is created for each high-probability pixel and added to the output list.
    """
    pixel_data = load_and_preprocess_tiff(
        tiff_image, r_band=1, g_band=2, b_band=3, ik_band=4, mask_band=5
    )

    with rasterio.open(tiff_image) as src:
        original_shape = src.read(1).shape
        transform = src.transform

    csv_mean_data = process_csv(csv_info)

    csv_data_expanded = pd.DataFrame(
        np.tile(csv_mean_data.values, (len(pixel_data), 1)), columns=csv_mean_data.index
    )
    df = pd.concat([pixel_data, csv_data_expanded], axis=1)

    feature_names = loaded_model.feature_names_

    missing_columns = [col for col in feature_names if col not in df.columns]

    for col in missing_columns:
        df[col] = np.nan

    df = df.reindex(columns=feature_names)

    cb_pred_proba = loaded_model.predict_proba(df)[:, 1].reshape(
        original_shape
    )  # Get the probability estimates for the positive class

    geojson_points = []

    for row in range(cb_pred_proba.shape[0]):
        for col in range(cb_pred_proba.shape[1]):
            if cb_pred_proba[row, col] > THRESHOLD:
                x, y = pixel_to_coord(row, col, transform)
                point = geojson.Point([x, y])
                geojson_points.append(point)

    return geojson_points


if __name__ == "__main__":
    with open("tests/test.tiff", "rb") as tiff_file:
        tiff_bytes = tiff_file.read()

    tiff_image = io.BytesIO(tiff_bytes)
    csv_info = pd.read_csv("tests/test.csv")

    print(generate_fire_points(csv_info, tiff_image))
