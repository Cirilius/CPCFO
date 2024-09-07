import io

import geojson
import pandas as pd

from ml.pipeline import generate_fire_points


class MlService:
    def __init__(self):
        pass

    def generate_fire_points(
        self, csv_info: pd.DataFrame, tiff_image: io.BytesIO
    ) -> list[geojson.Point]:
        return generate_fire_points(csv_info, tiff_image)

    def generate_fire_heat_map(
        self, csv_info: pd.DataFrame, tiff_image: io.BytesIO
    ) -> dict:
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"weight": 0.8},
                    "geometry": {"type": "Point", "coordinates": [-73.9708, 40.7648]},
                },
                {
                    "type": "Feature",
                    "properties": {"weight": 0.6},
                    "geometry": {"type": "Point", "coordinates": [-73.9851, 40.7580]},
                },
                {
                    "type": "Feature",
                    "properties": {"weight": 1.0},
                    "geometry": {"type": "Point", "coordinates": [-73.9926, 40.7467]},
                },
                {
                    "type": "Feature",
                    "properties": {"weight": 0.9},
                    "geometry": {"type": "Point", "coordinates": [-74.0017, 40.7328]},
                },
            ],
        }
