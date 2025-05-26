from model.contract import Contract
from model.klant import Klant
from model.vestiging import Vestiging

# De associaties tussen Klant en Vestiging met Contract worden vastgelegd in deze class
# Iedere Contract is voor een Klant op een Vestiging, de objecten dienen opgeslagen te worden na het instantiëren
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