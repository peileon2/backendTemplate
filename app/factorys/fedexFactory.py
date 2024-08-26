from app.models.sku import Sku
from app.models.deliverys import (
    AssembleDeliveryFees,
    BaseRate,
    Ahs,
    Das,
    Oversize,
    Rdc,
    DemandCharge,
)
from app.models.Enums import AhsType


class Judge:
    def __init__(self, _sku: Sku) -> None:
        self.sku = _sku

    @property
    def max_length(self):
        return max(self.sku.height + self.sku.weight + self.sku.width)

    @property
    def min_length(self):
        return min(self.sku.height + self.sku.weight + self.sku.width)

    @property
    def middle_length(self):
        return (
            self.sku.height
            + self.sku.weight
            + self.sku.width
            - self.max_length
            - self.min_length
        )

    def judge_ahs_type(self):
        type_ahs = None
        if self.max_length > 48 or self.middle_length > 30 or self.round_size > 105:
            type_ahs = AhsType.AHS_Dimension
        if self.sku.weight > 50:
            type_ahs = AhsType.AHS_Weight
        return type_ahs


class FedexFactory:
    def __init__(
        self,
        _sku: Sku,
        _baserate: BaseRate,
        _ahs: Ahs,
        _das: Das,
        _oversize: Oversize,
        _rdc: Rdc,
        _demandCharge: DemandCharge,
    ) -> None:
        self.sku = _sku
        self.base_rate = _baserate
        self.ahs = _ahs
        self.das = _das
        self.oversize = _oversize
        self.rdc = _rdc
        self.demandCharge = _demandCharge

    @property
    def max_length(self):
        return max(self.sku.height + self.sku.weight + self.sku.width)

    @property
    def min_length(self):
        return min(self.sku.height + self.sku.weight + self.sku.width)

    @property
    def middle_length(self):
        return (
            self.sku.height
            + self.sku.weight
            + self.sku.width
            - self.max_length
            - self.min_length
        )

    @property
    def rated_weight_charge(self):
        return (
            self.sku.height * self.sku.weight * self.sku.width
        ) / self.demandCharge.DIM

    @property
    def base_rate_charge(self):
        return self.base_rate.fees

    @property
    def das_charge(self):
        return self.das.fees

    @property
    def round_size(self):
        return self.max_length + self.middle_length * 2 + self.min_length * 2

    @property
    def oversize_charge(self):
        if 130 < self.round_size < 165 or 96 < max < 108:
            return self.oversize.fees * self.oversize.discount
        return 0

    @property
    def ahs_charge(self):
        return self.ahs.fees

    @property
    def peak_os_charge(self):
        if not self.oversize == 0:
            return self.demandCharge.peak_os_charge
        else:
            return 0

    @property
    def peak_ahs_charge(self):
        if not self.ahs_charge == 0:
            return self.ahs.fees

    @property
    def rds_charge(self):
        return self.rdc.fees

    @property
    def peak_rdc_charge(self):
        return self.demandCharge.peak_rdc_charge

    @property
    def fuel_charge(self):
        return (
            self.base_rate_charge
            + self.das_charge
            + self.oversize_charge
            + self.ahs_charge
            + self.peak_os_charge
            + self.rds_charge
            + self.peak_rdc_charge
        ) * self.demandCharge.fuel_rate

    @property
    def total_charge(self):
        return (
            self.base_rate_charge
            + self.das_charge
            + self.oversize_charge
            + self.ahs_charge
            + self.peak_os_charge
            + self.rds_charge
            + self.peak_rdc_charge
        ) * (1 + self.demandCharge.fuel_rate)
