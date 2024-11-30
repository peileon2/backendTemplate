from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List


class FedexAccurated(BaseModel):
    AHS: float
    OS: float
    DAS: float
    RDC: float
    DIM: int
    peak_ahs_charge: float
    peak_os_charge: float
    peak_rdc_charge: float
