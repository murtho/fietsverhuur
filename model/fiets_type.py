
class FietsType:
    MANDATORY_KEYS = [
        'beschrijving',
        'model',
        'dagprijs',
    ]

    OPTIONAL_KEYS = [
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
        for key in self.MANDATORY_KEYS:
            if key not in fiets_type_data:
                raise Exception('Missing mandatory key: ' + key)

        # Kopieer alle data van het fiets type
        for attribute, value in fiets_type_data.items():
            setattr(self, attribute, value)

    def __dict__(self):
        dictionary = {}

        dictionary['fiets_type_id'] = getattr(self, 'fiets_type_id')

        for attribute in self.MANDATORY_KEYS:
            dictionary[attribute] = getattr(self, attribute)

        for key in self.OPTIONAL_KEYS:
            if hasattr(self, key):
                dictionary[key] = getattr(self, key)
            else:
                dictionary[key] = None

        return dictionary