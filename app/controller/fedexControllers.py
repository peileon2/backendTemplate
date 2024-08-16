from app.models.sku import Sku
from app.models.deliverys import AssembleDeliveryFees


class FedexController:
    def __init__(self, sku: Sku, ADF: AssembleDeliveryFees) -> None:
        self.sku = sku
        self.adf = ADF

    @property
    def rated_weight(self):
        pass

    ## return (self.sku.height * self.sku.weight * self.sku.width) / self.delivery.DIM
    @property
    def base_rate(self):
        pass

    @property
    def das_fees(self):
        pass

    @property
    def round_size(self):
        return self.sku.height + self.sku.weight + self.sku.width

    @property
    def oversize_fees(self):
        pass

    @property
    def ahs_fees(self):
        pass

    @property
    def peak_os(self):
        pass

    @property
    def peak_ahs(self):
        pass

    @property
    def peak_rdc(self):
        pass

    @property
    def rds_fees(self):
        pass

    @property
    def fuel_fees(self):
        pass

    @property
    def total(self):
        pass
