from enum import Enum


class GdAndHd(Enum):
    GROUND = 1
    HOMEDELIVERY = 2


class ResAndComm(Enum):
    RESIDENTIAL = 1
    COMMERCIAL = 2


class AhsType(Enum):
    AHS_Dimension = 1
    AHS_Weight = 2
    AHS_Packing = 3


class DasType(Enum):
    DAS = 1
    DASE = 2
    RAS = 3
