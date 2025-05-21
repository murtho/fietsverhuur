from model.contract import Contract
from model.klant import Klant
from model.vestiging import Vestiging


class HydratedContract(Contract):

    klant: Klant = None
    vestiging: Vestiging = None

    def __init__(self, model: dict[str, str | int]) -> None:
        super().__init__(model)

    def set_klant(self, klant: Klant):
        self.klant = klant

    def set_vestiging(self, vestiging: Vestiging):
        self.vestiging = vestiging

    def __dict__(self):
        dictionary = super().__dict__()
        dictionary['klant'] = self.klant.__dict__()
        dictionary['vestiging'] = self.vestiging.__dict__()

        return dictionary