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
