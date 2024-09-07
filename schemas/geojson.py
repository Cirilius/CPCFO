from typing import List

from pydantic import BaseModel


class GeoJSONPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float]
