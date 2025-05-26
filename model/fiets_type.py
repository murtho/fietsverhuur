
class FietsType:
    MANDATORY_ATTRIBUTES = [
        'beschrijving',
        'model',
        'dagprijs',
    ]

    OPTIONAL_ATTRIBUTES = [
        'electrisch',
    ]

    BESCHRIJVING_MAX_LENGTH = 32
    MODEL_MAX_LENGTH = 32

    fiets_type_id : int | None = None
    beschrijving : str | None = None
    model : str | None = None
    dagprijs : int | None = None
    electrisch : bool | None = None

    def __init__(self, fiets_type_data : dict[str, str | int]):
        # Valideer of alle attributen van het fiets type aanwezig zijn
        for attribute in self.MANDATORY_ATTRIBUTES:
            if attribute not in fiets_type_data:
                raise Exception('Missing mandatory attribute: ' + attribute)

        # Kopieer alle data van het fiets type
        for attribute, value in fiets_type_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['fiets_type_id'] = getattr(self, 'fiets_type_id')

        for attribute in self.MANDATORY_ATTRIBUTES:
            dictionary[attribute] = getattr(self, attribute)

        for attribute in self.OPTIONAL_ATTRIBUTES:
            if hasattr(self, attribute):
                dictionary[attribute] = getattr(self, attribute)
            else:
                dictionary[attribute] = None

        return dictionary

    @staticmethod
    def fields() -> list:
        return ['fiets_type_id'] + FietsType.MANDATORY_ATTRIBUTES + FietsType.OPTIONAL_ATTRIBUTES