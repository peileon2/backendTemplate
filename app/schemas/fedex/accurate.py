from pydantic import BaseModel, Field
from app.models.Enums import GdAndHd, ResAndComm, AhsType, DasType


class Accurate(BaseModel):
    ahs_type: AhsType
    gd_hd_type: GdAndHd
    res_comm_type: ResAndComm
    das_type: DasType
    zone: int
