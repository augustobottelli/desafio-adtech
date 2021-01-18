from typing import Optional

from pydantic import BaseModel

class CoordsParams(BaseModel):
    long: str
    lat: str
    start_date: str
    end_date: str
    scale: Optional[int] = 10
    cloud_pixel_pct: Optional[int] = 10
