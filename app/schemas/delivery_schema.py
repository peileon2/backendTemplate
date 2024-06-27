from pydantic import BaseModel
from datetime import datetime


class DeliverySingle(BaseModel):
    height: float
    length: float
    width: float
    weight: float
    zone: int
    ahs_type: int
    volume_factor: int


