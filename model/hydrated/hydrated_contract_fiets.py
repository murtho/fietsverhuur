from model.contract_fiets import ContractFiets
from model.hydrated.hydrated_fiets import HydratedFiets

# De associaties van Fiets en FietsType met ContractFiets worden vastgelegd in deze class
# Ieder contract heeft een Fiets van een FietsType, dit dient opgeslagen te worden na het instantiëren van de class
class HydratedContractFiets(ContractFiets):

    fiets: HydratedFiets = None

    def __init__(self, model: dict[str, str | int]) -> None:
        super().__init__(model)

    def set_fiets(self, fiets: HydratedFiets):
        self.fiets = fiets

    def __dict__(self):
        dictionary = super().__dict__()
        dictionary['fiets'] = self.fiets.__dict__()

        return dictionary