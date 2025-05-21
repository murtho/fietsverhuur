from model.fiets import Fiets
from model.fiets_type import FietsType


class HydratedFiets(Fiets):

    fiets_type: FietsType = None

    def __init__(self, model: dict[str, str | int]):
        super().__init__(model)

    def set_fiets_type(self, fiets_type: FietsType):
        self.fiets_type = fiets_type

    def __dict__(self):
        dictionary = super().__dict__()
        dictionary['fiets_type'] = self.fiets_type.__dict__()

        return dictionary