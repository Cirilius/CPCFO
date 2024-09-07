import geojson
from PIL import Image
import pandas as pd


class MlService:
    def __init__(self):
        pass


    def generate_fire_points(self, csv_info: pd.DataFrame, tiff_image: Image) -> list[geojson.Point]:
        coordinates = [
            [100.0, 0.0],
            [101.0, 1.0],
            [102.0, 2.0],
            [103.0, 3.0]
        ]

        geojson_points = []
        for coord in coordinates:
            point = geojson.Point(coord)
            geojson_points.append(point)

        return geojson_points


    def generate_fire_heat_map(self, csv_info: pd.DataFrame, tiff_image: Image) -> dict:
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "weight": 0.8
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [ -73.9708, 40.7648 ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "weight": 0.6
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [ -73.9851, 40.7580 ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "weight": 1.0
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [ -73.9926, 40.7467 ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "weight": 0.9
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [ -74.0017, 40.7328 ]
                    }
                }
            ]
        }
